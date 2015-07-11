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
    QStyleFactory
)


def __get_versions():
    """ Version information for components used by Pireal """

    import platform
    from PyQt4.QtCore import QT_VERSION_STR

    # OS
    if sys.platform.startswith('linux'):
        system, name = platform.uname()[:2]
    else:
        system, name = "Windows", platform.uname().release
    # Python version
    python_version = platform.python_version()

    return {
        'python': python_version,
        'os': system,
        'name': name,
        'qt': QT_VERSION_STR  # Qt version
    }


if __name__ == "__main__":

    info = __get_versions()
    print("Executing Pireal from source")
    print("01. Python {0} - Qt {1} on {2} {3}".format(
          info['python'], info['qt'], info['os'], info['name']))

    # Import resources
    from src import resources  # lint:ok

    qapp = QApplication(sys.argv)

    from src.gui.main_window import Pireal
    from src.gui import container  # lint:ok
    from src.gui import table_widget  # lint:ok
    from src.gui.query_editor import query_widget  # lint:ok
    from src.gui import lateral_widget  # lint:ok
    #from src.gui import mdi_area  # lint:ok
    #from src.gui import actions  # lint:ok

    # Style
    qapp.setStyle(QStyleFactory.create("gtk"))
    print("02. Loading GUI...")
    gui = Pireal()
    gui.show()
    gui.showMaximized()
    print("Ok.")
    sys.exit(qapp.exec_())