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
import os
import json

from PyQt5.QtCore import QObject

from PyQt5.QtGui import QFont


# Detecting Operating System
LINUX, WINDOWS, MAC = False, False, False
if sys.platform == 'darwin':
    MAC = True
elif sys.platform == 'linux' or sys.platform == 'linux2':
    LINUX = True
else:
    WINDOWS = True

# Directories used by Pireal
# Project path
if getattr(sys, 'frozen', ''):
    ROOT_DIR = os.path.realpath(os.path.dirname(sys.argv[0]))
else:
    # Not frozen: regular python interpreter
    ROOT_DIR = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), '..', '..')
# Absolute path of the user's home directory
HOME = os.path.expanduser('~')
# Absolute path of the pireal home directory
# this is used to save the settings, log file, etc.
PIREAL_DIR = os.path.join(HOME, '.pireal')
# Here are saved by default the databases
PIREAL_DATABASES = os.path.join(HOME, 'PirealDatabases')
# Settings
SETTINGS_PATH = os.path.join(PIREAL_DIR, 'settings.ini')
# User settings
USER_SETTINGS_PATH = os.path.join(PIREAL_DIR, "config.json")
# Log file
LOG_PATH = os.path.join(PIREAL_DIR, 'pireal_log.log')
# Language files
LANGUAGE_PATH = os.path.join(ROOT_DIR, 'src', 'lang')
# Path for QML files
QML_PATH = os.path.join(ROOT_DIR, 'src', 'gui', 'qml')
# Style sheet
STYLE_SHEET = os.path.join(ROOT_DIR, 'src', 'style.qss')
# Carpeta de ejemplos
EXAMPLES = os.path.join(ROOT_DIR, 'samples')


# Supported files
SUPPORTED_FILES = ("Pireal Database File (*.pdb);;"
                   "Pireal Query File (*.pqf);;"
                   "Pireal Relation File (*.prf)")


DEFAULT_SETTINGS = {
    "language": "English",
    "highlightCurrentLine": True,
    "matchParenthesis": True,
    "recentFiles": [],
    "lastOpenFolder": None,
    "fontFamily": None,
    "fontSize": 12
}


class Config(QObject):

    def __init__(self, path=USER_SETTINGS_PATH):
        QObject.__init__(self)
        self._path = path
        self._settings = {}

    def load_settings(self):
        if not os.path.exists(self._path):
            self._settings = DEFAULT_SETTINGS
            with open(self._path, mode="w") as fp:
                json.dump(DEFAULT_SETTINGS, fp)
        else:
            with open(self._path) as fp:
                self._settings = json.load(fp)

    def save_settings(self):
        with open(self._path, mode="w") as fp:
            json.dump(self._settings, fp)

    def get(self, option, default=None):
        if option not in self._settings:
            raise Exception("%s no es una opción de configuración" % option)
        value = self._settings.get(option, default)
        return value

    def set_value(self, option, value):
        self._settings[option] = value

    def _get_font(self):
        font = QFont("consolas", 11)
        if LINUX:
            font = QFont("monospace", 12)
        return font.family(), font.pointSize()


CONFIG = Config()
