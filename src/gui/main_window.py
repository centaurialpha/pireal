# -*- coding: utf-8 -*-
#
# Copyright 2015 - Gabriel Acosta <acostadariogabriel@gmail.com>
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

""" Pireal Main Window """

from collections import Callable
from PyQt4.QtGui import (
    QMainWindow,
    QMessageBox,
    QToolBar,
    QIcon,
)
from PyQt4.QtCore import (
    SIGNAL,
    Qt
)


class Pireal(QMainWindow):

    """
    Main Window class

    This class is responsible for installing all application services.
    The services are in a dictionary that can be accessed
    from the class methods.

    """

    __SERVICES = {}
    __ACTIONS = {}

    # The name of items is the connection text
    TOOLBAR_ITEMS = [
        'create_data_base',
        'new_query',
        '',  # Is a separator!
        'open_file',
        'save_file',
        '',
        'undo_action',
        'redo_action',
        'cut_action',
        'copy_action',
        'paste_action',
        '',
        'create_new_relation',
        'remove_relation',
        'insert_tuple',
        'remove_tuple',
        '',
        'execute_queries'
    ]

    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle(self.tr("Pireal"))

        menubar = self.menuBar()
        self.__load_menubar(menubar)

        # Central widget
        central_widget = self.__load_ui()
        self.setCentralWidget(central_widget)
        #mdi = Pireal.get_service("mdi")
        #self.setCentralWidget(mdi)

        # Install service
        Pireal.load_service("pireal", self)

    @classmethod
    def get_service(cls, service):
        """ Return the instance of a loaded service """

        return cls.__SERVICES.get(service, None)

    @classmethod
    def load_service(cls, name, instance):
        """ Load a service providing the service name and the instance """

        cls.__SERVICES[name] = instance

    @classmethod
    def get_action(cls, name):
        """ Return the instance of a loaded QAction """

        return cls.__ACTIONS.get(name, None)

    @classmethod
    def load_action(cls, name, action):
        """ Load a QAction """

        cls.__ACTIONS[name] = action

    def __load_menubar(self, menubar):
        """
        This method installs the menubar and toolbar, menus and QAction's,
        also connects to a slot each QAction.
        """

        from src.gui import menu_actions
        from src import keymap

        # Keymap
        kmap = keymap.KEYMAP
        # Toolbar items
        toolbar_items = {}
        # Actions
        container = Pireal.get_service("container")

        for item in menu_actions.MENU:
            menubar_item = menu_actions.MENU[item]
            menu_name = menubar_item['name']
            items = menubar_item['items']
            menu = menubar.addMenu(menu_name)
            for menu_item in items:
                if isinstance(menu_item, str):
                    # Is a separator
                    menu.addSeparator()
                else:
                    action = menu_item['name']
                    obj, connection = menu_item['slot'].split(':')
                    obj = self if obj.startswith("pireal") else container
                    qaction = menu.addAction(action)

                    # Icon name is connection
                    icon = QIcon(":img/%s" % connection)
                    qaction.setIcon(icon)

                    # Install shortcuts
                    shortcut = kmap.get(connection, None)
                    if shortcut is not None:
                        qaction.setShortcut(shortcut)

                    # Items for toolbar
                    if connection in Pireal.TOOLBAR_ITEMS:
                        toolbar_items[connection] = qaction

                    # The name of QAction is the connection
                    Pireal.load_action(connection, qaction)
                    slot = getattr(obj, connection, None)
                    if isinstance(slot, Callable):
                        self.connect(qaction, SIGNAL("triggered()"), slot)

        # Install toolbar
        toolbar = QToolBar(self)
        for action in Pireal.TOOLBAR_ITEMS:
            qaction = toolbar_items.get(action, None)
            if qaction is not None:
                toolbar.addAction(qaction)
            else:
                toolbar.addSeparator()
        self.addToolBar(toolbar)

        self.enable_disable_db_actions(False)
        self.enable_disable_relation_actions(False)
        self.enable_disable_query_actions(False)

    def __load_ui(self):
        container = Pireal.get_service("container")
        container.show_start_page()
        # Query Widget
        query_widget = Pireal.get_service("query_widget")
        query_widget.hide()
        # Lateral Widget
        lateral = Pireal.get_service("lateral")
        lateral.hide()

        self.addDockWidget(Qt.LeftDockWidgetArea, lateral)
        self.addDockWidget(Qt.BottomDockWidgetArea, query_widget)

        return container

    def change_title(self, title):
        self.setWindowTitle(title + " - Pireal")

    def enable_disable_db_actions(self, enable=True):
        """ Public method. Enables or disables db QAction """

        actions = [
            'new_query',
            'save_file',
            'save_file_as',
            'create_new_relation',
            'remove_relation',
            'load_relation'
        ]

        for action in actions:
            qaction = Pireal.get_action(action)
            qaction.setEnabled(enable)

    def enable_disable_relation_actions(self, enable=True):
        """ Public method. Enables or disables relation's QAction """

        actions = [
            'insert_tuple',
            'remove_tuple',
            'execute_queries'
        ]

        for action in actions:
            qaction = Pireal.get_action(action)
            qaction.setEnabled(enable)

    def enable_disable_query_actions(self, enable=True):
        """ Public method. Enables or disables queries QAction """

        actions = [
            'undo_action',
            'redo_action',
            'copy_action',
            'cut_action',
            'paste_action',
            'execute_queries'
        ]

        for action in actions:
            qaction = Pireal.get_action(action)
            qaction.setEnabled(enable)

    def about_qt(self):
        """ Show about qt dialog """

        QMessageBox.aboutQt(self)
