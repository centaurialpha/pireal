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
from PyQt6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QToolButton,
)

from pireal import __version__
from pireal import translations as tr
from pireal.gui.theme.manager import get_theme_manager
from pireal.gui.theme.schema import ColorScheme, EditorColorRole
from pireal.helpers import Font


class ThemeButton(QToolButton):
    themeRequested = pyqtSignal(str)

    _ICONS = {
        "light": "\uf185",  # solcito
        "dark": "\uf186",  # lunita
    }
    _DEFAULT_ICON = "\uf042"

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAutoRaise(True)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setCheckable(False)
        self._themes: list[str] = []
        self._current_index: int = 0
        self.clicked.connect(self._on_clicked)

    def set_themes(self, themes: list[tuple[str, str]]):
        self._themes = [theme_id for theme_id, _ in themes]
        current_id = get_theme_manager().current_id
        if current_id in self._themes:
            self._current_index = self._themes.index(current_id)
        self._update_icon()

    def _on_clicked(self):
        self._current_index = (self._current_index + 1) % len(self._themes)
        theme_id = self._themes[self._current_index]
        self._update_icon()
        self.themeRequested.emit(theme_id)

    def _update_icon(self):
        if not self._themes:
            return
        # Mostrar el ícono del próximo tema
        next_index = (self._current_index + 1) % len(self._themes)
        next_theme_id = self._themes[next_index]
        self.setText(self._ICONS.get(next_theme_id, self._DEFAULT_ICON))


class StatusBar(QFrame):
    """Status bar divide in three areas"""

    playClicked = pyqtSignal()
    gearClicked = pyqtSignal()
    expandClicked = pyqtSignal(bool)
    feedbackClicked = pyqtSignal()

    def __init__(self, main_window: QMainWindow, parent=None):
        super().__init__(parent)
        self.setFrameStyle(0)
        self._main_window = main_window

        layout = QGridLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Left widgets - version
        left_widget = QFrame(parent)
        left_layout = QHBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_widget.setStyleSheet("border: none;")
        self._version_label = QLabel(f"Pireal v{__version__}")
        left_layout.addWidget(self._version_label)

        # Mid widgets - temporal messages and editor info
        mid_widget = QFrame(parent)
        mid_layout = QHBoxLayout(mid_widget)
        mid_layout.setContentsMargins(0, 0, 0, 0)
        self._message_label = QLabel()
        mid_layout.addWidget(self._message_label)

        # Right widgets
        right_widget = QFrame(parent)
        right_layout = QHBoxLayout(right_widget)
        right_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        right_layout.setContentsMargins(0, 0, 0, 0)

        fa = Font.instance()

        theme_manager = get_theme_manager()
        # Right widgets
        self._execute_button = QToolButton()
        self._execute_button.setAutoRaise(True)
        self._execute_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self._execute_button.setText("\uf04b")
        self._update_execute_color(theme_manager.current_scheme)
        fa.apply_to(self._execute_button)
        self._execute_button.clicked.connect(lambda: self.playClicked.emit())
        theme_manager.themeChanged.connect(self._update_execute_color)
        right_layout.addWidget(self._execute_button)

        self._execute_button.setStyleSheet(
            f"color: {theme_manager.current_scheme.editor.get(EditorColorRole.SUCCESS).name()};"
        )
        right_layout.addWidget(self._execute_button)

        self.theme_button = ThemeButton()
        fa.apply_to(self.theme_button)
        right_layout.addWidget(self.theme_button)

        if True:
            feedback_button = QToolButton()
            feedback_button.setAutoRaise(True)
            feedback_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            feedback_button.setText("\uf086")
            feedback_button.setToolTip(tr.TR_MENU_HELP_FEEDBACK)
            fa.apply_to(feedback_button)
            feedback_button.setFixedSize(26, 26)
            feedback_button.clicked.connect(lambda: self.feedbackClicked.emit())
            right_layout.addWidget(feedback_button)

        settings_button = QToolButton()
        settings_button.setAutoRaise(True)
        settings_button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextOnly)
        settings_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        settings_button.setText("\uf013")
        fa.apply_to(settings_button)
        settings_button.clicked.connect(lambda: self.gearClicked.emit())
        right_layout.addWidget(settings_button)

        fullscreen_button = QToolButton()
        fullscreen_button.setAutoRaise(True)
        fullscreen_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        fullscreen_button.setText("\uf065")
        fa.apply_to(fullscreen_button)
        fullscreen_button.setCheckable(True)
        fullscreen_button.setChecked(self._main_window.isFullScreen())
        fullscreen_button.toggled.connect(lambda v: self.expandClicked.emit(v))
        right_layout.addWidget(fullscreen_button)

        layout.addWidget(left_widget, 0, 0, 0, 1, Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(mid_widget, 0, 1, 0, 1, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(right_widget, 0, 2, 0, 1, Qt.AlignmentFlag.AlignRight)

        for btn in (
            self._execute_button,
            self.theme_button,
            settings_button,
            fullscreen_button,
        ):
            btn.setFixedSize(26, 26)

        layout.setContentsMargins(2, 2, 2, 0)

    @pyqtSlot(ColorScheme)
    def _update_execute_color(self, scheme):
        color = scheme.editor.get(EditorColorRole.SUCCESS).name()
        self._execute_button.setStyleSheet(f"color: {color};")

    def show_message(self, msg: str, timeout=4000, error=False):
        if error:
            scheme = get_theme_manager().current_scheme
            color = scheme.editor.get(EditorColorRole.ERROR).name()
            self._message_label.setText(f'<span style="color:{color}">{msg}</span>')
        else:
            self._message_label.setText(msg)
        if timeout > 0:
            QTimer.singleShot(timeout, self._message_label.clear)

    def paintEvent(self, a0):
        super().paintEvent(a0)
        from PyQt6.QtGui import QPainter

        painter = QPainter(self)
        color = self.palette().color(self.palette().ColorRole.Mid)
        color.setAlpha(120)
        painter.setPen(color)
        painter.drawLine(0, 0, self.width(), 0)
