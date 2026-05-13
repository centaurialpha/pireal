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

import logging
import sys

from PyQt6.QtCore import QTimer, QTranslator
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication

from pireal.core.db import DB
from pireal.dirs import THEMES_DIR
from pireal.gui.controller import Controller
from pireal.gui.query_widget import QueryWidget
from pireal.gui.right_pane import RightPane
from pireal.gui.status_bar import StatusBar
from pireal.registry import Registry
from pireal.resources import image, translation

logger = logging.getLogger(__name__)


class Application:
    def __init__(self):
        self._translator = None
        self._app = QApplication(sys.argv)
        self._app.setApplicationName("Pireal")
        self._app.setDesktopFileName("pireal")
        self._registry = Registry()

        self._initialize_settings()
        self._initialize_translations()
        self._initialize_theme()
        self._initialize_widgets()

    def _initialize_settings(self):
        from pireal.settings import settings

        logger.info("Loading settings...")
        settings.load()

    def _initialize_translations(self):
        from pireal.settings import settings

        translator = QTranslator()
        is_ok = translator.load(translation(settings.language))
        if is_ok:
            self._app.installTranslator(translator)
        # Mantener la referencia porque Qt/C++ necesita
        # ptm horas de debuggggg
        self._translator = translator

    def _initialize_theme(self):
        from pireal.gui.theme.manager import get_theme_manager
        from pireal.settings import settings

        manager = get_theme_manager(custom_themes_dir=THEMES_DIR)
        theme_id = settings.theme

        try:
            manager.apply(theme_id)
        except ValueError:
            manager.apply("dark")
            settings.theme = "dark"

    def _initialize_widgets(self):
        from pireal.gui.database_container import DatabaseContainer
        from pireal.gui.lateral_widget import LateralWidget
        from pireal.gui.main_window import Pireal
        from pireal.gui.query_widget import QueryWidget
        from pireal.gui.start_page import StartPage
        from pireal.gui.table_widget import TableWidget

        logger.info("Widgets initialization")

        database = DB()
        self._registry.register("db", database)

        lateral_widget = LateralWidget()
        self._registry.register("lateral-widget", lateral_widget)

        table_widget = TableWidget()
        self._registry.register("table-widget", table_widget)

        query_widget = QueryWidget()
        self._registry.register("query-widget", query_widget)

        status_bar = StatusBar()
        self._registry.register("status-bar", status_bar)

        right_pane = RightPane()
        self._registry.register("right-pane", right_pane)

        database_container = DatabaseContainer()
        self._registry.register("database-container", database_container)

        start_page = StartPage()
        self._registry.register("start-page", start_page)

        controller = Controller()
        self._registry.register("controller", controller)

        self._main_window = Pireal()
        self._main_window.setWindowIcon(QIcon(image("pireal_icon.png")))
        self._registry.register("pireal", self._main_window)

        self._wire_components(status_bar, query_widget)

        self._main_window.setCentralWidget(controller)
        controller.add_widget(start_page)

        logger.info("Widgets initialized")

    def _wire_components(self, status_bar: StatusBar, query_widget: QueryWidget) -> None:
        from pireal.settings import settings

        status_bar.symbolModeToggled.connect(query_widget.set_symbol_mode)
        status_bar.show_symbol_mode(settings.symbol_mode)

    def run(self):
        self._main_window.showMaximized()

        QTimer.singleShot(400, self._check_olakase)

        sys.exit(self._app.exec())

    def _check_olakase(self) -> None:
        from pireal.core.olakase import _Kind, check_launch, mark_seen

        momento = check_launch()
        if momento is None:
            return

        if momento.kind == _Kind.A:
            mark_seen()
            QTimer.singleShot(800, self._show_obito)

    def _show_obito(self) -> None:
        from pireal.gui.dialogs.obito_dialog import ObitoDialog

        ObitoDialog(self._main_window).show()
