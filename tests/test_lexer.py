# -*- coding: utf-8 -*-
#
# Copyright 2015-2016 - Gabriel Acosta <acostadariogabriel@gmail.com>
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

import unittest
from src.core.interpreter import (
    lexer,
    scanner
)
from src.core.interpreter.tokens import (
    ID,
    GREATER,
    LESS,
    LEQUAL,
    GEQUAL,
    NOTEQUAL,
    EQUAL,
    NUMBER,
    LPAREN,
    RPAREN,
    SEMI,
    STRING,
    SEMICOLON,
    PROJECT,
    SELECT,
    NJOIN,
    EOF
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
            (GEQUAL, '>='),
            (LEQUAL, '<='),
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
        self.assertEqual(token.value, "esto    es un  string")

    def test_semi(self):
        lex = self.make_lexer(",")
        token = lex.next_token()
        self.assertEqual(token.type, SEMI)
        self.assertEqual(token.value, ',')

    def test_semicolon(self):
        lex = self.make_lexer(";")
        token = lex.next_token()
        self.assertEqual(token.type, SEMICOLON)
        self.assertEqual(token.value, ';')

    def test_tokens(self):
        lex = self.make_lexer("project name, age (select id=2 (p njoin q));")
        tkn = lex.next_token()
        self.assertEqual(PROJECT, tkn.type)
        self.assertEqual('project', tkn.value)
        tkn = lex.next_token()
        self.assertEqual(ID, tkn.type)
        self.assertEqual('name', tkn.value)
        tkn = lex.next_token()
        self.assertEqual(SEMI, tkn.type)
        self.assertEqual(',', tkn.value)
        tkn = lex.next_token()
        self.assertEqual(ID, tkn.type)
        self.assertEqual('age', tkn.value)
        tkn = lex.next_token()
        self.assertEqual(LPAREN, tkn.type)
        self.assertEqual('(', tkn.value)
        tkn = lex.next_token()
        self.assertEqual(SELECT, tkn.type)
        self.assertEqual('select', tkn.value)
        tkn = lex.next_token()
        self.assertEqual(ID, tkn.type)
        self.assertEqual('id', tkn.value)
        tkn = lex.next_token()
        self.assertEqual(EQUAL, tkn.type)
        self.assertEqual('=', tkn.value)
        tkn = lex.next_token()
        self.assertEqual(NUMBER, tkn.type)
        self.assertEqual(2, tkn.value)
        tkn = lex.next_token()
        self.assertEqual(LPAREN, tkn.type)
        self.assertEqual('(', tkn.value)
        tkn = lex.next_token()
        self.assertEqual(ID, tkn.type)
        self.assertEqual('p', tkn.value)
        tkn = lex.next_token()
        self.assertEqual(NJOIN, tkn.type)
        self.assertEqual('njoin', tkn.value)
        tkn = lex.next_token()
        self.assertEqual(ID, tkn.type)
        self.assertEqual('q', tkn.value)
        tkn = lex.next_token()
        self.assertEqual(RPAREN, tkn.type)
        self.assertEqual(')', tkn.value)
        tkn = lex.next_token()
        self.assertEqual(RPAREN, tkn.type)
        self.assertEqual(')', tkn.value)
        tkn = lex.next_token()
        self.assertEqual(SEMICOLON, tkn.type)
        self.assertEqual(';', tkn.value)
        tkn = lex.next_token()
        self.assertEqual(EOF, tkn.type)
        self.assertEqual(None, tkn.value)

if __name__ == '__main__':
    unittest.main()
