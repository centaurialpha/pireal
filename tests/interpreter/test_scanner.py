import pytest

from src.core.interpreter import scanner


@pytest.fixture
def scanner_bot():
    text = "hola gabo\ncomo estas?\n\n!"
    sc = scanner.Scanner(text)
    return text, sc


def test_1(scanner_bot):
    text, sc = scanner_bot
    for i in range(7):
        sc.next()
    assert sc.char == "b"


def test_2(scanner_bot):
    text, sc = scanner_bot
    assert sc.index == 0
    for i in range(7):
        sc.next()
    assert sc.char == "b"

    assert sc.index == 7


def test_3(scanner_bot):
    text, sc = scanner_bot
    for i in range(7):
        sc.next()

    assert sc.lineno == 1
    assert sc.colno == 8


def test_4(scanner_bot):
    text, sc = scanner_bot
    for i in range(23):
        sc.next()
    assert sc.char == "!"
    assert sc.lineno == 4


def test_5():
    sc = scanner.Scanner("\n\n\n\n\nasdasd\n\n  \n  \n\n\n    \n    % asdasd")
    while sc.char:
        sc.next()
    assert sc.lineno == 13