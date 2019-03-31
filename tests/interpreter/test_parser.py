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


def test_parser_select_expression(fixture_parser):
    p = fixture_parser('q1 := select id=1 (p);')
    tree = p.parse()
    assert isinstance(tree, parser.Compound)
    for c in tree.children:
        assert isinstance(c, parser.Assignment)
        assert isinstance(c.query, parser.SelectExpr)


def test_parser_project_expression(fixture_parser):
    p = fixture_parser('q1 := project a, b, c (p);')
    tree = p.parse()
    assert isinstance(tree, parser.Compound)
    for c in tree.children:
        assert isinstance(c, parser.Assignment)
        assert isinstance(c.query, parser.ProjectExpr)


def test_parser_binary_expression(fixture_parser):
    p = fixture_parser('q1 := a intersect b;')
    tree = p.parse()
    assert isinstance(tree, parser.Compound)
    for c in tree.children:
        assert isinstance(c, parser.Assignment)
        assert isinstance(c.query, parser.BinaryOp)


def test_parser_condition(fixture_parser):
    p = fixture_parser('q1 := select i<2 (p);')
    tree = p.parse()
    assert isinstance(tree, parser.Compound)
    for c in tree.children:
        assert isinstance(c, parser.Assignment)
        assert isinstance(c.query.condition, parser.Condition)


def test_string_node(fixture_parser):
    p = fixture_parser('q1 := select name=\'gabo\' (p);')
    tree = p.parse()
    assert isinstance(tree, parser.Compound)
    for c in tree.children:
        assert isinstance(c, parser.Assignment)
        assert isinstance(c.query.condition.op2, parser.String)


@pytest.mark.parametrize(
    'date',
    [
        ('20/01/1991',),
        ('1991/01/20')
    ]
)
def test_date_node(fixture_parser, date):
    p = fixture_parser('q1 := select date=\'%s\' (p);' % date)
    tree = p.parse()
    assert isinstance(tree, parser.Compound)
    for c in tree.children:
        assert isinstance(c, parser.Assignment)
        assert isinstance(c.query.condition.op2, parser.Date)


def test_time_node(fixture_parser):
    p = fixture_parser('q1 := select hour=\'20:15\' (p);')
    tree = p.parse()
    assert isinstance(tree, parser.Compound)
    for c in tree.children:
        assert isinstance(c, parser.Assignment)
        assert isinstance(c.query.condition.op2, parser.Time)


def test_bool_node(fixture_parser):
    p = fixture_parser('q1 := select edad < 20 or edad > 10 (p);')
    tree = p.parse()
    assert isinstance(tree, parser.Compound)
    for c in tree.children:
        assert isinstance(c, parser.Assignment)
        assert isinstance(c.query.condition, parser.BoolOp)
        assert 'or' in c.query.condition.ops
        for c, c2 in zip(['<', '>'], c.query.condition.conditions):
            assert c == c2.operator.value
# # @pytest.mark.parametrize(
# #     'query',
# #     [
# #         ('q1:=')
# #     ]
# # )
# # FIXME: parametrizar esto
# @pytest.mark.parametrize(
#     'query, consumed',
#     [
#         ('q1 :=', (lexer.ID, lexer.ASSIGNMENT)),
#         ('select id=', (lexer.KEYWORDS['select'], lexer.ID, lexer.EQUAL)),
#         ('project a,b', (lexer.KEYWORDS['project'], lexer.ID, lexer.SEMI, lexer.ID))
#     ]
# )
# def test_consume(fixture_parser, query, consumed):
#     p = fixture_parser(query)
#     for token_to_consume in consumed:
#         p.consume(token_to_consume)


# def test_consume_error(fixture_parser):
#     p = fixture_parser('q1 :=')
#     p.consume(lexer.ID)
#     with pytest.raises(parser.ConsumeError):
#         p.consume(lexer.SEMI)


# def test_variable(fixture_parser):
#     p = fixture_parser('q1 :=')
#     node = p._variable()
#     assert isinstance(node, parser.Variable)
#     assert node.token.type == lexer.ID
#     assert node.token.value == 'q1'


# def test_condition(fixture_parser):
#     p = fixture_parser("name='gabo'")
#     node = p._condition()
#     assert isinstance(node, parser.Condition)


