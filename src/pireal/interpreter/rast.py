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
