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

from PyQt5.QtWidgets import (
    QApplication,
    QDialog,
    QGroupBox,
    QVBoxLayout,
    QHBoxLayout,
    QRadioButton,
    QSpacerItem,
    QSizePolicy,
    QGraphicsOpacityEffect,
    QToolButton,
    QPushButton,
    QCheckBox,
    QMessageBox,
    QComboBox,
    QStyleFactory
    #QLabel,
    #QMovie
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import (
    QPropertyAnimation,
    QParallelAnimationGroup,
    QRect,
    QSize,
    QSettings,
    pyqtSignal
)

from src import translations as tr
from src.core import (
    settings,
    file_manager
)
from src.gui import overlay_widget, updates


class Preferences(QDialog):
    settingsClosed = pyqtSignal()

    def __init__(self, parent=None):
        super(Preferences, self).__init__(parent)

        # Thread updates
        self.thread = updates.Updates()

        hbox = QHBoxLayout(self)
        hbox.setContentsMargins(50, 50, 500, 0)
        vbox = QVBoxLayout()
        btn_back = QToolButton()
        btn_back.setAutoRaise(True)
        btn_back.setIconSize(QSize(32, 32))
        btn_back.setIcon(QIcon(":img/arrow-left"))
        vbox.addWidget(btn_back)
        hbox.addLayout(vbox)
        vbox.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding,
                     QSizePolicy.Expanding))

        container = QVBoxLayout()
        container.setContentsMargins(0, 0, 0, 0)

        # General
        group_gral = QGroupBox(tr.TR_PREFERENCES_GROUP_GRAL)
        box_gral = QVBoxLayout(group_gral)
        # Start Page
        self._check_start_page = QCheckBox(tr.TR_PREFERENCES_CHECK_START_PAGE)
        self._check_start_page.setChecked(settings.PSettings.SHOW_START_PAGE)
        box_gral.addWidget(self._check_start_page)
        # Updates
        hhbox = QHBoxLayout()
        self._check_updates = QCheckBox(tr.TR_PREFERENCES_CHECK_UPDATES)
        self._check_updates.setChecked(settings.PSettings.CHECK_UPDATES)
        hhbox.addWidget(self._check_updates)
        btn_updates = QPushButton(tr.TR_PREFERENCES_BTN_CHECK_FOR_UPDATES)
        hhbox.addWidget(btn_updates)
        box_gral.addLayout(hhbox)

        # Language
        group_language = QGroupBox(tr.TR_PREFERENCES_GROUP_LANG)
        box = QVBoxLayout(group_language)
        # Find .qm files in language path
        available_langs = file_manager.get_files_from_folder(settings.LANG_PATH)

        languages = ["English"] + available_langs
        self._radio_buttons = []
        for lang in languages:
            radio = QRadioButton()
            self._radio_buttons.append(radio)
            radio.setText(lang)
            box.addWidget(radio)
        index = 0
        if settings.PSettings.LANGUAGE:
            for i in range(len(self._radio_buttons)):
                text = self._radio_buttons[i].text()
                if text == settings.PSettings.LANGUAGE:
                    index = i
        self._radio_buttons[index].setChecked(True)

        # Connect radio buttons
        for radiob in self._radio_buttons:
            radiob.clicked.connect(self._change_lang)

        # Stylesheet
        group_style = QGroupBox("Theme")
        box = QVBoxLayout(group_style)
        self.combo_themes = QComboBox()
        styles = QStyleFactory.keys()
        self.combo_themes.addItems(styles)
        current_style = QApplication.instance().style().objectName()
        try:
            index = styles.index(current_style.upper())
        except:
            index = styles.index(current_style.title())
        self.combo_themes.setCurrentIndex(index)
        box.addWidget(self.combo_themes)

        # Add widgets
        container.addWidget(group_gral)
        container.addWidget(group_language)
        container.addWidget(group_style)
        container.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding,
                          QSizePolicy.Expanding))
        btn_reset = QPushButton(tr.TR_PREFERENCES_BTN_RESET)
        btn_reset.setObjectName("cancel")
        container.addWidget(btn_reset)
        container.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding,
                          QSizePolicy.Expanding))

        hbox.addLayout(container)

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
        btn_back.clicked.connect(self.close)
        btn_reset.clicked.connect(self._reset_settings)
        btn_updates.clicked.connect(self._check_for_updates)
        self.thread.finished.connect(self._on_thread_finished)
        self.combo_themes.currentIndexChanged['QString'].connect(
            self._change_theme)

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
        self.overlay.show()
        self.thread.start()

    def _on_thread_finished(self):
        self.overlay.hide()

    def _reset_settings(self):
        """ Remove all settings """

        flags = QMessageBox.Yes
        flags |= QMessageBox.No
        result = QMessageBox.question(self, tr.TR_PREFERENCES_RESET_TITLE,
                                      tr.TR_PREFERENCES_RESET_MSG, flags)

        if result == QMessageBox.Yes:
            QSettings(settings.SETTINGS_PATH, QSettings.IniFormat).clear()
            self.close()

    def _change_lang(self):
        for radiob in self._radio_buttons:
            if radiob.isChecked():
                settings.set_setting('language', radiob.text())
                settings.PSettings.LANGUAGE = radiob.text()
        print(settings.PSettings.LANGUAGE)

    def _change_theme(self, style):
        #if self._radio_styles[0].isChecked():
            #name = 'Default'
            #style = file_manager.open_file(settings.STYLESHEET)
        #else:
            #style = None
            #name = ''
        QApplication.setStyle(style)
        settings.set_setting('stylesheet', style)
        settings.PSettings.THEME = style
