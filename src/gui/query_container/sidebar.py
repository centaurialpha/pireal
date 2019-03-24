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

"""
Sidebar widget with line numbers

based on:
john.nachtimwald.com/2009/08/19/better-qplaintextedit-with-line-numbers/
"""

from PyQt5.QtWidgets import QFrame
from PyQt5.QtGui import (
    QFontMetrics,
    QPainter,
    QPen,
    QColor,
)
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QSize


class Sidebar(QFrame):
    """ Sidebar widget """

    def __init__(self, editor):
        super(Sidebar, self).__init__(editor)
        self.editor = editor

        self.editor.blockCountChanged.connect(self.update_viewport)
        self.editor.updateRequest.connect(self.update)
        # self.editor.blockCountChanged.connect(self.editor.update)

    def sizeHint(self):
        return QSize(self.__calculate_width(), 0)

    def redimensionar(self):
        cr = self.editor.contentsRect()
        current_x = cr.left()
        top = cr.top()
        height = cr.height()
        width = self.sizeHint().width()
        self.setGeometry(current_x, top, width, height)

    def update_viewport(self):
        self.editor.setViewportMargins(self.sizeHint().width(), 0, 0, 0)

    def __calculate_width(self):
        digits = len(str(max(1, self.editor.blockCount())))
        fmetrics_width = QFontMetrics(
            self.editor.document().defaultFont()).width("9")
        return 5 + fmetrics_width * digits + 3

    def paintEvent(self, event):
        """This method draws a left sidebar

        :param event: QEvent
        """

        painter = QPainter(self)
        painter.fillRect(event.rect(), Qt.white)
        width = self.width() - 8
        height = self.editor.fontMetrics().height()
        font = self.editor.font()
        font_bold = self.editor.font()
        font_bold.setBold(True)
        painter.setFont(font)
        pen = QPen(Qt.gray)
        painter.setPen(QPen(QColor("#e9e9e9")))
        painter.drawLine(width + 7, 0, width + 7, event.rect().height())
        painter.setPen(pen)
        current_line = self.editor.textCursor().blockNumber()

        for top, line, block in self.editor.visible_blocks:
            if current_line == line:
                painter.setFont(font_bold)
            else:
                painter.setFont(font)
            painter.drawText(5, top, width, height,
                             Qt.AlignRight, str(line + 1))
