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

from PyQt6.QtWidgets import (
    QMainWindow,
    QMessageBox,
    QSystemTrayIcon,
    QFrame,
    QGridLayout,
    QLabel,
    QToolButton,
    QHBoxLayout,
    QApplication,
)
from PyQt6.QtGui import QIcon

from PyQt6.QtCore import (
    QSettings,
    QThread,
    Qt,
    QTimer,
    pyqtSlot as Slot,
    pyqtSignal as Signal,
)

import pireal
from pireal import keymap
from pireal.gui.central_widget import CentralWidget
from pireal.gui.database_container import DatabaseContainer
from pireal.gui.updater import Updater
from pireal.gui import (
    menu_actions,
)

from pireal.settings import SETTINGS
from pireal.gui.theme import apply_theme
from pireal import __version__
from pireal.dirs import DATA_SETTINGS
from pireal import translations as tr


class _StatusBar(QFrame):
    """Status bar divide in three areas"""

    playClicked = Signal()
    gearClicked = Signal()
    moonClicked = Signal(bool)
    expandClicked = Signal(bool)

    def __init__(self, main_window: QMainWindow, parent=None):
        super().__init__(parent)
        self._main_window = main_window

        layout = QGridLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        left_widget = QFrame(parent)
        mid_widget = QFrame(parent)
        right_widget = QFrame(parent)

        left_layout = QHBoxLayout(left_widget)
        left_widget.setLayout(left_layout)
        left_layout.setContentsMargins(0, 0, 0, 0)
        mid_layout = QHBoxLayout(mid_widget)
        mid_widget.setLayout(mid_layout)
        mid_layout.setContentsMargins(0, 0, 0, 0)
        right_layout = QHBoxLayout(right_widget)
        right_widget.setLayout(right_layout)
        right_layout.setContentsMargins(0, 0, 0, 0)

        # Left widgets
        self._messages_label = QLabel()
        self._messages_label.setText(f"Pireal v{__version__}")
        left_layout.addWidget(self._messages_label)
        # Mid widgets
        self._line_col_label = QLabel("Line: 0, Col: 0")
        self._line_col_label.hide()
        mid_layout.addWidget(self._line_col_label)
        # Right widgets
        execute_button = QToolButton()
        execute_button.setAutoRaise(True)
        execute_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        execute_button.setText("\uf04b")
        execute_button.clicked.connect(lambda: self.playClicked.emit())
        right_layout.addWidget(execute_button)
        dark_mode_button = QToolButton()
        dark_mode_button.setAutoRaise(True)
        dark_mode_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        dark_mode_button.setCheckable(True)
        dark_mode_button.setChecked(SETTINGS.dark_mode)
        dark_mode_button.setText("\uf186")
        dark_mode_button.toggled.connect(lambda v: self.moonClicked.emit(v))
        right_layout.addWidget(dark_mode_button)
        settings_button = QToolButton()
        settings_button.setAutoRaise(True)
        settings_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        settings_button.setText("\uf013")
        settings_button.clicked.connect(lambda: self.gearClicked.emit())
        right_layout.addWidget(settings_button)

        fullscreen_button = QToolButton()
        fullscreen_button.setAutoRaise(True)
        fullscreen_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        fullscreen_button.setText("\uf065")
        fullscreen_button.setCheckable(True)
        fullscreen_button.setChecked(self._main_window.isFullScreen())
        fullscreen_button.toggled.connect(lambda v: self.expandClicked.emit(v))
        right_layout.addWidget(fullscreen_button)

        layout.addWidget(left_widget, 0, 0, 0, 1, Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(mid_widget, 0, 1, 0, 1, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(right_widget, 0, 2, 0, 1, Qt.AlignmentFlag.AlignRight)

        layout.setContentsMargins(2, 0, 2, 0)

    def show_message(self, msg: str, timeout=4000):
        self._messages_label.setText(msg)
        if timeout > 0:
            QTimer.singleShot(timeout, self._messages_label.clear)

    def update_line_and_col(self, line, col):
        if not self._line_col_label.isVisible():
            self._line_col_label.show()
        self._line_col_label.setText("Line: {}, Col: {}".format(line, col))


class Pireal(QMainWindow):

    """
    Main Window class

    This class is responsible for installing all application services.
    """

    def __init__(self, check_updates=True):
        pireal.instance = self
        QMainWindow.__init__(self)
        self.setWindowTitle("Pireal")
        self.setMinimumSize(880, 600)
        # Load window geometry
        qsettings = QSettings(str(DATA_SETTINGS), QSettings.Format.IniFormat)
        window_maximized = qsettings.value("window_max", True)
        if window_maximized:
            self.showMaximized()
        else:
            size = qsettings.value("window_size")
            self.resize(size)
            position = qsettings.value("window_pos")
            self.move(position)

        # Central widget
        self.central_widget = CentralWidget()
        self.setCentralWidget(self.central_widget)
        self.central_widget.add_start_page()

        self.db_container: DatabaseContainer | None = None

        # Menu bar)
        menubar = self.menuBar()
        self.__load_menubar(menubar)

        # Status bar
        self.status_bar = _StatusBar(self, parent=self.statusBar())
        self.statusBar().addWidget(self.status_bar, 1)
        self.statusBar().setStyleSheet(
            "QStatusBar { margin: 0; padding: 0; border-top: 1px solid palette(dark); }"
        )
        self.statusBar().setSizeGripEnabled(False)
        self.statusBar().show()
        self.status_bar.gearClicked.connect(self.central_widget.show_settings)
        self.status_bar.moonClicked.connect(self.toggle_theme)
        self.status_bar.playClicked.connect(self.central_widget.execute_queries)
        self.status_bar.expandClicked.connect(self.toggle_maximized)

        if check_updates:
            self.tray = QSystemTrayIcon(QIcon("icons:pireal_icon.png"))
            self.tray.setToolTip(tr.TR_TOOLTIP_VERSION_AVAILABLE)
            self.tray.activated.connect(self._on_system_tray_clicked)
            self.tray.messageClicked.connect(self._on_system_tray_message_clicked)

            updater_thread = QThread(self)
            self._updater = Updater()
            self._updater.moveToThread(updater_thread)
            updater_thread.started.connect(self._updater.check_updates)
            self._updater.finished.connect(updater_thread.quit)
            updater_thread.finished.connect(updater_thread.deleteLater)
            self._updater.finished.connect(self._on_updater_finished)
            updater_thread.start()

    @Slot(QSystemTrayIcon.ActivationReason)
    def _on_system_tray_clicked(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.open_download_release()
            self.tray.hide()

    @Slot(bool)
    def toggle_theme(self, value: bool):
        qapp = QApplication.instance()
        SETTINGS.dark_mode = value
        apply_theme(qapp)
        self.statusBar().setStyleSheet(
            "QStatusBar { margin: 0; padding: 0; border-top: 1px solid palette(dark); }"
        )

        active_db = self.central_widget.get_active_db()
        if active_db is not None:
            editor_widget = active_db.query_container.currentWidget()
            if editor_widget is None:
                return
            editor = editor_widget.get_editor()
            if editor is not None:
                editor.re_paint()

    @Slot()
    def _on_system_tray_message_clicked(self):
        self.open_download_release()
        self.tray.hide()

    @Slot(bool)
    def toggle_maximized(self, value):
        if value:
            self.showFullScreen()
        else:
            self.showMaximized()

    def open_download_release(self):
        webbrowser.open_new("https://github.com/centaurialpha/pireal/releases/latest")

    def __load_menubar(self, menubar):
        """
        This method installs the menubar and toolbar, menus and QAction's,
        also connects to a slot each QAction.
        """
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

                    obj_name, slot = action.slot.split(":")

                    shortcut = keymap.KEYMAP.get(slot)
                    if shortcut is not None:
                        qaction.setShortcut(shortcut)

                    obj = self.central_widget
                    if obj_name == "pireal":
                        obj = self

                    func = getattr(obj, slot, None)
                    if callable(func):
                        qaction.triggered.connect(func)

    @Slot()
    def _on_updater_finished(self):
        if self._updater.version:
            self.tray.show()
            self.tray.showMessage(
                tr.TR_MSG_UPDATES,
                tr.TR_MSG_UPDATES_BODY.format(self._updater.version),
                QSystemTrayIcon.MessageIcon.Information,
                10000,
            )

        self._updater.deleteLater()

    def change_title(self, title=""):
        if title:
            _title = title + " - Pireal "
        else:
            _title = "Pireal"
        self.setWindowTitle(_title)

    def about_qt(self):
        """Show about qt dialog"""

        QMessageBox.aboutQt(self)

    def about_pireal(self):
        """Show the bout Pireal dialog"""

        from pireal.gui.dialogs import about_dialog

        dialog = about_dialog.AboutDialog(self)
        dialog.exec()

    def report_issue(self):
        """Open in the browser the page to create new  issue"""

        webbrowser.open("http://github.com/centaurialpha/pireal/issues/new")

    def show_hide_menubar(self):
        """Change visibility of menu bar"""

        if self.menuBar().isVisible():
            self.menuBar().hide()
        else:
            self.menuBar().show()

    def closeEvent(self, event):

        # Qt settings
        qsettings = QSettings(str(DATA_SETTINGS), QSettings.Format.IniFormat)

        qsettings.setValue("last_open_folder", self.central_widget.last_open_folder)
        qsettings.setValue("recent_databases", self.central_widget.recent_databases)

        # Save window geometry
        if self.isMaximized():
            qsettings.setValue("window_max", True)
        else:
            qsettings.setValue("window_max", False)
            qsettings.setValue("window_pos", self.pos())
            qsettings.setValue("window_size", self.size())

        if self.db_container is not None:
            # Save splitters size
            self.db_container.save_sizes()
            # Databases unsaved
            if self.db_container.modified:
                ret = QMessageBox.question(
                    self,
                    tr.TR_MSG_SAVE_CHANGES,
                    tr.TR_MSG_SAVE_CHANGES_BODY,
                    QMessageBox.StandardButton.Yes
                    | QMessageBox.StandardButton.No
                    | QMessageBox.StandardButton.Cancel,
                )
                if ret == QMessageBox.StandardButton.Yes:
                    self.central_widget.save_database()
                elif ret == QMessageBox.StandardButton.Cancel:
                    event.ignore()
            # Query files
            unsaved_editors = self.central_widget.get_unsaved_queries()
            if unsaved_editors:
                text = "\n".join([editor.name for editor in unsaved_editors])
                ret = QMessageBox.question(
                    self,
                    tr.TR_QUERY_NOT_SAVED,
                    tr.TR_QUERY_NOT_SAVED_BODY.format(files=text),
                    QMessageBox.StandardButton.Yes
                    | QMessageBox.StandardButton.No
                    | QMessageBox.StandardButton.Cancel,
                )

                if ret == QMessageBox.StandardButton.Yes:
                    for editor in unsaved_editors:
                        self.central_widget.save_query(editor)
                elif ret == QMessageBox.StandardButton.Cancel:
                    event.ignore()
