from PyQt6.QtWidgets import QMainWindow

from pireal.gui.controller import Controller
from pireal.gui.menu import MenuBuilder
from pireal.gui.status_bar import StatusBar
from pireal.registry import Registry


class Pireal(QMainWindow):
    _instance: "Pireal"

    def __init__(self, check_updates=True):
        super().__init__()
        Pireal._instance = self

        # Status bar
        self._status_bar = StatusBar(self)
        _status_bar = self.statusBar()
        if _status_bar is not None:
            _status_bar.addWidget(self._status_bar, 1)
            _status_bar.setSizeGripEnabled(False)

        controller = Registry.get("controller", Controller)

        # Menu bar
        menu_builder = MenuBuilder(self, controller)
        menu_builder.build()

        self._status_bar.playClicked.connect(controller.execute_queries)

    @classmethod
    def instance(cls):
        return cls._instance
