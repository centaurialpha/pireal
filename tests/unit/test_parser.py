import datetime

import pytest

from pireal.interpreter.scanner import Scanner
from pireal.interpreter.lexer import Lexer, Token
from pireal.interpreter.parser import Parser
from pireal.interpreter import rast as ast
from pireal.interpreter.tokens import TokenTypes, BINARY_OPERATORS
from pireal.interpreter.exceptions import ConsumeError


def test_mix_boolean_expression():
    query = "name = 'gabox' or age >= 18 and age <= 30"
    parser = Parser(Lexer(Scanner(query)))

    node = parser.boolean_expression()

    expected_node = ast.BooleanExpression(
        left_formula=ast.BooleanExpression(
            left_formula=ast.Condition(
                ast.Variable(Token(TokenTypes.ID, "name")),
                Token(TokenTypes.EQUAL, "="),
                ast.String(Token(TokenTypes.STRING, "gabox")),
            ),
            operator=TokenTypes.OR,
            right_formula=ast.Condition(
                ast.Variable(Token(TokenTypes.ID, "age")),
                Token(TokenTypes.GEQUAL, ">="),
                ast.Number(Token(TokenTypes.INTEGER, 18)),
            ),
        ),
        operator=TokenTypes.AND,
        right_formula=ast.Condition(
            ast.Variable(Token(TokenTypes.ID, "age")),
            Token(TokenTypes.LEQUAL, "<="),
            ast.Number(Token(TokenTypes.INTEGER, 30)),
        ),
    )

    assert node == expected_node


def test_consume_error():
    query = "q := select id=1 (personas)"
    parser = Parser(Lexer(Scanner(query)))
    with pytest.raises(ConsumeError):
        parser.parse()

def test_consume_expression():
    query = "select id=1 (personas)"
    parser = Parser(Lexer(Scanner(query)))

    node = parser.expression()
    expected_node = ast.SelectExpr(
        cond=ast.Condition(
            op1=ast.Variable(Token(TokenTypes.ID, "id")),
            operator=Token(TokenTypes.EQUAL, "="),
            op2=ast.Number(Token(TokenTypes.INTEGER, 1))
        ),
        expr=ast.Variable(Token(TokenTypes.ID, "personas")),
    )

    assert node == expected_node


def test_consume_project():
    query = "project name,age (personas)"
    parser = Parser(Lexer(Scanner(query)))

    node = parser.expression()

    expected_node = ast.ProjectExpr(
        attrs=[
            ast.Variable(Token(TokenTypes.ID, "name")),
            ast.Variable(Token(TokenTypes.ID, "age")),
        ],
        expr=ast.Variable(Token(TokenTypes.ID, "personas"))
    )

    assert node == expected_node


def test_consume_nested_expression():
    query = "select id='1' (project name,age (personas))"
    parser = Parser(Lexer(Scanner(query)))

    node = parser.expression()

    expected_node = ast.SelectExpr(
        cond=ast.Condition(
            op1=ast.Variable(Token(TokenTypes.ID, "id")),
            operator=Token(TokenTypes.EQUAL, "="),
            op2=ast.String(Token(TokenTypes.STRING, '1')),
        ),
        expr=ast.ProjectExpr(
            attrs=[
                ast.Variable(Token(TokenTypes.ID, "name")),
                ast.Variable(Token(TokenTypes.ID, "age")),
            ],
            expr=ast.Variable(Token(TokenTypes.ID, "personas"))
        ),
    )

    assert node == expected_node


def test_consume_assignment():
    query = "q := personas"
    parser = Parser(Lexer(Scanner(query)))

    node = parser.assignment()

    expected_node = ast.Assignment(
        rname=ast.Variable(Token(TokenTypes.ID, "q")),
        query=ast.Variable(Token(TokenTypes.ID, "personas"))
    )

    assert node == expected_node
