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

import platform

from PyQt6.QtCore import QObject, QSettings, pyqtSignal
from PyQt6.QtGui import QFontDatabase

from pireal.dirs import CONFIG_FILE

# Supported files.
# DON'T change the order!
SUPPORTED_FILES = (
    "Pireal Database File (*.pdb)",
    "Pireal Query File (*.pqf)",
    "Pireal Relation File (*.prf)",
)


MAX_RECENT_DATABASES = 10


def get_extension_filter(extension):
    for sf in SUPPORTED_FILES:
        if extension in sf:
            return sf


def _get_default_font() -> str:
    """Devuelve la fuente por defecto según el OS"""
    families = QFontDatabase.families()

    fonts = {
        "Linux": ["Ubuntu Mono", "Liberation Mono", "Source Code Pro"],
        "Windows": ["Consolas", "Courier New"],
        "Darwin": ["SF Mono", "Monaco", "Menlo"],
    }

    preferred_fonts = fonts.get(platform.system(), ["Courier"])

    for font in preferred_fonts:
        if font in families:
            return font

    return "Courier"


class Settings(QObject):
    settingsChanged = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._qs = QSettings(str(CONFIG_FILE), QSettings.Format.IniFormat)
        self._loaded = False

    def load(self) -> None:
        if self._loaded:
            return

        self.language: str = self._qs.value("language", "es")

        self.font_family: str = self._qs.value("font_family", _get_default_font())
        self.font_size: int = self._qs.value("font_size", 12, type=int)
        self.highlight_current_line: bool = self._qs.value("highlight_current_line", True, type=bool)
        self.match_parenthesis: bool = self._qs.value("match_parenthesis", True, type=bool)
        self.dark_mode: bool = self._qs.value("dark_mode", True, type=bool)
        self.symbol_mode: bool = self._qs.value("symbol_mode", False, type=bool)

        default_theme = "light" if not self._qs.contains("theme") else self._qs.value("theme")
        self.theme: str = default_theme

        self._loaded = True

    def save(self) -> None:
        if not self._loaded:
            return

        self._qs.setValue("language", self.language)
        self._qs.setValue("font_family", self.font_family)
        self._qs.setValue("font_size", self.font_size)
        self._qs.setValue("highlight_current_line", self.highlight_current_line)
        self._qs.setValue("match_parenthesis", self.match_parenthesis)
        self._qs.setValue("dark_mode", self.dark_mode)
        self._qs.setValue("theme", self.theme)
        self._qs.setValue("symbol_mode", self.symbol_mode)

        self._qs.sync()

    def __setattr__(self, name: str, value) -> None:
        super().__setattr__(name, value)

        if getattr(self, "_loaded", False) and not name.startswith("_"):
            save_value = list(value) if isinstance(value, tuple) else value
            self._qs.setValue(name, save_value)
            self._qs.sync()
            self.settingsChanged.emit(name)


settings = Settings()
