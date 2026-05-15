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

from PyQt6.QtCore import (
    Qt,
    QTimer,
    pyqtSignal,
    pyqtSlot,
)
from PyQt6.QtGui import (
    QColor,
    QPainter,
)
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QWidget,
)

from pireal.gui.theme.manager import get_theme_manager
from pireal.gui.theme.schema import (
    ColorScheme,
    EditorColorRole,
)
from pireal.gui.widgets import (
    ClickablePill,
    RunPill,
    TextPill,
)
from pireal.registry import Registry


class DBPill(ClickablePill):
    def __init__(self, parent=None):
        super().__init__(color_fn=lambda: get_theme_manager().current_scheme.highlight, parent=parent)
        self._modified = False
        self._base_text = ""
        self.setCursor(Qt.CursorShape.ArrowCursor)
        self.clicked.connect(self._on_clicked)

    def set_text(self, text: str) -> None:
        self._base_text = text
        super().set_text(self._display_text())

    def set_modified(self, modified: bool) -> None:
        self._modified = modified
        self._color_fn = lambda: (
            QColor(210, 140, 30) if self._modified else get_theme_manager().current_scheme.highlight
        )
        self.setCursor(Qt.CursorShape.PointingHandCursor if modified else Qt.CursorShape.ArrowCursor)
        super().set_text(self._display_text())

    def _display_text(self) -> str:
        return f"{self._base_text} •" if self._modified else self._base_text

    @pyqtSlot()
    def _on_clicked(self) -> None:
        if not self._modified:
            return
        from pireal.gui.controller import Controller

        Registry.get("controller", Controller).save_database()

    def paintEvent(self, a0) -> None:
        # hover solo activo cuando modificado
        if not self._modified:
            self._hovered = False
        super().paintEvent(a0)


class SymbolModePill(ClickablePill):
    def __init__(self, parent=None):
        self._enabled = False
        super().__init__(color_fn=self._symbol_color, text="σ symbols", parent=parent)
        self.setToolTip("Toggle symbol mode (σ/π/⋈...)")

    def _symbol_color(self) -> QColor:
        scheme = get_theme_manager().current_scheme
        return (
            scheme.editor.get(EditorColorRole.SUCCESS)
            if self._enabled
            else scheme.editor.get(EditorColorRole.FOREGROUND)
        )

    def set_enabled(self, enabled: bool) -> None:
        self._enabled = enabled
        self.update()


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
        layout.setSpacing(6)

        # Left - db name (always visible, StatusBar only lives with an open DB)
        self._db_label = DBPill()
        layout.addWidget(self._db_label)

        # Center - temporary messages (expanding)
        self._message_label = QLabel()
        self._message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._message_label.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Preferred)
        self._message_label.setMinimumWidth(0)
        layout.addWidget(self._message_label)

        self._pipeline_pill = TextPill(
            color_fn=lambda: get_theme_manager().current_scheme.editor.get(EditorColorRole.KEYWORD),
        )
        self._pipeline_pill.hide()

        # Right - technical indicators
        self._line_col_label = TextPill(
            color_fn=lambda: get_theme_manager().current_scheme.editor.get(EditorColorRole.FOREGROUND),
        )

        self._symbol_mode_label = SymbolModePill()
        self._symbol_mode_label.hide()
        self._symbol_mode_label.clicked.connect(self._on_symbol_mode_clicked)

        self._block_pill = TextPill(
            color_fn=lambda: get_theme_manager().current_scheme.editor.get(EditorColorRole.FOREGROUND),
        )
        self._block_pill.hide()
        layout.addWidget(self._block_pill)

        self._run_pill = RunPill()
        self._run_pill.clicked.connect(self._on_run_clicked)

        layout.addWidget(self._line_col_label)
        layout.addWidget(self._pipeline_pill)
        layout.addWidget(self._symbol_mode_label)
        layout.addWidget(self._run_pill)

        self._apply_theme(get_theme_manager().current_scheme)
        get_theme_manager().themeChanged.connect(self._apply_theme)

    def show_pipeline(self, text: str) -> None:
        self._pipeline_pill.set_text(text)
        self._pipeline_pill.show()

    def hide_pipeline(self) -> None:
        self._pipeline_pill.hide()

    def set_current_block(self, name: str) -> None:
        if name:
            self._block_pill.set_text(name)
            self._block_pill.show()
        else:
            self._block_pill.hide()

    def show_message(self, msg: str, timeout: int = 4000, error: bool = False) -> None:
        self._timer.stop()
        if error:
            scheme = get_theme_manager().current_scheme
            color = scheme.editor.get(EditorColorRole.ERROR).name()
            self._message_label.setText(f'<span style="color:{color}">{msg}</span>')
        else:
            self._message_label.setText(msg)
        self._message_label.setToolTip(msg)
        if timeout > 0:
            self._timer.start(timeout)

    def update_db_name(self, name: str) -> None:
        self._db_label.set_text(name)

    def update_line_col(self, line: int, col: int) -> None:
        self._line_col_label.set_text(f"Ln {line}, Col {col}")
        self._line_col_label.show()

    def hide_line_col(self) -> None:
        self._line_col_label.hide()

    def show_symbol_mode(self, enabled: bool) -> None:
        self._symbol_mode_on = enabled
        self._symbol_mode_label.set_enabled(enabled)
        self._symbol_mode_label.show()

    @pyqtSlot()
    def _on_run_clicked(self) -> None:
        from pireal.gui.controller import Controller

        Registry.get("controller", Controller).execute_queries()

    @pyqtSlot()
    def _on_symbol_mode_clicked(self) -> None:
        self._symbol_mode_on = not self._symbol_mode_on
        self.show_symbol_mode(self._symbol_mode_on)
        self.symbolModeToggled.emit(self._symbol_mode_on)

    @pyqtSlot()
    def _clear_message(self) -> None:
        self._message_label.clear()
        self._message_label.setToolTip("")

    @pyqtSlot(ColorScheme)
    def _apply_theme(self, scheme: ColorScheme) -> None:
        self._db_label.update()
        self._symbol_mode_label.update()

    def paintEvent(self, a0) -> None:
        super().paintEvent(a0)
        painter = QPainter(self)
        color = self.palette().color(self.palette().ColorRole.Mid)
        color.setAlpha(120)
        painter.setPen(color)
        painter.drawLine(0, 0, self.width(), 0)

    def set_db_modified(self, modified: bool) -> None:
        self._db_label.set_modified(modified)
