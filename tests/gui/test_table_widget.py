import pytest
from unittest import mock

from pireal.gui.table_widget import TableWidget


@pytest.fixture
def table_widget(qtbot):
    tw = TableWidget(parent=None)
    tw._relations['a'] = 'aa'
    tw._relations['b'] = 'bb'
    return tw


@pytest.mark.gui
def test_correct_initialize_with_empty_widget(qtbot, table_widget):
    assert table_widget.count_table_relations() == 1
    assert table_widget.count_table_results() == 0


@pytest.mark.gui
def test_add_relation(qtbot, table_widget):
    with mock.patch('pireal.gui.table_widget.TableWidget.create_table') as mock_create_table:
        with mock.patch('PyQt5.QtWidgets.QStackedWidget.addWidget') as w:
            table_widget.add_relation(123, 'r1')
            # assert table_widget.count_table_relations() == 1
            # table_widget.add_relation(123, 'r2')
            # assert table_widget.count_table_relations() == 2
