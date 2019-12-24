import pytest

from pireal.gui.relation_widget import RelationWidget
from pireal.gui.model_view_delegate import View


class FakeRelation(object):

    header = ['algo']

    def degree(self):
        return 1

    def cardinality(self):
        return 2


@pytest.fixture
def relation_widget_fixture(qtbot):
    w = RelationWidget()
    qtbot.addWidget(w)
    return w


@pytest.mark.gui
def test_add_view(relation_widget_fixture):
    r = FakeRelation()
    assert relation_widget_fixture.count() == 0
    relation_widget_fixture.add_view(r)
    assert relation_widget_fixture.count() == 1


def test_current_view(relation_widget_fixture):
    r = FakeRelation()
    r2 = FakeRelation()
    relation_widget_fixture.add_view(r)
    relation_widget_fixture.add_view(r2)
    current = relation_widget_fixture.current_view()
    assert isinstance(current, View)
    assert current.model().relation == r2


def test_set_current_index(relation_widget_fixture):
    r1 = FakeRelation()
    r2 = FakeRelation()
    r3 = FakeRelation()
    relation_widget_fixture.add_view(r1)
    relation_widget_fixture.add_view(r2)
    relation_widget_fixture.add_view(r3)

    assert relation_widget_fixture._stack.currentIndex() == 2
    relation_widget_fixture.set_current_index(0)
    assert relation_widget_fixture._stack.currentIndex() == 0
