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
from __future__ import annotations

import datetime
import enum
from dataclasses import dataclass


class TokenTypes(enum.Enum):
    # Single character
    SEMI = ";"
    COMMA = ","
    LESS = "<"
    GREATER = ">"
    LEFT_PARENTHESIS = "("
    RIGHT_PARENTHESIS = ")"
    EQUAL = "="

    LESS_EQUAL = "<="
    GREATHER_EQUAL = ">="
    NOTEQUAL = "<>"
    ASSIGNMENT = ":="

    ID = "IDENTIFIER"
    CONSTANT = "CONSTANT"
    INTEGER = "INTEGER"
    REAL = "REAL"
    STRING = "STRING"
    DATE = "DATE"
    TIME = "TIME"
    KEYWORD = "KEYWORD"
    EOF = "EOF"

    # RA operators
    SELECT = "select"  # no cambiar
    PROJECT = "project"
    # Binary operators
    PRODUCT = "product"  # no cambiar
    INTERSECT = "intersect"
    UNION = "union"
    DIFFERENCE = "difference"
    NJOIN = "njoin"
    LEFT_OUTER_JOIN = "louter"
    RIGHT_OUTER_JOIN = "router"
    FULL_OUTER_JOIN = "fouter"  # no cambiar
    # Conditional
    AND = "and"
    OR = "or"  # no cambiar

    UNKNOWN = "unknown"


def _build(start_token, end_token):
    token_type_list = list(TokenTypes)
    start_index = token_type_list.index(start_token)
    end_index = token_type_list.index(end_token)
    return {
        token_type.value: token_type
        for token_type in token_type_list[start_index : end_index + 1]
    }


def _build_binary_operators():
    return _build(TokenTypes.PRODUCT, TokenTypes.FULL_OUTER_JOIN)


def _build_reserved_keywords():
    return _build(TokenTypes.SELECT, TokenTypes.OR)


@dataclass(eq=False)
class Token:
    type: TokenTypes
    value: int | float | str | datetime.date | datetime.time | None
    line: int | None = None
    col: int | None = None

    def __eq__(self, other):
        return self.type == other.type and self.value == other.value


BINARY_OPERATORS = _build_binary_operators()
RESERVED_KEYWORDS = _build_reserved_keywords()
