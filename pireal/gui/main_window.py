# -*- coding: utf-8 -*-
#
# Copyright 2015-2020 - Gabriel Acosta <acostadariogabriel@gmail.com>
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
import logging
from typing import List

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QMessageBox

from PyQt5.QtGui import QIcon

from PyQt5.QtCore import pyqtSignal as Signal
from PyQt5.QtCore import pyqtSlot as Slot
from PyQt5.QtCore import QThread
# from PyQt5.QtCore import QSize

from pireal import translations as tr
from pireal import keymap
from pireal.gui.updater import Updater
from pireal.gui.central_widget import CentralWidget
from pireal.gui import menu_actions

from pireal.core.settings import (
    DATA_SETTINGS,
    USER_SETTINGS
)

logger = logging.getLogger('gui.main_window')

TOOLBAR_ITEMS: List[str] = [
    'create_database',
    'save_database',
    'new_query',
    'save_query',
    '',  # separator
    'create_relation',
    'remove_relation',
    '',
    'execute_query'

]


class Pireal(QMainWindow):

    """
    Main Window class

    This class is responsible for installing all application services.
    """
    __ACTIONS = {}
    goingDown = Signal()

    def __init__(self, check_updates=True):
        QMainWindow.__init__(self)
        self.setWindowTitle('Pireal')
        # Load window geometry
        geometry = DATA_SETTINGS.value('window_geometry')
        if geometry is None:
            self.showMaximized()
        else:
            self.restoreGeometry(geometry)
        self.toolbar = self.addToolBar('')

        # Central widget
        self.central_widget = CentralWidget(self)
        self.setCentralWidget(self.central_widget)
        # Menu bar
        self._load_menubar()

        if check_updates:
            updater_thread = QThread(self)
            self.updater = Updater()
            self.updater.moveToThread(updater_thread)
            updater_thread.started.connect(self.updater.check_updates)
            self.updater.finished.connect(updater_thread.quit)
            updater_thread.finished.connect(updater_thread.deleteLater)
            self.updater.finished.connect(self._on_thread_updater_finished)
            updater_thread.start()

    def show_status_message(self, message, *, timeout=4000):
        self.statusBar().showMessage(message, timeout)

    def switch_theme(self):
        USER_SETTINGS.dark_mode = not USER_SETTINGS.dark_mode
        USER_SETTINGS.save()

    @classmethod
    def get_action(cls, name):
        """ Return the instance of a loaded QAction """

        return cls.__ACTIONS.get(name, None)

    @classmethod
    def load_action(cls, name, action):
        """ Load a QAction """

        cls.__ACTIONS[name] = action

    def _load_menubar(self):
        """
        This method installs the menubar and toolbar, menus and QAction's,
        also connects to a slot each QAction.
        """

        logger.debug('loading menu bar')
        toolbar_actions = {}
        menu_bar = self.menuBar()

        for menu in menu_actions.MENU:
            menu_name, actions = menu.values()

            qmenu = menu_bar.addMenu(menu_name)
            for action in actions:
                if isinstance(action, str):
                    qmenu.addSection(action)
                elif not action:
                    qmenu.addSeparator()
                else:
                    qaction = qmenu.addAction(action.name)
                    if action.is_checkable:
                        qaction.setCheckable(True)
                        attr = qaction.text().lower().replace(' ', '_')
                        try:
                            attr_value = getattr(USER_SETTINGS, attr)
                        except AttributeError as reason:
                            # ok, not big deal
                            logger.warning(reason)
                        else:
                            qaction.setChecked(attr_value)

                    obj_name, slot = action.slot.split(':')

                    if slot in TOOLBAR_ITEMS:
                        toolbar_actions[slot] = qaction

                    shortcut = keymap.KEYMAP.get(slot)
                    if shortcut is not None:
                        qaction.setShortcut(shortcut)

                    obj = self.central_widget
                    if obj_name == 'pireal':
                        obj = self

                    func = getattr(obj, slot, None)
                    if callable(func):
                        qaction.triggered.connect(func)

        for toolbar_item in TOOLBAR_ITEMS:
            if toolbar_item:
                qaction = toolbar_actions[toolbar_item]
                qaction.setIcon(QIcon(f':img/{toolbar_item}'))
                self.toolbar.addAction(qaction)
            else:
                self.toolbar.addSeparator()

    @Slot()
    def _on_thread_updater_finished(self):
        if self.updater.version:
            reply = QMessageBox.information(
                self,
                'New Version!',
                'Visit?',
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                from pireal import __url__
                webbrowser.open(__url__)

        self.updater.deleteLater()

    def update_title(self):
        text = 'Pireal'
        if self.central_widget.has_db():
            db_name = self.central_widget.db_panel.db.display_name()
            text = f'Pireal - {tr.TR_NOTIFICATION_DB_CONNECTED} {db_name}'
        self.setWindowTitle(text)

    def about_qt(self):
        """ Show about qt dialog """

        QMessageBox.aboutQt(self)

    def about_pireal(self):
        """ Show the bout Pireal dialog """

        from pireal.gui.dialogs import AboutDialog
        dialog = AboutDialog(self)
        dialog.exec_()

    def report_issue(self):
        """ Open in the browser the page to create new  issue """

        webbrowser.open("http://github.com/centaurialpha/pireal/issues/new")

    def save_settings(self):
        """Save data settings"""
        # Save window geometry
        logger.debug('saving settings')
        DATA_SETTINGS.setValue(
            'window_geometry', self.saveGeometry())
        # Save last folder
        if self.central_widget.last_open_folder is not None:
            DATA_SETTINGS.setValue(
                'lastOpenFolder', self.central_widget.last_open_folder)
        # Save recent databases
        DATA_SETTINGS.setValue(
            'recentDbs', self.central_widget.recent_databases)

    def closeEvent(self, event):
        logger.debug('shutting down')
        # self.goingDown.emit()
        # self.central_widget.goingDown.emit()
        self.save_settings()
        # self.central_widget.save_state()
        # if self.central_widget.has_db():
        #     pass
        #     if self.central_widget.db.is_dirty():
        #         reply = QMessageBox.question(
        #             self,
        #             tr.TR_MSG_SAVE_CHANGES,
        #             tr.TR_MSG_SAVE_CHANGES_BODY,
        #             QMessageBox.Cancel | QMessageBox.Yes | QMessageBox.No
        #         )
        #         if reply == QMessageBox.Yes:
        #             self.central_widget.save_database()
        #     TODO: misma lógica para las queries sin guardar
