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

import webbrowser
from collections import Callable

from PyQt5.QtWidgets import (
    QMainWindow,
    QMenu,
    QToolButton,
    QMessageBox,
    QToolBar
)
from PyQt5.QtGui import QIcon

from PyQt5.QtCore import QSettings
from PyQt5.QtCore import QSize
from PyQt5.QtCore import Qt

from src import keymap
from src.core import settings
from src.gui import (
    menu_actions,
    # message_error
)

from src.core.settings import CONFIG


class Pireal(QMainWindow):

    """
    Main Window class

    This class is responsible for installing all application services.
    """

    __SERVICES = {}
    __ACTIONS = {}

    # The name of items is the connection text
    TOOLBAR_ITEMS = [
        'create_database',
        'open_database',
        'save_database',
        '',  # Is a separator!
        'new_query',
        'open_query',
        'save_query',
        '',
        'relation_menu',
        '',
        # 'create_new_relation',
        # 'remove_relation',
        # '',
        # 'add_tuple',
        # 'delete_tuple',
        # 'add_column',
        # 'delete_column',
        # '',
        'execute_queries'
    ]

    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle(self.tr("Pireal"))
        self.setMinimumSize(880, 600)
        # Load window geometry
        qsettings = QSettings(settings.SETTINGS_PATH, QSettings.IniFormat)
        window_maximized = qsettings.value('window_max', True, type=bool)
        if window_maximized:
            self.showMaximized()
        else:
            size = qsettings.value('window_size')
            self.resize(size)
            position = qsettings.value('window_pos')
            self.move(position)
        # Toolbar
        self.toolbar = QToolBar(self)
        self.toolbar.setFixedWidth(38)
        self.toolbar.setIconSize(QSize(38, 38))
        self.toolbar.setMovable(False)
        self.addToolBar(Qt.RightToolBarArea, self.toolbar)

        # Menu bar
        menubar = self.menuBar()
        self.__load_menubar(menubar)
        # Load notification widget after toolbar actions
        notification_widget = Pireal.get_service("notification")
        self.toolbar.addWidget(notification_widget)
        # Message error
        # self._msg_error_widget = message_error.MessageError(self)
        # Central widget
        central_widget = Pireal.get_service("central")
        central_widget.databaseSaved.connect(notification_widget.show_text)
        central_widget.querySaved.connect(notification_widget.show_text)
        central_widget.databaseConected.connect(self.change_title)
        self.setCentralWidget(central_widget)
        central_widget.add_start_page()

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

        # Keymap
        kmap = keymap.KEYMAP

        central = Pireal.get_service("central")

        # Load menu bar
        rela_actions = []
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
                    obj_name, connection = menu_item['slot'].split(':')
                    obj = central
                    if obj_name.startswith('pireal'):
                        obj = self
                    qaction = menu.addAction(action)
                    # Icon name is connection
                    icon = QIcon(":img/%s" % connection)
                    qaction.setIcon(icon)

                    # Install shortcuts
                    shortcut = kmap.get(connection, None)
                    if shortcut is not None:
                        qaction.setShortcut(shortcut)

                    # The name of QAction is the connection
                    if item == "relation":
                        if connection != "execute_queries":
                            rela_actions.append(qaction)
                    Pireal.load_action(connection, qaction)
                    slot = getattr(obj, connection, None)
                    if isinstance(slot, Callable):
                        qaction.triggered.connect(slot)

        # Install toolbar
        # self.__install_toolbar(toolbar_items, rela_actions)
        self.__install_toolbar(rela_actions)
        # Disable some actions
        self.set_enabled_db_actions(False)
        self.set_enabled_relation_actions(False)
        self.set_enabled_query_actions(False)
        self.set_enabled_editor_actions(False)

    def __install_toolbar(self, rela_actions):
        menu = QMenu()
        tool_button = QToolButton()
        tool_button.setIcon(QIcon(":img/create_new_relation"))
        tool_button.setMenu(menu)
        tool_button.setPopupMode(QToolButton.InstantPopup)
        for item in self.TOOLBAR_ITEMS:
            if item:
                if item == "relation_menu":
                    # Install menu for relation
                    menu.addActions(rela_actions)
                    self.toolbar.addWidget(tool_button)
                else:
                    self.toolbar.addAction(self.__ACTIONS[item])
            else:
                self.toolbar.addSeparator()

    def __show_status_message(self, msg):
        status = Pireal.get_service("status")
        status.show_message(msg)

    def __on_thread_update_finished(self):
        self._thread.quit()
        # Clear notificator
        notification_widget = Pireal.get_service("notification")
        notification_widget.clear()

        msg = QMessageBox(self)
        if not self._updater.error and self._updater.version:
            version = self._updater.version
            msg.setWindowTitle(self.tr("New version available!"))
            msg.setText(self.tr("Check the web site to "
                                "download <b>Pireal {}</b>".format(
                                    version)))
            download_btn = msg.addButton(self.tr("Download!"),
                                         QMessageBox.YesRole)
            msg.addButton(self.tr("Cancel"),
                          QMessageBox.RejectRole)
            msg.exec_()
            r = msg.clickedButton()
            if r == download_btn:
                webbrowser.open_new("http://centaurialpha.github.io/pireal")
        self._thread.deleteLater()
        self._updater.deleteLater()

    def change_title(self, title=''):
        if title:
            _title = title + " - Pireal "
        else:
            _title = "Pireal"
        self.setWindowTitle(_title)

    def set_enabled_db_actions(self, value):
        """ Public method. Enables or disables db QAction """

        actions = [
            'new_query',
            'open_query',
            'close_database',
            'save_database',
            'save_database_as',
            'load_relation'
        ]

        for action in actions:
            qaction = Pireal.get_action(action)
            qaction.setEnabled(value)

    def set_enabled_relation_actions(self, value):
        """ Public method. Enables or disables relation's QAction """

        actions = [
            'create_new_relation',
            'remove_relation',
            'add_tuple',
            'delete_tuple',
            # 'add_column',
            # 'delete_column'
        ]

        for action in actions:
            qaction = Pireal.get_action(action)
            qaction.setEnabled(value)

    def set_enabled_query_actions(self, value):
        """ Public method. Enables or disables queries QAction """

        actions = [
            'execute_queries',
            'save_query'
        ]

        for action in actions:
            qaction = Pireal.get_action(action)
            qaction.setEnabled(value)

    def set_enabled_editor_actions(self, value):
        """ Public slot. Enables or disables editor actions """

        actions = [
            'undo_action',
            'redo_action',
            'copy_action',
            'cut_action',
            'paste_action',
            'zoom_in',
            'zoom_out',
            'comment',
            'uncomment',
            'search'
        ]

        for action in actions:
            qaction = Pireal.get_action(action)
            qaction.setEnabled(value)

    def about_qt(self):
        """ Show about qt dialog """

        QMessageBox.aboutQt(self)

    def about_pireal(self):
        """ Show the bout Pireal dialog """

        from src.gui.dialogs import about_dialog
        dialog = about_dialog.AboutDialog(self)
        dialog.exec_()

    def report_issue(self):
        """ Open in the browser the page to create new  issue """

        webbrowser.open("http://github.com/centaurialpha/pireal/issues/new")

    def show_hide_menubar(self):
        """ Change visibility of menu bar """

        if self.menuBar().isVisible():
            self.menuBar().hide()
        else:
            self.menuBar().show()

    def show_hide_toolbar(self):
        """ Change visibility of tool bar """

        if self.toolbar.isVisible():
            self.toolbar.hide()
        else:
            self.toolbar.show()

    def show_error_message(self, text, syntax_error=True):
        self._msg_error_widget.show_msg(text, syntax_error)
        self._msg_error_widget.show()

    def save_user_settings(self):
        central_widget = Pireal.get_service("central")
        CONFIG.set_value("lastOpenFolder", central_widget.last_open_folder)
        CONFIG.set_value("recentFiles", central_widget.recent_databases)

        # Write settings
        CONFIG.save_settings()

    def closeEvent(self, event):
        self.save_user_settings()

        # Qt settings
        qsettings = QSettings(settings.SETTINGS_PATH, QSettings.IniFormat)
        # # Save window geometry
        if self.isMaximized():
            qsettings.setValue('window_max', True)
        else:
            qsettings.setValue('window_max', False)
            qsettings.setValue('window_pos', self.pos())
            qsettings.setValue('window_size', self.size())

        central_widget = Pireal.get_service("central")
        db = central_widget.get_active_db()
        if db is not None:
            # Save splitters size
            db.save_sizes()
            # Databases unsaved
            if db.modified:
                msg = QMessageBox(self)
                msg.setIcon(QMessageBox.Question)
                msg.setWindowTitle(self.tr("Algunos cambios no fueron guardados"))
                msg.setText(
                    self.tr("Desea guardar los cambios en la base de datos?"))
                cancel_btn = msg.addButton(self.tr("Cancelar"),
                                           QMessageBox.RejectRole)
                msg.addButton(self.tr("No"),
                              QMessageBox.NoRole)
                yes_btn = msg.addButton(self.tr("Si"),
                                        QMessageBox.YesRole)
                msg.exec_()
                r = msg.clickedButton()
                if r == yes_btn:
                    central_widget.save_database()
                if r == cancel_btn:
                    event.ignore()
            # Query files
            unsaved_editors = central_widget.get_unsaved_queries()
            if unsaved_editors:
                msg = QMessageBox(self)
                msg.setIcon(QMessageBox.Question)
                msg.setWindowTitle(self.tr("Consultas no guardadas"))
                text = '\n'.join([editor.name for editor in unsaved_editors])
                msg.setText(self.tr("{files}\n\nQuiere guardarlas?".format(
                    files=text)))
                cancel_btn = msg.addButton(self.tr("Cancelar"),
                                           QMessageBox.RejectRole)
                msg.addButton(self.tr("No"),
                              QMessageBox.NoRole)
                yes_btn = msg.addButton(self.tr("Si"),
                                        QMessageBox.YesRole)
                msg.exec_()
                if msg.clickedButton() == yes_btn:
                    for editor in unsaved_editors:
                        central_widget.save_query(editor)
                if msg.clickedButton() == cancel_btn:
                    event.ignore()
