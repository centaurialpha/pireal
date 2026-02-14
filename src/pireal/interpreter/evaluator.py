from pireal.core.relation import Relation
from pireal.interpreter import rast as ast
from pireal.interpreter.exceptions import DuplicateRelationNameError
from pireal.interpreter.tokens import TokenTypes

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
}


class UndefinedRelationError(Exception):
    def __init__(self, name: str, lineno: int | None = None):
        super().__init__(f"Relation '{name}' is not defined")
        self.name = name
        self.lineno = lineno


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
            raise UndefinedRelationError(name, lineno=node.lineno)
        return relation

    def visit_BinaryOp(self, node: ast.BinaryOp) -> Relation:
        left = self.visit(node.left)
        right = self.visit(node.right)
        op_name = BINARY_OP_MAP[node.op]
        return getattr(left, op_name)(right)

    def visit_ProjectExpr(self, node: ast.ProjectExpr) -> Relation:
        relation = self.visit(node.expr)
        attrs = [attr.value for attr in node.attrs]
        return relation.project(*attrs)

    def visit_SelectExpr(self, node: ast.SelectExpr) -> Relation:
        relation = self.visit(node.expr)
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
