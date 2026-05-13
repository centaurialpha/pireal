# Copyright 2015-2019 - Gabriel Acosta <acostadariogabriel@gmail.com>
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

"""Test para el Scanner"""

import pytest

from pireal.interpreter import scanner

pytestmark = pytest.mark.interpreter


@pytest.fixture
def scanner_bot():
    def _make_scanner(text, pos=0):
        sc = scanner.Scanner(text)
        sc.index = pos
        return sc

    return _make_scanner


@pytest.mark.parametrize("text, pos, expected", [("hola", 1, "o"), ("hola", 3, "a"), ("hola", 9, None)])
def test_char_property(scanner_bot, text, pos, expected):
    sc = scanner_bot(text, pos)
    assert sc.char == expected


@pytest.mark.parametrize(
    "text, moves, expected",
    [
        ("h\nol\na", 3, (2, 2, 3)),
        ("h\nol\na", 1, (1, 2, 1)),
    ],
)
def test_next(scanner_bot, text, moves, expected):
    sc = scanner_bot(text)
    for _ in range(moves):
        sc.next()
    line, col, index = expected
    assert sc.lineno == line
    assert sc.colno == col
    assert sc.index == index


def test_repr(scanner_bot):
    sc = scanner_bot("pireal")
    assert repr(sc) == "<Scanner at 1:1 - Character: p>"
    sc.next()
    sc.next()
    assert repr(sc) == "<Scanner at 1:3 - Character: r>"


def test_peek(scanner_bot):
    sc = scanner_bot("ola k ace")
    assert sc.char == "o"
    assert sc.peek() == "l"
    assert sc.char == "o"
    for _ in range(8):
        sc.next()
    assert sc.char == "e"
    assert sc.peek() is None


def test_peek_at_end(scanner_bot):
    sc = scanner_bot("ab")
    sc.next()  # en 'b'
    assert sc.peek() is None


def test_char_at_eof(scanner_bot):
    sc = scanner_bot("a")
    sc.next()
    assert sc.char is None


def test_lineno_colno_tracking(scanner_bot):
    sc = scanner_bot("a\nb\nc")
    sc.next()  # '\n'
    assert sc.lineno == 1
    sc.next()  # 'b'
    assert sc.lineno == 2
    assert sc.colno == 1
    sc.next()  # '\n'
    sc.next()  # 'c'
    assert sc.lineno == 3
    assert sc.colno == 1


def test_repr_at_eof(scanner_bot):
    sc = scanner_bot("a")
    sc.next()
    assert repr(sc) == "<Scanner at 1:2 - Character: None>"
