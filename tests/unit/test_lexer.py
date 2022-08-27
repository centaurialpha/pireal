import pytest

from pireal.interpreter.lexer import (
    Lexer,
    Token,
)
from pireal.interpreter.exceptions import InvalidSyntaxError, MissingQuoteError
from pireal.interpreter.tokens import TokenTypes
from pireal.interpreter.scanner import Scanner

pytestmark = pytest.mark.interpreter


@pytest.fixture()
def lexer():
    def _make_lexer(code):
        sc = Scanner(code)
        return Lexer(sc)

    return _make_lexer


@pytest.mark.parametrize(
    "text,expected",
    [
        ("asd123", Token(TokenTypes.ID, "asd123")),
        ("asd123&asd", Token(TokenTypes.ID, "asd123")),
        ("select", Token(TokenTypes.SELECT, "select")),
        ("_asd123", Token(TokenTypes.ID, "_asd123")),
    ],
)
def test_get_id_or_keyword(lexer, text, expected):
    lex = lexer(text)
    token = lex.get_identifier_or_keyword()
    assert expected.value == token.value
    assert expected.type == token.type


@pytest.mark.parametrize(
    "text,token_types",
    [
        ("select         hola123", [TokenTypes.SELECT, TokenTypes.ID]),
        ("_hola123  hola      ", [TokenTypes.ID, TokenTypes.ID]),
    ],
)
def test_skip_whitespace(lexer, text, token_types):
    lex = lexer(text)
    for token_type in token_types:
        token = lex.next_token()
        assert token.type == token_type


def test_skip_comments(lexer):
    lex = lexer("hola\n123\n%select")
    assert lex.next_token().type == TokenTypes.ID
    assert lex.next_token().type == TokenTypes.INTEGER
    assert lex.next_token().type == TokenTypes.EOF
    assert lex.next_token().type == TokenTypes.EOF


@pytest.mark.parametrize(
    "text,expected_token_type",
    [
        ("1234", TokenTypes.INTEGER),
        ("0.1", TokenTypes.REAL),
    ],
)
def test_get_number(lexer, text, expected_token_type):
    lex = lexer(text)
    assert lex.get_number().type == expected_token_type


@pytest.mark.parametrize(
    "text,expected_token_type",
    [
        ("'1234'", TokenTypes.STRING),
        ("'hola que haces'", TokenTypes.STRING),
        ("'20/01/1991'", TokenTypes.DATE),
        ("'10:58'", TokenTypes.TIME),
    ],
)
def test_get_string(lexer, text, expected_token_type):
    lex = lexer(text)
    assert lex.next_token().type == expected_token_type


def test_analize_string_missing_quote_error(lexer):
    lex = lexer("'hola que haces")
    with pytest.raises(MissingQuoteError):
        lex.analize_string()


def test_assignment(lexer):
    lex = lexer(":= =: ::")
    token = lex.next_token()
    assert token.type == TokenTypes.ASSIGNMENT
    assert lex.next_token().type == TokenTypes.EQUAL
    with pytest.raises(InvalidSyntaxError):
        lex.next_token()


def test_operators(lexer):
    lex = lexer("<> << <= >>=")
    token = lex.next_token()
    assert token.type == TokenTypes.NOTEQUAL
    assert lex.next_token().type == TokenTypes.LESS
    assert lex.next_token().type == TokenTypes.LESS
    assert lex.next_token().type == TokenTypes.LEQUAL
    assert lex.next_token().type == TokenTypes.GREATER
    assert lex.next_token().type == TokenTypes.GEQUAL
