import unittest
from src.core.interpreter import (
    lexer,
    scanner
)
from src.core.interpreter.token import (
    IDENTIFIER,
    ASSIGNMENT,
    GREATER,
    NUMBER,
    LPAREN,
    RPAREN,
    COMA,
    STRING,
    SEMI
)


class LexerTestCase(unittest.TestCase):

    def test_string_token(self):
        sc = scanner.Scanner("'test    string'")
        lex = lexer.Lexer(sc)
        tkn = lex.next_token()
        self.assertEqual(tkn.type, STRING)

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
