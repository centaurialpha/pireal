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
import platform
import logging

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QT_VERSION_STR
from PyQt5.QtCore import QTranslator
from PyQt5.QtGui import QIcon

from pireal import __version__
from pireal.core import settings
# from pireal.core.settings import CONFIG
from pireal.gui import main_window

logger = logging.getLogger(__name__)


def start_pireal():
    # CONFIG.load_settings()

    # OS
    if sys.platform.startswith('linux'):
        system, os_name = platform.uname()[:2]
    else:
        system = platform.uname()[0]
        os_name = platform.uname()[2]
    # Python version
    python_version = platform.python_version()

    version_info = {
        'pireal': __version__,
        'python': python_version,
        'system': system,
        'os': os_name,
        'qt': QT_VERSION_STR
    }
    print('Running Pireal {pireal}...\nPython {python} on {system}-{os}, Qt {qt}'.format(
        **version_info))
    logger.info('Running Pireal %s with Python %s on %r',
                __version__, sys.version_info, sys.platform)

    app = QApplication(sys.argv)

    # Set application icon
    app.setWindowIcon(QIcon(':img:/icon'))
    # Language
    # lang = CONFIG.get('language')
    # if lang != 'English':
    #     translator = QTranslator()
    #     translator.load(os.path.join(settings.LANGUAGE_PATH, lang + '.qm'))
    #     app.installTranslator(translator)

    # TODO: Load stylesheet

    pireal_gui = main_window.Pireal()
    pireal_gui.show()

    sys.exit(app.exec_())
