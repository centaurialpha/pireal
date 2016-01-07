#!/usr/bin/env python
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

import sys
import os

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import (
    QLocale,
    QTranslator,
    QLibraryInfo,
    QT_VERSION_STR
)

from src.core import settings
from src.core.logger import PirealLogger


def __get_versions():
    """ Version information for components used by Pireal """

    import platform

    # OS
    if sys.platform.startswith('linux'):
        system, name = platform.uname()[:2]
    else:
        system = platform.uname()[0]
        name = platform.uname()[2]
    # Python version
    python_version = platform.python_version()

    return {
        'python': python_version,
        'os': system,
        'name': name,
        'qt': QT_VERSION_STR  # Qt version
    }


def detect_language(system_lang):
    languages = {'es': 'Spanish'}
    return languages.get(system_lang, None)


if __name__ == "__main__":

    # Create dir
    settings.create_dir()

    # Logger
    logger = PirealLogger(__name__)
    INFO = logger.info

    info = __get_versions()
    INFO("Executing Pireal from source")
    INFO("Python {0} - Qt {1} on {2} {3}".format(
          info['python'], info['qt'], info['os'], info['name']))
    INFO("Loading settings...")
    settings.load_settings()

    # Import resources
    from src import resources  # lint:ok

    qapp = QApplication(sys.argv)

    # Style
    style = settings.PSettings.THEME
    if style:
        QApplication.instance().setStyle(style)

    # Icon
    qapp.setWindowIcon(QIcon(":img/icon"))

    # System and app language
    local = QLocale.system().name()
    lang = settings.get_setting('language', local)
    translator = QTranslator()
    if settings.PSettings.LANGUAGE:
        translator.load(os.path.join(settings.LANG_PATH, lang + '.qm'))
        qapp.installTranslator(translator)

        qtranslator = QTranslator()
        qtranslator.load("qt_" + local, QLibraryInfo.location(
                         QLibraryInfo.TranslationsPath))
        qapp.installTranslator(qtranslator)

    # Load services
    #from src.gui import table_widget  # lint:ok
    from src.gui import central_widget  # lint:ok
    from src.gui import main_container  # lint:ok
    #from src.gui import lateral_widget  # lint:ok
    #from src.gui.query_container import query_container  # lint:ok
    from src.gui.main_window import Pireal
    #from src.gui import status_bar  # lint:ok
    #from src.gui import container  # lint:ok

    INFO("Loading GUI...")
    gui = Pireal()
    gui.show()

    # Console
    # Enable from settings file
    if settings.PSettings.CONSOLE:
        from src.utils.console import console_widget
        from PyQt5.QtWidgets import QDesktopWidget
        console = console_widget.ConsoleWidget()
        console.show()
        console.resize(700, 150)
        d = QDesktopWidget()
        geo = d.screenGeometry()
        console.move(geo.width() / 4, geo.height() / 1.5)

    INFO("Pireal ready!")
    sys.exit(qapp.exec_())
