from pytest import Parser

from pireal.interpreter.lexer import Lexer
from pireal.interpreter.scanner import Scanner
from pireal.interpreter.parser import Parser
from pireal.interpreter.evaluator import Evaluator
from pireal.core.relation import Relation


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


def test_basic_project():
    rb = make_relation(
        ["id", "skill"],
        [("3", "Web"), ("23", "Satellites"), ("1", "Python")],
    )
    results = evaluate("q := project skill (rb);", {"rb": rb})
    expected = make_relation(["skill"], [("Web",), ("Satellites",), ("Python",)])
    assert_relation_equal(results["q"], expected)


def test_project_many_attrs():
    r = make_relation(
        ["id", "birth", "lastname", "age", "name"],
        [
            ("1", "20/01/1991", "Acosta", "35", "Gabriel"),
            ("3", "06/07/1994", "Pereyra", "32", "Marisel"),
        ],
    )
    results = evaluate("q := project id, name, age (r);", {"r": r})
    expected = make_relation(
        ["id", "name", "age"],
        [("1", "Gabriel", "35"), ("3", "Marisel", "32")],
    )
    assert_relation_equal(results["q"], expected)


def test_nested_project():
    r = make_relation(
        ["id", "name", "age"],
        [("1", "Gabriel", "35"), ("3", "Marisel", "32"), ("2", "Rodrigo", "25")],
    )
    results = evaluate("q := project id (project id, name, age (r));", {"r": r})
    expected = make_relation(["id"], [("1",), ("3",), ("2",)])
    assert_relation_equal(results["q"], expected)


def test_basic_select():
    r = make_relation(
        ["id", "name"],
        [("1", "Gabriel"), ("2", "Marisel"), ("3", "Rodrigo"), ("4", "Hector")],
    )
    results = evaluate("q := select id=4 (r);", {"r": r})
    expected = make_relation(["id", "name"], [("4", "Hector")])
    assert_relation_equal(results["q"], expected)


def test_select_and_expression():
    r = make_relation(
        ["name", "age"],
        [("Gabriel", "35"), ("Marisel", "32"), ("Rodrigo", "25"), ("Hector", "51")],
    )
    results = evaluate("q := select age>=32 and age<=35 (r);", {"r": r})
    expected = make_relation(
        ["name", "age"],
        [("Gabriel", "35"), ("Marisel", "32")],
    )
    assert_relation_equal(results["q"], expected)


def test_select_nested_and():
    r = make_relation(
        ["name", "age"],
        [
            ("Gabriel", "35"),
            ("Marisel", "32"),
            ("gabox", "19"),
            ("gabox", "25"),
            ("gabox", "34"),
            ("gabox", "49"),
        ],
    )
    results = evaluate(
        "q := select age>=33 and age<=35 and name='gabox' (r);", {"r": r}
    )
    expected = make_relation(["name", "age"], [("gabox", "34")])
    assert_relation_equal(results["q"], expected)


def test_variable_reference():
    rb = make_relation(["id", "skill"], [("3", "Web"), ("1", "Python")])
    results = evaluate("q := rb;", {"rb": rb})
    assert_relation_equal(results["q"], rb)
