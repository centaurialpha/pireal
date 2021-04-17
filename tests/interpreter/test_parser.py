import pytest
from unittest import (
    TestCase,
    mock,
)

from pireal.interpreter.scanner import Scanner
from pireal.interpreter.lexer import Lexer, Token
from pireal.interpreter.parser import Parser
from pireal.interpreter import rast as ast
from pireal.interpreter.tokens import TokenTypes
from pireal.interpreter.exceptions import ConsumeError


class ParserTestCase(TestCase):

    def test_compound(self):
        query = 'query := q1 njoin q2; qq := query njoin otro;'
        parser = Parser(Lexer(Scanner(query)))

        node = parser.compound()

        self.assertIsInstance(node, ast.Compound)
        self.assertEqual(len(node.children), 2)

    def test_assignment(self):
        query = 'q := project name (r);'
        parser = Parser(Lexer(Scanner(query)))

        with mock.patch.multiple(
            parser,
            consume=mock.DEFAULT,
            expression=mock.DEFAULT,
        ) as mocks:
            node = parser.assignment()

        self.assertEqual(mocks['consume'].call_count, 3)
        self.assertIsInstance(node, ast.Assignment)

    def test_expression_binary(self):
        query = 'q1 njoin q2'
        parser = Parser(Lexer(Scanner(query)))

        node = parser.expression()

        self.assertIsInstance(node, ast.BinaryOp)

    def test_nested_expression(self):
        query = 'select id = 1 (project name, id (q1))'
        parser = Parser(Lexer(Scanner(query)))

        node = parser.expression()

        self.assertIsInstance(node, ast.SelectExpr)
        self.assertIsInstance(node.expr, ast.ProjectExpr)

    def test_attributes(self):
        query = 'id, name, age, attr1, attr2'
        parser = Parser(Lexer(Scanner(query)))

        node = parser.attributes()

        self.assertIsInstance(node, list)
        self.assertEqual(len(node), 5)
        for attr_node in node:
            self.assertIsInstance(attr_node, ast.Variable)

    def test_condition(self):
        queries = (
            'algo > algo2',
            '(algo < algo2)',
        )
        for query in queries:
            parser = Parser(Lexer(Scanner(query)))

            node = parser.condition()

            self.assertIsInstance(node, ast.Condition)

    def test_consume(self):
        query = 'q1 :='
        parser = Parser(Lexer(Scanner(query)))

        parser.consume(TokenTypes.ID)
        with self.assertRaises(ConsumeError):
            parser.consume(TokenTypes.SELECT)
        parser.consume(TokenTypes.ASSIGNMENT)


class SelectExpressionTestCase(TestCase):

    def test_simple(self):
        query = 'select id = 1 (q)'
        parser = Parser(Lexer(Scanner(query)))

        node = parser.select_expression()

        self.assertIsInstance(node, ast.SelectExpr)

    def test_and_operator(self):
        query = 'select id = 1 and age = 20 (q)'
        parser = Parser(Lexer(Scanner(query)))

        node = parser.select_expression()

        self.assertIsInstance(node, ast.SelectExpr)
        self.assertEqual(len(node.condition.conditions), 2)
        self.assertEqual(node.condition.ops, ['and'])

    def test_or_operator(self):
        query = 'select id = 1 or age = 20 (q)'
        parser = Parser(Lexer(Scanner(query)))

        node = parser.select_expression()

        self.assertIsInstance(node, ast.SelectExpr)
        self.assertEqual(len(node.condition.conditions), 2)
        self.assertEqual(node.condition.ops, ['or'])


class ProjectExpressionTestCase(TestCase):

    def test_simple(self):
        query = 'project name (algo)'
        parser = Parser(Lexer(Scanner(query)))

        node = parser.project_expression()

        self.assertIsInstance(node, ast.ProjectExpr)
        self.assertEqual(len(node.attrs), 1)

    def test_multiple_attributes(self):
        query = 'project name, id, age (algo)'
        parser = Parser(Lexer(Scanner(query)))

        expected_attrs = ['name', 'id', 'age']

        node = parser.project_expression()

        self.assertIsInstance(node, ast.ProjectExpr)
        for index, expected_attr in enumerate(expected_attrs):
            self.assertEqual(node.attrs[index].token.value, expected_attr)

