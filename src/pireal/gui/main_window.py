from typing import Optional

from PyQt6.QtCore import QSettings
from PyQt6.QtGui import QCloseEvent
from PyQt6.QtWidgets import QMainWindow, QMessageBox

from pireal import translations as tr
from pireal.core.db import DB
from pireal.core.pireal_file import is_example_file
from pireal.dirs import DATA_SETTINGS
from pireal.gui.controller import Controller
from pireal.gui.menu import MenuBuilder
from pireal.gui.query_widget import EditorWidget, QueryWidget
from pireal.gui.status_bar import StatusBar
from pireal.gui.theme.manager import get_theme_manager
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

        theme_manager = get_theme_manager()

        db = Registry.get("db", DB)
        db.hasModified.connect(self._update_title)
        db.databaseStateChanged.connect(self._update_title)

        self._status_bar.playClicked.connect(controller.execute_queries)
        self._status_bar.gearClicked.connect(self._show_settings)
        self._status_bar.theme_button.set_themes(theme_manager.themes())
        self._status_bar.theme_button.themeRequested.connect(self._on_theme_requested)

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

    def closeEvent(self, a0: Optional[QCloseEvent]) -> None:
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
