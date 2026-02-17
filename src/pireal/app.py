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

import argparse
import logging
import sys

from PyQt6.QtCore import QTranslator
from PyQt6.QtWidgets import QApplication

from pireal.core.db import DB
from pireal.dirs import LOCALES_DIR, THEMES_DIR
from pireal.registry import Registry

logger = logging.getLogger(__name__)


class Application:
    def __init__(self, args: argparse.Namespace):
        self._args = args

        self._translator = None
        self._app = QApplication(sys.argv)
        self._app.setApplicationName("Pireal")
        self._app.setApplicationDisplayName("Pireal")

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
        is_ok = translator.load(f"{settings.language}", str(LOCALES_DIR))
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
        from pireal.gui.controller import Controller
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

        controller = Controller()
        self._registry.register("controller", controller)

        start_page = StartPage()
        self._registry.register("start-page", start_page)

        table_widget = TableWidget()
        self._registry.register("table-widget", table_widget)

        query_widget = QueryWidget()
        self._registry.register("query-widget", query_widget)

        database_container = DatabaseContainer()
        self._registry.register("database-container", database_container)

        self._main_window = Pireal()
        self._registry.register("pireal", self._main_window)

        self._main_window.setCentralWidget(controller)

        controller.add_widget(start_page)
        logger.info("Widgets initialized")

    def run(self):
        self._main_window.showMaximized()
        from pireal.gui.dialogs.tour_dialog import TourDialog

        if TourDialog.should_show():
            TourDialog(self._main_window).exec()

        sys.exit(self._app.exec())
