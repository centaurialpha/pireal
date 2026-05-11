# Copyright 2015-2026 - Gabriel Acosta <acostadariogabriel@gmail.com>
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

from collections.abc import Callable

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QPainter
from PyQt6.QtWidgets import QWidget


class Pill(QWidget):
    """
    Reusable pill-shaped label
    """

    _PADDING_H = 8
    _PADDING_V = 3

    def __init__(
        self,
        color_fn: Callable[[], QColor],
        text: str = "",
        radius: int = 2,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._color_fn = color_fn
        self._radius = radius
        self._text = ""
        self.setFixedHeight(self.fontMetrics().height() + self._PADDING_V * 2)
        if text:
            self.set_text(text)

    def set_text(self, text: str) -> None:
        self._text = text
        width = self.fontMetrics().horizontalAdvance(text) + self._PADDING_H * 2
        self.setFixedWidth(max(width, 1))
        self.update()

    def paintEvent(self, a0) -> None:
        if not self._text:
            return

        _ = a0

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        color = self._color_fn()
        background_color = QColor(color)
        background_color.setAlpha(35)
        painter.setBrush(background_color)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), self._radius, self._radius)

        painter.setPen(color)
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, self._text)


class ClickablePill(Pill):
    """
    Pill that emits clicked and shows hover feedback
    """

    clicked = pyqtSignal()

    def __init__(
        self,
        color_fn: Callable[[], QColor],
        text: str = "",
        radius: int = 2,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(color_fn, text, radius, parent)
        self._hovered = False
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def mousePressEvent(self, a0) -> None:
        if a0 is not None and a0.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(a0)

    def enterEvent(self, event) -> None:
        self._hovered = True
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, a0) -> None:
        self._hovered = False
        self.update()
        super().leaveEvent(a0)

    def paintEvent(self, a0) -> None:
        if not self._text:
            return

        _ = a0

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        color = self._color_fn()
        background_color = QColor(color)
        background_color.setAlpha(60 if self._hovered else 35)
        painter.setBrush(background_color)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), self._radius, self._radius)

        painter.setPen(color)
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, self._text)
