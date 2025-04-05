import pytest

from pireal.core.relation import Relation
from pireal.core.db import DB


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

    db.eval_query("users.njoin(orders)", "q1")

    assert db.count == 3

    db.clear_query_results()

    assert db.count == 2
