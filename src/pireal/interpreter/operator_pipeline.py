# Copyright 2015-2026 - Gabriel Acosta <acostadariogabriel@gmail.com>
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


from pireal.interpreter import rast as ast
from pireal.interpreter.tokens import TokenTypes

_BINARY_SYMBOLS: dict[TokenTypes, str] = {
    TokenTypes.SELECT: "σ",
    TokenTypes.PROJECT: "π",
    TokenTypes.NJOIN: "⋈",
    TokenTypes.LOUTER: "⟕",
    TokenTypes.ROUTER: "⟖",
    TokenTypes.FOUTER: "⟗",
    TokenTypes.PRODUCT: "×",
    TokenTypes.UNION: "∪",
    TokenTypes.DIFFERENCE: "−",
    TokenTypes.INTERSECT: "∩",
    TokenTypes.DIVIDE: "÷",
}


def extract_pipeline(node: object) -> list[str]:
    """
    Returns the list of operator symbols used in the expression,
    in bottom-up (execution) order, without duplicates
    """
    seen: set[str] = set()
    result: list[str] = []

    def _walk(n: object) -> None:
        if isinstance(n, ast.SelectExpr):
            _walk(n.expr)
            _add("σ")
        elif isinstance(n, ast.ProjectExpr):
            _walk(n.expr)
            _add("π")
        elif isinstance(n, ast.BinaryOp):
            _walk(n.left)
            _walk(n.right)
            symbol = _BINARY_SYMBOLS.get(n.op)
            if symbol:
                _add(symbol)
        elif isinstance(n, ast.Assignment):
            _walk(n.query)

    def _add(symbol: str) -> None:
        if symbol not in seen:
            seen.add(symbol)
            result.append(symbol)

    _walk(node)
    return result


def pipeline_text(node: object) -> str:
    """
    Returns a formatted string like 'σ -> π -> ⋈' or empty string
    """
    symbols = extract_pipeline(node)
    return " ➜ ".join(symbols)
