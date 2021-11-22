import unittest
import datetime

from pireal.interpreter.lexer import (
    Lexer,
    Token,
)
from pireal.interpreter.exceptions import InvalidSyntaxError
from pireal.interpreter.tokens import TokenTypes
from pireal.interpreter.scanner import Scanner


class LexerTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def test_get_number(self):
        numbers = ['28', '3.14156', '111111', '1.33']
        expected_tokens = [
            Token(TokenTypes.INTEGER, 28),
            Token(TokenTypes.REAL, 3.14156),
            Token(TokenTypes.INTEGER, 111111),
            Token(TokenTypes.REAL, 1.33),
        ]

        for number, expected_token in zip(numbers, expected_tokens):
            with self.subTest(number=number):
                lex = Lexer(Scanner(number))
                current_token = lex.get_number()

                self.assertEqual(current_token, expected_token)

    def test_next_token(self):
        text = (
            '% comentario\n'
            '; , < > ( ) ='  # single characters
            '<= >= <> :='
            'query_1234 qqq '
            'select project product intersect union difference njoin louter router fouter '
            'and or '
            '1234 22.22 '
            '\'gabox\' \'20/01/1991\' \'15:15\''
        )
        lex = Lexer(Scanner(text))
        expected_tokens = (
            Token(TokenTypes.SEMI, ';'),
            Token(TokenTypes.COMMA, ','),
            Token(TokenTypes.LESS, '<'),
            Token(TokenTypes.GREATER, '>'),
            Token(TokenTypes.LPAREN, '('),
            Token(TokenTypes.RPAREN, ')'),
            Token(TokenTypes.EQUAL, '='),
            Token(TokenTypes.LEQUAL, '<='),
            Token(TokenTypes.GEQUAL, '>='),
            Token(TokenTypes.NOTEQUAL, '<>'),
            Token(TokenTypes.ASSIGNMENT, ':='),
            Token(TokenTypes.ID, 'query_1234'),
            Token(TokenTypes.ID, 'qqq'),
            Token(TokenTypes.SELECT, 'select'),
            Token(TokenTypes.PROJECT, 'project'),
            Token(TokenTypes.PRODUCT, 'product'),
            Token(TokenTypes.INTERSECT, 'intersect'),
            Token(TokenTypes.UNION, 'union'),
            Token(TokenTypes.DIFFERENCE, 'difference'),
            Token(TokenTypes.NJOIN, 'njoin'),
            Token(TokenTypes.LEFT_OUTER_JOIN, 'louter'),
            Token(TokenTypes.RIGHT_OUTER_JOIN, 'router'),
            Token(TokenTypes.FULL_OUTER_JOIN, 'fouter'),
            Token(TokenTypes.AND, 'and'),
            Token(TokenTypes.OR, 'or'),
            Token(TokenTypes.INTEGER, 1234),
            Token(TokenTypes.REAL, 22.22),
            Token(TokenTypes.STRING, 'gabox'),
            Token(TokenTypes.DATE, datetime.date(day=20, month=1, year=1991)),
            Token(TokenTypes.TIME, datetime.time(hour=15, minute=15)),
            Token(TokenTypes.EOF, None),
        )

        for expected_token in expected_tokens:
            with self.subTest(token=expected_token):
                current_token = lex.next_token()
                self.assertEqual(current_token, expected_token)

    def test_syntax_error(self):
        lex = Lexer(Scanner('12 / id * 2'))
        lex.next_token()
        with self.assertRaises(InvalidSyntaxError):
            lex.next_token()

    def test_get_identifier_or_keyword(self):
        keywords_and_ids = [
            'id',
            'hola_como_estas',
            'select',
            'query_123',
        ]
        expected_tokens = [
            Token(TokenTypes.ID, 'id'),
            Token(TokenTypes.ID, 'hola_como_estas'),
            Token(TokenTypes.SELECT, 'select'),
            Token(TokenTypes.ID, 'query_123'),
        ]
        for word, expected_token in zip(keywords_and_ids, expected_tokens):
            with self.subTest(identifier=word):
                lex = Lexer(Scanner(word))
                token = lex.get_identifier_or_keyword()

                self.assertEqual(token, expected_token)
