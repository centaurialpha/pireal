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
