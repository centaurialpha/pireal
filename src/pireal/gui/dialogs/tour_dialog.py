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

from PyQt6.QtCore import QSettings, Qt
from PyQt6.QtWidgets import QDialog, QHBoxLayout, QLabel, QPlainTextEdit, QPushButton, QVBoxLayout, QWidget

from pireal import translations as tr
from pireal.dirs import DATA_SETTINGS
from pireal.gui.db_highlighter import DBHighlighter
from pireal.gui.highlighter import Highlighter
from pireal.gui.theme.manager import get_theme_manager
from pireal.settings import settings

SLIDES = [
    {
        "icon": "",
        "title": tr.TR_TOUR_SLIDE1_TITLE,
        "body": tr.TR_TOUR_SLIDE1_BODY,
        "code": "",
        "highlighter_type": "",
    },
    {
        "icon": "",
        "title": tr.TR_TOUR_SLIDE2_TITLE,
        "body": tr.TR_TOUR_SLIDE2_BODY,
        "code": "@students:id,name,age\n1,Gabriel,25\n2,Marisel,22",
        "highlighter_type": DBHighlighter,
    },
    {
        "icon": "",
        "title": tr.TR_TOUR_SLIDE3_TITLE,
        "body": tr.TR_TOUR_SLIDE3_BODY,
        "code": "adults := select age >= 18 (students);\nnames := project name (adults);",
        "highlighter_type": Highlighter,
    },
    {
        "icon": "",
        "title": tr.TR_TOUR_SLIDE4_TITLE,
        "body": tr.TR_TOUR_SLIDE4_BODY,
        "code": "",
    },
    {
        "icon": "",
        "title": "Choose your theme",
        "body": "You can always change this later in Settings.",
        "code": None,
        "highlighter_type": None,
        "theme_selector": True,  # flag para renderizar los botones
    },
]


class CodeSnippet(QPlainTextEdit):
    def __init__(self, code: str, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self.setPlainText(code)
        self.setMaximumHeight(80)
        self.setFrameShape(QPlainTextEdit.Shape.NoFrame)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        font = self.font()
        font.setFamily("Monospace")
        font.setPointSize(10)
        self.setFont(font)
        self._highlighter = None

    def set_highlighter(self, highlighter_class):
        if self._highlighter is not None:
            self._highlighter.setDocument(None)
        if highlighter_class is not None:
            self._highlighter = highlighter_class(self.document())
        else:
            self._highlighter = None


class WelcomeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Welcome to Pireal")
        self.setMinimumSize(520, 340)
        self.resize(540, 360)
        if parent is not None:
            parent_geometry = parent.geometry()
            x = parent_geometry.x() + (parent_geometry.width() - self.width()) // 2
            y = parent_geometry.y() + (parent_geometry.height() - self.height()) // 2
            self.move(x, y)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)

        self._current = 0
        self._build_ui()
        self._update_slide()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(32, 28, 32, 20)

        # Indicadores de progreso
        self._indicators_layout = QHBoxLayout()
        self._indicators_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self._indicators = []
        for _ in SLIDES:
            dot = QLabel("●")
            dot.setStyleSheet("color: #ccc; font-size: 10px;")
            self._indicators.append(dot)
            self._indicators_layout.addWidget(dot)
        layout.addLayout(self._indicators_layout)

        # Ícono
        self._icon_lbl = QLabel()
        self._icon_lbl.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        font = self._icon_lbl.font()
        font.setPointSize(36)
        self._icon_lbl.setFont(font)
        layout.addWidget(self._icon_lbl)

        # Título
        self._title_lbl = QLabel()
        self._title_lbl.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        font = self._title_lbl.font()
        font.setPointSize(16)
        font.setBold(True)
        self._title_lbl.setFont(font)
        layout.addWidget(self._title_lbl)

        # Cuerpo
        self._body_lbl = QLabel()
        self._body_lbl.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self._body_lbl.setWordWrap(True)
        self._body_lbl.setTextFormat(Qt.TextFormat.RichText)
        layout.addWidget(self._body_lbl, stretch=1)

        self._code_widget = CodeSnippet("")
        self._code_widget.hide()
        layout.addWidget(self._code_widget)
        # Botones
        btn_layout = QHBoxLayout()
        self._skip_btn = QPushButton("Skip tour")
        self._skip_btn.setFlat(True)
        self._skip_btn.clicked.connect(self._on_skip)

        self._next_btn = QPushButton("Next")
        self._next_btn.setMinimumWidth(100)
        self._next_btn.clicked.connect(self._on_next)

        btn_layout.addWidget(self._skip_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(self._next_btn)
        layout.addLayout(btn_layout)

        self._theme_widget = QWidget()
        theme_layout = QHBoxLayout(self._theme_widget)
        self._btn_light = QPushButton("Light")
        self._btn_dark = QPushButton("Dark")
        for btn in (self._btn_light, self._btn_dark):
            btn.setCheckable(True)
            btn.setMinimumHeight(48)
        theme_layout.addWidget(self._btn_light)
        theme_layout.addWidget(self._btn_dark)
        self._btn_light.setChecked(True)  # default
        self._btn_light.clicked.connect(lambda: self._select_theme("light"))
        self._btn_dark.clicked.connect(lambda: self._select_theme("dark"))
        self._theme_widget.hide()
        layout.addWidget(self._theme_widget)

        self._selected_theme = "light"

    def _select_theme(self, theme_id: str) -> None:
        self._selected_theme = theme_id
        self._btn_light.setChecked(theme_id == "light")
        self._btn_dark.setChecked(theme_id == "dark")
        get_theme_manager().apply(theme_id)  # preview en tiempo real

    def _update_slide(self) -> None:
        slide = SLIDES[self._current]
        self._icon_lbl.setText(str(slide["icon"]))
        self._title_lbl.setText(str(slide["title"]))
        self._body_lbl.setText(str(slide["body"]))

        has_code = bool(slide.get("code"))
        has_theme = bool(slide.get("theme_selector"))

        if has_code:
            self._code_widget.set_highlighter(slide["highlighter_type"])
            self._code_widget.setPlainText(str(slide["code"]))
        self._code_widget.setVisible(has_code)
        self._theme_widget.setVisible(has_theme)

        is_last = self._current == len(SLIDES) - 1
        self._next_btn.setText(tr.TR_TOUR_GET_STARTED if is_last else tr.TR_TOUR_NEXT)

        for i, dot in enumerate(self._indicators):
            dot.setStyleSheet(
                "color: #1565c0; font-size: 10px;" if i == self._current else "color: #ccc; font-size: 10px;"
            )

    def _on_next(self):
        if self._current < len(SLIDES) - 1:
            self._current += 1
            self._update_slide()
        else:
            self._mark_seen()
            self.accept()

    def _on_skip(self):
        self._mark_seen()
        self.reject()

    def _mark_seen(self):
        qs = QSettings(str(DATA_SETTINGS), QSettings.Format.IniFormat)
        qs.setValue("tour_seen", True)
        settings.theme = self._selected_theme

    @staticmethod
    def should_show() -> bool:
        qs = QSettings(str(DATA_SETTINGS), QSettings.Format.IniFormat)
        return not qs.value("tour_seen", False, type=bool)
