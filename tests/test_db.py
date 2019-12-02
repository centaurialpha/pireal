import os
from unittest import mock
import pytest

from pireal.core.db import DB, DBIOError


class MockedRelation:
    pass


def test_add_relation():
    db = DB()
    assert len(db) == 0
    r1 = MockedRelation()
    db.add('r1', r1)
    assert len(db) == 1


def test_add_relation_with_raise_relation_exist():
    db = DB()
    r1 = MockedRelation()
    r2 = MockedRelation()
    r3 = MockedRelation()
    db.add('r1', r1)
    db.add('r2', r2)
    with pytest.raises(NameError):
        db.add('r1', r3)


def test_remove_relation():
    db = DB()
    r1 = MockedRelation()
    r2 = MockedRelation()
    r3 = MockedRelation()
    db.add('r1', r1)
    db.add('r2', r2)
    db.add('r3', r3)
    assert len(db) == 3
    db.remove_from_name('r2')
    db.remove_from_name('asdasdasd')
    assert len(db) == 2
    assert 'r2' not in db
    assert db.is_dirty()


def test_new_db(tmpdir):
    db = DB()
    assert db.is_new()
    db = DB(path='/path/no/existe')
    assert db.is_new()
    fh = tmpdir.join('test')
    fh.write('algo')
    db = DB(path=fh)
    assert not db.is_new()


def test_display_name(tmpdir):
    fh = tmpdir.join('db_example.pdb')
    db = DB(path=fh)
    with mock.patch('pireal.core.db.get_basename_with_extension') as mock_basename:
        db.display_name()
        mock_basename.assert_called_with(fh)


def test_save(tmpdir):
    fh = tmpdir.join('db_example.pdb')
    db = DB(path=fh)
    r1 = MockedRelation()
    r1.header = ['id', 'name']
    r1.content = {('1', 'gabox'), ('2', 'rodrigo'), ('3', 'mechi')}
    db.add('r1', r1)
    assert db.is_dirty()
    with mock.patch('pireal.core.db.generate_database') as mock_gen_db:
        mock_gen_db.return_value = 'algo'
        db.save()
        assert not db.is_dirty()
        assert os.path.exists(db.file_path())


def test_load(tmpdir):
    fh = tmpdir.join('db_example.pdb')
    fh.write('algo acá')

    db = DB(path=fh)
    with mock.patch('pireal.core.db.parse_database_content') as mock_parse_db:
        db.load()
        mock_parse_db.assert_called_with('algo acá')


def test_load_with_error(tmpdir):
    fh = tmpdir.join('db_example.pdb')
    fh.write('')
    db = DB()
    os.remove(fh)
    with pytest.raises(DBIOError):
        db.load(fh)
