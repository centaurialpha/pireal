from dataclasses import dataclass, field
from typing import List, Union

from PyQt6.QtGui import QAction, QIcon

from pireal import translations as tr


@dataclass
class Action:
    name: str
    target: str
    is_checkable: bool = False
    shorcut: str = ""
    icon: str = ""


@dataclass
class Menu:
    name: str
    items: List[Union["Menu", Action, str]] = field(default_factory=list)

    def add_item(self, item):
        self.items.append(item)
        return self


class MenuBuilder:
    def __init__(self, main_window, controller):
        self.main_window = main_window
        self.controller = controller

    def build(self):
        menu_bar = self.main_window.menuBar()
        for menu in menus:
            qmenu = menu_bar.addMenu(menu.name)
            for item in menu.items:
                if item == "separator":
                    qmenu.addSeparator()
                elif isinstance(item, Action):
                    qaction = QAction(item.name, self.main_window)
                    qaction.setCheckable(item.is_checkable)

                    if item.shorcut:
                        qaction.setShortcut(item.shorcut)
                    if item.icon:
                        qaction.setIcon(QIcon(item.icon))

                    if item.target:
                        component, slot = item.target.split(":")
                        if component == "controller":
                            slot = getattr(self.controller, slot)
                            qaction.triggered.connect(slot)

                    qmenu.addAction(qaction)

        return menu_bar


file_menu = Menu("Archivo")
file_menu.add_item(
    Action(tr.TR_MENU_FILE_NEW_DB, "controller:create_database", shorcut="Ctrl+n")
)
file_menu.add_item(Action(tr.TR_MENU_FILE_OPEN_DB, "controller:open_database"))
file_menu.add_item(Action(tr.TR_MENU_FILE_SAVE_DB, ""))
file_menu.add_item(Action(tr.TR_MENU_FILE_SAVE_AS_DB, ""))
file_menu.add_item(Action(tr.TR_MENU_FILE_CLOSE_DB, ""))
file_menu.add_item(Action(tr.TR_MENU_FILE_NEW_QUERY, "controller:new_query"))

scheme_menu = Menu("Esquema")
scheme_menu.add_item(Action(tr.TR_MENU_SCHEME_CREATE_RELATION, "controller:create_relation"))

menus = [file_menu, scheme_menu]
