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

"""
Pireal Settings
"""

import sys

from PyQt5.QtCore import QSettings
from PyQt5.QtCore import QVariant

from pireal.dirs import CONFIG_FILE

# Detecting Operating System
IS_LINUX, IS_WINDOWS, MAC = False, False, False
if sys.platform == 'darwin':
    MAC = True
elif sys.platform == 'linux' or sys.platform == 'linux2':
    IS_LINUX = True
else:
    IS_WINDOWS = True


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


class _QSettings(QSettings):

    def __init__(self, path=CONFIG_FILE.stem, prefix=''):
        super().__init__(path, QSettings.IniFormat)
        self._prefix = prefix

    def setValue(self, key, value):
        key = f'{self._prefix}/{key}'
        super().setValue(key, value)

    def value(self, key, default=QVariant(), type=None):
        key = f'{self._prefix}/{key}'
        if type is not None:
            value = super().value(key, defaultValue=default, type=type)
        else:
            value = super().value(key, defaultValue=default)
        return value


class Settings:

    def __init__(self):
        self._qsettings = _QSettings(prefix='us')

        self.language: str = 'english'
        self.font_family: str = self._get_font()
        self.font_size: int = 14
        self.highlight_current_line: bool = False
        self.match_parenthesis: bool = True
        self.alternate_row_colors: bool = True
        self.dark_mode: bool = False
        self.cursor_width: int = 3

    def _get_font(self):
        if IS_LINUX:
            return 'monospace'
        elif IS_WINDOWS:
            return 'courier'
        return 'monaco'

    def save(self):
        for key, value in self.__dict__.items():
            if not key.startswith('_'):
                self._qsettings.setValue(key, value)

    def load(self):
        settings_map = {}
        keys = self._qsettings.allKeys()
        for key in keys:
            if not key.startswith('us/'):
                continue
            type_ = type(getattr(self, key.split('/')[-1]))
            key = key.split('/')[-1]
            settings_map[key] = self._qsettings.value(key, type=type_)

        self.language = settings_map.get('language', self.language)
        self.font_family = settings_map.get('font_family', self.font_family)
        self.font_size = settings_map.get('font_size', self.font_size)
        self.highlight_current_line = settings_map.get(
            'highlight_current_line', self.highlight_current_line)
        self.match_parenthesis = settings_map.get('match_parenthesis', self.match_parenthesis)
        self.alternate_row_colors = settings_map.get(
            'alternate_row_colors', self.alternate_row_colors)
        self.dark_mode = settings_map.get('dark_mode', self.dark_mode)
        self.cursor_width = settings_map.get('cursor_width', self.cursor_width)


USER_SETTINGS = Settings()
DATA_SETTINGS = _QSettings(prefix='ds')
