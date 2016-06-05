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

import re
from src.core.interpreter.token import (
    Token,
    IDENTIFIER,
    ASSIGNMENT,
    LPAREN,
    RPAREN,
    COMA,
    SEMI,
    NUMBER,
    STRING,
    DATE,
    EQUAL,
    NEQUAL,
    GREATER,
    GREATEREQUAL,
    LESS,
    LESSEQUAL,
    EOF,
    KEYWORDS
)

ISDATE = re.compile(
    r'^([\d+]{2}|[\d+]{4})[\/][\d+]{2}[\/]([\d+]{2}|[\d+]{4})$')


class Lexer(object):
    """ This is the first stage of analysys.

    The Lexer serves to break up the source text into chuncks, "tokens",
    it calls the `next()` method to get characters one at time and organizes
    them into tokens and token types. For example, if the source text is:

    query_1 := people njoin skills

    The lexer organized in this way:

    Token(IDENTIFIER, 'query_1')
    Token(ASSIGNMENT, ':=')
    Token(IDENTIFIER, 'people')
    Token(KEYWORD, 'njoin')
    Token(IDENTIFIER, 'skills')


    """

    __slots__ = ('_text', '_index', 'char', 'token', 'lineno', 'colno')

    def __init__(self, text):
        self._text = text
        self.lineno = 1
        self.colno = -1
        self._index = 0
        # Current char in position 0
        self.char = self._text[self._index]
        # Current token
        self.token = None

    def next(self):
        """ Advance one position in the source text and set current char """

        self._index += 1

        if self._index < len(self._text):
            # Current char in the new position
            self.char = self._text[self._index]
            if self.char == '\n':
                # We are in a new line, therefore we increase the line
                # number and restart the column number
                self.lineno += 1
                self.colno = -1
        else:
            # End of file
            self.char = None

        self.colno += 1

    def _skip_whitespace(self):
        while self.char is not None and self.char.isspace():
            self.next()

    def _get_identifier_or_keyword(self):
        # FIXME: Recognize identifiers like: var_foo, foo_1
        var = ''

        while self.char is not None and self.char.isalpha():
            var += self.char
            self.next()

        return KEYWORDS.get(var, Token(IDENTIFIER, var))

    def _get_number(self):
        """ Returns a multidigit token """

        number = ''
        if self.char == '-':
            number += self.char
            self.next()
        while self.char is not None and self.char.isdigit():
            number += self.char
            self.next()
        return int(number)

    def next_token(self):
        while self.char is not None:
            # Recognize identifiers and keywords
            if self.char.isalpha():
                return self._get_identifier_or_keyword()

            # Ignore any whitespace characters or any comments
            if self.char.isspace():
                self._skip_whitespace()
                continue

            # Manage assignment
            if self.char == ':':
                self.next()
                if self.char == '=':
                    self.next()
                    return Token(ASSIGNMENT, ':=')

            # Operators
            if self.char == '>':
                self.next()
                return Token(GREATER, '>')

            # Numbers
            if self.char == '-' or self.char.isdigit():
                number = self._get_number()
                return Token(NUMBER, number)

            # Strings, date
            if self.char == "'":
                var = ''
                self.next()
                while True:
                    if self.char is None:
                        raise Exception("Missing end quote")
                    if self.char.isspace():
                        var += ' '
                    if self.char == '/':
                        var += self.char
                    if self.char.isdigit():
                        var += self.char
                    if self.char == "'":
                        break
                    if self.char.isalpha():
                        var += self.char
                    self.next()

                if self.char == "'":
                    if ISDATE.match(var):
                        return Token(DATE, var)
                    else:
                        var = "'" + var + "'"
                        return Token(STRING, var)

            # Left parenthesis
            if self.char == '(':
                self.next()
                return Token(LPAREN, '(')

            # Right parenthesis
            if self.char == ')':
                self.next()
                return Token(RPAREN, ')')

            # Coma
            if self.char == ',':
                self.next()
                return Token(COMA, ',')

            raise Exception("Invalid Syntax {0}:{1}".format(
                self.lineno, self.colno))
        return Token(EOF, None)

    def __str__(self):
        """ Returns a representation of token """

        return 'Token({type}, {value})'.format(
            type=self.token.type,
            value=self.token.value
        )

    def __repr__(self):
        return self.__str__()
