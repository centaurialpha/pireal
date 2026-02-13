import pytest
from pireal.interpreter.lexer import Lexer
from pireal.interpreter.scanner import Scanner
from pireal.interpreter.parser import Parser
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
