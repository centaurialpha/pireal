from typing import Dict

from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtWidgets import QApplication

from pireal.settings import settings

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

UI_LIGHT = {
    "Window": "#f8f9fa",
    "WindowText": "#2c2c2c",
    "Base": "#ffffff",
    "AlternateBase": "#f1f3f4",
    "Text": "#2c2c2c",
    "Button": "#f1f3f4",
    "ButtonText": "#2c2c2c",
    "Highlight": "#e8f0fe",
    "HighlightedText": "#1565c0",
    "Link": "#1a73e8",
    "BrightText": "#d93025",
    "Dark": "#e8eaed",
    "Mid": "#bdc1c6",
    "Shadow": "#1a73e8",
    "Light": "#5f6368",
}

UI_DARK = {
    "Window": "#202124",
    "WindowText": "#e8eaed",
    "Base": "#2d2e30",
    "AlternateBase": "#35363a",
    "Text": "#e8eaed",
    "Button": "#3c4043",
    "ButtonText": "#e8eaed",
    "Highlight": "#3d2e30",
    "HighlightedText": "#ffffff",
    "Link": "#8ab4f8",
    "BrightText": "#f28b82",
    "Dark": "#3c4043",
    "Mid": "#5f6368",
    "Shadow": "#8ab4f8",
    "Light": "#9aa0a6",
}

EDITOR_LIGHT = {
    "background": "#ffffff",
    "foreground": "#2c2c2c",
    "current_line": "#f8f9fa",
    "selection": "#cce7ff",
    "sidebar_background": "#f5f7fa",
    "sidebar_foreground": "#5f6368",
    "keyword": "#1a73e8",
    "string": "#137333",
    "comment": "#5f6368",
    "number": "#8e24aa",
    "operator": "#ea4335",
    "variable": "#1976d2",
}

EDITOR_DARK = {
    "background": "#1f1f1f",
    "foreground": "#e8eaed",
    "current_line": "#2d2e30",
    "selection": "#264f78",
    "sidebar_background": "#202124",
    "sidebar_foreground": "#9aa0a6",
    "keyword": "#8ab4f8",
    "string": "#81c995",
    "comment": "#9aa0a6",
    "number": "#c58af9",
    "operator": "#f28b82",
    "variable": "#78d9ec",
}


class EditorColors:
    def __init__(self, colors: Dict[str, str]):
        self.background = colors["background"]
        self.foreground = colors["foreground"]
        self.current_line = colors["current_line"]
        self.selection = colors["selection"]
        self.sidebar_background = colors["sidebar_background"]
        self.sidebar_foreground = colors["sidebar_foreground"]
        self.keyword = colors["keyword"]
        self.string = colors["string"]
        self.comment = colors["comment"]
        self.number = colors["number"]
        self.operator = colors["operator"]
        self.variable = colors["variable"]


class ThemeManager(QObject):
    theme_changed = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self._initialized = False

    def initialize(self):
        if not self._initialized:
            self._update_colors()
            self._initialized = True

    def _update_colors(self):
        if settings.dark_mode:
            self._ui_colors = UI_DARK
            self.editor = EditorColors(EDITOR_DARK)
        else:
            self._ui_colors = UI_LIGHT
            self.editor = EditorColors(EDITOR_LIGHT)

    @property
    def is_dark(self) -> bool:
        return settings.dark_mode

    def set_dark_mode(self, enabled: bool):
        if settings.dark_mode != enabled:
            settings.dark_mode = enabled
            if self._initialized:
                self._update_colors()
                self.theme_changed.emit(enabled)

    def toggle_dark_mode(self):
        self.set_dark_mode(not self.is_dark)

    def apply_theme(self, app: QApplication):
        if not self._initialized:
            return

        if settings.dark_mode:
            self._apply_dark_theme(app)
        else:
            self._apply_light_theme(app)

    def _apply_light_theme(self, app: QApplication):
        style = app.style()
        if style is None:
            return
        app.setPalette(style.standardPalette())

    def _apply_dark_theme(self, app: QApplication):
        palette = QPalette()

        for role_name, color_hex in self._ui_colors.items():
            color = QColor(color_hex)

            if hasattr(QPalette.ColorRole, role_name):
                role = getattr(QPalette.ColorRole, role_name)
                palette.setColor(QPalette.ColorGroup.All, role, color)

        app.setPalette(palette)

    def get_color(self, name: str) -> str:
        return self._ui_colors.get(name, "#000000")

    def get_editor_color(self, name: str) -> str:
        return getattr(self.editor, name, "#000000")


theme_manager = ThemeManager()
