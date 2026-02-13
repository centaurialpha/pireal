# -*- coding: utf-8 -*-
#
# Copyright 2015-2025 - Gabriel Acosta <acostadariogabriel@gmail.com>
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

"""Sidebar widget with line numbers.

based on:
john.nachtimwald.com/2009/08/19/better-qplaintextedit-with-line-numbers/
"""

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QColor, QFontMetrics, QPainter, QPen
from PyQt6.QtWidgets import QFrame

from pireal.gui.theme.manager import get_theme_manager
from pireal.gui.theme.schema import ColorScheme, EditorColorRole


class Sidebar(QFrame):
    """Sidebar widget"""

    def __init__(self, editor):
        super(Sidebar, self).__init__(editor)
        self.editor = editor

        self.editor.blockCountChanged.connect(self.update_viewport)
        self.editor.updateRequest.connect(self.update)

        theme_manager = get_theme_manager()
        theme_manager.themeChanged.connect(self._on_theme_changed)

        self._apply_colors(theme_manager.current_scheme)

    def _apply_colors(self, scheme: ColorScheme):
        """Aplica colores desde un ColorScheme."""
        editor = scheme.editor
        self._background_color = editor.get(EditorColorRole.SIDEBAR_BACKGROUND)
        self._foreground_color = editor.get(EditorColorRole.SIDEBAR_FOREGROUND)
        self.update()  # Forzar repaint

    def _on_theme_changed(self, scheme: ColorScheme):
        """Handler de cambio de tema."""
        self._apply_colors(scheme)

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
            self.editor.document().defaultFont()
        ).horizontalAdvance("9")
        return 5 + fmetrics_width * digits + 3

    def paintEvent(self, event):
        """This method draws a left sidebar

        :param event: QEvent
        """
        painter = QPainter(self)
        painter.fillRect(event.rect(), self._background_color)
        width = self.width() - 8
        height = self.editor.fontMetrics().height()
        font = self.editor.font()
        font_bold = self.editor.font()
        font_bold.setBold(True)
        painter.setFont(font)
        pen = QPen(self._foreground_color)
        painter.setPen(pen)
        current_line = self.editor.textCursor().blockNumber()

        for top, line, block in self.editor.visible_blocks:
            if line + 1 == self.editor._error_line:
                painter.setPen(QPen(QColor("#DD4040")))
                painter.setFont(font_bold)
            elif current_line == line:
                painter.setPen(pen)
                painter.setFont(font_bold)
            else:
                painter.setPen(pen)
                painter.setFont(font)
            painter.drawText(
                5, int(top), width, height, Qt.AlignmentFlag.AlignRight, str(line + 1)
            )
