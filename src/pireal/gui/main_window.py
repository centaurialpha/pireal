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


from PyQt6.QtCore import QSettings, Qt
from PyQt6.QtGui import QCloseEvent
from PyQt6.QtWidgets import QHBoxLayout, QMainWindow, QMessageBox, QPushButton, QToolButton, QWidget

from pireal import translations as tr
from pireal.core.db import DB
from pireal.core.pireal_file import is_example_file
from pireal.dirs import DATA_SETTINGS
from pireal.gui.controller import Controller
from pireal.gui.menu import MenuBuilder
from pireal.gui.query_widget import EditorWidget, QueryWidget
from pireal.gui.status_bar import StatusBar
from pireal.gui.theme.manager import get_theme_manager
from pireal.gui.theme.schema import EditorColorRole
from pireal.helpers import Font
from pireal.registry import Registry
from pireal.settings import settings


class Pireal(QMainWindow):
    _instance: "Pireal"

    def __init__(self, check_updates=True):
        super().__init__()
        Pireal._instance = self

        # Status bar
        self._status_bar = StatusBar(self)
        Registry.register("status-bar", self._status_bar)
        _status_bar = self.statusBar()
        if _status_bar is not None:
            _status_bar.addWidget(self._status_bar, 1)
            _status_bar.setSizeGripEnabled(False)

        controller = Registry.get("controller", Controller)

        # Menu bar
        menu_builder = MenuBuilder(self, controller)
        menu_builder.build()

        corner = self._build_corner_widget(controller)
        self.menuBar().setCornerWidget(corner, Qt.Corner.TopRightCorner)
        theme_manager = get_theme_manager()

        db = Registry.get("db", DB)
        db.hasModified.connect(self._update_title)
        db.databaseStateChanged.connect(self._update_title)

        if check_updates:
            self._start_updater()

        self._status_bar.playClicked.connect(controller.execute_queries)
        self._status_bar.gearClicked.connect(self._show_settings)
        self._status_bar.theme_button.set_themes(theme_manager.themes())
        self._status_bar.theme_button.themeRequested.connect(self._on_theme_requested)
        if True:
            self._status_bar.feedbackClicked.connect(controller.send_feedback)

    def _build_corner_widget(self, controller) -> QWidget:
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 4, 8, 4)
        layout.setSpacing(6)

        fa = Font.instance()

        # Settings
        settings_btn = QToolButton()
        settings_btn.setAutoRaise(True)
        settings_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        settings_btn.setText("\uf013")
        settings_btn.setToolTip(tr.TR_SETTINGS_TITLE)
        fa.apply_to(settings_btn)
        settings_btn.setFixedSize(28, 28)
        settings_btn.clicked.connect(self._show_settings)

        # Run
        run_btn = QPushButton("\uf04b  Run Query")
        run_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        run_btn.setFixedHeight(28)
        run_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        fa_font = fa.font(11)
        run_btn.setFont(fa_font)
        run_btn.clicked.connect(controller.execute_queries)

        # Estilo del botón Run
        scheme = get_theme_manager().current_scheme
        success = scheme.editor.get(EditorColorRole.SUCCESS).name()
        run_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {success};
                color: #ffffff;
                border: none;
                border-radius: 6px;
                padding: 0 14px;
                font-size: 12px;
            }}
            QPushButton:hover {{ background-color: {success}dd; }}
            QPushButton:pressed {{ background-color: {success}aa; }}
        """)

        layout.addWidget(settings_btn)
        layout.addWidget(run_btn)
        return widget

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
        theme_manager = get_theme_manager()
        highlight = theme_manager.current_scheme.highlight.name()

        msg = (
            f'Nueva versión <b>{version}</b> disponible — <a href="{url}" '
            f'style="color: {highlight}; text-decoration: none;">Descargar ↗</a>'
        )
        self._status_bar.show_message(msg, timeout=0)
        self._status_bar._message_label.setOpenExternalLinks(True)

    def _update_title(self, *args):
        db = Registry.get("db", DB)
        if not db.is_active:
            self.setWindowTitle("Pireal")
            return
        name = db.file.display_name if db.file else "Untitled"
        modified = "*" if db.modified else ""
        self.setWindowTitle(f"Pireal — {name}{modified}")

    @classmethod
    def instance(cls):
        return cls._instance

    def _show_settings(self):
        from pireal.gui.dialogs.settings_dialog import SettingsDialog

        dialog = SettingsDialog(self)
        dialog.exec()

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
            and w.editor.document().isModified()
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

        qsettings = QSettings(str(DATA_SETTINGS), QSettings.Format.IniFormat)
        qsettings.setValue("recent_databases", controller.recent_databases)

        return super().closeEvent(a0)
