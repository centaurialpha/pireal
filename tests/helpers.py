from pireal.core.relation import Relation
from pireal.interpreter.evaluator import Evaluator
from pireal.interpreter.lexer import Lexer
from pireal.interpreter.parser import Parser
from pireal.interpreter.scanner import Scanner


def make_relation(header: list, rows: list[tuple]) -> Relation:
    r = Relation()
    r.header = header
    for row in rows:
        r.insert(row)
    return r


def evaluate(query: str, relations: dict) -> dict:
    tree = Parser(Lexer(Scanner(query))).parse()
    return Evaluator(relations).evaluate(tree)


def assert_relation_equal(r1: Relation, r2: Relation):
    assert r1.header == r2.header
    assert r1.degree() == r2.degree()
    assert r1.cardinality() == r2.cardinality()
    assert r1.content == r2.content
