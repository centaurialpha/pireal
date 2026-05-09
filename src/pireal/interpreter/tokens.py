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
    GREATER_EQUAL = ">="
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
    LOUTER = "louter"
    ROUTER = "router"
    FOUTER = "fouter"  # no cambiar
    DIVIDE = "divide"
    # Conditional
    AND = "and"
    OR = "or"  # no cambiar

    UNKNOWN = "unknown"


BINARY_OPERATORS: dict[str, TokenTypes] = {
    TokenTypes.PRODUCT.value: TokenTypes.PRODUCT,
    TokenTypes.INTERSECT.value: TokenTypes.INTERSECT,
    TokenTypes.UNION.value: TokenTypes.UNION,
    TokenTypes.DIFFERENCE.value: TokenTypes.DIFFERENCE,
    TokenTypes.NJOIN.value: TokenTypes.NJOIN,
    TokenTypes.LOUTER.value: TokenTypes.LOUTER,
    TokenTypes.ROUTER.value: TokenTypes.ROUTER,
    TokenTypes.FOUTER.value: TokenTypes.FOUTER,
    TokenTypes.DIVIDE.value: TokenTypes.DIVIDE,
}

RESERVED_KEYWORDS: dict[str, TokenTypes] = {
    TokenTypes.SELECT.value: TokenTypes.SELECT,
    TokenTypes.PROJECT.value: TokenTypes.PROJECT,
    **BINARY_OPERATORS,
    TokenTypes.AND.value: TokenTypes.AND,
    TokenTypes.OR.value: TokenTypes.OR,
}


KEYWORD_SYMBOLS: dict[str, TokenTypes] = {
    "σ": TokenTypes.SELECT,
    "π": TokenTypes.PROJECT,
    "⋈": TokenTypes.NJOIN,
    "∪": TokenTypes.UNION,
    "∩": TokenTypes.INTERSECT,
    "−": TokenTypes.DIFFERENCE,
    "×": TokenTypes.PRODUCT,
    "⟕": TokenTypes.LOUTER,
    "⟖": TokenTypes.ROUTER,
    "⟗": TokenTypes.FOUTER,
    "÷": TokenTypes.DIVIDE,
}

KEYWORD_TO_SYMBOL: dict[str, str] = {token_type.value: symbol for symbol, token_type in KEYWORD_SYMBOLS.items()}

SYMBOL_TO_KEYWORD: dict[str, str] = {symbol: token_type.value for symbol, token_type in KEYWORD_SYMBOLS.items()}


@dataclass(eq=False)
class Token:
    type: TokenTypes
    value: int | float | str | datetime.date | datetime.time | None
    line: int | None = None
    col: int | None = None

    def __eq__(self, other):
        return self.type == other.type and self.value == other.value
