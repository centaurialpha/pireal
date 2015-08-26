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
    QCheckBox
)
from PyQt4.QtCore import (
    QPropertyAnimation,
    QParallelAnimationGroup,
    SIGNAL,
    QRect,
    QSize
)
from src import translations as tr


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
        box.addWidget(self._check_start_page)
        # Updates
        hhbox = QHBoxLayout()
        self._check_updates = QCheckBox(tr.TR_PREFERENCES_CHECK_UPDATES)
        hhbox.addWidget(self._check_updates)
        btn_updates = QPushButton(tr.TR_PREFERENCES_BTN_CHECK_FOR_UPDATES)
        hhbox.addWidget(btn_updates)
        box.addLayout(hhbox)

        # Language
        group_language = QGroupBox(tr.TR_PREFERENCES_GROUP_LANG)
        box = QVBoxLayout(group_language)
        languages = ["English", "Spanish"]
        for lang in languages:
            radio = QRadioButton()
            radio.setText(lang)
            box.addWidget(radio)

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
        # Animation start
        # Opacity animation
        self.opacity_animation_s = QPropertyAnimation(self.effect, "opacity")
        self.opacity_animation_s.setDuration(400)
        self.opacity_animation_s.setStartValue(0.0)
        self.opacity_animation_s.setEndValue(1.0)
        # X animation
        self.x_animation_s = QPropertyAnimation(self, "geometry")
        self.x_animation_s.setDuration(200)
        self.x_animation_s.setStartValue(QRect(300, 0, parent.width(),
                                       parent.height()))
        self.x_animation_s.setEndValue(QRect(0, 0, parent.width(),
                                     parent.height()))
        # Animation end
        # Opacity animation
        self.opacity_animation_e = QPropertyAnimation(self.effect, "opacity")
        self.opacity_animation_e.setDuration(200)
        self.opacity_animation_e.setStartValue(1.0)
        self.opacity_animation_e.setEndValue(0.0)
        # X animation
        self.x_animation_e = QPropertyAnimation(self, "geometry")
        self.x_animation_e.setDuration(200)
        self.x_animation_e.setStartValue(QRect(0, 0, parent.width(),
                                         parent.height()))
        self.x_animation_e.setEndValue(QRect(200, 0, parent.width(),
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

    def showEvent(self, event):
        super(Preferences, self).showEvent(event)
        self.group_animation_s.start()

    def done(self, result):
        self.res = result
        self.group_animation_e.start()

    def _on_group_animation_finished(self):
        super(Preferences, self).done(self.res)