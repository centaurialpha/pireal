import unittest

from pireal.interpreter.tokens import (
    TokenTypes,
    _build_binary_operators,
    _build_reserved_keywords,
)


class TokenTestCase(unittest.TestCase):
    def test_build_binary_operators(self):
        expected_operators = {
            "product": TokenTypes.PRODUCT,
            "intersect": TokenTypes.INTERSECT,
            "union": TokenTypes.UNION,
            "difference": TokenTypes.DIFFERENCE,
            "njoin": TokenTypes.NJOIN,
            "louter": TokenTypes.LEFT_OUTER_JOIN,
            "router": TokenTypes.RIGHT_OUTER_JOIN,
            "fouter": TokenTypes.FULL_OUTER_JOIN,
        }

        binary_operators = _build_binary_operators()

        self.assertDictEqual(binary_operators, expected_operators)

    def test_build_reserved_keywords(self):
        expected_keywords = {
            "select": TokenTypes.SELECT,
            "project": TokenTypes.PROJECT,
            "product": TokenTypes.PRODUCT,
            "intersect": TokenTypes.INTERSECT,
            "union": TokenTypes.UNION,
            "difference": TokenTypes.DIFFERENCE,
            "njoin": TokenTypes.NJOIN,
            "louter": TokenTypes.LEFT_OUTER_JOIN,
            "router": TokenTypes.RIGHT_OUTER_JOIN,
            "fouter": TokenTypes.FULL_OUTER_JOIN,
            "and": TokenTypes.AND,
            "or": TokenTypes.OR,
        }

        reserved_keywords = _build_reserved_keywords()

        self.assertDictEqual(reserved_keywords, expected_keywords)
