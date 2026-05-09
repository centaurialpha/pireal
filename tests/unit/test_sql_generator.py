# Copyright 2015-2026 - Gabriel Acosta <acostadariogabriel@gmail.com>
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

import pytest

from pireal.interpreter.lexer import Lexer
from pireal.interpreter.parser import Parser
from pireal.interpreter.scanner import Scanner
from pireal.interpreter.sql_generator import SQLGenerator

pytestmark = pytest.mark.interpreter


def _generate(query: str) -> dict:
    tree = Parser(Lexer(Scanner(query))).parse()
    return SQLGenerator(tree).generate()


@pytest.mark.parametrize(
    "query, expected",
    [
        (
            "q := select id=1 (personas);",
            "SELECT * FROM personas WHERE id = 1",
        ),
        (
            "q := project name, age (personas);",
            "SELECT name, age FROM personas",
        ),
        (
            "q := personas union salarios;",
            "personas\nUNION\nsalarios",
        ),
        (
            "q := personas intersect salarios;",
            "personas\nINTERSECT\nsalarios",
        ),
        (
            "q := personas difference salarios;",
            "personas\nEXCEPT\nsalarios",
        ),
        (
            "q := personas njoin salarios;",
            "personas NATURAL JOIN salarios",
        ),
        (
            "q := personas product salarios;",
            "personas CROSS JOIN salarios",
        ),
    ],
)
def test_generate(query, expected):
    result = _generate(query)
    assert result["q"] == expected


def test_divide_raises_not_implemented():
    with pytest.raises(NotImplementedError):
        _generate("q := r1 divide r2;")
