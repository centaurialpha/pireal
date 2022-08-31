# -*- coding: utf-8 -*-
#
# Copyright 2015-2022 Gabriel Acosta <acostadariogabriel@gmail.com>
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

"""Run Pireal user interface"""

import logging
import os
import platform
import sys
from pathlib import Path

from PyQt6.QtCore import (QT_VERSION_STR, QDir, QLibraryInfo, QLocale,
                          QTranslator)
from PyQt6.QtGui import QFont, QFontDatabase, QIcon
from PyQt6.QtWidgets import QApplication

from pireal import __version__
from pireal.core import cliparser
from pireal.core import logger as _logger
from pireal.dirs import create_app_dirs
from pireal.gui.main_window import Pireal
from pireal.gui.theme import apply_theme
from pireal.settings import SETTINGS

logger = logging.getLogger("main")

ROOT_DIR = Path(__file__).parent
RESOURCES_DIR = ROOT_DIR / "resources"
IMAGES_DIR = RESOURCES_DIR / "images"
LANGUAGES_DIR = RESOURCES_DIR / "lang"


if ROOT_DIR not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


def run():
    QDir.addSearchPath("icons", str(IMAGES_DIR))
    QDir.addSearchPath("languages", str(LANGUAGES_DIR))

    # Parse CLI
    args = cliparser.get_cli().parse_args()
    if args.version:
        print(__version__)
        sys.exit(0)

    # Creo los dirs antes de leer logs. see #84
    create_app_dirs()

    # Set up logger
    _logger.set_up(verbose=args.verbose)

    start_pireal(args)


def start_pireal(args):
    # OS
    if platform.system() == "Linux":
        system, os_name = platform.uname()[:2]
    else:
        system = platform.uname()[0]
        os_name = platform.uname()[2]

    # Python version
    python_version = platform.python_version()

    logger.info("Running pireal %s...", __version__)
    logger.info(
        "Python %s on %s-%s, Qt %s", python_version, system, os_name, QT_VERSION_STR
    )

    app = QApplication(sys.argv)
    app.setApplicationName("Pireal")
    app.setApplicationDisplayName("Pireal")
    app.setWindowIcon(QIcon("icons:pireal_icon.png"))

    SETTINGS.load()

    app.setStyle("fusion")
    apply_theme(app)

    # Add Font Awesome
    family = QFontDatabase.applicationFontFamilies(
        QFontDatabase.addApplicationFont(str(IMAGES_DIR / "font-awesome.ttf"))
    )[0]
    font = QFont(family)
    font.setStyleName("Solid")
    app.setFont(font)
    # Install translators
    # Qt translations
    system_locale_name = QLocale.system().name()
    qt_languages_path = QLibraryInfo.path(QLibraryInfo.LibraryPath.TranslationsPath)
    qt_translator = QTranslator()
    translator_loaded = qt_translator.load(
        os.path.join(qt_languages_path, f"qt_{SETTINGS.language}.qm")
    )
    if not translator_loaded:
        qt_translator.load(
            os.path.join(
                qt_languages_path, "qt_{}.qml".format(system_locale_name.split("_")[0])
            )
        )
    app.installTranslator(qt_translator)
    # App translator
    translator = QTranslator()
    if translator.load(f"languages:{SETTINGS.language}"):
        app.installTranslator(translator)

    check_updates = not args.no_check_updates
    pireal_gui = Pireal(check_updates)
    pireal_gui.show()

    sys.exit(app.exec())
