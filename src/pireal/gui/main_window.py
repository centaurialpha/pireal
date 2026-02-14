from typing import Optional

from PyQt6.QtCore import QSettings
from PyQt6.QtGui import QCloseEvent
from PyQt6.QtWidgets import QMainWindow

from pireal.dirs import DATA_SETTINGS
from pireal.gui.controller import Controller
from pireal.gui.menu import MenuBuilder
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

        self._status_bar.playClicked.connect(controller.execute_queries)
        self._status_bar.gearClicked.connect(self._show_settings)
        self._status_bar.theme_button.set_themes(theme_manager.themes())
        self._status_bar.theme_button.themeRequested.connect(self._on_theme_requested)

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
        qsettings = QSettings(str(DATA_SETTINGS), QSettings.Format.IniFormat)

        qsettings.setValue("recent_databases", controller.recent_databases)

        return super().closeEvent(a0)
