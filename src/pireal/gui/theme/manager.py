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

from pathlib import Path

from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QApplication, QStyleFactory

from pireal.gui.theme.base import Theme
from pireal.gui.theme.builtin import DarkTheme, LightTheme
from pireal.gui.theme.custom import discover_themes
from pireal.gui.theme.schema import ColorScheme


class ThemeManager(QObject):
    themeChanged = pyqtSignal(ColorScheme)

    def __init__(self, custom_themes_dir: Path | None = None):
        super().__init__()
        self._themes: dict[str, Theme] = {}
        self._current_id: str = "dark"
        self._load_builtin_themes()

        if custom_themes_dir:
            self._load_custom_themes(custom_themes_dir)

    @property
    def current(self) -> Theme:
        return self._themes[self._current_id]

    @property
    def current_id(self) -> str:
        return self._current_id

    @property
    def current_scheme(self) -> ColorScheme:
        return self.current.color_scheme()

    def _load_builtin_themes(self):
        builtin = [
            DarkTheme(),
            LightTheme(),
        ]

        for theme in builtin:
            self.register(theme)

    def _load_custom_themes(self, themes_dir: Path):
        custom_themes = discover_themes(themes_dir)
        for theme in custom_themes:
            self.register(theme)

    def register(self, theme: Theme):
        if theme.identifier in self._themes:
            print("WARNINGGGGG")

        self._themes[theme.identifier] = theme

    def get(self, theme_id: str) -> Theme | None:
        return self._themes.get(theme_id)

    def apply(self, theme_id: str):
        theme = self.get(theme_id)
        if theme is None:
            available = list(self._themes.keys())
            raise ValueError(f"Theme {theme_id} not found. Available: {available}")

        app_instance = QApplication.instance()
        if not isinstance(app_instance, QApplication):
            raise RuntimeError("No QApplication instance found")

        app_instance.setStyleSheet("")

        style = QStyleFactory.create(theme.qt_style())
        if style:
            QApplication.setStyle(style)
        else:
            print("WARNINGNGNGNGNGN")

        color_scheme = theme.color_scheme()
        QApplication.setPalette(color_scheme.to_palette())

        stylesheet = theme.stylesheet()
        if stylesheet:
            app_instance.setStyleSheet(stylesheet)

        self._current_id = theme_id

        self.themeChanged.emit(color_scheme)

    def themes(self) -> list[tuple[str, str]]:
        return [(theme_id, theme.name) for theme_id, theme in self._themes.items()]


_instance: ThemeManager | None = None


def get_theme_manager(custom_themes_dir: Path | None = None) -> ThemeManager:
    global _instance
    if _instance is None:
        _instance = ThemeManager(custom_themes_dir=custom_themes_dir)
    return _instance
