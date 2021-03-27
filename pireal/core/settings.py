# -*- coding: utf-8 -*-
#
# Copyright 2015-2016 - Gabriel Acosta <acostadariogabriel@gmail.com>
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

from PyQt5.QtCore import QSettings

from pireal.dirs import CONFIG_FILE

# Supported files.
# DON'T change the order!
SUPPORTED_FILES = (
    "Pireal Database File (*.pdb)",
    "Pireal Query File (*.pqf)",
    "Pireal Relation File (*.prf)",
)


def get_extension_filter(extension):
    for sf in SUPPORTED_FILES:
        if extension in sf:
            return sf


class SettingManager:
    """Wrapper around QSettings to manage user settings"""

    def __init__(self):
        self._qs = QSettings(str(CONFIG_FILE), QSettings.IniFormat)

    def load(self):
        self._language: str = self._qs.value(
            'language', defaultValue='english')
        self._highlight_current_line: bool = self._qs.value(
            'highlight_current_line', defaultValue=False, type=bool)
        self._match_parenthesis: bool = self._qs.value(
            'match_parenthesis', defaultValue=True, type=bool)
        self._font_family: str = self._qs.value('font_family')
        self._font_size: float = self._qs.value('font_size', defaultValue=12, type=bool)

    @property
    def language(self) -> str:
        return self._language

    @language.setter
    def language(self, lang):
        if lang != self._language:
            self._language = lang
            self._qs.setValue('language', lang)

    @property
    def highlight_current_line(self) -> bool:
        return self._highlight_current_line

    @highlight_current_line.setter
    def highlight_current_line(self, value):
        if value != self._highlight_current_line:
            self._highlight_current_line = value
            self._qs.setValue('highlight_current_line', value)

    @property
    def match_parenthesis(self) -> bool:
        return self._match_parenthesis

    @match_parenthesis.setter
    def match_parenthesis(self, value):
        if value != self._match_parenthesis:
            self._match_parenthesis = value
            self._qs.setValue('match_parenthesis', value)

    @property
    def font_family(self) -> str:
        ff = self._font_family
        if ff is None:
            ff = 'Hermit'
        return ff

    @font_family.setter
    def font_family(self, font):
        if font != self._font_family:
            self._font = font
            self._qs.setValue('font_family', font)

    @property
    def font_size(self) -> float:
        return self._font_size

    @font_size.setter
    def font_size(self, size):
        if size != self._font_size:
            self._font_size = size
            self._qs.setValue('font_size', size)


SETTINGS = SettingManager()
