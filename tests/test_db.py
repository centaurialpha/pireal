import os
from unittest import mock
import pytest

from pireal.core.db import DB, DBFileNotFoundError, DBSyntaxError


class MockedRelation:
    pass


@pytest.fixture
def db():
    db = DB()
    r1 = MockedRelation()
    r1.name = 'r1'
    r2 = MockedRelation()
    r2.name = 'r2'
    r3 = MockedRelation()
    r3.name = 'r3'
    db.add(r1)
    db.add(r2)
    db.add(r3)
    return db


def test_add_relation():
    db = DB()
    assert len(db) == 0
    r1 = MockedRelation()
    r1.name = 'r1'
    db.add(r1)
    assert len(db) == 1


def test_get_relations():
    db = DB()
    max_relations = 100

    for i in range(max_relations):
        mock_relation = mock.Mock(name=f'relation_{i}')
        db.add(mock_relation)

    assert len(db.relations) == max_relations


def test_add_relation_with_raise_relation_exist(db):
    other = MockedRelation()
    other.name = 'r1'
    with pytest.raises(NameError):
        db.add(other)


def test_remove_relation(db):
    assert len(db) == 3
    db.remove_from_name('r2')
    db.remove_from_name('asdasdasd')
    assert len(db) == 2
    assert 'r2' not in db
    assert db.is_dirty()


def test_get_relation(db):
    assert db.give_relation('r1').name == 'r1'
    assert db.give_relation('r3').name == 'r3'
    assert db['r2'].name == 'r2'
    with pytest.raises(NameError):
        db.give_relation('r4')


def test_save(tmpdir):
    fh = tmpdir.join('db_example.pdb')
    fh2 = tmpdir.join('db_example_2.pdb')
    db = DB(path=fh)
    r1 = MockedRelation()
    r1.name = 'r1'
    r1.header = ['id', 'name']
    r1.content = {('1', 'gabox'), ('2', 'rodrigo'), ('3', 'mechi')}
    db.add(r1)
    assert db.is_dirty()
    with mock.patch('pireal.core.db.generate_database') as mock_gen_db:
        mock_gen_db.return_value = 'algo'
        db.save()
        assert not db.is_dirty()
        assert os.path.exists(db.file.path)
        db.save(file_path=fh2)
        assert db.file.path == fh2
        assert os.path.exists(db.file.path)


def test_create_from_file(tmpdir):
    text = (
        '@programmers:id,name\n'
        '1,gabox\n2,chino\n3,salteño\n\n'
        '@skills:id,skill\n'
        '2,django\n1,python\n3,mobile\n'
    )
    fh = tmpdir.join('db_example.db')
    fh.write(text)

    db = DB.create_from_file(fh)

    assert db.display_name() == 'db_example.db'
    assert db.relation_names == ('programmers', 'skills')


def test_create_from_file_fail_to_read():
    fake_file = 'not_exists.pdb'

    with pytest.raises(DBFileNotFoundError):
        DB.create_from_file(fake_file)
