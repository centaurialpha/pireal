# Copyright 2015-2026 - Gabriel Acosta <acostadariogabriel@gmail.com>
#
# This file is part of Pireal.
#
# Pireal is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# any later version.
#
# Pireal is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Pireal; If not, see <http://www.gnu.org/licenses/>.


from PyQt6.QtGui import QCloseEvent
from PyQt6.QtWidgets import (
    QMainWindow,
    QMessageBox,
)

from pireal import translations as tr
from pireal.core.db import DB
from pireal.core.pireal_file import is_example_file
from pireal.gui.controller import Controller
from pireal.gui.menu import MenuBuilder
from pireal.gui.query_widget import (
    EditorWidget,
    QueryWidget,
)
from pireal.gui.start_page import StartPage
from pireal.gui.status_bar import StatusBar
from pireal.gui.theme.manager import get_theme_manager
from pireal.registry import Registry
from pireal.settings import settings


class Pireal(QMainWindow):
    _instance: "Pireal"

    def __init__(self, check_updates=True):
        super().__init__()
        Pireal._instance = self

        controller = Registry.get("controller", Controller)

        # Menu bar
        self._menu_builder = MenuBuilder(self, controller)
        self._menu_builder.build()

        menubar = self.menuBar()
        assert menubar is not None

        db = Registry.get("db", DB)
        db.hasModified.connect(self._update_title)
        db.databaseStateChanged.connect(self._update_title)

        status_bar = Registry.get("status-bar", StatusBar)
        db.hasModified.connect(status_bar.set_db_modified)
        db.databaseStateChanged.connect(lambda _: status_bar.set_db_modified(False))

        if check_updates:
            self._start_updater()

        statusbar = self.statusBar()
        assert statusbar is not None
        statusbar.hide()

    def _start_updater(self):
        from PyQt6.QtCore import QThread

        from pireal.gui.updater import Updater

        updater_thread = QThread(self)
        self._updater = Updater()
        self._updater.moveToThread(updater_thread)

        updater_thread.started.connect(self._updater.check_updates)
        self._updater.finished.connect(updater_thread.quit)
        updater_thread.finished.connect(updater_thread.deleteLater)
        self._updater.updateAvailable.connect(self._on_update_available)

        updater_thread.start()

    def _on_update_available(self, version: str, url: str):
        start_page = Registry.get("start-page", StartPage)
        start_page.show_update(version, url)

    def _update_title(self, *args):
        db = Registry.get("db", DB)
        if not db.is_active:
            self.setWindowTitle("Pireal")
            return
        name = db.file.display_name if db.file else "Untitled"
        modified = "*" if db.modified else ""
        self.setWindowTitle(f"Pireal - {name}{modified}")

    @classmethod
    def instance(cls):
        return cls._instance

    def _on_theme_requested(self, theme_id: str):
        theme_manager = get_theme_manager()
        theme_manager.apply(theme_id)
        settings.theme = theme_id

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        controller = Registry.get("controller", Controller)
        db = Registry.get("db", DB)
        query_widget = Registry.get("query-widget", QueryWidget)

        unsaved_editors = [
            w
            for i in range(query_widget._editor_tabs.count())
            if isinstance((w := query_widget._editor_tabs.widget(i)), EditorWidget)
            and (doc := w.editor.document()) is not None
            and doc.isModified()
            and not is_example_file(w.file)
        ]

        if unsaved_editors:
            names = ", ".join(e.file.display_name for e in unsaved_editors)
            ret = QMessageBox.question(
                self,
                tr.TR_UNSAVED_QUERIES_TITLE,
                tr.TR_UNSAVED_QUERIES_BODY.format(names=names),
                QMessageBox.StandardButton.Save
                | QMessageBox.StandardButton.Discard
                | QMessageBox.StandardButton.Cancel,
            )
            if ret == QMessageBox.StandardButton.Cancel:
                if a0:
                    a0.ignore()
                return
            if ret == QMessageBox.StandardButton.Save:
                for editor in unsaved_editors:
                    query_widget._editor_tabs.setCurrentWidget(editor)
                    controller.save_query()

        if db.is_active and db.modified and not is_example_file(db.file):
            ret = QMessageBox.question(
                self,
                tr.TR_CLOSE_DB_TITLE,
                tr.TR_CLOSE_DB_BODY,
                QMessageBox.StandardButton.Save
                | QMessageBox.StandardButton.Discard
                | QMessageBox.StandardButton.Cancel,
            )
            if ret == QMessageBox.StandardButton.Cancel:
                if a0:
                    a0.ignore()
                return
            if ret == QMessageBox.StandardButton.Save:
                controller.save_database()

        controller.save_state()

        return super().closeEvent(a0)
