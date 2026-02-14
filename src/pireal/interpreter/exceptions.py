# -*- coding: utf-8 -*-
#
# Copyright 2015-2017 - Gabriel Acosta <acostadariogabriel@gmail.com>
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

from __future__ import annotations


class InterpreterError(Exception):
    """Base exception for interpreter errors."""

    lineno: int | None = None
    column: int | None = None


class MissingQuoteError(InterpreterError):
    """Missing closing quote in a string literal."""

    def __init__(self, lineno: int, col: int):
        super().__init__(f"Missing closing quote on line {lineno}.")
        self.lineno = lineno
        self.column = col


class InvalidSyntaxError(InterpreterError):
    """Unexpected character found in the query."""

    def __init__(self, lineno: int, col: int, char: str):
        super().__init__(
            f"Unexpected character '{char}' on line {lineno}, column {col}."
        )
        self.lineno = lineno
        self.column = col
        self.char = char


class ConsumeError(InterpreterError):
    """Unexpected token found while parsing."""

    def __init__(self, expected, got, lineno: int, got_value: str | None = None):
        got_str = got_value or got.value
        super().__init__(
            f"Syntax error on line {lineno}: "
            f"expected '{expected.value}' but got '{got_str}'."
        )
        self.expected = expected
        self.got = got
        self.lineno = lineno


class DuplicateRelationNameError(InterpreterError):
    """A relation name was defined more than once."""

    def __init__(self, rname: str):
        super().__init__(f"Relation '{rname}' is already defined in this query.")
        self.rname = rname


class UndefinedAttributeError(InterpreterError):
    """An attribute referenced in the query does not exist in the relation."""

    def __init__(self, attribute: str, relation_name: str, lineno: int | None = None):
        super().__init__(
            f"Attribute '{attribute}' does not exist in relation '{relation_name}'."
        )
        self.attribute = attribute
        self.relation_name = relation_name
        self.lineno = lineno
