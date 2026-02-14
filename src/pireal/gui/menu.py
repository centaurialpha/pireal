from dataclasses import dataclass, field
from typing import List, Union

from PyQt6.QtGui import QAction, QIcon

from pireal import translations as tr


@dataclass
class Section:
    name: str


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
    items: List[Union["Menu", Action, Section, str]] = field(default_factory=list)

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
                if isinstance(item, Section):
                    qmenu.addSection(item.name)
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
                elif item == "separator":
                    qmenu.addSeparator()

        return menu_bar


file_menu = Menu("&File")
file_menu.add_item(Section("Database"))
file_menu.add_item(
    Action(tr.TR_MENU_FILE_NEW_DB, "controller:create_database", shorcut="Ctrl+N")
)
file_menu.add_item(
    Action(
        tr.TR_MENU_FILE_NEW_DB_FROM_TEXT,
        "controller:create_database_from_text",
        shorcut="Ctrl+Shift+N",
    )
)
file_menu.add_item(
    Action(tr.TR_MENU_FILE_OPEN_DB, "controller:open_database", shorcut="Ctrl+O")
)
file_menu.add_item("separator")
file_menu.add_item(
    Action(tr.TR_MENU_FILE_SAVE_DB, "controller:save_database", shorcut="Ctrl+S")
)
file_menu.add_item(Action(tr.TR_MENU_FILE_SAVE_AS_DB, "controller:save_database_as"))
file_menu.add_item(
    Action(tr.TR_MENU_FILE_CLOSE_DB, "controller:close_database", shorcut="Ctrl+W")
)
file_menu.add_item(Section("Query"))
file_menu.add_item(
    Action(tr.TR_MENU_FILE_NEW_QUERY, "controller:new_query", shorcut="Ctrl+T")
)
file_menu.add_item(
    Action(tr.TR_MENU_FILE_OPEN_QUERY, "controller:open_query", shorcut="Ctrl+Shift+O")
)
file_menu.add_item("separator")
file_menu.add_item(
    Action(tr.TR_MENU_FILE_SAVE_QUERY, "controller:save_query", shorcut="Ctrl+Shift+S")
)
file_menu.add_item(Action(tr.TR_MENU_FILE_SAVE_AS_QUERY, "controller:save_query_as"))
file_menu.add_item("separator")
file_menu.add_item(Action(tr.TR_MENU_FILE_QUIT, "controller:quit", shorcut="Ctrl+Q"))

scheme_menu = Menu("&Scheme")
scheme_menu.add_item(
    Action(tr.TR_MENU_SCHEME_CREATE_RELATION, "controller:create_relation")
)
# scheme_menu.add_item(
#     Action(tr.TR_MENU_SCHEME_REMOVE_RELATION, "controller:remove_relation")
# )
scheme_menu.add_item("separator")
scheme_menu.add_item(
    Action(
        tr.TR_MENU_SCHEME_EXECUTE_QUERIES, "controller:execute_queries", shorcut="F5"
    )
)

help_menu = Menu("&Help")
help_menu.add_item(Action(tr.TR_MENU_HELP_SHOW_TOUR, "controller:show_tour"))
help_menu.add_item("separator")
help_menu.add_item(Action(tr.TR_MENU_HELP_REPORT_ISSUE, "controller:report_issue"))
help_menu.add_item(Action(tr.TR_MENU_HELP_ABOUT_PIREAL, "controller:about_pireal"))
help_menu.add_item(Action(tr.TR_MENU_HELP_ABOUT_QT, "controller:about_qt"))

menus = [file_menu, scheme_menu, help_menu]
