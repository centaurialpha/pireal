import argparse
import sys

import structlog
from PyQt6.QtWidgets import QApplication

from pireal.core.db import DB
from pireal.gui.controller import Controller
from pireal.gui.database_container import DatabaseContainer
from pireal.gui.lateral_widget import LateralWidget
from pireal.gui.main_window import Pireal
from pireal.gui.query_widget import QueryWidget
from pireal.gui.start_page import StartPage
from pireal.gui.table_widget import TableWidget
from pireal.registry import Registry


class Application:
    def __init__(self, args: argparse.Namespace):
        self._logger = structlog.get_logger()
        self._args = args

        self._app = QApplication(sys.argv)
        self._registry = Registry()

        self._initialize_settings()
        self._initialize_theme()
        self._initialize_widgets()

    def _initialize_settings(self):
        from pireal.settings import settings

        self._logger.info("loading_settings")
        settings.load()

    def _initialize_theme(self):
        from pireal.theme import theme_manager

        self._logger.info("applying_theme")
        theme_manager.initialize()
        theme_manager.apply_theme(self._app)

    def _initialize_widgets(self):
        self._logger.info("widgets_initialization")

        database = DB()
        self._registry.register("db", database)

        controller = Controller()
        self._registry.register("controller", controller)

        start_page = StartPage()

        lateral_widget = LateralWidget()
        self._registry.register("lateral-widget", lateral_widget)

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
        self._logger.info("widgets_initialized")

    def run(self):
        self._main_window.show()
        sys.exit(self._app.exec())
