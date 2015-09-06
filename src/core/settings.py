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

"""
Pireal settings
"""

import sys
import os
from PyQt4.QtGui import QFont
from PyQt4.QtCore import QSettings


# Operating System
LINUX, WINDOWS = False, False
if sys.platform.startswith('linux'):
    LINUX = True
else:
    WINDOWS = True


# Font
if LINUX:
    FONT = QFont('Monospace', 12)
else:
    FONT = QFont('Courier', 10)

# Supported files
RFILES = "Pireal Relation File (*.prf *.csv *.txt)"
DBFILE = "Pireal Data Base File (*.pdb);;Pireal Query File (*.pqf)"

# Create folder (settings and logging)
PATH = os.path.realpath(os.path.dirname(sys.argv[0]))
HOME = os.path.expanduser("~")
PIREAL_DIR = os.path.join(HOME, ".pireal")
LOG_FILE = os.path.join(PIREAL_DIR, "pireal_logging.log")
SETTINGS_PATH = os.path.join(PIREAL_DIR, "pireal_settings.ini")
LANG_PATH = os.path.join(PATH, "src", "lang")


class PSettings:
    SHOW_START_PAGE = True
    CHECK_UPDATES = True
    MAX_RECENT_FILES = 5
    LANGUAGE = ""


def create_dir():
    if not os.path.isdir(PIREAL_DIR):
        os.mkdir(PIREAL_DIR)


def get_setting(key, default):
    psettings = QSettings(SETTINGS_PATH, QSettings.IniFormat)
    return psettings.value(key, default)


def set_setting(key, value):
    psettings = QSettings(SETTINGS_PATH, QSettings.IniFormat)
    psettings.setValue(key, value)


def load_settings():
    """ Load settings from .ini file """

    settings = QSettings(SETTINGS_PATH, QSettings.IniFormat)
    PSettings.SHOW_START_PAGE = settings.value('show-start-page',
                                               True, type=bool)
    PSettings.LANGUAGE = settings.value('language', "", type='QString')
