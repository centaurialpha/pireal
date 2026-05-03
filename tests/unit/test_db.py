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

from pireal.core.db import DB
from pireal.core.relation import Relation


@pytest.fixture
def db():
    return DB()


@pytest.fixture
def sample_relations():
    rel1 = Relation()
    rel1.name = "users"

    rel2 = Relation()
    rel2.name = "orders"

    return {"users": rel1, "orders": rel2}


def test_initial_state(db: DB):
    assert db.count == 0
    assert len(db) == 0
    assert not db.modified


def test_add_relation(db, sample_relations):
    db.add(sample_relations["users"])

    assert db.count == 1
    assert db.modified
    assert sample_relations["users"] in db.relations


@pytest.mark.parametrize("relation_name", ["users", "orders"])
def test_add_and_get_relation(db, sample_relations, relation_name):
    db.add(sample_relations[relation_name])
    relation = db.get(relation_name)
    assert relation == sample_relations[relation_name]


def test_add_duplicate_relation(db, sample_relations):
    db.add(sample_relations["users"])

    duplicate = Relation()
    duplicate.name = "users"

    db.add(duplicate)

    assert db.count == 1


@pytest.mark.parametrize("relation_name", ["users", "orders"])
def test_remove_relation(db, sample_relations, relation_name):
    db.add(sample_relations[relation_name])

    db.remove(relation_name)

    assert db.count == 0


def test_clear_query_results(db, sample_relations):
    db.add(sample_relations["users"])
    db.add(sample_relations["orders"])
    assert db.count == 2

    result = Relation()
    result.name = "q1"
    db.load(result)
    db.add_query_result("q1")
    assert db.count == 3

    db.clear_query_results()
    assert db.count == 2


def test_db_file_is_none_by_default(db):
    assert db.file is None
    assert db.is_new


def test_db_file_setter(db, tmp_path):
    from pireal.core.pireal_file import File

    f = File(str(tmp_path / "test.pdb"))
    db.file = f
    assert db.file is f
    assert not db.is_new


def test_db_save(db, tmp_path):
    from pireal.core.pireal_file import File

    filepath = tmp_path / "test.pdb"
    db.file = File(str(filepath))

    r = Relation()
    r.name = "personas"
    r.header = ["id", "nombre"]
    r.insert(("1", "Gabriel"))
    db.load(r)

    result = db.save()
    assert result
    assert not db.modified
    assert filepath.exists()


def test_remove_emits_relations_changed(qtbot):
    db = DB()
    r = Relation()
    r.name = "estudiantes"
    r.header = ["id", "nombre"]
    db.load(r)

    with qtbot.waitSignal(db.relationsChanged) as blocker:
        db.remove("estudiantes")

    assert blocker.args == [[]]
