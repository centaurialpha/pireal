# -*- coding: utf-8 -*-
#
# Copyright 2015-2021 - Gabriel Acosta <acostadariogabriel@gmail.com>
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

from pireal.interpreter.exceptions import InvalidSyntaxError, MissingQuoteError
from pireal.interpreter.scanner import Scanner
from pireal.interpreter.tokens import RESERVED_KEYWORDS, Token, TokenTypes
from pireal.interpreter.utils import is_date, is_time


class Lexer:
    """First stage of analysis.

    The Lexer serves to break up the source text into chuncks, "tokens".
    It calls the Scanner to get characters one at a time and organizes them
    into token types.

    For example, if the source text is:

    query_1 := people njoin skills

    The lexer organized in this way:

    Token(ID, 'query_1')
    Token(ASSIGNMENT, ':=')
    Token(ID, 'people')
    Token(NJOIN, 'njoin')
    Token(ID, 'skills')
    """

    QUOTES = ('"', "'")

    def __init__(self, scanner: Scanner):
        self.sc = scanner

    def _skip_whitespace(self):
        while self.sc.char is not None and self.sc.char.isspace():
            self.sc.next()

    def _skip_comment(self):
        while self.sc.char is not None and self.sc.char != "\n":
            self.sc.next()
        self.sc.next()

    def get_identifier_or_keyword(self) -> Token:
        """Handle identifiers and reserved keywords."""
        token = Token(
            type=TokenTypes.UNKNOWN, value=None, line=self.sc.lineno, col=self.sc.colno
        )

        var = ""
        while self.sc.char is not None and not self.sc.char.isspace():
            # Recognize identifiers like: query_1, query2323
            if self.sc.char == "_":
                var += "_"
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

        token_type = RESERVED_KEYWORDS.get(var)
        if token_type is None:
            token.type = TokenTypes.ID
        else:
            token.type = token_type
        token.value = var
        return token

    def get_number(self) -> Token:
        """Return a multidigit integer or float."""
        token = Token(
            type=TokenTypes.UNKNOWN, value=None, line=self.sc.lineno, col=self.sc.colno
        )

        number = ""
        while self.sc.char is not None and self.sc.char.isdigit():
            number += self.sc.char
            self.sc.next()

        if self.sc.char == ".":
            number += self.sc.char
            self.sc.next()

            while self.sc.char is not None and self.sc.char.isdigit():
                number += self.sc.char
                self.sc.next()

            token.type = TokenTypes.REAL
            token.value = float(number)
        else:
            token.type = TokenTypes.INTEGER
            token.value = int(number)

        return token

    def analize_string(self) -> Token:
        self.sc.next()
        string = ""
        count = 1
        while self.sc.char is not None:
            if self.sc.char == "'":
                count -= 1
                if count == 0:
                    break
                self.sc.next()

            string += self.sc.char
            self.sc.next()

        if count == 1:
            raise MissingQuoteError("Faltan comillas", lineno=1, col=1)
        self.sc.next()

        # Is date? is time? or just string?
        ok, date = is_date(string)
        if ok:
            return Token(
                type=TokenTypes.DATE, value=date, line=self.sc.lineno, col=self.sc.colno
            )

        ok, time = is_time(string)
        if ok:
            return Token(
                type=TokenTypes.TIME, value=time, line=self.sc.lineno, col=self.sc.colno
            )
        return Token(
            type=TokenTypes.STRING, value=string, line=self.sc.lineno, col=self.sc.colno
        )

    def next_token(self) -> Token:
        """Lexical analyzer.

        This method is responsible for breaking a sentence apart
        into tokens. One token at a time
        """
        while self.sc.char is not None:
            # Recognize identifiers and keywords
            if self.sc.char.isalpha() or self.sc.char.startswith("_"):
                return self.get_identifier_or_keyword()

            # Ignore any whitespace characters
            if self.sc.char.isspace():
                self._skip_whitespace()
                continue

            # Comments inline
            if self.sc.char == "%":
                self._skip_comment()
                continue

            # Assignment
            if self.sc.char == ":" and self.sc.peek() == "=":
                token = Token(
                    type=TokenTypes.ASSIGNMENT,
                    value=TokenTypes.ASSIGNMENT.value,
                    line=self.sc.lineno,
                    col=self.sc.colno,
                )
                self.sc.next()
                self.sc.next()
                return token

            # Operators <>, <=, >=
            if self.sc.char == "<" and self.sc.peek() == ">":
                token = Token(
                    type=TokenTypes.NOTEQUAL,
                    value=TokenTypes.NOTEQUAL.value,
                    line=self.sc.lineno,
                    col=self.sc.colno,
                )
                self.sc.next()
                self.sc.next()
                return token

            if self.sc.char == "<" and self.sc.peek() == "=":
                token = Token(
                    type=TokenTypes.LESS_EQUAL,
                    value=TokenTypes.LESS_EQUAL.value,
                    line=self.sc.lineno,
                    col=self.sc.colno,
                )
                self.sc.next()
                self.sc.next()
                return token

            if self.sc.char == ">" and self.sc.peek() == "=":
                token = Token(
                    type=TokenTypes.GREATHER_EQUAL,
                    value=TokenTypes.GREATHER_EQUAL.value,
                    line=self.sc.lineno,
                    col=self.sc.colno,
                )
                self.sc.next()
                self.sc.next()
                return token

            # Number
            if self.sc.char.isdigit():
                return self.get_number()

            # Strings, dates, times
            if self.sc.char == "'":
                token = self.analize_string()
                return token

            # Single-character
            try:
                token_type = TokenTypes(self.sc.char)
            except ValueError:
                raise InvalidSyntaxError(
                    self.sc.lineno, self.sc.colno, self.sc.char
                ) from None
            else:
                token = Token(
                    type=token_type,
                    value=token_type.value,
                    line=self.sc.lineno,
                    col=self.sc.colno,
                )
                self.sc.next()
                return token

        # EOF
        return Token(TokenTypes.EOF, None)
