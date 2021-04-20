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

from pireal.interpreter.tokens import (
    Token,
    TokenTypes,
    RESERVED_KEYWORDS,
)

from pireal.interpreter.exceptions import (
    MissingQuoteError,
    InvalidSyntaxError
)

from pireal.interpreter.utils import (
    is_date,
    is_time,
)


class Lexer(object):
    """ This is the first stage of analysis.

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

    def __init__(self, scanner):
        self.sc = scanner

    def _skip_whitespace(self):
        while self.sc.char is not None and self.sc.char.isspace():
            self.sc.next()

    def _skip_comment(self):
        while self.sc.char is not None and self.sc.char != '\n':
            self.sc.next()
        self.sc.next()

    def get_identifier_or_keyword(self):
        """ Handle identifiers and reserved keywords """

        token = Token(type=None, value=None, line=self.sc.lineno, col=self.sc.colno)

        var = ''
        while self.sc.char is not None and not self.sc.char.isspace():
            # Recognize identifiers like: query_1, query2323
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

        token_type = RESERVED_KEYWORDS.get(var)
        if token_type is None:
            token.type = TokenTypes.ID
        else:
            token.type = token_type
        token.value = var
        return token

    def get_number(self):
        """ Returns a multidigit integer or float """

        token = Token(type=None, value=None, line=self.sc.lineno, col=self.sc.colno)

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

            token.type = TokenTypes.REAL
            token.value = float(number)
        else:
            token.type = TokenTypes.INTEGER
            token.value = int(number)

        return token

    def _get_string(self):
        """Handle string inside quotes"""
        self.sc.next()  # consume first quote

        saved_lineno = self.sc.lineno
        save_col = self.sc.colno

        string = ""
        while True:
            # FIXME: check complementary
            if self.sc.char in Lexer.QUOTES:
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

        self.sc.next()  # consume second quote

        return string

    def next_token(self):
        """ Lexical analyzer.

        This method is responsible for breaking a sentence apart
        into tokens. One token at a time
        """

        while self.sc.char is not None:
            # Recognize identifiers and keywords
            if self.sc.char.isalpha():
                return self.get_identifier_or_keyword()

            # Ignore any whitespace characters
            if self.sc.char.isspace():
                self._skip_whitespace()
                continue

            # Comments inline
            if self.sc.char == '%':
                self._skip_comment()
                continue

            # Assignment
            if self.sc.char == ':' and self.sc.peek() == '=':
                token = Token(
                    type=TokenTypes.ASSIGNMENT,
                    value=TokenTypes.ASSIGNMENT.value,
                    line=self.sc.lineno,
                    col=self.sc.colno
                )
                self.sc.next()
                self.sc.next()
                return token

            # Operators <>, <=, >=
            if self.sc.char == '<' and self.sc.peek() == '>':
                token = Token(
                    type=TokenTypes.NOTEQUAL,
                    value=TokenTypes.NOTEQUAL.value,
                    line=self.sc.lineno,
                    col=self.sc.colno
                )
                self.sc.next()
                self.sc.next()
                return token

            if self.sc.char == '<' and self.sc.peek() == '=':
                token = Token(
                    type=TokenTypes.LEQUAL,
                    value=TokenTypes.LEQUAL.value,
                    line=self.sc.lineno,
                    col=self.sc.colno
                )
                self.sc.next()
                self.sc.next()
                return token

            if self.sc.char == '>' and self.sc.peek() == '=':
                token = Token(
                    type=TokenTypes.GEQUAL,
                    value=TokenTypes.GEQUAL.value,
                    line=self.sc.lineno,
                    col=self.sc.colno
                )
                self.sc.next()
                self.sc.next()
                return token

            # Number
            if self.sc.char.isdigit():
                return self.get_number()

            # Strings, dates, times
            if self.sc.char in Lexer.QUOTES:
                string = self._get_string()
                ok, date = is_date(string)
                if ok:
                    return Token(
                        type=TokenTypes.DATE,
                        value=date,
                        line=self.sc.lineno,
                        col=self.sc.colno
                    )
                ok, time = is_time(string)
                if ok:
                    return Token(
                        type=TokenTypes.TIME,
                        value=time,
                        line=self.sc.lineno,
                        col=self.sc.colno
                    )
                return Token(
                    type=TokenTypes.STRING,
                    value=string,
                    line=self.sc.lineno,
                    col=self.sc.colno
                )

            # Single-character
            try:
                token_type = TokenTypes(self.sc.char)
            except ValueError:
                raise InvalidSyntaxError(
                    self.sc.lineno,
                    self.sc.colno,
                    self.sc.char
                )
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
