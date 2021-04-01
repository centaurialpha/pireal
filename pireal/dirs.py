# -*- coding: utf-8 -*-
#
# Copyright 2015-2020 - Gabriel Acosta <acostadariogabriel@gmail.com>
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
This module contains variables and functions related to directories used by Pireal
"""

import platform
from pathlib import Path

from PyQt5.QtCore import QStandardPaths


_ROOT_DIR = Path(__file__).resolve().parent.parent

_HOME_DIR = Path.home()

EXAMPLES_DIR = _ROOT_DIR / 'pireal' / 'resources' / 'samples'


def _data_dir() -> Path:
    """Return the app data dir for Pireal"""

    pireal_dir_name = '.pireal'

    if platform.system() == 'Linux':
        # Store data files in $HOME
        pireal_data_dir = _HOME_DIR / pireal_dir_name
    else:
        # In windows and mac, use standard paths provided by Qt
        pireal_data_dir = Path(QStandardPaths.writableLocation(
            QStandardPaths.GenericDataLocation)) / pireal_dir_name

    return pireal_data_dir


def _get_databases_location() -> Path:
    """Return the path used for store the user databases"""

    db_dir = Path(QStandardPaths.writableLocation(
        QStandardPaths.HomeLocation)) / 'PirealDBs'

    return db_dir


LOGS_DIR = _data_dir() / 'logs'
CONFIG_FILE = _data_dir() / 'config.ini'
DATA_SETTINGS = _data_dir() / 'data_settings.ini'
LANGUAGES_DIR = _ROOT_DIR / 'pireal' / 'resources' / 'lang'
DATABASES_DIR = _get_databases_location()


def create_app_dirs():
    """Create all dirs needed by Pireal"""
    for d in (_data_dir(), LOGS_DIR, DATABASES_DIR):
        d.mkdir(exist_ok=True)
