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

from pireal.core.relation import Relation
from pireal.interpreter import rast as ast
from pireal.interpreter.exceptions import (
    DuplicateRelationNameError,
    UndefinedAttributeError,
)
from pireal.interpreter.tokens import TokenTypes
from pireal.interpreter.utils import suggest_closest

OPERATOR_MAP = {
    TokenTypes.EQUAL: "==",
    TokenTypes.NOTEQUAL: "!=",
    TokenTypes.LESS: "<",
    TokenTypes.LESS_EQUAL: "<=",
    TokenTypes.GREATER: ">",
    TokenTypes.GREATER_EQUAL: ">=",
}

BINARY_OP_MAP = {
    TokenTypes.UNION: "union",
    TokenTypes.INTERSECT: "intersect",
    TokenTypes.DIFFERENCE: "difference",
    TokenTypes.PRODUCT: "product",
    TokenTypes.NJOIN: "njoin",
    TokenTypes.LOUTER: "louter",
    TokenTypes.ROUTER: "router",
    TokenTypes.FOUTER: "fouter",
    TokenTypes.DIVIDE: "divide",
}


class UndefinedRelationError(Exception):
    def __init__(self, name: str, lineno: int | None = None, suggestion: str | None = None):
        msg = f"Relation '{name}' is not defined."
        if suggestion:
            msg += f" Did you mean '{suggestion}'?"
        super().__init__(msg)
        self.name = name
        self.lineno = lineno
        self.suggestion = suggestion


class Evaluator(ast.NodeVisitor):
    def __init__(self, relations: dict[str, Relation]):
        self._relations = relations.copy()
        self._results: dict[str, Relation] = {}

    @property
    def results(self) -> dict[str, Relation]:
        return self._results

    def evaluate(self, tree: ast.Compound) -> dict[str, Relation]:
        self.visit(tree)
        return self._results

    def visit_Compound(self, node: ast.Compound) -> None:
        for child in node.children:
            self.visit(child)

    def visit_Assignment(self, node: ast.Assignment) -> None:
        name = node.rname.value
        if name in self._results:
            raise DuplicateRelationNameError(name)
        relation: Relation = self.visit(node.query)
        relation.name = name
        self._relations[name] = relation
        self._results[name] = relation

    def visit_Variable(self, node: ast.Variable) -> Relation:
        name = node.value
        relation = self._relations.get(name)
        if relation is None:
            suggestion = suggest_closest(name, list(self._relations.keys()))
            raise UndefinedRelationError(name, lineno=node.lineno, suggestion=suggestion)
        return relation

    def visit_BinaryOp(self, node: ast.BinaryOp) -> Relation:
        left = self.visit(node.left)
        right = self.visit(node.right)
        op_name = BINARY_OP_MAP[node.op]
        return getattr(left, op_name)(right)

    def visit_ProjectExpr(self, node: ast.ProjectExpr) -> Relation:
        relation = self.visit(node.expr)
        attrs = [attr.value for attr in node.attrs]
        for attr in attrs:
            if attr not in relation.header:
                suggestion = suggest_closest(attr, relation.header)
                raise UndefinedAttributeError(attr, relation.name, suggestion=suggestion)
        return relation.project(*attrs)

    def visit_SelectExpr(self, node: ast.SelectExpr) -> Relation:
        relation = self.visit(node.expr)
        self._validate_condition_attrs(node.condition, relation)
        condition = self.visit(node.condition)
        return relation.select(condition)

    def visit_Condition(self, node: ast.Condition) -> str:
        left = self._visit_operand(node.op1)
        op = OPERATOR_MAP[node.operator.type]
        right = self._visit_operand(node.op2)
        return f"{left} {op} {right}"

    def visit_BooleanExpression(self, node: ast.BooleanExpression) -> str:
        left = self.visit(node.left_formula)
        op = "and" if node.operator == TokenTypes.AND else "or"
        right = self.visit(node.right_formula)
        return f"{left} {op} {right}"

    def _visit_operand(self, node: object) -> str:
        if isinstance(node, ast.Variable):
            return node.value
        if isinstance(node, (ast.String, ast.Number, ast.Date, ast.Time)):
            return repr(node.value)
        return str(self.visit(node))

    def _validate_condition_attrs(self, node: object, relation: Relation) -> None:
        if isinstance(node, ast.Condition):
            if isinstance(node.op1, ast.Variable) and node.op1.value not in relation.header:
                suggestion = suggest_closest(node.op1.value, relation.header)
                raise UndefinedAttributeError(node.op1.value, relation.name, suggestion=suggestion)
        elif isinstance(node, ast.BooleanExpression):
            self._validate_condition_attrs(node.left_formula, relation)
            self._validate_condition_attrs(node.right_formula, relation)
