# -*- coding: utf-8 -*-
#
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


@pytest.fixture
def scanner_bot():
    def _make_scanner(text, pos=0):
        sc = scanner.Scanner(text)
        sc.index = pos
        return sc
    return _make_scanner


@pytest.mark.parametrize(
    'text, pos, expected',
    [
        ('hola', 1, 'o'),
        ('hola', 3, 'a'),
        ('hola', 9, None)
    ]
)
def test_char_property(scanner_bot, text, pos, expected):
    sc = scanner_bot(text, pos)
    assert sc.char == expected


@pytest.mark.parametrize(
    'text, moves, expected',
    [
        ('h\nol\na', 3, (2, 2, 3)),
        ('h\nol\na', 1, (1, 2, 1)),
    ]
)
def test_next(scanner_bot, text, moves, expected):
    sc = scanner_bot(text)
    for _ in range(moves):
        sc.next()
    line, col, index = expected
    assert sc.lineno == line
    assert sc.colno == col
    assert sc.index == index


@pytest.mark.parametrize(
    'text, moves, expected',
    [
        ('hola como estas', 1, 'o'),
        ('hola como estas', 4, ' '),
        ('hola como estas', 7, 'm'),
        ('hola como estas', 0, '')
    ]
)
def test_next_char(scanner_bot, text, moves, expected):
    sc = scanner_bot(text)
    char = ''
    for _ in range(moves):
        char = sc.next_char()
    assert char == expected


def test_repr(scanner_bot):
    sc = scanner_bot('pireal')
    assert repr(sc) == '<Scanner at 1:1 - Character: p>'
    sc.next()
    sc.next()
    assert repr(sc) == '<Scanner at 1:3 - Character: r>'
