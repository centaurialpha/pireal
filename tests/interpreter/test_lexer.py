import pytest

from src.core.interpreter import scanner
from src.core.interpreter import lexer
from src.core.interpreter import tokens
from src.core.interpreter import exceptions


@pytest.fixture
def lexer_bot():
    sc = scanner.Scanner("q1_ := select nombre='Gabriel' (personas);")
    lex = lexer.Lexer(sc)
    return lex


@pytest.fixture
def lexer_tokens():
    sc = scanner.Scanner("> < <= >= = <> , ; ( )")
    return lexer.Lexer(sc)


def move_lexer_to(lex, n=1):
    token = None
    for _ in range(n):
        token = lex.next_token()
    return token


def test_token():
    tkn = lexer.Token(type=tokens.ID, value='query_1')
    assert str(tkn) == "Token(IDENTIFIER, query_1)"
    assert repr(tkn) == "Token(IDENTIFIER, query_1)"


def test_lexer_str(lexer_bot):
    tkn = lexer.Token(type=tokens.ID, value='query_1')
    lexer_bot.token = tkn
    assert str(lexer_bot) == 'Token(IDENTIFIER, query_1)'
    assert repr(lexer_bot) == "Token(IDENTIFIER, query_1)"


def test_operators(lexer_tokens):
    assert lexer_tokens.next_token().value == ">"
    assert lexer_tokens.next_token().value == "<"
    assert lexer_tokens.next_token().value == "<="
    assert lexer_tokens.next_token().value == ">="
    assert lexer_tokens.next_token().value == "="
    assert lexer_tokens.next_token().value == "<>"
    assert lexer_tokens.next_token().value == ","
    assert lexer_tokens.next_token().value == ";"
    assert lexer_tokens.next_token().value == "("
    assert lexer_tokens.next_token().value == ")"
    assert lexer_tokens.next_token().value is None


def test_id_token(lexer_bot):
    assert lexer_bot.token is None
    token = lexer_bot.next_token()
    assert token.type == tokens.ID
    assert token.value == "q1_"


def test_assignment_token(lexer_bot):
    lexer_bot.next_token()
    token = lexer_bot.next_token()
    assert token.type == tokens.ASSIGNMENT
    assert token.value == ":="


def test_select_keyword_token(lexer_bot):
    token = move_lexer_to(lexer_bot, 3)
    assert token.type == tokens.SELECT
    assert token.value == "select"


def test_equal_token(lexer_bot):
    token = move_lexer_to(lexer_bot, 5)
    assert token.type == tokens.EQUAL
    assert token.value == "="


def test_string_token(lexer_bot):
    token = move_lexer_to(lexer_bot, 6)
    assert token.type == tokens.STRING
    assert token.value == "Gabriel"


def test_left_paren_token(lexer_bot):
    token = move_lexer_to(lexer_bot, 7)
    assert token.type == tokens.LPAREN
    assert token.value == "("


def test_right_paren_token(lexer_bot):
    token = move_lexer_to(lexer_bot, 9)
    assert token.type == tokens.RPAREN
    assert token.value == ")"


def test_semicolon_token(lexer_bot):
    token = move_lexer_to(lexer_bot, 10)
    assert token.type == tokens.SEMICOLON
    assert token.value == ";"


def test_with_comment():
    sc = scanner.Scanner((
        "% this is a comment\n"
        "q1 := select nombre='Gabriel' (personas);\n"
        "% otro comentario\n"
        "% lalala\n"
        "%dddd\n"
        "% dddd\n\n\n"
        "q2 := select nombre='Gabriel (personas);"))
    lex = lexer.Lexer(sc)
    for i in range(12):
        token = lex.next_token()
    assert token.value == ":="
    assert lex.sc.lineno == 9
    for i in range(3):
        token = lex.next_token()

    assert token.value == "="
    with pytest.raises(exceptions.MissingQuoteError):
        lex.next_token()
    assert lex.sc.lineno == 9
    assert lex.sc.colno == 41


def test_with_comment2():
    text = ("% this is a comment\n"
            "q1 := select nombre='Gabriel (personas);\n"
            "% oasdlaskdalksjdlaksd\n"
            "% sdksjdksjdkjskdjskdj")
    sc = scanner.Scanner(text)
    lex = lexer.Lexer(sc)
    t = lex.next_token()
    t = lex.next_token()
    t = lex.next_token()
    t = lex.next_token()
    t = lex.next_token()
    assert t.value == "="
    with pytest.raises(exceptions.MissingQuoteError):
        lex.next_token()


def test_invalid_syntax():
    sc = scanner.Scanner("q1 := !!")
    lex = lexer.Lexer(sc)
    lex.next_token()  # ok
    lex.next_token()  # ok
    with pytest.raises(exceptions.InvalidSyntaxError):
        lex.next_token()
