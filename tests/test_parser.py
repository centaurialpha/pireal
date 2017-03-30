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
    parser,
    scanner,
    lexer
)
# TODO: terminar los tests


class ParserTestCase(unittest.TestCase):

    def setUp(self):
        sc = scanner.Scanner("q1 := select id=2 (p);")
        lex = lexer.Lexer(sc)
        self.parser = parser.Parser(lex)

    def test_compound(self):
        node = self.parser._compound()
        self.assertIsInstance(node, parser.Compound)
        self.assertIsInstance(node.children, list)

    def test_assignment(self):
        node = self.parser._assignment()
        self.assertIsInstance(node, parser.Assignment)


if __name__ == '__main__':
    unittest.main()
