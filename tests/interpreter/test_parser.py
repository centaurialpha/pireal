import pytest

from src.core.interpreter import scanner
from src.core.interpreter import lexer
from src.core.interpreter import parser


@pytest.fixture
def select_bot():
    sc = scanner.Scanner("q1 := select id=2 (ages);")
    lex = lexer.Lexer(sc)
    par = parser.Parser(lex)
    return par
