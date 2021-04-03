# -*- coding: utf-8 -*-
#
# Copyright 2015-2016 - Gabriel Acosta <acostadariogabriel@gmail.com>
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

import os

from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal as Signal
from PyQt5.QtCore import QFile
from PyQt5.QtCore import QTextStream
from PyQt5.QtCore import QTextCodec
from PyQt5.QtCore import QIODevice


class File(QObject):

    """ This class represents an object file"""

    fileSaved = Signal(str)

    def __init__(self, filename=''):
        QObject.__init__(self)
        self.is_new = True
        if filename:
            self.is_new = False
        self.filename = filename

    @property
    def display_name(self):
        """ Returns only the file name with extension, without the path"""

        return os.path.basename(self.filename)

    def save(self, data, path=None):
        if path:
            self.filename = path
            self.is_new = False

        _file = QFile(self.filename)
        if not _file.open(QIODevice.WriteOnly | QIODevice.Truncate):
            raise Exception(_file.errorString())

        stream = QTextStream(_file)
        stream.setCodec(QTextCodec.codecForLocale())
        stream << data
        stream.flush()
        _file.close()
        # Emit the signal
        self.fileSaved.emit(self.filename)

    def read(self):
        """ Reads the file and returns the content """

        with open(self.filename, encoding='utf-8') as f:
            return f.read()
