import pytest

from src.core.interpreter import scanner
from src.core.interpreter import lexer
from src.core.interpreter import parser


@pytest.fixture
def fixture_parser():
    def _make_parser(text):
        sc = scanner.Scanner(text)
        lex = lexer.Lexer(sc)
        par = parser.Parser(lex)
        return par
    return _make_parser


# @pytest.mark.parametrize(
#     'query',
#     [
#         ('q1:=')
#     ]
# )
# FIXME: parametrizar esto
def test_consume(fixture_parser):
    p = fixture_parser('q1 := select')
    p.consume(lexer.ID)
    with pytest.raises(parser.ConsumeError):
        p.consume(lexer.REAL)
    assert p.token.type == lexer.ASSIGNMENT


def test_variable(fixture_parser):
    p = fixture_parser('q1 :=')
    node = p._variable()
    assert isinstance(node, parser.Variable)
    assert node.token.type == lexer.ID
    assert node.token.value == 'q1'


def test_condition(fixture_parser):
    p = fixture_parser("name='gabo'")
    node = p._condition()
    assert isinstance(node, parser.Condition)

