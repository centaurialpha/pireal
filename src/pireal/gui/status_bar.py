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
from PyQt6.QtGui import QPainter
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QSizePolicy, QWidget

from pireal.gui.theme.manager import get_theme_manager
from pireal.gui.theme.schema import ColorScheme, EditorColorRole


class _ClickableLabel(QLabel):
    clicked = pyqtSignal()

    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def mousePressEvent(self, ev):
        assert ev is not None
        if ev.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(ev)


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
        layout.setContentsMargins(8, 0, 8, 0)
        layout.setSpacing(0)

        # Left - db name (always visible, StatusBar only lives with an open DB)
        self._db_label = QLabel()
        layout.addWidget(self._db_label)

        # Center - temporary messages (expanding)
        self._message_label = QLabel()
        self._message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._message_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        layout.addWidget(self._message_label)

        # Right - technical indicators
        self._line_col_label = QLabel()
        self._line_col_label.hide()

        self._sep1 = QLabel(self._SEPARATOR)
        self._sep1.hide()

        self._symbol_mode_label = _ClickableLabel()
        self._symbol_mode_label.hide()
        self._symbol_mode_label.clicked.connect(self._on_symbol_mode_clicked)

        # Right side: line_col, symbol_mode
        for widget in (
            self._line_col_label,
            self._sep1,
            self._symbol_mode_label,
        ):
            layout.addWidget(widget)

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
        self._db_label.setText(name)

    def update_line_col(self, line: int, col: int) -> None:
        self._line_col_label.setText(f"Ln {line}, Col {col}")
        self._line_col_label.show()
        self._sep1.show()

    def hide_line_col(self) -> None:
        self._line_col_label.hide()
        self._sep1.hide()

    def show_symbol_mode(self, enabled: bool) -> None:
        self._symbol_mode_on = enabled
        self._symbol_mode_label.setText(f"Symbol Mode: {'On' if enabled else 'Off'}")
        self._symbol_mode_label.show()
        self._refresh_symbol_mode_color()

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
        accent = scheme.editor.get(EditorColorRole.KEYWORD).name()
        self._db_label.setStyleSheet(f"color: {accent};")
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
