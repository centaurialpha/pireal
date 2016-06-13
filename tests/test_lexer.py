import unittest
from src.core.interpreter import (
    lexer,
    scanner
)
from src.core.interpreter.token import (
    IDENTIFIER,
    ASSIGNMENT,
    GREATER,
    LESS,
    LESSEQUAL,
    GREATEREQUAL,
    NOTEQUAL,
    EQUAL,
    NUMBER,
    LPAREN,
    RPAREN,
    COMA,
    STRING,
    SEMI
)


class LexerTestCase(unittest.TestCase):

    def make_lexer(self, text):
        sc = scanner.Scanner(text)
        lex = lexer.Lexer(sc)
        return lex

    def test_number(self):
        lex = self.make_lexer("9282")
        token = lex.next_token()
        self.assertEqual(token.type, NUMBER)
        self.assertEqual(token.value, 9282)

    def test_paren(self):
        lex = self.make_lexer("()")
        tokens = (
            (LPAREN, '('),
            (RPAREN, ')')
        )
        for tkn_type, tkn_value in tokens:
            token = lex.next_token()
            self.assertEqual(token.type, tkn_type)
            self.assertEqual(token.value, tkn_value)

    def test_operators(self):
        lex = self.make_lexer("< > <> >= <= =")
        tokens = (
            (LESS, '<'),
            (GREATER, '>'),
            (NOTEQUAL, '<>'),
            (GREATEREQUAL, '>='),
            (LESSEQUAL, '<='),
            (EQUAL, '=')
        )
        for tkn_type, tkn_value in tokens:
            token = lex.next_token()
            self.assertEqual(token.type, tkn_type)
            self.assertEqual(token.value, tkn_value)

    def test_string(self):
        lex = self.make_lexer("'esto    es un  string'")
        token = lex.next_token()
        self.assertEqual(token.type, STRING)
        self.assertEqual(token.value, "'esto    es un  string'")

    def test_assignment(self):
        lex = self.make_lexer(":=")
        token = lex.next_token()
        self.assertEqual(token.type, ASSIGNMENT)
        self.assertEqual(token.value, ':=')

    def test_semi(self):
        lex = self.make_lexer(",")
        token = lex.next_token()
        self.assertEqual(token.type, COMA)
        self.assertEqual(token.value, ',')

    def test_semicolon(self):
        lex = self.make_lexer(";")
        token = lex.next_token()
        self.assertEqual(token.type, SEMI)
        self.assertEqual(token.value, ';')

    def test_tokens(self):
        sc = scanner.Scanner(("q1 := select id > 12 (people njoin skills);"
                              "q_2 := project name, age (q1);"))
        lex = lexer.Lexer(sc)
        tkn = lex.next_token()
        self.assertEqual(tkn.type, IDENTIFIER)
        tkn = lex.next_token()
        self.assertEqual(tkn.type, ASSIGNMENT)
        tkn = lex.next_token()
        self.assertEqual(tkn.type, 'KEYWORD')
        tkn = lex.next_token()
        self.assertEqual(tkn.type, IDENTIFIER)
        tkn = lex.next_token()
        self.assertEqual(tkn.type, GREATER)
        tkn = lex.next_token()
        self.assertEqual(tkn.type, NUMBER)
        tkn = lex.next_token()
        self.assertEqual(tkn.type, LPAREN)
        tkn = lex.next_token()
        self.assertEqual(tkn.type, IDENTIFIER)
        tkn = lex.next_token()
        self.assertEqual(tkn.type, 'KEYWORD')
        tkn = lex.next_token()
        self.assertEqual(tkn.type, IDENTIFIER)
        tkn = lex.next_token()
        self.assertEqual(tkn.type, RPAREN)
        tkn = lex.next_token()
        self.assertEqual(tkn.type, SEMI)
        tkn = lex.next_token()
        self.assertEqual(tkn.type, IDENTIFIER)
        tkn = lex.next_token()
        self.assertEqual(tkn.type, ASSIGNMENT)
        tkn = lex.next_token()
        self.assertEqual(tkn.type, 'KEYWORD')
        tkn = lex.next_token()
        self.assertEqual(tkn.type, IDENTIFIER)
        tkn = lex.next_token()
        self.assertEqual(tkn.type, COMA)
        tkn = lex.next_token()
        self.assertEqual(tkn.type, IDENTIFIER)
        tkn = lex.next_token()
        self.assertEqual(tkn.type, LPAREN)
        tkn = lex.next_token()
        self.assertEqual(tkn.type, IDENTIFIER)
        tkn = lex.next_token()
        self.assertEqual(tkn.type, RPAREN)
        tkn = lex.next_token()
        self.assertEqual(tkn.type, SEMI)


if __name__ == '__main__':
    unittest.main()
