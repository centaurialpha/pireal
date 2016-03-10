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

from PyQt5.QtWidgets import QMessageBox
from urllib.request import urlopen
from PyQt5.QtCore import QThread

URL = "http://centaurialpha.github.io/pireal"


class Updates(QThread):
    """ This thread checks for a new version of Pireal """

    def __init__(self):
        super(Updates, self).__init__()

    def run(self):
        try:
            web_version = urlopen(URL).read().decode('utf8')
            print(web_version)
        except:
            print("Error")
