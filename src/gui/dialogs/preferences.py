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

from PyQt4.QtGui import (
    QDialog,
    QGroupBox,
    QVBoxLayout,
    QHBoxLayout,
    QRadioButton,
    QSpacerItem,
    QSizePolicy,
    QGraphicsOpacityEffect,
    QIcon,
    QToolButton,
    QPushButton,
    QCheckBox,
    QMessageBox
)
from PyQt4.QtCore import (
    QPropertyAnimation,
    QParallelAnimationGroup,
    SIGNAL,
    QRect,
    QSize,
    QSettings
)
from src import translations as tr
from src.core import (
    settings,
    file_manager
)


class Preferences(QDialog):

    def __init__(self, parent=None):
        super(Preferences, self).__init__(parent)

        hbox = QHBoxLayout(self)
        hbox.setContentsMargins(50, 50, 500, 0)
        vbox = QVBoxLayout()
        btn_back = QToolButton()
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
        box = QVBoxLayout(group_gral)
        # Start Page
        self._check_start_page = QCheckBox(tr.TR_PREFERENCES_CHECK_START_PAGE)
        self._check_start_page.setChecked(settings.PSettings.SHOW_START_PAGE)
        box.addWidget(self._check_start_page)
        # Updates
        hhbox = QHBoxLayout()
        self._check_updates = QCheckBox(tr.TR_PREFERENCES_CHECK_UPDATES)
        self._check_updates.setChecked(settings.PSettings.CHECK_UPDATES)
        hhbox.addWidget(self._check_updates)
        btn_updates = QPushButton(tr.TR_PREFERENCES_BTN_CHECK_FOR_UPDATES)
        hhbox.addWidget(btn_updates)
        box.addLayout(hhbox)

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
            self.connect(radiob, SIGNAL("clicked()"), self._change_lang)
        # Add widgets
        container.addWidget(group_gral)
        container.addWidget(group_language)
        container.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding,
                          QSizePolicy.Expanding))
        btn_reset = QPushButton(tr.TR_PREFERENCES_BTN_RESET)
        btn_reset.setObjectName("cancel")
        container.addWidget(btn_reset)
        container.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding,
                          QSizePolicy.Expanding))

        hbox.addLayout(container)

        # Effect and animations
        self.effect = QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.effect)
        duration = 180  # 1.8 s
        x = 150
        # Animation start
        # Opacity animation
        self.opacity_animation_s = QPropertyAnimation(self.effect, "opacity")
        self.opacity_animation_s.setDuration(duration)
        self.opacity_animation_s.setStartValue(0.0)
        self.opacity_animation_s.setEndValue(1.0)
        # X animation
        self.x_animation_s = QPropertyAnimation(self, "geometry")
        self.x_animation_s.setDuration(duration)
        self.x_animation_s.setStartValue(QRect(x, 0, parent.width(),
                                       parent.height()))
        self.x_animation_s.setEndValue(QRect(0, 0, parent.width(),
                                     parent.height()))
        # Animation end
        # Opacity animation
        self.opacity_animation_e = QPropertyAnimation(self.effect, "opacity")
        self.opacity_animation_e.setDuration(duration)
        self.opacity_animation_e.setStartValue(1.0)
        self.opacity_animation_e.setEndValue(0.0)
        # X animation
        self.x_animation_e = QPropertyAnimation(self, "geometry")
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
        self.connect(self.group_animation_e, SIGNAL("finished()"),
                     self._on_group_animation_finished)
        self.connect(btn_back, SIGNAL("clicked()"),
                     self.close)
        self.connect(btn_reset, SIGNAL("clicked()"),
                     self._reset_settings)
        #self.connect(self._check_start_page,
                     #SIGNAL("valueChanged(QString, PyQt_PyObject)"),
                     #lambda v, k: self.emit(
                         #SIGNAL("valueChanged(QString, PyQt_PyObject)"), v, k))

    def showEvent(self, event):
        super(Preferences, self).showEvent(event)
        self.group_animation_s.start()

    def done(self, result):
        self.res = result
        self.group_animation_e.start()

    def _on_group_animation_finished(self):
        super(Preferences, self).done(self.res)
        self.emit(SIGNAL("settingsClosed()"))

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

#class CheckBox(QCheckBox):

    #def __init__(self, text, parent=None):
        #super(CheckBox, self).__init__(text, parent)
        #self.connect(self, SIGNAL("stateChanged(int)"), self._state_changed)

    #def _state_changed(self, value):
        #key = "show-start-page"
        #self.emit(SIGNAL("valueChanged(QString, PyQt_PyObject)"), key, value)
