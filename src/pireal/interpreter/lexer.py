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
        # self.sc.next()

    def _make_token(self, token_type: TokenTypes) -> Token:
        token = Token(
            type=token_type,
            value=token_type.value,
            line=self.sc.lineno,
            col=self.sc.colno,
        )
        self.sc.next()
        return token

    def _make_two_char_token(self, token_type: TokenTypes) -> Token:
        token = Token(
            type=token_type,
            value=token_type.value,
            line=self.sc.lineno,
            col=self.sc.colno,
        )
        self.sc.next()
        self.sc.next()
        return token

    def get_identifier_or_keyword(self) -> Token:
        line, col = self.sc.lineno, self.sc.colno
        chars = []

        while self.sc.char is not None and not self.sc.char.isspace():
            if self.sc.char in ("_",) or self.sc.char.isdigit() or self.sc.char.isalpha():
                chars.append(self.sc.char)
                self.sc.next()
            else:
                break

        value = "".join(chars)
        token_type = RESERVED_KEYWORDS.get(value, TokenTypes.ID)
        return Token(type=token_type, value=value, line=line, col=col)

    def get_number(self) -> Token:
        """Return a multidigit integer or float."""
        line, col = self.sc.lineno, self.sc.colno
        digits = []

        while self.sc.char is not None and self.sc.char.isdigit():
            digits.append(self.sc.char)
            self.sc.next()

        if self.sc.char == ".":
            digits.append(self.sc.char)
            self.sc.next()
            while self.sc.char is not None and self.sc.char.isdigit():
                digits.append(self.sc.char)
                self.sc.next()
            return Token(type=TokenTypes.REAL, value=float("".join(digits)), line=line, col=col)

        return Token(type=TokenTypes.INTEGER, value=int("".join(digits)), line=line, col=col)

    def _read_string(self) -> Token:
        line, col = self.sc.lineno, self.sc.colno
        # Consumir la comilla
        self.sc.next()
        chars = []

        while self.sc.char is not None and self.sc.char != "'":
            chars.append(self.sc.char)
            self.sc.next()

        if self.sc.char is None:
            raise MissingQuoteError(lineno=line, col=col)

        # Consumir la comilla de cierre
        self.sc.next()
        value = "".join(chars)

        ok, date = is_date(value)
        if ok:
            return Token(type=TokenTypes.DATE, value=date, line=line, col=col)

        ok, time = is_time(value)
        if ok:
            return Token(type=TokenTypes.TIME, value=time, line=line, col=col)

        return Token(type=TokenTypes.STRING, value=value, line=line, col=col)

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
            raise MissingQuoteError(lineno=1, col=1)
        self.sc.next()

        # Is date? is time? or just string?
        ok, date = is_date(string)
        if ok:
            return Token(type=TokenTypes.DATE, value=date, line=self.sc.lineno, col=self.sc.colno)

        ok, time = is_time(string)
        if ok:
            return Token(type=TokenTypes.TIME, value=time, line=self.sc.lineno, col=self.sc.colno)
        return Token(type=TokenTypes.STRING, value=string, line=self.sc.lineno, col=self.sc.colno)

    def next_token(self) -> Token:
        """Lexical analyzer.

        This method is responsible for breaking a sentence apart
        into tokens. One token at a time
        """
        while self.sc.char is not None:
            # Recognize identifiers and keywords
            if self.sc.char.isalpha() or self.sc.char == "_":
                return self.get_identifier_or_keyword()

            # Ignore any whitespace characters
            if self.sc.char.isspace():
                self._skip_whitespace()
                continue

            # Comments inline
            if self.sc.char == "%":
                self._skip_comment()
                continue

            if self.sc.char == "'":
                return self._read_string()

            if self.sc.char.isdigit():
                return self.get_number()

            # Two-char tokens
            peek = self.sc.peek()
            # Assignment
            if self.sc.char == ":" and peek == "=":
                return self._make_two_char_token(TokenTypes.ASSIGNMENT)
            # Not equal
            if self.sc.char == "<" and peek == ">":
                return self._make_two_char_token(TokenTypes.NOTEQUAL)
            # Less equal
            if self.sc.char == "<" and peek == "=":
                return self._make_two_char_token(TokenTypes.LESS_EQUAL)
            # Greater equal
            if self.sc.char == ">" and peek == "=":
                return self._make_two_char_token(TokenTypes.GREATER_EQUAL)

            # Single-char tokens
            try:
                token_type = TokenTypes(self.sc.char)
            except ValueError:
                raise InvalidSyntaxError(self.sc.lineno, self.sc.colno, self.sc.char) from None

            return self._make_token(token_type)
        return Token(TokenTypes.EOF, None)
