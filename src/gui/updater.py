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

from distutils.version import LooseVersion
from urllib.request import urlopen
from urllib.error import URLError

from PyQt5.QtCore import (
    QObject,
    pyqtSignal
)

from src import gui


URL = "http://centaurialpha.github.io/pireal/version"


class Updater(QObject):
    finished = pyqtSignal()

    def __init__(self):
        QObject.__init__(self)
        self.version = ""
        self.error = False

    def check_updates(self):
        try:
            web_version = urlopen(URL).read().decode('utf8').strip()
            if LooseVersion(gui.__version__) < LooseVersion(web_version):
                self.version = web_version
        except URLError:
            self.error = True

        self.finished.emit()
