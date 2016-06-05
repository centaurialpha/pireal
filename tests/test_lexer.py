import unittest
from src.core.interpreter import lexer
from src.core.interpreter.token import (
    IDENTIFIER,
    ASSIGNMENT,
    GREATER,
    NUMBER,
    LPAREN,
    RPAREN,
    COMA,
    STRING
)


class LexerTestCase(unittest.TestCase):

    def test_next(self):
        lex = lexer.Lexer("hola\na todos !")
        self.assertEqual(lex.char, 'h')
        for i in range(5):
            lex.next()
        self.assertEqual(lex.char, 'a')

    def test_position(self):
        lex = lexer.Lexer("\n\n\n      gabo")
        lex.next()
        lex.next()
        self.assertEqual(lex.lineno, 3)
        self.assertEqual(lex.colno, 0)
        for i in range(8):
            lex.next()
        self.assertEqual(lex.colno, 8)

    def test_string_token(self):
        lex = lexer.Lexer("'test     string'")
        tkn = lex.next_token()
        self.assertEqual(tkn.type, STRING)

    def test_tokens(self):
        lex = lexer.Lexer(("q := select id > 12 (people njoin skills)"
                           "qq := project name, age (q)"))
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


if __name__ == '__main__':
    unittest.main()
