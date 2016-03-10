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

# Based on A full widget waiting indicator
# https://wiki.python.org/moin/PyQt

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import (
    QPainter,
    QBrush,
    QColor,
    QPen
)
from PyQt5.QtCore import Qt


class OverlayWidget(QWidget):

    def __init__(self, parent=None):

        QWidget.__init__(self, parent)

    def paintEvent(self, event):

        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(event.rect(), QBrush(QColor(255, 255, 255, 127)))
        painter.setPen(QPen(Qt.NoPen))

        for i in range(3):
            if (self.counter / 3) % 3 == i:
                painter.setBrush(QBrush(QColor(99, 137, 168)))
            else:
                painter.setBrush(QBrush(QColor(127, 127, 127)))
            painter.drawEllipse(self.width() / 2.5 + 50 * i,
                                self.height() / 2, 35, 35)

        painter.end()

    def showEvent(self, event):

        self.timer = self.startTimer(100)
        self.counter = 0

    def timerEvent(self, event):

        self.counter += 3
        self.update()
