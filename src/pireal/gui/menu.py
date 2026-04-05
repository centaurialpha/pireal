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

from dataclasses import dataclass, field
from typing import Union

from PyQt6.QtGui import QAction, QIcon

from pireal import translations as tr
from pireal.core.db import DB
from pireal.registry import Registry


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
    requires_db: bool = False
    requires_modified: bool = False


@dataclass
class Menu:
    name: str
    items: list[Union["Menu", Action, Section, str]] = field(default_factory=list)

    def add_item(self, item):
        self.items.append(item)
        return self


class MenuBuilder:
    def __init__(self, main_window, controller):
        self.main_window = main_window
        self.controller = controller
        self.db_dependent_actions = []
        self.modified_dependent_actions = []

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

                    if item.requires_db:
                        self.db_dependent_actions.append(qaction)
                    if item.requires_modified:
                        self.modified_dependent_actions.append(qaction)

                    qmenu.addAction(qaction)
                elif item == "separator":
                    qmenu.addSeparator()

        db = Registry.get("db", DB)
        db.databaseStateChanged.connect(self._update_actions)
        db.hasModified.connect(self._update_actions)

        self._update_actions()

        return menu_bar

    def _update_actions(self):
        from pireal.core.db import DB
        from pireal.registry import Registry

        db = Registry.get("db", DB)

        # Acciones que solo requieren DB abierta
        for action in self.db_dependent_actions:
            action.setEnabled(db.is_active)

        # Acciones que requieren DB abierta Y modificada
        for action in self.modified_dependent_actions:
            action.setEnabled(db.is_active and db.modified)


file_menu = Menu(tr.TR_MENU_FILE)
file_menu.add_item(Section("Database"))
file_menu.add_item(Action(tr.TR_MENU_FILE_NEW_DB, "controller:create_database", shorcut="Ctrl+N"))
file_menu.add_item(
    Action(
        tr.TR_MENU_FILE_NEW_DB_FROM_TEXT,
        "controller:create_database_from_text",
        shorcut="Ctrl+Shift+N",
    )
)
file_menu.add_item(Action(tr.TR_MENU_FILE_OPEN_DB, "controller:open_database", shorcut="Ctrl+O"))
file_menu.add_item("separator")
file_menu.add_item(
    Action(tr.TR_MENU_FILE_SAVE_DB, "controller:save_database", shorcut="Ctrl+S", requires_modified=True)
)
file_menu.add_item(Action(tr.TR_MENU_FILE_SAVE_AS_DB, "controller:save_database_as"))
file_menu.add_item(Action(tr.TR_MENU_FILE_CLOSE_DB, "controller:close_database", shorcut="Ctrl+W"))
file_menu.add_item(Section("Query"))
file_menu.add_item(Action(tr.TR_MENU_FILE_NEW_QUERY, "controller:new_query", shorcut="Ctrl+T"))
file_menu.add_item(Action(tr.TR_MENU_FILE_OPEN_QUERY, "controller:open_query", shorcut="Ctrl+Shift+O"))
file_menu.add_item(Action(tr.TR_MENU_FILE_CLOSE_QUERY, "controller:close_query"))
file_menu.add_item("separator")
file_menu.add_item(Action(tr.TR_MENU_FILE_SAVE_QUERY, "controller:save_query", shorcut="Ctrl+Shift+S"))
file_menu.add_item(Action(tr.TR_MENU_FILE_SAVE_AS_QUERY, "controller:save_query_as"))
file_menu.add_item("separator")
file_menu.add_item(Action(tr.TR_MENU_FILE_QUIT, "controller:quit", shorcut="Ctrl+Q"))

scheme_menu = Menu("&Scheme")
scheme_menu.add_item(Action(tr.TR_MENU_SCHEME_CREATE_RELATION, "controller:create_relation"))
# scheme_menu.add_item(
#     Action(tr.TR_MENU_SCHEME_REMOVE_RELATION, "controller:remove_relation")
# )
scheme_menu.add_item("separator")
scheme_menu.add_item(Action(tr.TR_MENU_SCHEME_EXECUTE_QUERIES, "controller:execute_queries", shorcut="F5"))

help_menu = Menu("&Help")
help_menu.add_item(Action(tr.TR_MENU_HELP_REPORT_ISSUE, "controller:report_issue"))
help_menu.add_item(Action(tr.TR_MENU_HELP_ABOUT_PIREAL, "controller:about_pireal"))
help_menu.add_item(Action(tr.TR_MENU_HELP_ABOUT_QT, "controller:about_qt"))

menus = [file_menu, scheme_menu, help_menu]
