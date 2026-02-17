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

from pireal.interpreter.tokens import BINARY_OPERATORS, RESERVED_KEYWORDS, TokenTypes

pytestmark = pytest.mark.interpreter


def test_binary_operators():
    expected = {
        "product": TokenTypes.PRODUCT,
        "intersect": TokenTypes.INTERSECT,
        "union": TokenTypes.UNION,
        "difference": TokenTypes.DIFFERENCE,
        "njoin": TokenTypes.NJOIN,
        "louter": TokenTypes.LOUTER,
        "router": TokenTypes.ROUTER,
        "fouter": TokenTypes.FOUTER,
    }
    assert expected == BINARY_OPERATORS


def test_reserved_keywords():
    expected = {
        "select": TokenTypes.SELECT,
        "project": TokenTypes.PROJECT,
        "product": TokenTypes.PRODUCT,
        "intersect": TokenTypes.INTERSECT,
        "union": TokenTypes.UNION,
        "difference": TokenTypes.DIFFERENCE,
        "njoin": TokenTypes.NJOIN,
        "louter": TokenTypes.LOUTER,
        "router": TokenTypes.ROUTER,
        "fouter": TokenTypes.FOUTER,
        "and": TokenTypes.AND,
        "or": TokenTypes.OR,
    }
    assert expected == RESERVED_KEYWORDS


@pytest.mark.parametrize(
    "op",
    [
        "product",
        "intersect",
        "union",
        "difference",
        "njoin",
        "louter",
        "router",
        "fouter",
    ],
)
def test_binary_operators_are_in_reserved_keywords(op):
    assert op in RESERVED_KEYWORDS
