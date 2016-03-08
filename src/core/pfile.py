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

import os

from PyQt5.QtCore import (
    QFile,
    QIODevice,
    QTextStream
)


class PFile(object):
    """ This class represents a Pireal File, database file or query file """

    def __init__(self, filename=''):
        """
        Recive the filename or set using the filename property
        """

        self.__is_new = True
        self.__filename = filename
        if filename:
            self.__is_new = False

    def __get_filename(self):
        """ Returns the filename """

        return self.__filename

    def __set_filename(self, fname):
        """ This function set the filename """

        self.__filename = fname

    filename = property(__get_filename, __set_filename)

    @property
    def name(self):
        """ This function returns the display name """

        return os.path.basename(self.filename)

    @property
    def is_new(self):
        """ This function returns True is the file is new, False otherwise """

        return self.__is_new

    def read(self):
        """ This function reads the file and returns the contents """

        file_ = QFile(self.filename)
        if not file_.open(QIODevice.ReadOnly | QIODevice.Text):
            raise Exception(file_.errorString())
        fstream = QTextStream(file_)
        fstream.setCodec('utf-8')
        return fstream.readAll()

    def write(self, content, new_fname=''):
        """ This function write the file """

        if self.is_new:
            self.__filename = new_fname
            self.__is_new = False

        file_ = QFile(self.filename)
        if not file_.open(QIODevice.WriteOnly | QIODevice.Truncate):
            raise Exception(file_.errorString())

        stream = QTextStream(file_)
        stream.setCodec('utf-8')
        stream << content
        stream.flush()
        file_.close()
