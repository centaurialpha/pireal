import pytest

from pireal.core.ordered_set import OrderedSet


def test_len():
    os = OrderedSet()
    assert len(os) == 0
    os = OrderedSet([1, 54, 0, 94])
    assert len(os) == 4
    os = OrderedSet([1, 3, 3, 3, 3, 11, 11, 90])
    assert len(os) == 4


def test_order():
    os = OrderedSet([3, 5, 1])
    assert list(reversed(os)) == [1, 5, 3]
    os = OrderedSet()
    os.add(0)
    os.add(-3)
    os.add(5)
    assert list(reversed(os)) == [5, -3, 0]


def test_get_by_index():
    os = OrderedSet('argentina')
    assert os[3] == 'e'
    assert os[0] == 'a'


def test_get_by_index_after_update():
    os = OrderedSet('argentina')
    assert os[3] == 'e'
    assert os[0] == 'a'
    os[3] = 'E'
    os[0] = 'A'
    assert os[3] == 'E'
    assert os[0] == 'A'


def test_update():
    os = OrderedSet('gabox')
    assert os[3] == 'o'
    os[3] = 'x'
    assert os[3] == 'x'


def test_intersection():
    s1 = OrderedSet([3, 1])
    s2 = OrderedSet([3, 10])
    assert s1.intersection(s2) == [3]

    s1 = OrderedSet([3, 1, 8])
    s2 = OrderedSet([10, 2, 0, 5])
    assert s1.intersection(s2) == []


def test_union():
    s1 = OrderedSet([3, 1])
    s2 = OrderedSet([3, 10])
    assert s1.union(s2) == [3, 1, 10]
    assert s2.union(s1) == [3, 10, 1]


def test_difference():
    s1 = OrderedSet([3, 1])
    s2 = OrderedSet([3, 10])
    assert s1.difference(s2) == [1]
    assert s2.difference(s1) == [10]
