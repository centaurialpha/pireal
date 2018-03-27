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
from src.core.interpreter.tokens import (
    ID,
    ASSIGNMENT,
    LPAREN,
    RPAREN,
    INTEGER,
    REAL,
    STRING,
    DATE,
    TIME,
    SEMI,
    SEMICOLON,
    LESS,
    GREATER,
    LEQUAL,
    GEQUAL,
    EQUAL,
    NOTEQUAL,
    KEYWORDS,
    EOF
)
from src.core.interpreter.exceptions import (
    MissingQuoteError,
    InvalidSyntaxError
)
# Formato DD/MM/AAAA o también AAAA/MM/DD
IS_DATE = re.compile(
    r'^([\d+]{2}|[\d+]{4})[\/][\d+]{2}[\/]([\d+]{2}|[\d+]{4})$')
# Formato HH:MM
IS_TIME = re.compile(r'^[\d+]{2}:[\d+]{2}$')


class Token(object):
    """ A Token is the kind of thing that Lexer returns.
    It holds:
    - The value of the token
    - The type of token that it is
    """

    __slots__ = ('type', 'value')

    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        """ Returns a representation of token. For example:

        Token(SEMICOLON, ';')
        Token(IDENTIFIER, foo)
        """

        return 'Token({type}, {value})'.format(
            type=self.type,
            value=self.value
        )

    def __repr__(self):
        return self.__str__()


class Lexer(object):
    """ This is the first stage of analysys.

    The Lexer serves to break up the source text into chuncks, "tokens".
    It calls the Scanner to get characters one at a time and organizes them
    into token types.

    For example, if the source text is:

    query_1 := people njoin skills

    The lexer organized in this way:

    Token(IDENTIFIER, 'query_1')
    Token(ASSIGNMENT, ':=')
    Token(IDENTIFIER, 'people')
    Token(NJOIN, 'njoin')
    Token(IDENTIFIER, 'skills')
    """

    __slots__ = ('sc', 'token')

    def __init__(self, scanner):
        self.sc = scanner
        # Current token
        self.token = None

    def _skip_whitespace(self):
        while self.sc.char is not None and self.sc.char.isspace():
            self.sc.next()

    def _skip_comment(self):
        while self.sc.char is not None and self.sc.char != '\n':
            self.sc.next()
        self.sc.next()

    def _get_identifier_or_keyword(self):
        """ Handle identifiers and reserved keywords """

        var = ''
        while self.sc.char is not None and not self.sc.char.isspace():
            # Recognize identifiers like: query_1, query2323
            # FIXME: improve this, regex?
            if self.sc.char == '_':
                var += '_'
                self.sc.next()
                continue
            if self.sc.char.isdigit():
                var += self.sc.char
                self.sc.next()
                continue
            if not self.sc.char.isalpha():
                break
            var += self.sc.char
            self.sc.next()

        return var

    def _get_number(self):
        """ Returns a multidigit integer or float """

        number = ''
        while self.sc.char is not None and self.sc.char.isdigit():
            number += self.sc.char
            self.sc.next()

        if self.sc.char == '.':
            number += self.sc.char
            self.sc.next()

            while self.sc.char is not None and self.sc.char.isdigit():
                number += self.sc.char
                self.sc.next()

            token = Token(REAL, float(number))
        else:
            token = Token(INTEGER, int(number))

        return token

    def peek(self, n=1):
        index = self.sc.index
        col = self.sc.colno
        line = self.sc.lineno
        for i in range(n):
            token = self.next_token()
        self.sc.index = index
        self.sc.colno = col
        self.sc.lineno = line
        return token

    def next_token(self):
        """ Lexical analyzer.

        This method is responsible for breaking a sentence apart
        into tokens. One token at a time
        """

        while self.sc.char is not None:
            # Recognize identifiers and keywords
            if self.sc.char.isalpha():
                _id = self._get_identifier_or_keyword()
                if _id in KEYWORDS:
                    return Token(KEYWORDS[_id], _id)
                return Token(ID, _id)

            # Assignment
            if self.sc.char == ':':
                self.sc.next()
                if self.sc.char == '=':
                    self.sc.next()
                    return Token(ASSIGNMENT, ':=')

            # Ignore any whitespace characters
            if self.sc.char.isspace():
                self._skip_whitespace()
                continue

            # Comments inline
            if self.sc.char == '%':
                self._skip_comment()
                continue

            # Operators
            # Less, not-equal and less-equal
            if self.sc.char == '<':
                self.sc.next()
                if self.sc.char == '>':
                    self.sc.next()
                    return Token(NOTEQUAL, '<>')
                elif self.sc.char == '=':
                    self.sc.next()
                    return Token(LEQUAL, '<=')
                return Token(LESS, '<')

            # Equal
            if self.sc.char == '=':
                self.sc.next()
                return Token(EQUAL, '=')

            # Greater and greater-equal
            if self.sc.char == '>':
                self.sc.next()
                if self.sc.char == '=':
                    self.sc.next()
                    return Token(GEQUAL, '>=')
                return Token(GREATER, '>')

            # Semicolon
            if self.sc.char == ';':
                self.sc.next()
                return Token(SEMICOLON, ';')

            # Number
            if self.sc.char.isdigit():
                return self._get_number()

            # Strings
            if self.sc.char == "'":
                self.sc.next()
                string = ""
                saved_lineno = self.sc.lineno
                save_col = self.sc.colno
                while True:
                    if self.sc.char == "'":
                        break
                    try:
                        string += self.sc.char
                    except TypeError:
                        raise MissingQuoteError(
                            "Missing quote on line: '{0}'",
                            saved_lineno + 1,
                            save_col
                        )
                    self.sc.next()

                self.sc.next()
                # Tengo la cadena, ahora compruebo si es una fecha o una
                # hora (time)
                if IS_DATE.match(string):
                    return Token(DATE, string)
                elif IS_TIME.match(string):
                    return Token(TIME, string)
                return Token(STRING, string)

            if self.sc.char == '(':
                self.sc.next()
                return Token(LPAREN, '(')

            # Right parenthesis
            if self.sc.char == ')':
                self.sc.next()
                return Token(RPAREN, ')')

            # Comma
            if self.sc.char == ',':
                self.sc.next()
                return Token(SEMI, ',')

            raise InvalidSyntaxError(
                self.sc.lineno,
                self.sc.colno,
                self.sc.char
            )

        # EOF
        return Token(EOF, None)

    def __str__(self):
        """ Returns a representation of token """

        return 'Token({type}, {value})'.format(
            type=self.token.type,
            value=self.token.value
        )

    def __repr__(self):
        return self.__str__()
