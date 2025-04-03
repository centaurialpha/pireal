import argparse
import sys

from PyQt6.QtWidgets import QApplication

from pireal.gui.controller import Controller
from pireal.gui.database_container import DatabaseContainer
from pireal.gui.lateral_widget import LateralWidget
from pireal.gui.main_window import Pireal
from pireal.gui.query_widget import QueryWidget
from pireal.gui.start_page import StartPage
from pireal.gui.table_widget import TableWidget
from pireal.registry import Registry
from pireal.settings import SETTINGS


class Application:
    def __init__(self, args: argparse.Namespace):
        self._args = args
        self._app = QApplication(sys.argv)
        SETTINGS.load()
        self._registry = Registry()

        self._initialize_widgets()

    def _initialize_widgets(self):
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

        # central_widget.add_widget(database_container)
        controller.add_widget(start_page)

    def run(self):
        self._main_window.show()
        sys.exit(self._app.exec())
