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

import webbrowser

from PyQt5.QtWidgets import (
    QDialog,
    QGroupBox,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QSpacerItem,
    QSizePolicy,
    QGraphicsOpacityEffect,
    QPushButton,
    QCheckBox,
    QMessageBox,
    QComboBox,
    QFontComboBox,
    QLabel
)
from PyQt5.QtGui import QFontDatabase
from PyQt5.QtCore import (
    QPropertyAnimation,
    QParallelAnimationGroup,
    QRect,
    QSettings,
    QThread,
    pyqtSignal
)

from src.core import (
    settings,
    file_manager
)
from src.gui.main_window import Pireal
from src.gui import (
    overlay_widget,
    updater
)


class Preferences(QDialog):
    # Signal to warn that the window is closed
    settingsClosed = pyqtSignal()

    def __init__(self, parent=None):
        super(Preferences, self).__init__(parent)

        # Main container
        # This contains a grid
        main_box = QVBoxLayout(self)
        main_box.setContentsMargins(200, 50, 200, 100)

        # The grid contains two containers
        # left container and right container
        grid = QGridLayout()

        # Left Container
        left_container = QVBoxLayout()
        left_container.setContentsMargins(0, 0, 0, 0)

        # General
        group_gral = QGroupBox(self.tr("General"))
        box_gral = QVBoxLayout(group_gral)
        # Updates
        btn_updates = QPushButton(self.tr("Check for updates"))
        box_gral.addWidget(btn_updates)
        # Language
        group_language = QGroupBox(self.tr("Language"))
        box = QVBoxLayout(group_language)
        # Find .qm files in language path
        available_langs = file_manager.get_files_from_folder(
            settings.LANG_PATH)

        languages = ["English"] + available_langs
        self._combo_lang = QComboBox()
        box.addWidget(self._combo_lang)
        self._combo_lang.addItems(languages)
        self._combo_lang.currentIndexChanged[int].connect(
            self._change_lang)
        if settings.LANGUAGE:
            self._combo_lang.setCurrentText(settings.LANGUAGE)
        box.addWidget(QLabel(self.tr("(Requires restart)")))

        # Add widgets
        left_container.addWidget(group_gral)
        left_container.addWidget(group_language)
        left_container.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding,
                                           QSizePolicy.Expanding))

        # Right Container
        right_container = QVBoxLayout()
        right_container.setContentsMargins(0, 0, 0, 0)

        # Editor
        editor_group = QGroupBox(self.tr("Editor Configurations"))
        box_editor = QHBoxLayout(editor_group)
        # Current line
        self._highlight_current_line = QCheckBox(
            self.tr("Highlight Current Line"))
        self._highlight_current_line.setChecked(
            settings.HIGHLIGHT_CURRENT_LINE)
        self._highlight_current_line.stateChanged[int].connect(
            self.__current_line_value_changed)
        box_editor.addWidget(self._highlight_current_line)
        # Matching paren
        self._matching_paren = QCheckBox(self.tr("Matching Parenthesis"))
        self._matching_paren.setChecked(
            settings.MATCHING_PARENTHESIS)
        self._matching_paren.stateChanged[int].connect(
            self.__set_enabled_matching_parenthesis)
        box_editor.addWidget(self._matching_paren)
        # Font group
        font_group = QGroupBox(self.tr("Font"))
        font_grid = QGridLayout(font_group)
        font_grid.addWidget(QLabel(self.tr("Family")), 0, 0)
        self._combo_font = QFontComboBox()
        self._combo_font.setCurrentFont(settings.FONT)
        font_grid.addWidget(self._combo_font, 0, 1)
        font_grid.addWidget(QLabel(self.tr("Point Size")), 1, 0)
        self._combo_font_size = QComboBox()
        fdb = QFontDatabase()
        combo_sizes = fdb.pointSizes(settings.FONT.family())
        current_size_index = combo_sizes.index(
            settings.FONT.pointSize())

        self._combo_font_size.addItems([str(f) for f in combo_sizes])
        self._combo_font_size.setCurrentIndex(current_size_index)
        font_grid.addWidget(self._combo_font_size, 1, 1)

        right_container.addWidget(editor_group)
        right_container.addWidget(font_group)
        right_container.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding,
                                            QSizePolicy.Expanding))

        # Add widgets
        grid.addLayout(left_container, 0, 0)
        grid.addLayout(right_container, 0, 1)
        main_box.addLayout(grid)

        # Button close and reset
        hbox = QHBoxLayout()
        hbox.setSpacing(20)
        hbox.addItem(QSpacerItem(1, 0, QSizePolicy.Expanding))
        btn_cancel = QPushButton(self.tr("Back"))
        hbox.addWidget(btn_cancel)
        btn_reset = QPushButton(self.tr("Reset Configurations"))
        hbox.addWidget(btn_reset)
        main_box.addLayout(hbox)

        # Overlay
        self.overlay = overlay_widget.OverlayWidget(self)
        self.overlay.hide()

        # Effect and animations
        self.effect = QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.effect)
        duration, x = 180, 150  # Animation duration
        # Animation start
        # Opacity animation
        self.opacity_animation_s = QPropertyAnimation(self.effect, b"opacity")
        self.opacity_animation_s.setDuration(duration)
        self.opacity_animation_s.setStartValue(0.0)
        self.opacity_animation_s.setEndValue(1.0)
        # X animation
        self.x_animation_s = QPropertyAnimation(self, b"geometry")
        self.x_animation_s.setDuration(duration)
        self.x_animation_s.setStartValue(QRect(x, 0, parent.width(),
                                               parent.height()))
        self.x_animation_s.setEndValue(QRect(0, 0, parent.width(),
                                             parent.height()))
        # Animation end
        # Opacity animation
        self.opacity_animation_e = QPropertyAnimation(self.effect, b"opacity")
        self.opacity_animation_e.setDuration(duration)
        self.opacity_animation_e.setStartValue(1.0)
        self.opacity_animation_e.setEndValue(0.0)
        # X animation
        self.x_animation_e = QPropertyAnimation(self, b"geometry")
        self.x_animation_e.setDuration(duration)
        self.x_animation_e.setStartValue(QRect(0, 0, parent.width(),
                                               parent.height()))
        self.x_animation_e.setEndValue(QRect(-x, 0, parent.width(),
                                             parent.height()))

        # Group animation start
        self.group_animation_s = QParallelAnimationGroup()
        self.group_animation_s.addAnimation(self.opacity_animation_s)
        self.group_animation_s.addAnimation(self.x_animation_s)

        # Group animation end
        self.group_animation_e = QParallelAnimationGroup()
        self.group_animation_e.addAnimation(self.opacity_animation_e)
        self.group_animation_e.addAnimation(self.x_animation_e)

        # Connections
        self.group_animation_e.finished.connect(
            self._on_group_animation_finished)
        btn_cancel.clicked.connect(self.close)
        btn_reset.clicked.connect(self._reset_settings)
        btn_updates.clicked.connect(self._check_for_updates)
        # self.thread.finished.connect(self._on_thread_finished)
        self._combo_font.currentFontChanged.connect(
            self._change_font)
        self._combo_font_size.currentTextChanged.connect(
            self._change_font_size)

    def __current_line_value_changed(self, value):
        settings.set_setting("highlight_current_line", value)
        settings.HIGHLIGHT_CURRENT_LINE = value

    def __set_enabled_matching_parenthesis(self, value):
        settings.set_setting("matching_parenthesis", value)
        settings.MATCHING_PARENTHESIS = value

    def _change_font(self, font):
        # FIXME: un quilombo esto
        central = Pireal.get_service("central")
        mcontainer = central.get_active_db()
        if mcontainer is not None:
            query_widget = mcontainer.query_container.currentWidget()
            if query_widget is not None:
                weditor = query_widget.get_editor()
                if weditor is not None:
                    weditor.set_font(font)
                    settings.set_setting("font", font)

    def _change_font_size(self, size):
        # FIXME: un quilombo esto
        font = self._combo_font.currentFont()
        font.setPointSize(int(size))
        central = Pireal.get_service("central")
        mcontainer = central.get_active_db()
        if mcontainer is not None:
            query_widget = mcontainer.query_container.currentWidget()
            if query_widget is not None:
                weditor = query_widget.get_editor()
                if weditor is not None:
                    weditor.set_font(font)
                    settings.set_setting("font", font)

    def showEvent(self, event):
        super(Preferences, self).showEvent(event)
        self.group_animation_s.start()

    def resizeEvent(self, event):
        self.overlay.resize(self.size())
        event.accept()

    def done(self, result):
        self.res = result
        self.group_animation_e.start()

    def _on_group_animation_finished(self):
        super(Preferences, self).done(self.res)
        self.settingsClosed.emit()

    def _check_for_updates(self):
        # Thread
        self._thread = QThread()
        self._updater = updater.Updater()
        self._updater.moveToThread(self._thread)
        self._thread.started.connect(self._updater.check_updates)
        self._updater.finished.connect(self.__on_thread_update_finished)
        # Show overlay widget
        self.overlay.show()
        # Start thread
        self._thread.start()

    def __on_thread_update_finished(self):
        # Hide overlay widget
        self.overlay.hide()
        self._thread.quit()
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
            else:
                msg.setWindowTitle(self.tr("Information"))
                msg.setText(self.tr("Last version installed"))
                msg.addButton(self.tr("Ok"),
                              QMessageBox.AcceptRole)
                msg.exec_()
        else:
            msg.critical(self, self.tr("Error"),
                         self.tr("Connection error"))

        self._thread.deleteLater()
        self._updater.deleteLater()

    def _reset_settings(self):
        """ Remove all settings """

        msg = QMessageBox(self)
        msg.setWindowTitle(self.tr("Reset Settings"))
        msg.setText(self.tr("Are you sure you want to clear all settings?"))
        msg.setIcon(QMessageBox.Question)
        msg.addButton(self.tr("No"), QMessageBox.NoRole)
        yes_btn = msg.addButton(self.tr("Yes"),
                                QMessageBox.YesRole)
        msg.exec_()
        r = msg.clickedButton()
        if r == yes_btn:
            QSettings(settings.SETTINGS_PATH, QSettings.IniFormat).clear()
            self.close()

    def _change_lang(self, index):
        lang = self._combo_lang.itemText(index)
        settings.set_setting('language', lang)
