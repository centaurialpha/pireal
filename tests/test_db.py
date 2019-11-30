import pytest
from unittest import mock

from pireal.core.db import DB


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
    assert len(db) == 2
    assert 'r2' not in db
    assert db.is_dirty()


def test_new_db():
    db = DB()
    assert db.is_new()


def test_is_no_new(tmpdir):
    fh = tmpdir.join('db_example.pdb')
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
    db.save()
    assert not db.is_dirty()
    expected = "@r1:id,name\n1,gabox\n2,rodrigo\n3,mechi"
    with open(fh) as fp:
        content = fp.read()
    assert content == expected
