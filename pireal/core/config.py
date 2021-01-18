# -*- coding: utf-8 -*-
#
# Copyright 2015 - Gabriel Acosta <acostadariogabriel@gmail.com>
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

from PyQt5.QtCore import QObject
from PyQt5.QtCore import QSettings
from PyQt5.QtCore import pyqtSignal as Signal

from PyQt5.QtGui import QFontDatabase
from PyQt5.QtGui import QFont


# Key Settings
P_DARK_MODE_KEY = 'general/darkMode'
P_LANGUAGE_KEY = 'general/language'
P_FONT_FAMILY_KEY = 'font/family'
P_FONT_SIZE_KEY = 'font/size'
P_EDITOR_HIGHLIGHT_LINE_KEY = 'editor/highlightLine'
P_EDITOR_HIGHLIGHT_BRACES_KEY = 'editor/highlightBraces'


class AppSetting(QObject):
    darkModeChanged = Signal(bool)
    fontFamilyChanged = Signal(str)
    fontSizeChanged = Signal(float)
    highlightLineChanged = Signal(bool)

    def __init__(self, parent=None):
        QObject.__init__(self, parent)
        self._dark_mode = False
        self._font_family = ''
        self._font_size = 0.0
        self._highlight_line = True

    @property
    def dark_mode(self) -> bool:
        return self._dark_mode

    @dark_mode.setter
    def dark_mode(self, value: bool):
        if value != self._dark_mode:
            self._dark_mode = value
            self.darkModeChanged.emit(value)

    @property
    def font_family(self) -> str:
        return self._font_family

    @font_family.setter
    def font_family(self, font: str):
        if font != self._font_family:
            self._font_family = font
            self.fontFamilyChanged.emit(font)

    @property
    def font_size(self) -> float:
        return self._font_size

    @font_size.setter
    def font_size(self, size: float):
        if size != self._font_size:
            self._font_size = size
            self.fontSizeChanged.emit(size)

    @property
    def highlight_line(self) -> bool:
        return self._highlight_line

    @highlight_line.setter
    def highlight_line(self, value: bool):
        if value != self._highlight_line:
            self._highlight_line = value
            self.highlightLineChanged.emit(value)

    def save(self):
        pass

    def load(self):
        qsettings = QSettings()

        if not qsettings.value(P_FONT_FAMILY_KEY):
            # Load font based on OS
            font_db = QFontDatabase()
            families = font_db.families()
            preferred_fonts = []

            if platform.system() == 'Linux':
                preferred_fonts.append('Ubuntu Mono')
                preferred_fonts.append('Liberation Mono')
            elif platform.system() == 'Windows':
                preferred_fonts.append('Courier New')
                preferred_fonts.append('Courier')
            else:
                # TODO: Mac support
                pass

            font = None
            for preferred_font in preferred_fonts:
                if preferred_font in families:
                    font = preferred_font
                    break
            if font is None:
                font = QFont("")
                font.setFixedPitch(True)
                font.setStyleHint(QFont.Monospace)
        else:
            self.font_family = qsettings.value(P_FONT_FAMILY_KEY)

        self.dark_mode = qsettings.value(P_DARK_MODE_KEY, defaultValue=False, type=bool)


AppSettings = AppSetting()