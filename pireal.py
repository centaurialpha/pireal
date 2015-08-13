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
from PyQt4.QtGui import (
    QApplication,
    QStyleFactory,
    QIcon
)
from PyQt4.QtCore import (
    QLocale,
    QTranslator,
    QLibraryInfo
)
from src.core import (
    settings,
    logger
)
log = logger.get_logger(__name__)
DEBUG = log.debug
INFO = log.info


def __get_versions():
    """ Version information for components used by Pireal """

    import platform
    from PyQt4.QtCore import QT_VERSION_STR

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


if __name__ == "__main__":

    # Create dir
    settings.create_dir()
    info = __get_versions()
    DEBUG("Executing Pireal from source")
    INFO("Python {0} - Qt {1} on {2} {3}".format(
         info['python'], info['qt'], info['os'], info['name']))

    # Import resources
    from src import resources  # lint:ok

    qapp = QApplication(sys.argv)
    qapp.setWindowIcon(QIcon(":img/logo"))
    # System language
    local = QLocale.system().name()
    translator = QTranslator()
    translator.load("qt_" + local, QLibraryInfo.location(
                    QLibraryInfo.TranslationsPath))
    qapp.installTranslator(translator)
    # Load services
    from src.gui import central_widget  # lint:ok
    from src.gui.main_window import Pireal
    from src.gui import status_bar  # lint:ok
    from src.gui import container  # lint:ok
    from src.gui import table_widget  # lint:ok
    from src.gui.query_editor import query_widget  # lint:ok
    from src.gui import lateral_widget  # lint:ok

    # Style
    qapp.setStyle(QStyleFactory.create("gtk"))
    INFO("Loading GUI...")
    gui = Pireal()
    # Style sheet
    with open('src/gui/style.qss') as f:
        qapp.setStyleSheet(f.read())
    gui.show()
    gui.showMaximized()
    INFO("Pireal ready!")
    sys.exit(qapp.exec_())