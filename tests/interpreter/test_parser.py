import unittest
import datetime

from pireal.interpreter.scanner import Scanner
from pireal.interpreter.lexer import Lexer, Token
from pireal.interpreter.parser import Parser
from pireal.interpreter import rast as ast
from pireal.interpreter.tokens import TokenTypes, BINARY_OPERATORS
from pireal.interpreter.exceptions import ConsumeError


class ParserTestCase(unittest.TestCase):

    def test_compound(self):
        query = 'q := qq; q2 := qqq;'
        parser = Parser(Lexer(Scanner(query)))

        node = parser.compound()

        self.assertIsInstance(node, ast.Compound)
        self.assertEqual(len(node.children), 2)

    def test_assignment(self):
        query = 'q:=qq;'
        parser = Parser(Lexer(Scanner(query)))

        node = parser.assignment()

        expected_node = ast.Assignment(
            rname=ast.Variable(Token(TokenTypes.ID, 'q')),
            query=ast.Variable(Token(TokenTypes.ID, 'qq'))
        )

        self.assertEqual(node.rname, expected_node.rname)
        self.assertEqual(node.query, expected_node.query)

    def test_binary_expression(self):
        query = 'q1 njoin q2'
        queries = ['q1 {} q2'.format(op.value) for op in BINARY_OPERATORS.values()]

        for query, op in zip(queries, BINARY_OPERATORS.values()):
            parser = Parser(Lexer(Scanner(query)))
            node = parser.expression()

            expected_node = ast.BinaryOp(
                left=ast.Variable(Token(TokenTypes.ID, 'q1')),
                op=op,
                right=ast.Variable(Token(TokenTypes.ID, 'q2'))
            )

            self.assertEqual(node, expected_node)

    def test_nested_binary_expression(self):
        query = 'q1 njoin (project id, name(q))'
        parser = Parser(Lexer(Scanner(query)))

        node = parser.expression()

        expected_node = ast.BinaryOp(
            left=ast.Variable(Token(TokenTypes.ID, 'q1')),
            op=TokenTypes.NJOIN,
            right=ast.ProjectExpr(
                attrs=[
                    ast.Variable(Token(TokenTypes.ID, 'id')),
                    ast.Variable(Token(TokenTypes.ID, 'name'))
                ],
                expr=ast.Variable(Token(TokenTypes.ID, 'q'))
            )
        )

        self.assertEqual(node, expected_node)

    # def test_nested_expression(self):
    #     query = 'select id = 1 (project name, id (q1))'
    #     parser = Parser(Lexer(Scanner(query)))

    #     node = parser.expression()

    #     self.assertIsInstance(node, ast.SelectExpr)
    #     self.assertIsInstance(node.expr, ast.ProjectExpr)

    def test_literal(self):
        queries = ['1', '3.14', '"20/01/1991"', '"14:14"', '"hola como estas"']
        expected_nodes = [
            ast.Number(Token(TokenTypes.INTEGER, 1)),
            ast.Number(Token(TokenTypes.REAL, 3.14)),
            ast.Date(Token(TokenTypes.DATE, datetime.date(1991, 1, 20))),
            ast.Time(Token(TokenTypes.TIME, datetime.time(14, 14))),
            ast.String(Token(TokenTypes.STRING, "hola como estas")),
        ]

        for query, expected_node in zip(queries, expected_nodes):
            parser = Parser(Lexer(Scanner(query)))

            node = parser.literal()

            self.assertEqual(node, expected_node)

    def test_operand(self):
        queries = ['3.14', 'query_1234']
        expected_nodes = [
            ast.Number(Token(TokenTypes.REAL, 3.14)),
            ast.Variable(Token(TokenTypes.ID, 'query_1234')),
        ]

        for query, expected_node in zip(queries, expected_nodes):
            parser = Parser(Lexer(Scanner(query)))

            node = parser.operand()

            self.assertEqual(node, expected_node)

    def test_attributes(self):
        query = 'id, name, age, attr1, attr2'
        parser = Parser(Lexer(Scanner(query)))

        node = parser.attributes()

        expected_nodes = [
            ast.Variable(Token(TokenTypes.ID, 'id')),
            ast.Variable(Token(TokenTypes.ID, 'name')),
            ast.Variable(Token(TokenTypes.ID, 'age')),
            ast.Variable(Token(TokenTypes.ID, 'attr1')),
            ast.Variable(Token(TokenTypes.ID, 'attr2')),
        ]

        self.assertListEqual(node, expected_nodes)

    def test_simple_boolean_expression(self):
        query = 'id <= 13'
        parser = Parser(Lexer(Scanner(query)))

        node = parser.boolean_expression()

        expected_node = ast.Condition(
            ast.Variable(Token(TokenTypes.ID, 'id')),
            Token(TokenTypes.LEQUAL, '<='),
            ast.Number(Token(TokenTypes.INTEGER, 13))
        )

        self.assertEqual(node, expected_node)

    def test_and_boolean_expression(self):
        query = 'age > 30 and age < 40'
        parser = Parser(Lexer(Scanner(query)))

        node = parser.boolean_expression()

        expected_node = ast.BooleanExpression(
            left_formula=ast.Condition(
                ast.Variable(Token(TokenTypes.ID, 'age')),
                Token(TokenTypes.GREATER, '>'),
                ast.Number(Token(TokenTypes.INTEGER, 30))
            ),
            operator=TokenTypes.AND,
            right_formula=ast.Condition(
                ast.Variable(Token(TokenTypes.ID, 'age')),
                Token(TokenTypes.LESS, '<'),
                ast.Number(Token(TokenTypes.INTEGER, 40))
            )
        )

        self.assertEqual(node, expected_node)

    def test_mix_boolean_expression(self):
        query = 'name = "gabox" or age >= 18 and age <= 30'
        parser = Parser(Lexer(Scanner(query)))

        node = parser.boolean_expression()

        expected_node = ast.BooleanExpression(
            left_formula=ast.BooleanExpression(
                left_formula=ast.Condition(
                    ast.Variable(Token(TokenTypes.ID, 'name')),
                    Token(TokenTypes.EQUAL, '='),
                    ast.String(Token(TokenTypes.STRING, 'gabox'))
                ),
                operator=TokenTypes.OR,
                right_formula=ast.Condition(
                    ast.Variable(Token(TokenTypes.ID, 'age')),
                    Token(TokenTypes.GEQUAL, '>='),
                    ast.Number(Token(TokenTypes.INTEGER, 18))
                )
            ),
            operator=TokenTypes.AND,
            right_formula=ast.Condition(
                ast.Variable(Token(TokenTypes.ID, 'age')),
                Token(TokenTypes.LEQUAL, '<='),
                ast.Number(Token(TokenTypes.INTEGER, 30))
            )
        )

        self.assertEqual(node, expected_node)

    def test_consume(self):
        query = 'q1 :='
        parser = Parser(Lexer(Scanner(query)))

        parser.consume(TokenTypes.ID)
        with self.assertRaises(ConsumeError):
            parser.consume(TokenTypes.SELECT)
        parser.consume(TokenTypes.ASSIGNMENT)


class SelectExpressionTestCase(unittest.TestCase):

    def test_simple(self):
        query = 'select id = 1 (q)'
        parser = Parser(Lexer(Scanner(query)))

        node = parser.select_expression()

        expected_node = ast.SelectExpr(
            cond=ast.Condition(
                ast.Variable(Token(TokenTypes.ID, 'id')),
                Token(TokenTypes.EQUAL, '='),
                ast.Number(Token(TokenTypes.INTEGER, 1))
            ),
            expr=ast.Variable(Token(TokenTypes.ID, 'q'))
        )
        self.assertEqual(node, expected_node)

    # def test_and_operator(self):
    #     query = 'select id = 1 and age = 20 (q)'
    #     parser = Parser(Lexer(Scanner(query)))

    #     node = parser.select_expression()

    #     self.assertIsInstance(node, ast.SelectExpr)
    #     self.assertEqual(len(node.condition.conditions), 2)
    #     self.assertEqual(node.condition.ops, ['and'])

    # def test_or_operator(self):
    #     query = 'select id = 1 or age = 20 (q)'
    #     parser = Parser(Lexer(Scanner(query)))

    #     node = parser.select_expression()

    #     self.assertIsInstance(node, ast.SelectExpr)
    #     self.assertEqual(len(node.condition.conditions), 2)
    #     self.assertEqual(node.condition.ops, ['or'])


@unittest.skip
class ProjectExpressionTestCase(unittest.TestCase):

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
