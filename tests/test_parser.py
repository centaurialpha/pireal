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
from src.core import relation


class ParserTestCase(unittest.TestCase):

    def test_parse(self):
        """
        r = relation.Relation()
        r.header = ['id', 'name']
        for i in {('1', 'gabo'), ('22', 'mechi')}:
            r.insert(i)

        r2 = relation.Relation()
        r2.header = ['id', 'skill']
        for i in {('22', 'rocas'), ('1', 'Python')}:
            r2.insert(i)

        relas = {'p': r, 'q': r2}
        """
        sc = scanner.Scanner("project name, id (people);")
        lex = lexer.Lexer(sc)
        par = parser.Parser(lex)
        tree = par.parse()
        print(tree)
