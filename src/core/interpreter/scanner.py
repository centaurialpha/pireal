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


class Scanner(object):
    __slots__ = ('lineno', 'colno', 'index', '_text')

    def __init__(self, text):
        self._text = text
        self.index = 0
        self.lineno = 1
        self.colno = 0

    @property
    def char(self):
        if self.index < len(self._text):
            return self._text[self.index]

        # End of file
        return None

    def next(self):
        """ Move on to the next character in the scanned text """

        if self.char == '\n':
            # We are in a new line, therefore we increase the line
            # number and restart the column number
            self.lineno += 1
            self.colno = 0
        else:
            self.colno += 1
        self.index += 1

    def next_char(self):
        """ Returns the new character """

        self.next()
        return self.char

    def __repr__(self):
        return '<Scanner at {line}:{col}>'.format(
            line=self.lineno,
            col=self.colno
        )