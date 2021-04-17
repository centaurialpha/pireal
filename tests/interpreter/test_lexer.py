import pytest
from unittest import mock

from pireal.interpreter import scanner
from pireal.interpreter import lexer
from pireal.interpreter.tokens import TokenTypes, RESERVED_KEYWORDS
from pireal.interpreter import exceptions


@pytest.fixture
def fixture_lexer():
    def _make_lexer(text):
        sc = scanner.Scanner(text)
        lex = lexer.Lexer(sc)
        return lex
    return _make_lexer


@pytest.mark.parametrize(
    'chars, expected, ttype, rep',
    [
        ('234asdasd asd ', 234, TokenTypes.INTEGER, 'INTEGER'),
        ('9.0<<>>', 9.0, TokenTypes.REAL, 'REAL'),
        ('9>====84<<>.223', 9, TokenTypes.INTEGER, 'INTEGER')
    ]
)
def test_get_number(fixture_lexer, chars, expected, ttype, rep):
    lex = fixture_lexer(chars)
    tkn = lex._get_number()
    assert tkn.type == ttype
    assert tkn.value == expected
    # assert repr(tkn) == 'Token({}, {})'.format(rep, tkn.value)


@pytest.mark.parametrize(
    'text, expected',
    [
        ('gab.o aa s', 'gab'),
        ('gab_o   ', 'gab_o'),
        ('project', 'project'),
        ('select_', 'select_'),
        ('foo_bar_23 foo', 'foo_bar_23')
    ]
)
def test_get_identifier_or_keyword(fixture_lexer, text, expected):
    lex = fixture_lexer(text)
    _id = lex._get_identifier_or_keyword()
    assert _id == expected


@pytest.mark.parametrize(
    'text, called',
    [
        ('asd asd', 1),
        ('sd sdsd sds s', 3),
        ('hola gabo como estas <>>>> pireal es lo más ', 9)
    ]
)
def test_skip_whitespace(fixture_lexer, text, called):
    lex = fixture_lexer(text)
    with mock.patch.object(lexer.Lexer, '_skip_whitespace', wraps=lex._skip_whitespace) as m:
        while lex.next_token().value is not None:
            pass
        assert m.call_count == called


@pytest.mark.parametrize(
    'text, called',
    [
        ('d\n%asda\n%dsd', 2),
        ('asdasd\n%dsadasd\n%dsadasd\n%dsad', 3),
        ('adasdasd', 0)
    ]
)
def test_skip_comment(fixture_lexer, text, called):
    lex = fixture_lexer(text)
    with mock.patch.object(lexer.Lexer, '_skip_comment', wraps=lex._skip_comment) as m:
        while lex.next_token().value is not None:
            pass
        assert m.call_count == called


@pytest.mark.parametrize(
    'token_str, ttype, value',
    [
        (':=', TokenTypes.ASSIGNMENT, ':='),
        ('<', TokenTypes.LESS, '<'),
        ('>', TokenTypes.GREATER, '>'),
        ('<>', TokenTypes.NOTEQUAL, '<>'),
        ('<=', TokenTypes.LEQUAL, '<='),
        ('>=', TokenTypes.GEQUAL, '>='),
        ('=', TokenTypes.EQUAL, '='),
        (';', TokenTypes.SEMI, ';'),
        ('(', TokenTypes.LPAREN, '('),
        (')', TokenTypes.RPAREN, ')'),
        (',', TokenTypes.COMMA, ','),
        ('123', TokenTypes.INTEGER, 123),
        ('3.14', TokenTypes.REAL, 3.14),
        ("'hola'", TokenTypes.STRING, "hola"),
        ("'20/01/1991'", TokenTypes.DATE, "20/01/1991"),
        ("'15:15'", TokenTypes.TIME, "15:15"),
        ("intersect", RESERVED_KEYWORDS['intersect'], "intersect")
    ]
)
def test_next_token(fixture_lexer, token_str, ttype, value):
    lex = fixture_lexer(token_str)
    token = lex.next_token()
    assert token.type == ttype
    assert token.value == value


def test_missing_quote_error(fixture_lexer):
    lex = fixture_lexer("'hola")
    with pytest.raises(exceptions.MissingQuoteError):
        lex.next_token()


def test_raise_invalid_syntax_error(fixture_lexer):
    lex = fixture_lexer('< > = ] <')
    for _ in range(3):
        lex.next_token()
    with pytest.raises(exceptions.InvalidSyntaxError):
        lex.next_token()
