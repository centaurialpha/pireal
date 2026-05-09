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

from pireal.core.relation import Relation
from pireal.interpreter.evaluator import Evaluator, UndefinedRelationError
from pireal.interpreter.exceptions import DuplicateRelationNameError, UndefinedAttributeError
from pireal.interpreter.lexer import Lexer
from pireal.interpreter.parser import Parser
from pireal.interpreter.scanner import Scanner

pytestmark = pytest.mark.interpreter


def make_relation(header: list[str], rows: list[tuple]) -> Relation:
    r = Relation()
    r.header = header
    for row in rows:
        r.insert(row)
    return r


@pytest.fixture
def personas():
    return make_relation(
        ["id", "name", "age"],
        [("1", "gabox", "25"), ("2", "ana", "30"), ("3", "bob", "25")],
    )


@pytest.fixture
def salarios():
    return make_relation(
        ["id", "salary"],
        [("1", "1000"), ("2", "2000")],
    )


@pytest.fixture
def relations(personas, salarios):
    return {"personas": personas, "salarios": salarios}


def evaluate(query: str, relations: dict) -> dict:
    tree = Parser(Lexer(Scanner(query))).parse()
    return Evaluator(relations).evaluate(tree)


def test_select(relations):
    results = evaluate("q := select age=25 (personas);", relations)
    assert results["q"].cardinality() == 2


def test_project(relations):
    results = evaluate("q := project name (personas);", relations)
    assert results["q"].header == ["name"]
    assert results["q"].cardinality() == 3


def test_njoin(relations):
    results = evaluate("q := personas njoin salarios;", relations)
    assert "salary" in results["q"].header
    assert results["q"].cardinality() == 2


def test_union(relations):
    r1 = make_relation(["id"], [("1",), ("2",)])
    r2 = make_relation(["id"], [("3",), ("2",)])
    results = evaluate("q := r1 union r2;", {"r1": r1, "r2": r2})
    assert results["q"].cardinality() == 3


def test_difference(relations):
    r1 = make_relation(["id"], [("1",), ("2",)])
    r2 = make_relation(["id"], [("2",)])
    results = evaluate("q := r1 difference r2;", {"r1": r1, "r2": r2})
    assert results["q"].cardinality() == 1


def test_intersect(relations):
    r1 = make_relation(["id"], [("1",), ("2",)])
    r2 = make_relation(["id"], [("2",), ("3",)])
    results = evaluate("q := r1 intersect r2;", {"r1": r1, "r2": r2})
    assert results["q"].cardinality() == 1


def test_product(relations):
    r1 = make_relation(["a"], [("1",)])
    r2 = make_relation(["b"], [("x",), ("y",)])
    results = evaluate("q := r1 product r2;", {"r1": r1, "r2": r2})
    assert results["q"].cardinality() == 2
    assert results["q"].degree() == 2


def test_undefined_relation(relations):
    with pytest.raises(UndefinedRelationError) as exc:
        evaluate("q := noexiste;", relations)
    assert exc.value.name == "noexiste"


def test_duplicate_relation_name(relations):
    with pytest.raises(DuplicateRelationNameError):
        evaluate("q := personas; q := salarios;", relations)


def test_chained_queries(relations):
    query = """
    q1 := select age=25 (personas);
    q2 := project name (q1);
    """
    results = evaluate(query, relations)
    assert results["q2"].header == ["name"]
    assert results["q2"].cardinality() == 2


def test_project_undefined_attribute(relations):
    with pytest.raises(UndefinedAttributeError) as exc:
        evaluate("q := project nonexistent (personas);", relations)
    assert exc.value.attribute == "nonexistent"


def test_select_undefined_attribute(relations):
    with pytest.raises(UndefinedAttributeError) as exc:
        evaluate("q := select nonexistent=1 (personas);", relations)
    assert exc.value.attribute == "nonexistent"


def test_select_nested_undefined_attribute(relations):
    with pytest.raises(UndefinedAttributeError) as exc:
        evaluate("q := select age=25 and nonexistent='x' (personas);", relations)
    assert exc.value.attribute == "nonexistent"


def test_divide():
    enrollments = make_relation(
        ["student_id", "course_id"],
        [
            ("1", "math"),
            ("1", "physics"),
            ("2", "math"),
            ("3", "math"),
            ("3", "physics"),
        ],
    )
    required = make_relation(["course_id"], [("math",), ("physics",)])

    results = evaluate(
        "q := enrollments divide required;",
        {"enrollments": enrollments, "required": required},
    )

    assert results["q"].header == ["student_id"]
    assert results["q"].content == {("1",), ("3",)}
