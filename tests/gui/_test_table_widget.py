import pytest
from unittest import mock

from pireal.gui.table_widget import TableWidget
from PyQt5.QtWidgets import QWidget
from pireal.core.relation import Relation


class MockRelation:
    pass


@pytest.mark.gui
def test_correct_initialize_with_empty_widget(qtbot):
    table_widget = TableWidget()
    qtbot.addWidget(table_widget)
    assert table_widget.count() == 1
    assert table_widget._relation_stack.widget(0) == table_widget._empty_widget


@pytest.mark.gui
def test_add_relation(qtbot):
    table_widget = TableWidget()
    qtbot.addWidget(table_widget)

    r1 = MockRelation()
    r1.name = 'r1'
    r2 = MockRelation()
    r2.name = 'r2'
    r3 = MockRelation()
    r3.name = 'r3'
    r4 = MockRelation()
    r4.name = 'r4'

    with mock.patch('pireal.gui.table_widget.TableWidget.create_table') as mock_create_table:
        mock_create_table.side_effect = [QWidget() for _ in range(4)]
        assert table_widget.count() == 1
        table_widget.add_relation(r1)
        assert table_widget.count() == 1
        table_widget.add_relation(r2)
        assert table_widget.count() == 2
        table_widget.add_relation(r3)
        table_widget.add_relation(r4)
        assert table_widget.count() == 4


@pytest.mark.gui
def test_remove_relation(qtbot):
    table_widget = TableWidget()
    qtbot.addWidget(table_widget)

    r1 = Relation()
    r1.name = 'r1'
    r2 = Relation()
    r2.name = 'r2'
    r3 = Relation()
    r3.name = 'r3'
    r4 = Relation()
    r4.name = 'r4'

    table_widget.add_relation(r1)
    table_widget.add_relation(r2)
    table_widget.add_relation(r3)
    table_widget.add_relation(r4)
    table_widget.remove_relation(2)
    assert table_widget.count() == 3
    table_widget.remove_relation(0)
    table_widget.remove_relation(1)
    assert table_widget.count() == 1
    assert r2 in table_widget._relations
    table_widget.remove_relation(0)
    assert table_widget.count() == 1
    assert table_widget._relation_stack.widget(0) == table_widget._empty_widget


@pytest.mark.gui
def test_results(qtbot):
    table_widget = TableWidget()
    qtbot.addWidget(table_widget)

    r1 = MockRelation()
    r1.name = 'r1'
    r2 = MockRelation()
    r2.name = 'r2'

    with mock.patch('pireal.gui.table_widget.TableWidget.create_table') as mock_create_table:
        mock_create_table.side_effect = [QWidget() for _ in range(3)]
        table_widget.add_relation_to_results(r1)
        table_widget.add_relation_to_results(r2)
        assert table_widget.count_results() == 2
        table_widget.add_relation_to_results(r2)
        assert table_widget.count_results() == 2

        table_widget.clear_results()
        assert table_widget.count_results() == 0
