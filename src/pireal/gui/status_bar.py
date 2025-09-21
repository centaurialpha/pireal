
from PyQt6.QtCore import QTimer, Qt, pyqtSignal
from PyQt6.QtWidgets import QFrame, QGridLayout, QHBoxLayout, QLabel, QMainWindow, QToolButton

from pireal.helpers import Font
from pireal.settings import settings
from pireal import __version__


class StatusBar(QFrame):
    """Status bar divide in three areas"""

    playClicked = pyqtSignal()
    gearClicked = pyqtSignal()
    moonClicked = pyqtSignal(bool)
    expandClicked = pyqtSignal(bool)

    def __init__(self, main_window: QMainWindow, parent=None):
        super().__init__(parent)
        self.setFrameStyle(0)
        self._main_window = main_window

        layout = QGridLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        left_widget = QFrame(parent)
        left_widget.setStyleSheet("border: none;")
        mid_widget = QFrame(parent)
        right_widget = QFrame(parent)

        left_layout = QHBoxLayout(left_widget)
        left_widget.setLayout(left_layout)
        left_layout.setContentsMargins(0, 0, 0, 0)
        mid_layout = QHBoxLayout(mid_widget)
        mid_widget.setLayout(mid_layout)
        mid_layout.setContentsMargins(0, 0, 0, 0)
        right_layout = QHBoxLayout(right_widget)
        right_widget.setLayout(right_layout)
        right_layout.setContentsMargins(0, 0, 0, 0)

        fa = Font.instance()
        # Left widgets
        self._messages_label = QLabel()
        self._messages_label.setText(f'Pireal v{__version__}')
        left_layout.addWidget(self._messages_label)
        # Mid widgets
        self._line_col_label = QLabel('Line: 0, Col: 0')
        self._line_col_label.hide()
        mid_layout.addWidget(self._line_col_label)
        # Right widgets
        execute_button = QToolButton()
        execute_button.setAutoRaise(True)
        execute_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        # execute_button.setText('\uf04b')
        execute_button.setIcon(fa.icon("\uf04b", color="red"))
        execute_button.clicked.connect(lambda: self.playClicked.emit())
        right_layout.addWidget(execute_button)
        dark_mode_button = QToolButton()
        dark_mode_button.setAutoRaise(True)
        dark_mode_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        dark_mode_button.setCheckable(True)
        dark_mode_button.setChecked(settings.dark_mode)
        # dark_mode_button.setText('\uf186')
        dark_mode_button.setIcon(fa.icon("\uf186", color="red"))
        dark_mode_button.toggled.connect(lambda v: self.moonClicked.emit(v))
        right_layout.addWidget(dark_mode_button)
        settings_button = QToolButton()
        settings_button.setAutoRaise(True)
        settings_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        settings_button.setText('\uf013')
        settings_button.clicked.connect(lambda: self.gearClicked.emit())
        right_layout.addWidget(settings_button)

        fullscreen_button = QToolButton()
        fullscreen_button.setAutoRaise(True)
        fullscreen_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        fullscreen_button.setText('\uf065')
        fullscreen_button.setCheckable(True)
        fullscreen_button.setChecked(self._main_window.isFullScreen())
        fullscreen_button.toggled.connect(lambda v: self.expandClicked.emit(v))
        right_layout.addWidget(fullscreen_button)

        layout.addWidget(left_widget, 0, 0, 0, 1, Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(mid_widget, 0, 1, 0, 1, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(right_widget, 0, 2, 0, 1, Qt.AlignmentFlag.AlignRight)

        layout.setContentsMargins(2, 0, 2, 0)

    def show_message(self, msg: str, timeout=4000):
        self._messages_label.setText(msg)
        if timeout > 0:
            QTimer.singleShot(timeout, self._messages_label.clear)

    def update_line_and_col(self, line, col):
        if not self._line_col_label.isVisible():
            self._line_col_label.show()
        self._line_col_label.setText('Line: {}, Col: {}'.format(line, col))
