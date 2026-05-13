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

from collections.abc import Callable
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from pireal.core.relation import Relation
from pireal.interpreter import rast as ast
from pireal.interpreter.tokens import TokenTypes
from pireal.interpreter.utils import condition_to_string


class OperatorType(Enum):
    # Unary
    SELECT = "σ"
    PROJECT = "π"
    RENAME = "ρ"
    # Binary
    PRODUCT = "×"
    UNION = "∪"
    DIFFERENCE = "−"
    INTERSECT = "∩"
    NJOIN = "⨝"
    LOUTER = "⟕"
    ROUTER = "⟖"
    FOUTER = "⟗"
    DIVIDE = "÷"
    # Leaf
    RELATION = "R"


class NodeState(Enum):
    PENDING = "pending"
    EXECUTING = "executing"
    EXECUTED = "executed"
    ERROR = "error"


@dataclass
class QueryPlanNode:
    operator: OperatorType
    params: str = ""  # condición, atributos, etc.
    children: list["QueryPlanNode"] = field(default_factory=list)

    ast_condition: Any = None  # para select, guardar el nodo Condition/BooleanExpression

    # Metadata
    schema: list[str] = field(default_factory=list)  # header resultante
    cardinality: int = 0
    relation_name: str = ""

    # Ejecución
    state: NodeState = NodeState.PENDING
    result: Relation | None = None
    error: str = ""

    def is_leaf(self) -> bool:
        return self.operator == OperatorType.RELATION


class QueryPlanBuilder:
    """Convierte AST de Pireal a árbol de plan de ejecución"""

    def __init__(self, relations: dict[str, Relation]):
        self.relations = relations
        self.intermediate_queries = {}  # nombre -> AST node

    def build(self, ast_tree: ast.Compound) -> list[QueryPlanNode]:
        """Retorna una lista de árboles (uno por assignment)"""
        # Primera pasada: registrar todas las queries intermedias
        for assignment in ast_tree.children:
            query_name = assignment.rname.value
            self.intermediate_queries[query_name] = assignment.query

        # Segunda pasada: construir planes expandidos
        plans = []
        for assignment in ast_tree.children:
            plan = self._visit(assignment.query)
            plan.relation_name = assignment.rname.value
            plans.append(plan)

        return plans

    def _visit(self, node) -> QueryPlanNode:
        """Visitor que despacha según tipo de nodo"""
        method_name = f"_visit_{type(node).__name__}"
        visitor = getattr(self, method_name, self._generic_visit)
        return visitor(node)

    def _generic_visit(self, node) -> QueryPlanNode:
        raise NotImplementedError(f"No visitor for {type(node).__name__}")

    def _visit_Variable(self, node: ast.Variable) -> QueryPlanNode:
        """Hoja - relación base o query intermedia"""
        var_name = node.value

        # Verificar si es query intermedia
        if var_name in self.intermediate_queries:
            # EXPANDIR: reemplazar con el subárbol de la query intermedia
            intermediate_ast = self.intermediate_queries[var_name]
            return self._visit(intermediate_ast)

        # Es relación base
        relation = self.relations.get(var_name)

        plan_node = QueryPlanNode(
            operator=OperatorType.RELATION,
            params=var_name,
            relation_name=var_name,
            schema=relation.header if relation else [],
            cardinality=relation.cardinality() if relation else 0,
        )
        return plan_node

    def _visit_SelectExpr(self, node: ast.SelectExpr) -> QueryPlanNode:
        """σ (select)"""
        child = self._visit(node.expr)
        condition = self._describe_condition(node.condition)

        return QueryPlanNode(
            operator=OperatorType.SELECT,
            params=condition,
            children=[child],
            ast_condition=node.condition,
        )

    def _visit_ProjectExpr(self, node: ast.ProjectExpr) -> QueryPlanNode:
        """π (project)"""
        child = self._visit(node.expr)
        attrs = ", ".join(attr.value for attr in node.attrs)

        return QueryPlanNode(operator=OperatorType.PROJECT, params=attrs, children=[child])

    def _visit_BinaryOp(self, node: ast.BinaryOp) -> QueryPlanNode:
        """Operadores binarios: ⨝ × ∪ − ∩"""
        left = self._visit(node.left)
        right = self._visit(node.right)

        op_map = {
            TokenTypes.PRODUCT: OperatorType.PRODUCT,
            TokenTypes.UNION: OperatorType.UNION,
            TokenTypes.DIFFERENCE: OperatorType.DIFFERENCE,
            TokenTypes.INTERSECT: OperatorType.INTERSECT,
            TokenTypes.NJOIN: OperatorType.NJOIN,
            TokenTypes.LOUTER: OperatorType.LOUTER,
            TokenTypes.ROUTER: OperatorType.ROUTER,
            TokenTypes.FOUTER: OperatorType.FOUTER,
            TokenTypes.DIVIDE: OperatorType.DIVIDE,
        }

        operator = op_map[node.op]

        return QueryPlanNode(operator=operator, params="", children=[left, right])

    def _describe_condition(self, condition) -> str:
        """Convierte una condición AST a string legible"""
        if isinstance(condition, ast.Condition):
            op1 = self._describe_operand(condition.op1)
            op2 = self._describe_operand(condition.op2)
            operator = condition.operator.value
            return f"{op1} {operator} {op2}"
        elif isinstance(condition, ast.BooleanExpression):
            left = self._describe_condition(condition.left_formula)
            right = self._describe_condition(condition.right_formula)
            op = "AND" if condition.operator == TokenTypes.AND else "OR"
            return f"({left} {op} {right})"
        return str(condition)

    def _describe_operand(self, operand) -> str:
        """Convierte operando AST a string"""
        if isinstance(operand, ast.Variable):
            return operand.value
        elif isinstance(operand, ast.Number):
            return str(operand.value)
        elif isinstance(operand, ast.String):
            return f"'{operand.value}'"
        return str(operand)


class QueryPlanEvaluator:
    """Evalúa un QueryPlanNode ejecutando las operaciones de álgebra relacional"""

    def __init__(self, relations: dict[str, Relation]):
        self.relations = relations
        self.cache: dict[int, Relation] = {}  # id(node) -> Relation (para no re-evaluar)

        self._operators: dict[OperatorType, Callable[[QueryPlanNode], Relation]] = {
            OperatorType.RELATION: self._eval_relation,
            OperatorType.SELECT: self._eval_select,
            OperatorType.PROJECT: self._eval_project,
            OperatorType.PRODUCT: self._eval_binary("product"),
            OperatorType.UNION: self._eval_binary("union"),
            OperatorType.DIFFERENCE: self._eval_binary("difference"),
            OperatorType.INTERSECT: self._eval_binary("intersect"),
            OperatorType.NJOIN: self._eval_binary("njoin"),
            OperatorType.LOUTER: self._eval_binary("louter"),
            OperatorType.ROUTER: self._eval_binary("router"),
            OperatorType.FOUTER: self._eval_binary("fouter"),
            OperatorType.DIVIDE: self._eval_binary("divide"),
        }

    def _eval_node(self, node: QueryPlanNode) -> Relation:
        handler = self._operators.get(node.operator)
        if handler is None:
            raise NotImplementedError(f"Operator {node.operator} not implemented")
        return handler(node)

    def _eval_relation(self, node: QueryPlanNode) -> Relation:
        return self.relations[node.params]

    def _eval_select(self, node: QueryPlanNode) -> Relation:
        child_result = self.evaluate(node.children[0])
        condition_str = condition_to_string(node.ast_condition) if node.ast_condition else node.params
        return child_result.select(condition_str)

    def _eval_project(self, node: QueryPlanNode) -> Relation:
        child_result = self.evaluate(node.children[0])
        attrs = [a.strip() for a in node.params.split(",")]
        return child_result.project(*attrs)

    def _eval_binary(self, method_name: str):
        """Factory que retorna función para operadores binarios"""

        def handler(node: QueryPlanNode) -> Relation:
            left = self.evaluate(node.children[0])
            right = self.evaluate(node.children[1])
            return getattr(left, method_name)(right)

        return handler

    def evaluate(self, node: QueryPlanNode) -> Relation:
        """Evalúa un nodo y retorna la relación resultante"""
        # Si ya lo evaluamos, usar cache
        node_id = id(node)
        if node_id in self.cache:
            return self.cache[node_id]

        # Marcar como ejecutando
        node.state = NodeState.EXECUTING

        try:
            result = self._eval_node(node)
            node.state = NodeState.EXECUTED
            node.result = result
            node.schema = result.header
            node.cardinality = result.cardinality()
            self.cache[node_id] = result
            return result
        except Exception as e:
            node.state = NodeState.ERROR
            node.error = str(e)
            raise
