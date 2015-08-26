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
    QComboBox,
    QSpacerItem,
    QSizePolicy,
    QGraphicsOpacityEffect
)
from PyQt4.QtCore import (
    #Qt,
    QPropertyAnimation,
    QParallelAnimationGroup,
    #QAbstractAnimation,
    #QEasingCurve,
    SIGNAL,
    QRect
)
from src import translations as tr


class Preferences(QDialog):

    def __init__(self, parent=None):
        super(Preferences, self).__init__(parent)

        container = QVBoxLayout(self)
        container.setContentsMargins(0, 0, 0, 0)

        group_language = QGroupBox(tr.TR_PREFERENCES_GROUP_LANG)
        box = QVBoxLayout(group_language)
        self._combo_lang = QComboBox()
        self._combo_lang.addItems(['English', 'Spanish'])
        box.addWidget(self._combo_lang)

        container.addWidget(group_language)
        container.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding,
                          QSizePolicy.Expanding))

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

        self.connect(self.group_animation_e, SIGNAL("finished()"),
                    self._on_group_animation_finished)

    def showEvent(self, event):
        super(Preferences, self).showEvent(event)
        self.group_animation_s.start()

    def done(self, result):
        self.res = result
        self.group_animation_e.start()

    def _on_group_animation_finished(self):
        super(Preferences, self).done(self.res)