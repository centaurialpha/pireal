from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QActionGroup
from PyQt6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMenu,
    QToolButton,
)

from pireal import __version__
from pireal.gui.theme.manager import get_theme_manager
from pireal.gui.theme.schema import EditorColorRole
from pireal.helpers import Font


class ThemeButton(QToolButton):
    themeRequested = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAutoRaise(True)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setText("\uf186")

    def set_themes(self, themes: list[tuple[str, str]]):
        if len(themes) <= 2:
            self._setup_toggle()
        else:
            self._setup_menu(themes)

    def _setup_toggle(self):
        self.setCheckable(True)
        self.setChecked(get_theme_manager().current_id == "dark")
        self.toggled.connect(self._on_toggled)

    def _setup_menu(self, themes: list[tuple[str, str]]):
        self.setCheckable(False)
        self.setPopupMode(QToolButton.ToolButtonPopupMode.MenuButtonPopup)
        menu = QMenu(self)
        group = QActionGroup(menu)
        group.setExclusive(True)
        current_id = get_theme_manager().current_id
        for theme_id, theme_name in themes:
            if action := menu.addAction(theme_name):
                action.setCheckable(True)
                action.setChecked(theme_id == current_id)
                group.addAction(action)
                action.triggered.connect(
                    lambda _, tid=theme_id: self._on_menu_action(tid)
                )
        self.setMenu(menu)

    def _on_toggled(self, checked: bool):
        theme_id = "dark" if checked else "light"
        self.themeRequested.emit(theme_id)

    def _on_menu_action(self, theme_id: str):
        self.themeRequested.emit(theme_id)


class StatusBar(QFrame):
    """Status bar divide in three areas"""

    playClicked = pyqtSignal()
    gearClicked = pyqtSignal()
    expandClicked = pyqtSignal(bool)

    def __init__(self, main_window: QMainWindow, parent=None):
        super().__init__(parent)
        self.setFrameStyle(0)
        self._main_window = main_window

        layout = QGridLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Left widgets - version
        left_widget = QFrame(parent)
        left_layout = QHBoxLayout(left_widget)
        left_widget.setStyleSheet("border: none;")
        self._version_label = QLabel(f"Pireal v{__version__}")
        left_layout.addWidget(self._version_label)

        # Mid widgets - temporal messages and editor info
        mid_widget = QFrame(parent)
        mid_layout = QHBoxLayout(mid_widget)
        self._message_label = QLabel()
        mid_layout.addWidget(self._message_label)

        right_widget = QFrame(parent)

        left_widget.setLayout(left_layout)
        left_layout.setContentsMargins(0, 0, 0, 0)
        mid_layout = QHBoxLayout(mid_widget)
        mid_widget.setLayout(mid_layout)
        mid_layout.setContentsMargins(0, 0, 0, 0)
        right_layout = QHBoxLayout(right_widget)
        right_widget.setLayout(right_layout)
        right_layout.setContentsMargins(0, 0, 0, 0)

        fa = Font.instance()

        # Right widgets
        execute_button = QToolButton()
        execute_button.setAutoRaise(True)
        execute_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        execute_button.setText("\uf04b")
        fa.apply_to(execute_button)
        execute_button.clicked.connect(lambda: self.playClicked.emit())
        right_layout.addWidget(execute_button)
        self.theme_button = ThemeButton()
        fa.apply_to(self.theme_button)
        right_layout.addWidget(self.theme_button)
        settings_button = QToolButton()
        settings_button.setAutoRaise(True)
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

        layout.setContentsMargins(2, 0, 2, 0)

    def show_message(self, msg: str, timeout=4000, error=False):
        if error:
            scheme = get_theme_manager().current_scheme
            color = scheme.editor.get(EditorColorRole.ERROR).name()
            self._message_label.setText(f'<span style="color:{color}">{msg}</span>')
        else:
            self._message_label.setText(msg)
        if timeout > 0:
            QTimer.singleShot(timeout, self._message_label.clear)
