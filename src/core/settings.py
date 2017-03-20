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
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QSettings


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
SETTINGS_PATH = os.path.join(PIREAL_DIR, 'pireal_settings.ini')
# Log file
LOG_PATH = os.path.join(PIREAL_DIR, 'pireal_log.log')
# Language files
LANGUAGE_PATH = os.path.join(ROOT_DIR, 'src', 'lang')
# Path for QML files
QML_PATH = os.path.join(ROOT_DIR, 'src', 'gui', 'qml')
# Style sheet
STYLE_SHEET = os.path.join(ROOT_DIR, 'src', 'style.qss')

# Supported files
SUPPORTED_FILES = ("Pireal Database File (*.pdb);;"
                   "Pireal Query File (*.pqf);;"
                   "Pireal Relation File (*.prf)")


class PSetting(object):
    LANGUAGE = ""
    HIGHLIGHT_CURRENT_LINE = False
    MATCHING_PARENTHESIS = True
    RECENT_DBS = []
    LAST_OPEN_FOLDER = None
    # FIXME: for Mac Os
    if LINUX:
        FONT = QFont("Monospace", 12)
    else:
        FONT = QFont("Courier", 10)


def load_settings():
    """ Load settings from INI file """

    qs = QSettings(SETTINGS_PATH, QSettings.IniFormat)
    PSetting.LANGUAGE = qs.value('language', "", type='QString')
    PSetting.RECENT_DBS = qs.value('recent_databases', [], type='QStringList')
    PSetting.LAST_OPEN_FOLDER = qs.value('last_open_folder',
                                         None, type='QString')
    PSetting.HIGHLIGHT_CURRENT_LINE = qs.value('highlight_current_line',
                                               False, type=bool)
    PSetting.MATCHING_PARENTHESIS = qs.value('matching_parenthesis',
                                             True, type=bool)
    font = qs.value('font', None)
    if font is not None:
        PSetting.FONT = font
