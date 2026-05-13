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

from tests.helpers import assert_relation_equal, evaluate, make_relation

pytestmark = pytest.mark.integration


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
    results = evaluate("q := select age>=33 and age<=35 and name='gabox' (r);", {"r": r})
    expected = make_relation(["name", "age"], [("gabox", "34")])
    assert_relation_equal(results["q"], expected)


def test_variable_reference():
    rb = make_relation(["id", "skill"], [("3", "Web"), ("1", "Python")])
    results = evaluate("q := rb;", {"rb": rb})
    assert_relation_equal(results["q"], rb)


def test_select_date():
    r = make_relation(
        ["nombre", "fecha_inicio"],
        [
            ("Curso A", "01/01/2017"),
            ("Curso B", "01/06/2017"),
            ("Curso C", "01/01/2016"),
        ],
    )
    results = evaluate("q := select fecha_inicio > '01/03/2017' (r);", {"r": r})
    assert results["q"].cardinality() == 1
    assert ("Curso B", "01/06/2017") in results["q"].content
