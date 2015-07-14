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

from PyQt4.QtGui import (
    QFrame,
    QFontMetrics,
    QPainter,
    QColor
)


class Sidebar(QFrame):
    """ Sidebar widget """

    def __init__(self, editor):
        super(Sidebar, self).__init__(editor)
        self.editor = editor

    def paintEvent(self, event):
        """This method draws a left sidebar

        :param event: QEvent
        """

        bottom = self.editor.viewport().height()
        font_metrics = QFontMetrics(self.editor.document().defaultFont())
        current_line = self.editor.document().findBlock(
            self.editor.textCursor().position())
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor("#D0D0D0"))
        block = self.editor.firstVisibleBlock()
        vpoffset = self.editor.contentOffset()
        line = block.blockNumber()
        painter.setFont(self.editor.document().defaultFont())

        while block.isValid():
            line += 1
            pos = self.editor.blockBoundingGeometry(block).topLeft() + vpoffset
            if pos.y() > bottom:
                break

            print(current_line)
            if block.isVisible():
                fm_ascent = font_metrics.ascent()
                fm_descent = font_metrics.descent()
                painter.drawText(self.width() -
                                 font_metrics.width(str(line)) - 7,
                                 pos.y() + fm_ascent + fm_descent, str(line))

            block = block.next()
        painter.end()
        QFrame.paintEvent(self, event)

    def update_area(self):
        """ This method adjust the width of the sidebar """

        # Length number, for example: 120 = 3
        line = len(str(self.editor.blockCount())) + 1
        width = self.fontMetrics().width('0' * line)
        if self.width() != width:
            self.setFixedWidth(width)
            self.editor.setViewportMargins(width, 0, 0, 0)
        self.update()
