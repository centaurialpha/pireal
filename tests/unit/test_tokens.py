import pytest

from pireal.interpreter.tokens import TokenTypes, BINARY_OPERATORS, RESERVED_KEYWORDS

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
    assert BINARY_OPERATORS == expected


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
    assert RESERVED_KEYWORDS == expected


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
