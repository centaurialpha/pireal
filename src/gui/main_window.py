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
    QMessageBox,
    QToolBar
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import (
    QSettings,
    QSize,
    QThread
)
from src.core import settings
from src.gui import (
    updater,
    message_error
)


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
        'undo_action',
        'redo_action',
        'cut_action',
        'copy_action',
        'paste_action',
        '',
        'create_new_relation',
        'remove_relation',
        'edit_relation',
        '',
        'execute_queries'
    ]

    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle(self.tr("Pireal"))
        self.setMinimumSize(700, 500)

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
        self.toolbar.setIconSize(QSize(22, 22))
        self.toolbar.setMovable(False)
        self.addToolBar(self.toolbar)

        # Menu bar
        menubar = self.menuBar()
        self.__load_menubar(menubar)
        # Load notification widget after toolbar actions
        notification_widget = Pireal.get_service("notification")
        self.toolbar.addWidget(notification_widget)
        # Message error
        self._msg_error_widget = message_error.MessageError(self)
        # Central widget
        central_widget = Pireal.get_service("central")
        central_widget.databaseSaved.connect(notification_widget.show_text)
        central_widget.querySaved.connect(notification_widget.show_text)
        self.setCentralWidget(central_widget)
        central_widget.add_start_page()

        # Check for updates
        self._thread = QThread()
        self._updater = updater.Updater()
        self._updater.moveToThread(self._thread)
        self._thread.started.connect(self._updater.check_updates)
        self._updater.finished.connect(self.__on_thread_update_finished)
        self._thread.start()
        notification_widget.show_text(
            self.tr("Checking for updates..."), time_out=0)

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

        central = Pireal.get_service("central")

        # Load menu bar
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
                    if obj.startswith('central'):
                        obj = central
                    else:
                        obj = self
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
                        qaction.triggered.connect(slot)

        # Install toolbar
        self.__install_toolbar(toolbar_items)
        # Disable some actions
        self.set_enabled_db_actions(False)
        self.set_enabled_relation_actions(False)
        self.set_enabled_query_actions(False)
        self.set_enabled_editor_actions(False)

    def __install_toolbar(self, toolbar_items):
        for action in Pireal.TOOLBAR_ITEMS:
            qaction = toolbar_items.get(action, None)
            if qaction is not None:
                self.toolbar.addAction(qaction)
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
        if not self._updater.error:
            if self._updater.version:
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
                    webbrowser.open_new(
                        "http://centaurialpha.github.io/pireal")
        self._thread.deleteLater()
        self._updater.deleteLater()

    def change_title(self, title):
        self.setWindowTitle("Pireal " + '[' + title + ']')

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
            'edit_relation'
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
            'uncomment'
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

    def closeEvent(self, event):
        qsettings = QSettings(settings.SETTINGS_PATH, QSettings.IniFormat)
        # Save window geometry
        if self.isMaximized():
            qsettings.setValue('window_max', True)
        else:
            qsettings.setValue('window_max', False)
            qsettings.setValue('window_pos', self.pos())
            qsettings.setValue('window_size', self.size())

        central_widget = Pireal.get_service("central")
        # Save recent databases
        qsettings.setValue('recent_databases',
                           central_widget.recent_databases)
        db = central_widget.get_active_db()
        if db is not None:
            # Save splitters size
            db.save_sizes()
            # Databases unsaved
            if db.modified:
                msg = QMessageBox(self)
                msg.setIcon(QMessageBox.Question)
                msg.setWindowTitle(self.tr("Some changes where not saved"))
                msg.setText(
                    self.tr("Do you want to save changes to the database?"))
                cancel_btn = msg.addButton(self.tr("Cancel"),
                                           QMessageBox.RejectRole)
                msg.addButton(self.tr("No"),
                              QMessageBox.NoRole)
                yes_btn = msg.addButton(self.tr("Yes"),
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
                msg.setWindowTitle(self.tr("Unsaved Queries"))
                text = '\n'.join([editor.name for editor in unsaved_editors])
                msg.setText(self.tr("{files}<br><br>Do you want to "
                                    "save them?".format(files=text)))
                cancel_btn = msg.addButton(self.tr("Cancel"),
                                           QMessageBox.RejectRole)
                msg.addButton(self.tr("No"),
                              QMessageBox.NoRole)
                yes_btn = msg.addButton(self.tr("Yes"),
                                        QMessageBox.YesRole)
                msg.exec_()
                if msg.clickedButton() == yes_btn:
                    for editor in unsaved_editors:
                        central_widget.save_query(editor)
                if msg.clickedButton() == cancel_btn:
                    event.ignore()
