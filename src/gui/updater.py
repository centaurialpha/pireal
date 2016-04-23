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

from urllib.request import urlopen
from urllib.error import URLError

from PyQt5.QtCore import (
    QObject,
    pyqtSignal
)

from src.core.logger import PirealLogger
from src import gui

logger = PirealLogger(__name__)
DEBUG = logger.debug

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
            web_version = tuple(web_version.split('.'))
            if ('1', '0', '0') < web_version:
                self.version = '.'.join(web_version)
        except URLError as reason:
            self.error = True
            DEBUG("Connection error: {}".format(reason))
        print("Hola")
        self.finished.emit()
