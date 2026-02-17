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

import datetime

import pytest

from pireal.interpreter.scanner import Scanner
from pireal.interpreter.lexer import Lexer, Token
from pireal.interpreter.parser import Parser
from pireal.interpreter import rast as ast
from pireal.interpreter.tokens import TokenTypes
from pireal.interpreter.exceptions import ConsumeError

pytestmark = pytest.mark.interpreter


@pytest.fixture
def make_parser():
    def _make(query: str) -> Parser:
        return Parser(Lexer(Scanner(query)))

    return _make


def test_boolean_expression_with_and_or(make_parser):
    node = make_parser("name = 'gabox' or age >= 18 and age <= 30").boolean_expression()

    expected = ast.BooleanExpression(
        left_formula=ast.BooleanExpression(
            left_formula=ast.Condition(
                ast.Variable(Token(TokenTypes.ID, "name")),
                Token(TokenTypes.EQUAL, "="),
                ast.String("gabox"),
            ),
            operator=TokenTypes.OR,
            right_formula=ast.Condition(
                ast.Variable(Token(TokenTypes.ID, "age")),
                Token(TokenTypes.GREATER_EQUAL, ">="),
                ast.Number(18),
            ),
        ),
        operator=TokenTypes.AND,
        right_formula=ast.Condition(
            ast.Variable(Token(TokenTypes.ID, "age")),
            Token(TokenTypes.LESS_EQUAL, "<="),
            ast.Number(30),
        ),
    )
    assert node == expected


def test_expression_select(make_parser):
    node = make_parser("select id=1 (personas)").expression()

    expected = ast.SelectExpr(
        condition=ast.Condition(
            op1=ast.Variable(Token(TokenTypes.ID, "id")),
            operator=Token(TokenTypes.EQUAL, "="),
            op2=ast.Number(1),
        ),
        expr=ast.Variable(Token(TokenTypes.ID, "personas")),
    )
    assert node == expected


def test_expression_project(make_parser):
    node = make_parser("project name,age (personas)").expression()

    expected = ast.ProjectExpr(
        attrs=[
            ast.Variable(Token(TokenTypes.ID, "name")),
            ast.Variable(Token(TokenTypes.ID, "age")),
        ],
        expr=ast.Variable(Token(TokenTypes.ID, "personas")),
    )
    assert node == expected


def test_expression_nested(make_parser):
    node = make_parser("select id='1' (project name,age (personas))").expression()

    expected = ast.SelectExpr(
        condition=ast.Condition(
            op1=ast.Variable(Token(TokenTypes.ID, "id")),
            operator=Token(TokenTypes.EQUAL, "="),
            op2=ast.String("1"),
        ),
        expr=ast.ProjectExpr(
            attrs=[
                ast.Variable(Token(TokenTypes.ID, "name")),
                ast.Variable(Token(TokenTypes.ID, "age")),
            ],
            expr=ast.Variable(Token(TokenTypes.ID, "personas")),
        ),
    )
    assert node == expected


@pytest.mark.parametrize(
    "token_type",
    [
        TokenTypes.NJOIN,
        TokenTypes.UNION,
        TokenTypes.INTERSECT,
        TokenTypes.PRODUCT,
        TokenTypes.DIFFERENCE,
    ],
)
def test_expression_binary_op(make_parser, token_type):
    node = make_parser(f"(personas {token_type.value} salarios)").expression()

    expected = ast.BinaryOp(
        left=ast.Variable(Token(TokenTypes.ID, "personas")),
        op=token_type,
        right=ast.Variable(Token(TokenTypes.ID, "salarios")),
    )
    assert node == expected


def test_assignment(make_parser):
    node = make_parser("q := personas").assignment()

    expected = ast.Assignment(
        rname=ast.Variable(Token(TokenTypes.ID, "q")),
        query=ast.Variable(Token(TokenTypes.ID, "personas")),
    )
    assert node == expected


@pytest.mark.parametrize(
    "text, expected",
    [
        ("12", ast.Number(12)),
        ("12.3", ast.Number(12.3)),
        ("'hola'", ast.String("hola")),
        ("'20/01/1991'", ast.Date(datetime.date(1991, 1, 20))),
        ("'12:30'", ast.Time(datetime.time(12, 30))),
    ],
)
def test_literal(make_parser, text, expected):
    node = make_parser(text).literal()
    assert node == expected


def test_compound(make_parser):
    node = make_parser("q:=select id=1 (p);").compound()

    expected = ast.Compound(
        children=[
            ast.Assignment(
                rname=ast.Variable(Token(TokenTypes.ID, "q")),
                query=ast.SelectExpr(
                    condition=ast.Condition(
                        op1=ast.Variable(Token(TokenTypes.ID, "id")),
                        operator=Token(TokenTypes.EQUAL, "="),
                        op2=ast.Number(1),
                    ),
                    expr=ast.Variable(Token(TokenTypes.ID, "p")),
                ),
            )
        ]
    )
    assert node == expected


def test_consume_error(make_parser):
    with pytest.raises(ConsumeError):
        make_parser("q := select id=1 (personas)").parse()
