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


class InterpreterError(Exception):
    """Excepción básica para errores generados por el intérprete."""


class MissingQuoteError(InterpreterError):
    """Excepción para comillas faltantes en strings."""

    def __init__(self, msg, lineno, col):
        InterpreterError.__init__(self, msg.format(lineno))
        self.lineno = lineno - 1
        self.column = col


class InvalidSyntaxError(InterpreterError):
    """Excepción para errores de sintáxis generados por el Lexer."""

    def __init__(self, lineno, col, char, msg="Invalid syntax on '{0}':'{1}'"):
        InterpreterError.__init__(self, msg.format(lineno, col))
        self.lineno = lineno
        self.column = col
        self.character = "<b>" + char + "</b>"


class ConsumeError(InterpreterError):

    def __init__(self, expected, got, lineno, msg=None):
        if msg is None:
            msg = (
                f"It is expected to find '{expected}' ('{expected.value}'), "
                f"but '{got.value}' found in line: '{lineno}'"
            )
        super().__init__(msg)
        self.expected = expected
        self.got = got
        self.lineno = lineno


class DuplicateRelationNameError(InterpreterError):

    def __init__(self, rname):
        super().__init__()
        self.rname = rname
