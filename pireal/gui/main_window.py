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

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLabel

from PyQt5.QtGui import QIcon

from PyQt5.QtCore import pyqtSignal as Signal
from PyQt5.QtCore import pyqtSlot as Slot
from PyQt5.QtCore import QThread
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import Qt

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


class _StatusBar(QFrame):
    """Status bar divide in three areas"""

    def __init__(self, main_window: QMainWindow, parent=None):
        super().__init__(parent)
        self._main_window = main_window

        layout = QGridLayout(self)

        left_widget = QFrame(self)
        mid_widget = QFrame(self)
        right_widget = QFrame(self)

        left_layout = QHBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        mid_layout = QHBoxLayout(mid_widget)
        mid_layout.setContentsMargins(0, 0, 0, 0)
        right_layout = QHBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)

        # Left widgets
        self._messages_label = QLabel()
        left_layout.addWidget(self._messages_label)
        # Mid widgets
        play = QPushButton()
        play.setIcon(QIcon(':/img/play'))
        right_layout.addWidget(play)
        # Right widgets
        settings_button = QPushButton()
        settings_button.setIcon(QIcon(':/img/configure-dark'))
        right_layout.addWidget(settings_button)

        fullscreen_button = QPushButton()
        fullscreen_button.setIcon(QIcon(':/img/fullscreen-dark'))
        fullscreen_button.setCheckable(True)
        right_layout.addWidget(fullscreen_button)


        layout.addWidget(left_widget, 0, 0, 0, 1, Qt.AlignLeft)
        layout.addWidget(mid_widget, 0, 1, 0, 1, Qt.AlignCenter)
        layout.addWidget(right_widget, 0, 2, 0, 1, Qt.AlignRight)

        layout.setContentsMargins(2, 0, 2, 0)

    def show_message(self, msg: str, timeout=0):
        self._messages_label.setText(msg)
        if timeout > 0:
            QTimer.singleShot(timeout, self._messages_label.clear)


class Pireal(QMainWindow):
    """
    Main Window class

    This class is responsible for installing all application services.
    """
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

        # Central widget
        self.central_widget = CentralWidget(self)
        self.setCentralWidget(self.central_widget)

        # Menu bar
        self._load_menubar()
        # Status bar
        self.status_bar = _StatusBar(self, parent=self.statusBar())
        self.statusBar().addWidget(self.status_bar, 1)
        self.statusBar().layout().setContentsMargins(0, 0, 0, 0)
        self.statusBar().show()

        if check_updates:
            updater_thread = QThread(self)
            self.updater = Updater()
            self.updater.moveToThread(updater_thread)
            updater_thread.started.connect(self.updater.check_updates)
            self.updater.finished.connect(updater_thread.quit)
            updater_thread.finished.connect(updater_thread.deleteLater)
            self.updater.finished.connect(self._on_thread_updater_finished)
            updater_thread.start()

    def toggle_full_screen(self, value: bool):
        if value:
            self.showFullScreen()
        else:
            self.showNormal()

    def show_message(self, message: str, duration: float = 5.0):
        """Show message in status bar"""
        duration = duration * 1000
        self.status_bar.show_message(message, timeout=duration)

    def _load_menubar(self):
        """
        This method installs the menubar, menus and QAction's,
        also connects to a slot each QAction.
        """

        logger.debug('loading menu bar')
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

                    shortcut = keymap.KEYMAP.get(slot)
                    if shortcut is not None:
                        qaction.setShortcut(shortcut)

                    obj = self.central_widget
                    if obj_name == 'pireal':
                        obj = self

                    func = getattr(obj, slot, None)
                    if callable(func):
                        qaction.triggered.connect(func)

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
            db_name = self.central_widget.db_panel.db.display_name
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
