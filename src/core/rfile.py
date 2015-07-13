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


class RFile(object):
    """ This class represents a file

    :param filename: Absolute file path
     """

    def __init__(self, filename=""):
        self.__is_new = True
        if not filename:
            self.__filename = "query_"
        else:
            self.__filename = filename
            self.__is_new = False

    def __get_filename(self):
        """ This function return the filename

        :returns: The filename
        """

        return self.__filename

    def __set_filename(self, filename):
        """ This function set the filename

        :param filename: Filename path
        """

        self.__filename = filename

    filename = property(__get_filename, __set_filename)

    def is_new(self):
        """ This function returns True if the file is new, false otherwise

        :returns: Boolean value
        """

        return self.__is_new

    def read(self):
        """ This function reads the file and returns the contents

        :returns: Content file
        """

        try:
            with open(self.filename, mode='r') as f:
                content = f.read()
            return content
        except IOError as reason:
            raise Exception(reason)

    def write(self, content, new_filename=''):
        pass
