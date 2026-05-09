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

from PyQt6.QtCore import Qt, QTimer, pyqtSignal, pyqtSlot
from PyQt6.QtGui import QColor, QPainter, QPalette
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QSizePolicy, QWidget

from pireal.gui.theme.manager import get_theme_manager
from pireal.gui.theme.schema import ColorScheme, EditorColorRole


class _SymbolModePill(QWidget):
    clicked = pyqtSignal()

    _PADDING_H = 8
    _PADDING_V = 3

    def __init__(self, parent=None):
        super().__init__(parent)
        self._enabled = False
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setToolTip("Toggle symbol mode (σ, π, ⋈...)")
        fm = self.fontMetrics()
        self._text_on = "σ  symbols"
        self._text_off = "σ  symbols"
        width = fm.horizontalAdvance(self._text_on) + self._PADDING_H * 2
        height = fm.height() + self._PADDING_V * 2
        self.setFixedSize(width, height)

    def set_enabled(self, enabled: bool) -> None:
        self._enabled = enabled
        self.update()

    def mousePressEvent(self, a0):
        if a0 is not None and a0.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(a0)

    def paintEvent(self, a0) -> None:
        _ = a0
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        scheme = get_theme_manager().current_scheme
        if self._enabled:
            color = scheme.editor.get(EditorColorRole.SUCCESS)
        else:
            color = self.palette().color(QPalette.ColorRole.PlaceholderText)

        bg = QColor(color)
        bg.setAlpha(35)
        painter.setBrush(bg)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 2, 2)

        painter.setPen(color)
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "σ  symbols")


class _DbPill(QWidget):
    _PADDING_H = 8
    _PADDING_V = 3

    def __init__(self, parent=None):
        super().__init__(parent)
        self._text = ""
        self._modified = False
        self.setFixedHeight(self.fontMetrics().height() + self._PADDING_V * 2)

    def set_text(self, text: str) -> None:
        self._text = text
        self._update_width()

    def set_modified(self, modified: bool) -> None:
        self._modified = modified
        self._update_width()

    def _update_width(self) -> None:
        display = self._display_text()
        w = self.fontMetrics().horizontalAdvance(display) + self._PADDING_H * 2
        self.setFixedWidth(max(w, 10))
        self.update()

    def _display_text(self) -> str:
        return f"{self._text} •" if self._modified else self._text

    def paintEvent(self, a0) -> None:
        if not self._text:
            return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        scheme = get_theme_manager().current_scheme
        # color = self.palette().color(QPalette.ColorRole.LinkVisited) if self._modified else scheme.highlight
        color = QColor(210, 140, 30) if self._modified else scheme.highlight

        bg = QColor(color)
        bg.setAlpha(35)
        painter.setBrush(bg)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 2, 2)

        painter.setPen(color)
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, self._display_text())


class __DbPill(QWidget):
    _PADDING_H = 8
    _PADDING_V = 3

    def __init__(self, parent=None):
        super().__init__(parent)
        self._text = ""
        fm = self.fontMetrics()
        self._h = fm.height() + self._PADDING_V * 2
        self.setFixedHeight(self._h)

    def set_text(self, text: str) -> None:
        self._text = text
        fm = self.fontMetrics()
        w = fm.horizontalAdvance(text) + self._PADDING_H * 2
        self.setFixedWidth(max(w, 10))
        self.update()

    def paintEvent(self, a0) -> None:
        _ = a0

        if not self._text:
            return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        scheme = get_theme_manager().current_scheme
        color = scheme.highlight

        bg = QColor(color)
        bg.setAlpha(35)
        painter.setBrush(bg)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 2, 2)

        painter.setPen(color)
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, self._text)


class _LineColPill(QWidget):
    _PADDING_H = 8
    _PADDING_V = 3

    def __init__(self, parent=None):
        super().__init__(parent)
        self._text = ""
        fm = self.fontMetrics()
        self._h = fm.height() + self._PADDING_V * 2
        self.setFixedHeight(self._h)
        self.hide()

    def set_text(self, text: str) -> None:
        self._text = text
        fm = self.fontMetrics()
        w = fm.horizontalAdvance(text) + self._PADDING_H * 2
        self.setFixedWidth(max(w, 10))
        self.update()

    def paintEvent(self, a0) -> None:
        _ = a0

        if not self._text:
            return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        color = self.palette().color(QPalette.ColorRole.PlaceholderText)

        bg = QColor(color)
        bg.setAlpha(35)
        painter.setBrush(bg)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 2, 2)

        painter.setPen(color)
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, self._text)


class StatusBar(QWidget):
    """
    Status bar for RightPane.

    Left - db name (accent color)
    Center - temporary messages (errors, info)
    Right - Ln/Col, Symbol Mode, Theme toggle
    """

    symbolModeToggled = pyqtSignal(bool)

    _SEPARATOR = "  ·  "

    def __init__(self, parent=None):
        super().__init__(parent)
        fm = self.fontMetrics()
        self.setFixedHeight(fm.height() + 16)

        self._symbol_mode_on = False
        self._timer = QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.timeout.connect(self._clear_message)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(4, 0, 8, 0)
        layout.setSpacing(2)

        # Left - db name (always visible, StatusBar only lives with an open DB)
        self._db_label = _DbPill()
        layout.addWidget(self._db_label)

        # Center - temporary messages (expanding)
        self._message_label = QLabel()
        self._message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._message_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        layout.addWidget(self._message_label)

        # Right - technical indicators
        self._line_col_label = _LineColPill()
        # self._line_col_label.hide()

        self._symbol_mode_label = _SymbolModePill()
        self._symbol_mode_label.hide()
        self._symbol_mode_label.clicked.connect(self._on_symbol_mode_clicked)

        layout.addWidget(self._line_col_label)
        gap = QLabel(" ")
        gap.setStyleSheet(f"color: {self.palette().color(QPalette.ColorRole.Mid).name()};")
        layout.addWidget(gap)
        layout.addWidget(self._symbol_mode_label)

        self._apply_theme(get_theme_manager().current_scheme)
        get_theme_manager().themeChanged.connect(self._apply_theme)

    def show_message(self, msg: str, timeout: int = 4000, error: bool = False) -> None:
        self._timer.stop()
        if error:
            scheme = get_theme_manager().current_scheme
            color = scheme.editor.get(EditorColorRole.ERROR).name()
            self._message_label.setText(f'<span style="color:{color}">{msg}</span>')
        else:
            self._message_label.setText(msg)
        if timeout > 0:
            self._timer.start(timeout)

    def update_db_name(self, name: str) -> None:
        self._db_label.set_text(name)

    def update_line_col(self, line: int, col: int) -> None:
        self._line_col_label.set_text(f"Ln {line}, Col {col}")
        self._line_col_label.show()
        # self._sep1.show()

    def hide_line_col(self) -> None:
        self._line_col_label.hide()
        # self._sep1.hide()

    def show_symbol_mode(self, enabled: bool) -> None:
        self._symbol_mode_on = enabled
        self._symbol_mode_label.set_enabled(enabled)
        self._symbol_mode_label.show()

    @pyqtSlot()
    def _on_symbol_mode_clicked(self) -> None:
        self._symbol_mode_on = not self._symbol_mode_on
        self.show_symbol_mode(self._symbol_mode_on)
        self.symbolModeToggled.emit(self._symbol_mode_on)

    @pyqtSlot()
    def _clear_message(self) -> None:
        self._message_label.clear()

    @pyqtSlot(ColorScheme)
    def _apply_theme(self, scheme: ColorScheme) -> None:
        # FIXME: no se usa acá, revisar este slot
        # accent = scheme.editor.get(EditorColorRole.KEYWORD).name()
        # self._db_label.setStyleSheet(f"color: {accent};")
        self._db_label.update()
        self._refresh_symbol_mode_color()

    def _refresh_symbol_mode_color(self) -> None:
        scheme = get_theme_manager().current_scheme
        if self._symbol_mode_on:
            color = scheme.editor.get(EditorColorRole.SUCCESS).name()
        else:
            color = scheme.editor.get(EditorColorRole.ERROR).name()
        self._symbol_mode_label.setStyleSheet(f"color: {color};")

    def paintEvent(self, a0) -> None:
        super().paintEvent(a0)
        painter = QPainter(self)
        color = self.palette().color(self.palette().ColorRole.Mid)
        color.setAlpha(120)
        painter.setPen(color)
        painter.drawLine(0, 0, self.width(), 0)

    def set_db_modified(self, modified: bool) -> None:
        self._db_label.set_modified(modified)
