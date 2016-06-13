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
    NOTEQUAL,
    GREATER,
    GREATEREQUAL,
    LESS,
    LESSEQUAL,
    EOF,
    KEYWORDS
)


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
    Token(KEYWORD, 'njoin')
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

    def _get_identifier_or_keyword(self):
        """ Handle identifiers and reserved keywords """

        var = ''
        while self.sc.char is not None and not self.sc.char.isspace():
            # Recognize identifiers like: query_1, query2323
            # FIXME: improve this
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

        return KEYWORDS.get(var, Token(IDENTIFIER, var))

    def _get_number(self):
        """ Returns a multidigit integer """

        number = ''
        if self.sc.char == '-':
            number += self.sc.char
            self.sc.next()
        while self.sc.char is not None and self.sc.char.isdigit():
            number += self.sc.char
            self.sc.next()
        return int(number)

    def next_token(self):
        """ Lexical analyzer.

        This method is responsible for breaking a sentence apart
        into tokens. One token at a time
        """

        while self.sc.char is not None:
            # Recognize identifiers and keywords
            if self.sc.char.isalpha():
                return self._get_identifier_or_keyword()

            # Ignore any whitespace characters or any comments
            if self.sc.char.isspace():
                self._skip_whitespace()
                continue

            # Manage assignment
            if self.sc.char == ':':
                self.sc.next()
                if self.sc.char == '=':
                    self.sc.next()
                    return Token(ASSIGNMENT, ':=')

            # Operators
            # Less, not-equal and less-equal
            if self.sc.char == '<':
                self.sc.next()
                if self.sc.char == '>':
                    self.sc.next()
                    return Token(NOTEQUAL, '<>')
                elif self.sc.char == '=':
                    self.sc.next()
                    return Token(LESSEQUAL, '<=')
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
                    return Token(GREATEREQUAL, '>=')
                return Token(GREATER, '>')

            # Semicolon
            if self.sc.char == ';':
                self.sc.next()
                return Token(SEMI, ';')

            # Numbers
            if self.sc.char == '-' or self.sc.char.isdigit():
                number = self._get_number()
                return Token(NUMBER, number)

            # Strings
            if self.sc.char == "'":
                string = ""
                while True:
                    if self.sc.char is None:
                        break
                    string += self.sc.char
                    self.sc.next()
                return Token(STRING, string)

            # Left parenthesis
            if self.sc.char == '(':
                self.sc.next()
                return Token(LPAREN, '(')

            # Right parenthesis
            if self.sc.char == ')':
                self.sc.next()
                return Token(RPAREN, ')')

            # Coma
            if self.sc.char == ',':
                self.sc.next()
                return Token(COMA, ',')

            raise Exception("Invalid Syntax {0}:{1}".format(
                self.sc.lineno, self.sc.colno))
        return Token(EOF, None)

    def __str__(self):
        """ Returns a representation of token """

        return 'Token({type}, {value})'.format(
            type=self.token.type,
            value=self.token.value
        )

    def __repr__(self):
        return self.__str__()
