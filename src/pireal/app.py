import argparse
import logging
import sys

from PyQt6.QtWidgets import QApplication

from pireal.core.db import DB
from pireal.dirs import THEMES_DIR
from pireal.gui.controller import Controller
from pireal.gui.database_container import DatabaseContainer
from pireal.gui.lateral_widget import LateralWidget
from pireal.gui.main_window import Pireal
from pireal.gui.query_widget import QueryWidget
from pireal.gui.start_page import StartPage
from pireal.gui.table_widget import TableWidget
from pireal.registry import Registry

logger = logging.getLogger(__name__)


class Application:
    def __init__(self, args: argparse.Namespace):
        self._args = args

        self._app = QApplication(sys.argv)
        self._registry = Registry()

        self._initialize_settings()
        self._initialize_theme()
        self._initialize_widgets()

    def _initialize_settings(self):
        from pireal.settings import settings

        logger.info("Loading settings...")
        settings.load()

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
        logger.info("Widgets initialization")

        database = DB()
        self._registry.register("db", database)

        controller = Controller()
        self._registry.register("controller", controller)

        start_page = StartPage()
        self._registry.register("start-page", start_page)

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
        logger.info("Widgets initialized")

    def run(self):
        self._main_window.show()
        sys.exit(self._app.exec())
