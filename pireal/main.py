# -*- coding: utf-8 -*-
#
# Copyright 2015-2019 Gabriel Acosta <acostadariogabriel@gmail.com>
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

import sys
import os
import logging

from PyQt5.QtWidgets import QApplication

from PyQt5.QtGui import QIcon, QFont, QFontDatabase

from PyQt5.QtCore import QTranslator
from PyQt5.QtCore import QLocale
from PyQt5.QtCore import QLibraryInfo


from pireal.gui.theme import apply_theme
from pireal.settings import SETTINGS

logger = logging.getLogger('main')


def start_pireal(args):

    # OS
    # if settings.IS_LINUX:
    #     system, os_name = platform.uname()[:2]
    # else:
    #     system = platform.uname()[0]
    #     os_name = platform.uname()[2]
    # # Python version
    # python_version = platform.python_version()

    # print(f'Running Pireal {__version__}...\n'
    #       f'Python {python_version} on {system}-{os_name}, Qt {QT_VERSION_STR}')
    # logger.info('Running Pireal %s with Python %s on %r',
    #             __version__, sys.version_info, sys.platform)

    app = QApplication(sys.argv)
    app.setApplicationName('Pireal')
    app.setApplicationDisplayName('Pireal')
    app.setWindowIcon(QIcon(':img/icon'))

    SETTINGS.load()

    app.setStyle('fusion')
    apply_theme(app)

    # Add Font Awesome
    family = QFontDatabase.applicationFontFamilies(
        QFontDatabase.addApplicationFont(':font/awesome'))[0]
    font = QFont(family)
    font.setStyleName('Solid')
    app.setFont(font)
    # Install translators
    # Qt translations
    system_locale_name = QLocale.system().name()
    qt_languages_path = QLibraryInfo.location(QLibraryInfo.TranslationsPath)
    qt_translator = QTranslator()
    translator_loaded = qt_translator.load(
        os.path.join(qt_languages_path, f'qt_{SETTINGS.language}.qm'))
    if not translator_loaded:
        qt_translator.load(
            os.path.join(qt_languages_path, 'qt_{}.qml'.format(system_locale_name.split('_')[0])))
    app.installTranslator(qt_translator)
    # App translator
    translator = QTranslator()
    if translator.load(f':lang/{SETTINGS.language}'):
        app.installTranslator(translator)
    # Load services
    from pireal.gui import central_widget  # noqa
    from pireal.gui.main_window import Pireal

    check_updates = not args.no_check_updates
    pireal_gui = Pireal(check_updates)
    pireal_gui.show()

    sys.exit(app.exec_())
