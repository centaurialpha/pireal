import pytest
from pireal.interpreter import rast as ast

pytestmark = pytest.mark.interpreter


def test_node_visitor_generic_visit():
    visitor = ast.NodeVisitor()
    with pytest.raises(NotImplementedError, match="visit_Compound"):
        visitor.visit(ast.Compound())


def test_node_visitor_dispatches_correctly():
    class MyVisitor(ast.NodeVisitor):
        def visit_Compound(self, node):
            return "visited"

    visitor = MyVisitor()
    assert visitor.visit(ast.Compound()) == "visited"


def test_variable_value():
    from pireal.interpreter.tokens import Token, TokenTypes

    token = Token(type=TokenTypes.ID, value="personas", line=1, col=1)
    var = ast.Variable(token)
    assert var.value == "personas"
    assert var.lineno == 1
