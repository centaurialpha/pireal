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

from PyQt6.QtCore import (
    QPoint,
    QRect,
    Qt,
    pyqtSignal,
)
from PyQt6.QtGui import (
    QColor,
    QFont,
    QPainter,
    QPalette,
    QPolygon,
)
from PyQt6.QtWidgets import QWidget

from pireal import translations as tr
from pireal.gui.theme.manager import get_theme_manager
from pireal.gui.theme.schema import EditorColorRole


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


class TogglePill(ClickablePill):
    """
    Pill checkable
    """

    toggled = pyqtSignal(bool)

    def __init__(
        self,
        text: str = "",
        radius: int = 2,
        checked: bool = True,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(
            color_fn=lambda: self.palette().color(QPalette.ColorRole.Highlight),
            text=text,
            radius=radius,
            parent=parent,
        )
        self._checked = checked
        self.clicked.connect(self._on_clicked)

    @property
    def is_checked(self) -> bool:
        return self._checked

    def set_checked(self, checked: bool) -> None:
        if self._checked != checked:
            self._checked = checked
            self.update()
            self.toggled.emit(self._checked)

    def _on_clicked(self) -> None:
        self.set_checked(not self._checked)

    def paintEvent(self, a0) -> None:
        _ = a0
        if not self._text:
            return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        color = self._color_fn()
        bg = QColor(color)
        if self._checked:
            bg.setAlpha(70 if self._hovered else 50)
        else:
            bg.setAlpha(30 if self._hovered else 15)
        painter.setBrush(bg)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), self._radius, self._radius)

        text_color = QColor(color)
        text_color.setAlpha(255 if self._checked else 140)
        painter.setPen(text_color)
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, self._text)


class RunPill(QWidget):
    clicked = pyqtSignal()
    _PADDING_H = 12
    _PADDING_V = 4

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setToolTip("Run queries (F5)")
        fm = self.fontMetrics()
        icon_w = fm.height()
        gap = 6
        text_w = fm.horizontalAdvance("Run")
        w = self._PADDING_H * 2 + icon_w + gap + text_w
        h = fm.height() + self._PADDING_V * 2
        self.setFixedSize(w, h)
        self._success_color: QColor | None = None
        self._hovered = False
        self._refresh_color()
        get_theme_manager().themeChanged.connect(lambda _: self._refresh_color())

    def _refresh_color(self) -> None:
        self._success_color = get_theme_manager().current_scheme.editor.get(EditorColorRole.SUCCESS)
        self.update()

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
        if self._success_color is None:
            return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        bg = QColor(self._success_color)
        bg.setAlpha(60 if self._hovered else 35)
        painter.setBrush(bg)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 1, 1)

        fm = self.fontMetrics()
        icon_h = fm.height()
        total_w = icon_h + 6 + fm.horizontalAdvance("Run")
        x = (self.width() - total_w) // 2
        y_center = self.height() // 2

        icon_rect = QRect(x, y_center - icon_h // 2, icon_h, icon_h)
        painter.setPen(self._success_color)

        # Triángulo play
        points = [
            icon_rect.topLeft() + QPoint(2, 1),
            icon_rect.bottomLeft() + QPoint(2, -1),
            QPoint(icon_rect.right() - 1, y_center),
        ]

        painter.setBrush(self._success_color)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawPolygon(QPolygon(points))

        font = painter.font()
        font.setWeight(QFont.Weight.Medium)
        painter.setFont(font)
        painter.setPen(self._success_color)
        text_x = x + icon_h + 6
        painter.drawText(
            QRect(text_x, 0, fm.horizontalAdvance(tr.TR_RUN_PILL_LABEL), self.height()),
            Qt.AlignmentFlag.AlignVCenter,
            tr.TR_RUN_PILL_LABEL,
        )

        painter.restore() if False else None
