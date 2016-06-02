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

# This module is responsible for organizing called "tokens" pieces,
# each of these tokens has a meaning in language


class Cursor(object):
    __slots__ = ('index', 'colno', 'lineno')

    def __init__(self, index, colno, lineno):
        self.index = index
        self.colno = colno
        self.lineno = lineno

    def __str__(self):
        return 'Cursor(line={0}, col={1}, index={2})'.format(
            self.lineno,
            self.colno,
            self.index
        )

    def __repr__(self):
        return self.__str__()


class Scanner(object):
    """ This is the first stage of analysis .

    The Scanner is responsible for reading the text character by character,
    carrying information such as line number, column number and the
    absolute position or index.
    """

    __slots__ = ('_text', '_index', '_lineno', '_colno', '_current_char')

    def __init__(self, text):
        self._text = text
        self._index = -1
        self._lineno = 0
        self._colno = 0
        self._current_char = self._text[self._index]

    def next_char(self):
        """ Advancing a position in the text """

        self._index += 1
        if self._index < len(self._text):
            self._current_char = self._text[self._index]
            if self._current_char == '\n':
                # We are in a new line, therefore we increase the line
                # number and restart the column number
                self._lineno += 1
                self._colno = 0
        else:
            # End of file
            self._current_char = None

        self._colno += 1

    def cursor(self):
        return Cursor(self._index,
                      self._colno,
                      self._lineno
                      )

    @property
    def char(self):
        """ Returns the next char in the text """

        self.next_char()
        return self._current_char
