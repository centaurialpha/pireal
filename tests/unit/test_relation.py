# -*- coding: utf-8 -*-
#
# Copyright 2015-2018 - Gabriel Acosta <acostadariogabriel@gmail.com>
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
import unittest
import pytest

from pireal.core import relation
from pireal.core.relation import Relation


class RelationTestCase(unittest.TestCase):
    def test_select_with_date(self):
        r1 = Relation()
        r1.header = ["id", "dates"]
        r1.insert(("1", "20/01/1991"))
        r1.insert(("2", "20/01/1993"))
        r1.insert(("3", "20/01/1998"))

        expected_relation = Relation()
        expected_relation.header = ["id", "dates"]
        expected_relation.insert(("2", "20/01/1993"))
        expected_relation.insert(("3", "20/01/1998"))

        r = r1.select("dates >= datetime.date(1993, 1, 20)")
        print(r)


@pytest.fixture
def relation_fixture():
    r1 = relation.Relation()
    r1.header = ["id", "name", "city"]
    data = {
        ("1", "Gabriel", "Belén"),
        ("23", "Rodrigo", "Belén"),
        ("12", "Mercedes", "Las Juntas"),
        ("2", "Diego", "Santiago del Estero"),
    }
    for d in data:
        r1.insert(d)

    r2 = relation.Relation()
    r2.header = ["id", "skill"]
    data = {("3", "Ruby"), ("1", "Python"), ("12", "Rocas"), ("23", "Games")}
    for d in data:
        r2.insert(d)

    r3 = relation.Relation()
    r3.header = ["date"]
    data = {("2015-12-12"), ("2012-07-09"), ("1998-12-09")}
    for d in data:
        r3.insert(d)
    return r1, r2, r3


def test_valid_header():
    r = relation.Relation()
    with pytest.raises(relation.InvalidFieldNameError):
        r.header = ["id", "nombre foo", "skills"]


def test_cardinality():
    r = relation.Relation()
    r.header = ["id", "nombre"]
    for i in {("1", "gabriel"), ("3", "rodrigo"), ("2", "mechi")}:
        r.insert(i)
    assert r.cardinality() == 3


def test_wrong_size_relation():
    r = relation.Relation()
    r.header = ["aaa", "bbb"]
    data = {("a", "b", "c", "d"), ("e", "f", "g", "h")}
    with pytest.raises(relation.WrongSizeError):
        for d in data:
            r.insert(d)


def test_projection(relation_fixture):
    # r1 projection
    r1, _, r3 = relation_fixture
    expected = {("Gabriel",), ("Rodrigo",), ("Mercedes",), ("Diego",)}
    assert r1.project("name").content == expected
    expected = {("2015-12-12",), ("2012-07-09",), ("1998-12-09",)}
    assert r3.project("date").content == expected


def test_invalid_field_in_projection(relation_fixture):
    # r2 projection
    _, r2, _ = relation_fixture
    with pytest.raises(relation.FieldNotInHeaderError):
        r2.project("cualquiera")


def test_selection(relation_fixture):
    r1, _, _ = relation_fixture
    expected = {("23", "Rodrigo", "Belén")}
    assert r1.select("id==23").content == expected


def test_selection2():
    r = relation.Relation()
    r.header = ["precio", "curso"]
    data = {
        ("400", "curso1"),
        ("104", "curso2"),
        ("500", "curso3"),
        ("1000", "curso4"),
        ("200", "curso5"),
    }
    for d in data:
        r.insert(d)
    assert r.cardinality() == 5
    assert r.degree() == 2
    sel = r.select("precio > 400")
    expected = {("500", "curso3"), ("1000", "curso4")}
    assert sel.content == expected


def test_selection3():
    r = relation.Relation()
    r.header = ["curso", "precio"]
    data = {
        ("curso1", "400"),
        ("curso2", "104"),
        ("curso3", "500"),
        ("curso4", "1000"),
        ("curso5", "200"),
    }
    for d in data:
        r.insert(d)
    assert r.cardinality() == 5
    assert r.degree() == 2
    sel = r.select("precio > 400")
    expected = {("curso3", "500"), ("curso4", "1000")}
    assert sel.content == expected


def test_selection_syntax_error(relation_fixture):
    # TODO
    pass


def test_combination(relation_fixture):
    r1, r2, _ = relation_fixture
    join_natural = r1.njoin(r2)
    projection = join_natural.project("name", "skill")
    expected = {("Gabriel", "Python"), ("Rodrigo", "Games"), ("Mercedes", "Rocas")}
    assert projection.cardinality() == 3
    assert projection.degree() == 2
    assert projection.content == expected


def test_product(relation_fixture):
    expected = {
        ("1", "Gabriel", "Belén", "2015-12-12"),
        ("1", "Gabriel", "Belén", "2012-07-09"),
        ("1", "Gabriel", "Belén", "1998-12-09"),
        ("23", "Rodrigo", "Belén", "2015-12-12"),
        ("23", "Rodrigo", "Belén", "2012-07-09"),
        ("23", "Rodrigo", "Belén", "1998-12-09"),
        ("12", "Mercedes", "Las Juntas", "2015-12-12"),
        ("12", "Mercedes", "Las Juntas", "2012-07-09"),
        ("12", "Mercedes", "Las Juntas", "1998-12-09"),
        ("2", "Diego", "Santiago del Estero", "2015-12-12"),
        ("2", "Diego", "Santiago del Estero", "2012-07-09"),
        ("2", "Diego", "Santiago del Estero", "1998-12-09"),
    }
    r1, _, r3 = relation_fixture
    product = r1.product(r3)
    assert product.cardinality() == 12
    assert product.degree() == 4
    assert product.content == expected


def test_product_duplicate_field_error(relation_fixture):
    _, r2, _ = relation_fixture
    r1 = relation.Relation()
    r1.header = ["algo", "skill"]  # skill duplicado!
    with pytest.raises(relation.DuplicateFieldError):
        r1.product(r2)


def test_njoin(relation_fixture):
    r1, r2, _ = relation_fixture
    expected = {
        ("1", "Gabriel", "Belén", "Python"),
        ("12", "Mercedes", "Las Juntas", "Rocas"),
        ("23", "Rodrigo", "Belén", "Games"),
    }
    r3 = r1.njoin(r2)
    assert r3.degree() == 4
    assert r3.content == expected
    assert r3.cardinality() == 3


def test_louter(relation_fixture):
    r1, r2, _ = relation_fixture
    expected = {
        ("1", "Gabriel", "Belén", "Python"),
        ("23", "Rodrigo", "Belén", "Games"),
        ("12", "Mercedes", "Las Juntas", "Rocas"),
        ("2", "Diego", "Santiago del Estero", "null"),
    }
    r = r1.louter(r2)
    assert r.degree() == 4
    assert r.cardinality() == 4
    assert r.content == expected


def test_router(relation_fixture):
    r1, r2, _ = relation_fixture
    expected = {
        ("3", "null", "null", "Ruby"),
        ("1", "Gabriel", "Belén", "Python"),
        ("12", "Mercedes", "Las Juntas", "Rocas"),
        ("23", "Rodrigo", "Belén", "Games"),
    }

    r = r1.router(r2)
    assert r.degree() == 4
    assert r.cardinality() == 4
    assert r.content == expected


def test_relation_compatible(relation_fixture):
    r1, r2, _ = relation_fixture
    with pytest.raises(relation.UnionCompatibleError):
        r1.intersect(r2)


def test_intersect():
    r1 = relation.Relation()
    r1.header = ["id", "name"]
    data = {("1", "Gabo"), ("2", "Rodrigo")}
    for d in data:
        r1.insert(d)
    r2 = relation.Relation()
    r2.header = ["id", "name"]
    data = {("1", "Gabo"), ("3", "Mercedes")}
    for d in data:
        r2.insert(d)
    expected = {("1", "Gabo")}
    assert r1.intersect(r2).content == expected


def test_fouther(relation_fixture):
    r1, r2, _ = relation_fixture
    expected = {
        ("1", "Gabriel", "Belén", "Python"),
        ("23", "Rodrigo", "Belén", "Games"),
        ("12", "Mercedes", "Las Juntas", "Rocas"),
        ("2", "Diego", "Santiago del Estero", "null"),
        ("3", "null", "null", "Ruby"),
    }

    r = r1.fouter(r2)
    assert r.degree() == 4
    assert r.cardinality() == 5
    assert r.content == expected


def test_difference():
    r = relation.Relation()
    r.header = ["patente"]
    data = {
        ("ass-002",),
        ("dde-456",),
        ("agt-303",),
        ("tsv-360",),
        ("k-23526",),
        ("cdd-479",),
        ("cdt-504",),
        ("exs-900",),
        ("beo-825",),
        ("afs-448",),
        ("fvj-530",),
        ("fvv-120",),
        ("gaa-589",),
    }
    for i in data:
        r.insert(i)
    r2 = relation.Relation()
    r2.header = ["patente"]
    data = {
        ("dde-456",),
        ("dde-456",),
        ("beo-825",),
        ("k-23526",),
        ("gaa-589",),
        ("ass-002",),
        ("ass-002",),
        ("fvj-530",),
        ("tsv-360",),
        ("tsv-360",),
        ("cdt-504",),
        ("cdt-504",),
    }
    for i in data:
        r2.insert(i)
    expected = {("agt-303",), ("cdd-479",), ("exs-900",), ("afs-448",), ("fvv-120",)}
    assert r.cardinality() == 13
    new = r.difference(r2)
    assert new.content == expected
    assert new.cardinality() == 5


def test_update_relation():
    r = relation.Relation()
    r.header = ["id", "name"]
    r.content.add(("21", "Rodrigo"))
    r.content.add(("1", "gabox"))

    expected = relation.OrderedSet([("21", "Rodrigo"), ("1", "Gabriel")])

    r.update(1, 1, "Gabriel")

    assert r.content == expected


def test_append_row():
    r = relation.Relation()
    r.header = ["id", "name"]
    r.content.add(("21", "Rodrigo"))
    r.content.add(("1", "gabox"))

    expected = relation.OrderedSet(
        [
            ("21", "Rodrigo"),
            ("1", "gabox"),
            ("null (1)", "null (2)"),
            ("null (3)", "null (4)"),
        ]
    )

    r.append_row()
    r.append_row()

    assert r.content == expected


def test_str_repr():
    r = relation.Relation()
    r.name = "test_r"
    r.header = ["id", "name"]
    r.content.add(("21", "Rodrigo"))

    expected_str = "|      id      |     name     |\n-------------------------------\n|      21      |   Rodrigo    |\n"
    expected_repr = "Relation(name=test_r, degree=2, cardinality=1)"
    assert r.__str__() == expected_str
    assert r.__repr__() == expected_repr


# import pytest
#
# from pireal.core import relation
#
#
# @pytest.fixture
# def relation_fixture():
#     r1 = relation.Relation()
#     r1.header = ["id", "name", "city"]
#     data = {
#         ("1", "Gabriel", "Belén"),
#         ("23", "Rodrigo", "Belén"),
#         ("12", "Mercedes", "Las Juntas"),
#         ("2", "Diego", "Santiago del Estero")
#     }
#     for d in data:
#         r1.insert(d)
#
#     r2 = relation.Relation()
#     r2.header = ["id", "skill"]
#     data = {
#         ("3", "Ruby"),
#         ("1", "Python"),
#         ("12", "Rocas"),
#         ("23", "Games")
#     }
#     for d in data:
#         r2.insert(d)
#
#     r3 = relation.Relation()
#     r3.header = ["date"]
#     data = {
#         ("2015-12-12"),
#         ("2012-07-09"),
#         ("1998-12-09")
#     }
#     for d in data:
#         r3.insert(d)
#     return r1, r2, r3
#
#
# def test_valid_header():
#     r = relation.Relation()
#     with pytest.raises(relation.InvalidFieldNameError):
#         r.header = ["id", "nombre foo", "skills"]
#
#
# def test_cardinality():
#     r = relation.Relation()
#     r.header = ["id", "nombre"]
#     for i in {("1", "gabriel"), ("3", "rodrigo"), ("2", "mechi")}:
#         r.insert(i)
#     assert r.cardinality() == 3
#
#
# def test_wrong_size_relation():
#     r = relation.Relation()
#     r.header = ["aaa", "bbb"]
#     data = {
#         ("a", "b", "c", "d"),
#         ("e", "f", "g", "h")
#     }
#     with pytest.raises(relation.WrongSizeError):
#         for d in data:
#             r.insert(d)
#
#
# def test_projection(relation_fixture):
#     # r1 projection
#     r1, _, r3 = relation_fixture
#     expected = {("Gabriel",), ("Rodrigo",), ("Mercedes",), ("Diego",)}
#     assert r1.project("name").content == expected
#     expected = {("2015-12-12",), ("2012-07-09",), ("1998-12-09",)}
#     assert r3.project("date").content == expected
#
#
# def test_invalid_field_in_projection(relation_fixture):
#     # r2 projection
#     _, r2, _ = relation_fixture
#     with pytest.raises(relation.FieldNotInHeaderError):
#         r2.project("cualquiera")
#
#
# def test_selection(relation_fixture):
#
#     r1, _, _ = relation_fixture
#     expected = {("23", "Rodrigo", "Belén")}
#     assert r1.select("id==23").content == expected
#
#
# def test_selection2():
#     r = relation.Relation()
#     r.header = ["precio", "curso"]
#     data = {
#         ("400", "curso1"),
#         ("104", "curso2"),
#         ("500", "curso3"),
#         ("1000", "curso4"),
#         ("200", "curso5")
#     }
#     for d in data:
#         r.insert(d)
#     assert r.cardinality() == 5
#     assert r.degree() == 2
#     sel = r.select("precio > 400")
#     expected = {("500", "curso3"), ("1000", "curso4")}
#     assert sel.content == expected
#
#
# def test_selection3():
#     r = relation.Relation()
#     r.header = ["curso", "precio"]
#     data = {
#         ("curso1", "400"),
#         ("curso2", "104"),
#         ("curso3", "500"),
#         ("curso4", "1000"),
#         ("curso5", "200")
#     }
#     for d in data:
#         r.insert(d)
#     assert r.cardinality() == 5
#     assert r.degree() == 2
#     sel = r.select("precio > 400")
#     expected = {("curso3", "500"), ("curso4", "1000")}
#     assert sel.content == expected
#
#
# def test_selection_syntax_error(relation_fixture):
#     # TODO
#     pass
#
#
# def test_combination(relation_fixture):
#     r1, r2, r3 = relation_fixture
#     join_natural = r1.njoin(r2)
#     projection = join_natural.project("name", "skill")
#     expected = {
#         ("Gabriel", "Python"),
#         ("Rodrigo", "Games"),
#         ("Mercedes", "Rocas")
#     }
#     assert projection.cardinality() == 3
#     assert projection.degree() == 2
#     assert projection.content == expected
#
#
# def test_product(relation_fixture):
#     expected = {
#         ("1", "Gabriel", "Belén", "2015-12-12"),
#         ("1", "Gabriel", "Belén", "2012-07-09"),
#         ("1", "Gabriel", "Belén", "1998-12-09"),
#         ("23", "Rodrigo", "Belén", "2015-12-12"),
#         ("23", "Rodrigo", "Belén", "2012-07-09"),
#         ("23", "Rodrigo", "Belén", "1998-12-09"),
#         ("12", "Mercedes", "Las Juntas", "2015-12-12"),
#         ("12", "Mercedes", "Las Juntas", "2012-07-09"),
#         ("12", "Mercedes", "Las Juntas", "1998-12-09"),
#         ("2", "Diego", "Santiago del Estero", "2015-12-12"),
#         ("2", "Diego", "Santiago del Estero", "2012-07-09"),
#         ("2", "Diego", "Santiago del Estero", "1998-12-09")
#     }
#     r1, _, r3 = relation_fixture
#     product = r1.product(r3)
#     assert product.cardinality() == 12
#     assert product.degree() == 4
#     assert product.content == expected
#
#
# def test_product_duplicate_field_error(relation_fixture):
#     _, r2, _ = relation_fixture
#     r1 = relation.Relation()
#     r1.header = ['algo', 'skill']  # skill duplicado!
#     with pytest.raises(relation.DuplicateFieldError):
#         r1.product(r2)
#
#
# def test_njoin(relation_fixture):
#
#     r1, r2, _ = relation_fixture
#     expected = {
#         ("1", "Gabriel", "Belén", "Python"),
#         ("12", "Mercedes", "Las Juntas", "Rocas"),
#         ("23", "Rodrigo", "Belén", "Games")
#     }
#     r3 = r1.njoin(r2)
#     assert r3.degree() == 4
#     assert r3.content == expected
#     assert r3.cardinality() == 3
#
#
# def test_louter(relation_fixture):
#     r1, r2, _ = relation_fixture
#     expected = {
#         ("1", "Gabriel", "Belén", "Python"),
#         ("23", "Rodrigo", "Belén", "Games"),
#         ("12", "Mercedes", "Las Juntas", "Rocas"),
#         ("2", "Diego", "Santiago del Estero", "null")
#     }
#     r = r1.louter(r2)
#     assert r.degree() == 4
#     assert r.cardinality() == 4
#     assert r.content == expected
#
#
# def test_router(relation_fixture):
#     r1, r2, _ = relation_fixture
#     expected = {
#         ("3", "null", "null", "Ruby"),
#         ("1", "Gabriel", "Belén", "Python"),
#         ("12", "Mercedes", "Las Juntas", "Rocas"),
#         ("23", "Rodrigo", "Belén", "Games")
#     }
#
#     r = r1.router(r2)
#     assert r.degree() == 4
#     assert r.cardinality() == 4
#     assert r.content == expected
#
#
# def test_relation_compatible(relation_fixture):
#     r1, r2, _ = relation_fixture
#     with pytest.raises(relation.UnionCompatibleError):
#         r1.intersect(r2)
#
#
# def test_intersect():
#     r1 = relation.Relation()
#     r1.header = ['id', 'name']
#     data = {
#         ("1", "Gabo"),
#         ("2", "Rodrigo")
#     }
#     for d in data:
#         r1.insert(d)
#     r2 = relation.Relation()
#     r2.header = ['id', 'name']
#     data = {
#         ("1", "Gabo"),
#         ("3", "Mercedes")
#     }
#     for d in data:
#         r2.insert(d)
#     expected = {("1", "Gabo")}
#     assert r1.intersect(r2).content == expected
#
#
# def test_fouther(relation_fixture):
#     r1, r2, _ = relation_fixture
#     expected = {
#         ("1", "Gabriel", "Belén", "Python"),
#         ("23", "Rodrigo", "Belén", "Games"),
#         ("12", "Mercedes", "Las Juntas", "Rocas"),
#         ("2", "Diego", "Santiago del Estero", "null"),
#         ("3", "null", "null", "Ruby")
#     }
#
#     r = r1.fouter(r2)
#     assert r.degree() == 4
#     assert r.cardinality() == 5
#     assert r.content == expected
#
#
# def test_difference():
#     r = relation.Relation()
#     r.header = ["patente"]
#     data = {
#         ("ass-002",), ("dde-456",), ("agt-303",),
#         ("tsv-360",), ("k-23526",), ("cdd-479",),
#         ("cdt-504",), ("exs-900",), ("beo-825",),
#         ("afs-448",), ("fvj-530",), ("fvv-120",),
#         ("gaa-589",)
#     }
#     for i in data:
#         r.insert(i)
#     r2 = relation.Relation()
#     r2.header = ["patente"]
#     data = {
#         ("dde-456",), ("dde-456",), ("beo-825",),
#         ("k-23526",), ("gaa-589",), ("ass-002",),
#         ("ass-002",), ("fvj-530",), ("tsv-360",),
#         ("tsv-360",), ("cdt-504",), ("cdt-504",)
#     }
#     for i in data:
#         r2.insert(i)
#     expected = {
#         ("agt-303",), ("cdd-479",), ("exs-900",),
#         ("afs-448",), ("fvv-120",)
#     }
#     assert r.cardinality() == 13
#     new = r.difference(r2)
#     assert new.content == expected
#     assert new.cardinality() == 5
#
#
# def test_str(relation_fixture):
#     _, _, r3 = relation_fixture
#     expected = ("|     date     |\n"
#                 "----------------\n"
#                 "|  2012-07-09  |\n"
#                 "|  1998-12-09  |\n"
#                 "|  2015-12-12  |\n")
#     # assert str(r3) == expected
#     # FIXME: el orden
