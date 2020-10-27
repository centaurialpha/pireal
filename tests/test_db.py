import os
import pytest

from pireal.core.db import DB, RelationNotFound

from ordered_set import OrderedSet


class FakeRelation:

    def __init__(self, name):
        self.name = name


def test_add_relation():
    r1 = FakeRelation('r1')
    r2 = FakeRelation('r2')

    db = DB()
    db.add(r1)
    db.add(r2)

    assert len(db) == 2


def test_add_relation_name_error():
    r1 = FakeRelation('r1')
    r2 = FakeRelation('r1')

    db = DB()
    db.add(r1)

    with pytest.raises(NameError) as exc:
        db.add(r2)

    assert str(exc.value) == 'Relation r1 already exist'


def test_is_dirty_or_not():
    r1 = FakeRelation('r1')

    db = DB()
    assert not db.dirty

    db.add(r1)
    assert db.dirty


def test_get_relation():
    r1 = FakeRelation('r1')
    r2 = FakeRelation('r2')

    db = DB()
    db.add(r1)
    db.add(r2)

    assert db.get('r2') == r2
    assert db.get('r1') == r1


def test_get_relation_name_error():
    r1 = FakeRelation('r1')
    db = DB()
    db.add(r1)

    with pytest.raises(RelationNotFound) as exc:
        db.get('r2')

    assert str(exc.value) == 'Relation r2 not found'


def test_remove_relation():
    r1 = FakeRelation('r1')
    r2 = FakeRelation('r2')

    db = DB()
    db.add(r1)
    db.add(r2)

    assert len(db) == 2
    db.remove('r2')
    assert len(db) == 1
    assert db.get('r1') == r1

    with pytest.raises(RelationNotFound):
        db.get('r2')

    db.remove('r1')
    assert len(db) == 0


def test_remove_relation_name_error():
    r1 = FakeRelation('r1')

    db = DB()
    db.add(r1)

    with pytest.raises(RelationNotFound) as exc:
        db.remove('r2')

    assert str(exc.value) == 'Relation r2 not found'


def test_load_from_file(tmpdir):
    text = (
        '@programmers:id,name\n'
        '1,gabox\n2,chino\n3,salteño\n\n'
        '@skills:id,skill\n'
        '2,django\n1,python\n3,mobile\n'
    )
    fh = tmpdir.join('db_example.pdb')
    fh.write(text)

    db = DB.load_from_file(fh)

    assert len(db) == 2
    assert db.display_name == 'db_example.pdb'


def test_write_to_file(tmpdir):
    dst = tmpdir.join('db_example.pdb')

    r1 = FakeRelation('r1')
    r1.header = ['id', 'name']
    r1.content = OrderedSet([('1', 'gabox'), ('2', 'rodrigo'), ('3', 'mechi')])
    r2 = FakeRelation('r2')
    r2.header = ['id', 'skill']
    r2.content = OrderedSet([('3', 'rocks'), ('2', 'games'), ('1', 'python')])

    db = DB()
    for relation in (r1, r2):
        db.add(relation)
    # FIXME: considerar pasar el filepath a DB, testear bien la creación!
    db.write_to_file(dst_path=dst)

    # verify if file exist
    assert os.path.exists(db.file.path)

    expected_content = (
        '@r1:id,name\n'
        '1,gabox\n'
        '2,rodrigo\n'
        '3,mechi\n\n'
        '@r2:id,skill\n'
        '3,rocks\n'
        '2,games\n'
        '1,python'
    )
    # verify content
    with open(db.file.path) as fh:
        assert fh.read() == expected_content
