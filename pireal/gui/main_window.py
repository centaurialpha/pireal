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
from typing import List, Dict

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QAction

from PyQt5.QtCore import QPoint
from PyQt5.QtCore import QSize
from PyQt5.QtCore import pyqtSignal as Signal

from pireal import translations as tr
from pireal import keymap
from pireal.gui import central_widget
from pireal.gui import menu_actions
from pireal.gui import theme

# FIXME: más arriba se usa settings, unificar
from pireal.core.settings import (
    DATA_SETTINGS,
    USER_SETTINGS
)

TOOLBAR_ITEMS: List[str] = []  # TODO: hacer esto cuando se active toolbar


class Pireal(QMainWindow):

    """
    Main Window class

    This class is responsible for installing all application services.
    """
    themeChanged = Signal()

    __ACTIONS: Dict[str, "QAction"] = {}

    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle('Pireal')
        self.setMinimumSize(1615, 850)
        # Load window geometry
        window_maximized = DATA_SETTINGS.value('ds/window_max', type=bool)
        if window_maximized:
            self.showMaximized()
        else:
            size = DATA_SETTINGS.value('ds/window_size', QSize(800, 600))
            self.resize(size)
            position = DATA_SETTINGS.value('ds/window_pos', QPoint(100, 100))
            self.move(position)
        # TODO: Create toolbar
        # TODO: Notification widget

        # Central widget
        self.central_widget = central_widget.CentralWidget(self)
        self.setCentralWidget(self.central_widget)
        self.central_widget.add_start_page()
        # Menu bar
        menubar = self.menuBar()
        self._load_menubar(menubar)

    def switch_theme(self):
        app = QApplication.instance()
        USER_SETTINGS.dark_mode = not USER_SETTINGS.dark_mode
        theme.apply_theme(app)
        USER_SETTINGS.save()
        self.themeChanged.emit()

    @classmethod
    def get_action(cls, name):
        """ Return the instance of a loaded QAction """

        return cls.__ACTIONS.get(name, None)

    @classmethod
    def load_action(cls, name, action):
        """ Load a QAction """

        cls.__ACTIONS[name] = action

    def _load_menubar(self, menubar):
        """
        This method installs the menubar and toolbar, menus and QAction's,
        also connects to a slot each QAction.
        """

        # Keymap
        kmap = keymap.KEYMAP

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
                    slot_name = menu_item['slot']

                    qaction = menu.addAction(action)
                    if slot_name is None:
                        continue

                    if menu_item.get('checkable', False):
                        qaction.setCheckable(True)
                        # FIXME: solo tengo en cuenta ese qaction
                        # Jugar un poco con Pireal.__ACTIONS
                        qaction.setChecked(USER_SETTINGS.dark_mode)

                    obj_name, connection = slot_name.split(':')

                    obj = self.central_widget
                    if obj_name.startswith('pireal'):
                        obj = self
                    # Install shortcuts
                    shortcut = kmap.get(connection, None)
                    if shortcut is not None:
                        qaction.setShortcut(shortcut)

                    Pireal.load_action(connection, qaction)
                    slot = getattr(obj, connection, None)
                    if callable(slot):
                        qaction.triggered.connect(slot)

        # Install toolbar
        # self.__install_toolbar(toolbar_items, rela_actions)
        # self.__install_toolbar(rela_actions)
        # Disable some actions
        # self.set_enabled_db_actions(False)
        # self.set_enabled_relation_actions(False)
        # self.set_enabled_query_actions(False)
        # self.set_enabled_editor_actions(False)

    # def __install_toolbar(self, rela_actions):
    #     menu = QMenu()
    #     tool_button = QToolButton()
    #     tool_button.setIcon(QIcon(":img/create_new_relation"))
    #     tool_button.setMenu(menu)
    #     tool_button.setPopupMode(QToolButton.InstantPopup)
    #     for item in self.TOOLBAR_ITEMS:
    #         if item:
    #             if item == "relation_menu":
    #                 # Install menu for relation
    #                 menu.addActions(rela_actions)
    #                 self.toolbar.addWidget(tool_button)
    #             else:
    #                 self.toolbar.addAction(self.__ACTIONS[item])
    #         else:
    #             self.toolbar.addSeparator()

    def __show_status_message(self, msg):
        # status = Pireal.get_service("status")
        # status.show_message(msg)
        # TODO
        pass

    def __on_thread_update_finished(self):
        self._thread.quit()
        # Clear notificator
        # notification_widget = Pireal.get_service("notification")
        # notification_widget.clear()
        # FIXME:

        msg = QMessageBox(self)
        if not self._updater.error and self._updater.version:
            version = self._updater.version
            msg.setWindowTitle(self.tr("New version available!"))
            msg.setText(self.tr("Check the web site to "
                                "download <b>Pireal {}</b>".format(version)))
            download_btn = msg.addButton(self.tr("Download!"), QMessageBox.YesRole)
            msg.addButton(tr.TR_MSG_CANCEL, QMessageBox.RejectRole)
            msg.exec_()
            r = msg.clickedButton()
            if r == download_btn:
                webbrowser.open_new("http://centaurialpha.github.io/pireal")
        self._thread.deleteLater()
        self._updater.deleteLater()

    def change_title(self, db_name=''):
        title = ''
        if db_name:
            title = tr.TR_NOTIFICATION_DB_CONNECTED.format(db_name)
        self.setWindowTitle(title + ' - Pireal')

    def set_enabled_actions(self, actions, value):
        for action in actions:
            qaction = Pireal.get_action(action)
            if qaction is not None:
                qaction.setEnabled(value)

    def set_enabled_db_actions(self, value):
        """ Public method. Enables or disables db QAction """

        actions = [
            'new_query',
            'open_query',
            'close_database',
            'save_database',
            'save_database_as',
        ]
        self.set_enabled_actions(actions, value)

    def set_enabled_relation_actions(self, value):
        """ Public method. Enables or disables relation's QAction """

        actions = (
            'create_new_relation',
            'remove_relation',
            'add_tuple',
            'delete_tuple',
        )
        self.set_enabled_actions(actions, value)

    def set_enabled_query_actions(self, value):
        """ Public method. Enables or disables queries QAction """

        actions = (
            'execute_queries',
            'save_query'
        )
        self.set_enabled_actions(actions, value)

    def set_enabled_editor_actions(self, value):
        """ Public slot. Enables or disables editor actions """

        actions = (
            'undo_action',
            'redo_action',
            'copy_action',
            'cut_action',
            'paste_action',
            'comment',
            'uncomment',
            'search'
        )
        self.set_enabled_actions(actions, value)

    def about_qt(self):
        """ Show about qt dialog """

        QMessageBox.aboutQt(self)

    def about_pireal(self):
        """ Show the bout Pireal dialog """

        from pireal.gui.dialogs import about_dialog
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

    # def show_hide_toolbar(self):
    #     """ Change visibility of tool bar """

    #     if self.toolbar.isVisible():
    #         self.toolbar.hide()
    #     else:
    #         self.toolbar.show()

    def show_error_message(self, text, syntax_error=True):
        self._msg_error_widget.show_msg(text, syntax_error)
        self._msg_error_widget.show()

    def save_settings(self):
        """Save data settings"""
        # Save window geometry
        if self.isMaximized():
            DATA_SETTINGS.setValue('window_max', True)
        else:
            DATA_SETTINGS.setValue('window_max', False)
            DATA_SETTINGS.setValue('window_pos', self.pos())
            DATA_SETTINGS.setValue('window_size', self.size())
        # Save last folder
        if self.central_widget.last_open_folder is not None:
            DATA_SETTINGS.setValue('lastOpenFolder', self.central_widget.last_open_folder)
        # Save recent databases
        DATA_SETTINGS.setValue('recentDbs', self.central_widget.recent_databases)

    def closeEvent(self, event):
        self.save_settings()

        # db = self.central_widget.get_active_db()
        # if db is not None:
        #     # Save splitters size
        #     db.save_sizes()
        #     # Databases unsaved
        #     if db.modified:
        #         msg = QMessageBox(self)
        #         msg.setIcon(QMessageBox.Question)
        #         msg.setWindowTitle(tr.TR_MSG_SAVE_CHANGES)
        #         msg.setText(tr.TR_MSG_SAVE_CHANGES_BODY)
        #         cancel_btn = msg.addButton(tr.TR_MSG_CANCEL, QMessageBox.RejectRole)
        #         msg.addButton(tr.TR_MSG_NO, QMessageBox.NoRole)
        #         yes_btn = msg.addButton(tr.TR_MSG_YES, QMessageBox.YesRole)
        #         msg.exec_()
        #         r = msg.clickedButton()
        #         if r == yes_btn:
        #             self.central_widget.save_database()
        #         if r == cancel_btn:
        #             event.ignore()
        #     # Query files
        #     unsaved_editors = self.central_widget.get_unsaved_queries()
        #     if unsaved_editors:
        #         msg = QMessageBox(self)
        #         msg.setIcon(QMessageBox.Question)
        #         msg.setWindowTitle(tr.TR_QUERY_NOT_SAVED)
        #         text = '\n'.join([editor.name for editor in unsaved_editors])
        #         msg.setText(tr.TR_QUERY_NOT_SAVED_BODY.format(files=text))
        #         cancel_btn = msg.addButton(tr.TR_MSG_CANCEL, QMessageBox.RejectRole)
        #         msg.addButton(tr.TR_MSG_NO, QMessageBox.NoRole)
        #         yes_btn = msg.addButton(tr.TR_MSG_YES, QMessageBox.YesRole)
        #         msg.exec_()
        #         if msg.clickedButton() == yes_btn:
        #             for editor in unsaved_editors:
        #                 self.central_widget.save_query(editor)
        #         if msg.clickedButton() == cancel_btn:
        #             event.ignore()
