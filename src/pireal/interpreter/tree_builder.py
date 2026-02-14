from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto

from pireal.interpreter import rast as ast
from pireal.interpreter.tokens import TokenTypes

BINARY_OP_SYMBOLS = {
    TokenTypes.NJOIN: "⋈",
    TokenTypes.LOUTER: "⟕",
    TokenTypes.ROUTER: "⟖",
    TokenTypes.FOUTER: "⟗",
    TokenTypes.UNION: "∪",
    TokenTypes.INTERSECT: "∩",
    TokenTypes.DIFFERENCE: "−",
    TokenTypes.PRODUCT: "×",
}

COMPARISON_SYMBOLS = {
    TokenTypes.EQUAL: "=",
    TokenTypes.NOTEQUAL: "≠",
    TokenTypes.LESS: "<",
    TokenTypes.LESS_EQUAL: "≤",
    TokenTypes.GREATER: ">",
    TokenTypes.GREATER_EQUAL: "≥",
}


class NodeKind(Enum):
    ASSIGNMENT = auto()  # resultado := ...
    UNARY_OP = auto()  # σ, π
    BINARY_OP = auto()  # ⋈, ∪, −, etc.
    RELATION = auto()  # hoja — nombre de relación
    CONDITION = auto()  # la condición dentro de σ


@dataclass
class TreeNode:
    label: str
    kind: NodeKind = NodeKind.RELATION
    children: list[TreeNode] = field(default_factory=list)


class TreeBuilder(ast.NodeVisitor):
    def build(self, tree: ast.Compound) -> list[TreeNode]:
        return [self.visit(child) for child in tree.children]

    def visit_Assignment(self, node: ast.Assignment) -> TreeNode:
        child = self.visit(node.query)
        return TreeNode(label=node.rname.value, kind=NodeKind.ASSIGNMENT, children=[child])

    def visit_SelectExpr(self, node: ast.SelectExpr) -> TreeNode:
        condition = self.visit(node.condition)
        expr = self.visit(node.expr)
        return TreeNode(label=f"σ ({condition.label})", kind=NodeKind.UNARY_OP, children=[expr])

    def visit_ProjectExpr(self, node: ast.ProjectExpr) -> TreeNode:
        attrs = ", ".join(a.value for a in node.attrs)
        expr = self.visit(node.expr)
        return TreeNode(label=f"π {attrs}", kind=NodeKind.UNARY_OP, children=[expr])

    def visit_BinaryOp(self, node: ast.BinaryOp) -> TreeNode:
        symbol = BINARY_OP_SYMBOLS[node.op]
        left = self.visit(node.left)
        right = self.visit(node.right)
        return TreeNode(label=symbol, kind=NodeKind.BINARY_OP, children=[left, right])

    def visit_Variable(self, node: ast.Variable) -> TreeNode:
        return TreeNode(label=node.value)

    def visit_Condition(self, node: ast.Condition) -> TreeNode:
        op1 = self.visit(node.op1)
        op = COMPARISON_SYMBOLS.get(node.operator.type, node.operator.value)
        op2 = self.visit(node.op2)
        return TreeNode(label=f"{op1.label} {op} {op2.label}", kind=NodeKind.CONDITION)

    def visit_BooleanExpression(self, node: ast.BooleanExpression) -> TreeNode:
        left = self.visit(node.left_formula)
        op = "∧" if node.operator == TokenTypes.AND else "∨"
        right = self.visit(node.right_formula)
        return TreeNode(label=f"{left.label} {op} {right.label}")

    def visit_Number(self, node: ast.Number) -> TreeNode:
        return TreeNode(label=str(node.value))

    def visit_String(self, node: ast.String) -> TreeNode:
        return TreeNode(label=f"'{node.value}'")

    def visit_Date(self, node: ast.Date) -> TreeNode:
        return TreeNode(label=str(node.value))

    def visit_Time(self, node: ast.Time) -> TreeNode:
        return TreeNode(label=str(node.value))
