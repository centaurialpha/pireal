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

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from pireal.interpreter.tokens import Token, TokenTypes


@dataclass
class Variable:
    token: Token

    @property
    def value(self) -> str:
        return str(self.token.value)

    @property
    def lineno(self) -> int | None:
        return self.token.line


@dataclass
class Number:
    value: int | float


@dataclass
class String:
    value: str


@dataclass
class Date:
    value: object  # datetime.date


@dataclass
class Time:
    value: object  # datetime.time


@dataclass
class ProjectExpr:
    attrs: list[Variable]
    expr: object  # cualquier nodo expresión


@dataclass
class SelectExpr:
    condition: object
    expr: object


@dataclass
class BinaryOp:
    left: object
    op: TokenTypes
    right: object


@dataclass
class Condition:
    op1: object
    operator: Token
    op2: object


@dataclass
class BooleanExpression:
    left_formula: object
    operator: TokenTypes
    right_formula: object


@dataclass
class Assignment:
    rname: Variable
    query: object


@dataclass
class Compound:
    children: list[Assignment] = field(default_factory=list)


class NodeVisitor:
    """Base visitor. Subclasses implement visit_ClassName methods."""

    def visit(self, node: object) -> Any:
        method_name = f"visit_{type(node).__name__}"
        visitor = getattr(self, method_name, self._generic_visit)
        return visitor(node)

    def _generic_visit(self, node: object) -> None:
        raise NotImplementedError(f"No visit_{type(node).__name__} method defined")
