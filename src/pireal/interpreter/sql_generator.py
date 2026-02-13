from pireal.interpreter import rast as ast
from pireal.interpreter.tokens import TokenTypes

OPERATOR_MAP = {
    TokenTypes.EQUAL: "=",
    TokenTypes.NOTEQUAL: "!=",
    TokenTypes.LESS: "<",
    TokenTypes.LESS_EQUAL: "<=",
    TokenTypes.GREATER: ">",
    TokenTypes.GREATHER_EQUAL: ">=",
}

BINARY_OP_MAP = {
    TokenTypes.UNION: "UNION",
    TokenTypes.INTERSECT: "INTERSECT",
    TokenTypes.DIFFERENCE: "EXCEPT",
    TokenTypes.PRODUCT: "CROSS JOIN",
    TokenTypes.NJOIN: "NATURAL JOIN",
    TokenTypes.LEFT_OUTER_JOIN: "LEFT OUTER JOIN",
    TokenTypes.RIGHT_OUTER_JOIN: "RIGHT OUTER JOIN",
    TokenTypes.FULL_OUTER_JOIN: "FULL OUTER JOIN",
}


class SQLGenerator(ast.NodeVisitor):
    def __init__(self, tree):
        self.tree = tree
        self.queries: dict[str, str] = {}

    def generate(self) -> dict[str, str]:
        self.visit(self.tree)
        return self.queries

    def visit_Compound(self, node):
        for child in node.children:
            self.visit(child)

    def visit_Assignment(self, node):
        name = node.rname.value
        sql = self.visit(node.query)
        self.queries[name] = sql

    def visit_Variable(self, node):
        return node.value

    def visit_Number(self, node):
        return str(node.num)

    def visit_String(self, node):
        return f"'{node.string}'"

    def visit_Date(self, node):
        return f"'{node.date}'"

    def visit_Time(self, node):
        return f"'{node.time}'"

    def visit_Condition(self, node):
        op1 = self.visit(node.op1)
        op = OPERATOR_MAP[node.operator.type]
        op2 = self.visit(node.op2)
        return f"{op1} {op} {op2}"

    def visit_BooleanExpression(self, node):
        left = self.visit(node.left_formula)
        op = "AND" if node.operator == TokenTypes.AND else "OR"
        right = self.visit(node.right_formula)
        return f"{left} {op} {right}"

    def visit_SelectExpr(self, node):
        condition = self.visit(node.condition)
        source = self.visit(node.expr)
        return f"SELECT * FROM {source} WHERE {condition}"

    def visit_ProjectExpr(self, node):
        attrs = ", ".join(self.visit(a) for a in node.attrs)
        source = self.visit(node.expr)
        # Si el source ya es un SELECT, lo envolvemos
        if source.startswith("SELECT"):
            return f"SELECT {attrs} FROM ({source})"
        return f"SELECT {attrs} FROM {source}"

    def visit_BinaryOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        op = BINARY_OP_MAP[node.op]

        if node.op in (TokenTypes.UNION, TokenTypes.INTERSECT, TokenTypes.DIFFERENCE):
            return f"{left}\n{op}\n{right}"

        # Para joins, si alguno es subquery lo envolvemos
        if left.startswith("SELECT"):
            left = f"({left})"
        if right.startswith("SELECT"):
            right = f"({right})"
        return f"{left} {op} {right}"
