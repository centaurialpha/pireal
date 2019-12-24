from unittest import mock
import pytest

from PyQt5.QtCore import Qt

from pireal.gui.dialogs.new_relation_dialog import NewRelationDialog
from pireal.core.relation import Relation
from pireal import translations as tr


@pytest.mark.gui
@pytest.mark.parametrize(
    'header',
    [['1', '2', '3'], ['  ', ' '], ['1ff', '-d']]
)
def test_create_relation_invalid_field_name(qtbot, header):
    dialog = NewRelationDialog()
    dialog.table.setHorizontalHeaderLabels(header)
    qtbot.addWidget(dialog)

    with mock.patch('pireal.gui.dialogs.new_relation_dialog.QMessageBox.warning') as mock_msg_box:
        assert dialog.create_relation() is None
        mock_msg_box.assert_called_with(
            None,
            'Error',
            'Invalid field name: {}'.format(header[0]))


@pytest.mark.gui
@pytest.mark.parametrize(
    'row, col',
    [(0, 1), (0, 0)]
)
def test_create_relation_missing_data(qtbot, row, col):
    dialog = NewRelationDialog()
    dialog.table.setHorizontalHeaderLabels(['id', 'name'])
    item = dialog.table.item(row, col)
    item.setText('        ')

    qtbot.addWidget(dialog)

    with mock.patch('pireal.gui.dialogs.new_relation_dialog.QMessageBox.warning') as mock_msg_box:
        assert dialog.create_relation() is None
        mock_msg_box.assert_called_with(
            None,
            'Error',
            tr.TR_RELATION_DIALOG_WHITESPACE.format(
                row + 1, col + 1))


@pytest.mark.gui
def test_create_relation(qtbot):
    relation_name = 'people'
    header = ['id', 'name']

    dialog = NewRelationDialog()
    dialog.table.setHorizontalHeaderLabels(header)
    qtbot.addWidget(dialog)

    qtbot.keyClicks(dialog.line_relation_name, relation_name)
    accept_btn = dialog.button_box.button(dialog.button_box.Ok)
    qtbot.mouseClick(accept_btn, Qt.LeftButton)

    # Expected result
    expected_relation = Relation()
    expected_relation.name = relation_name
    expected_relation.header = header
    expected_relation.insert('Value_0 Value_1')

    relation = dialog.get_data()

    assert relation.name == expected_relation.name
    assert relation.degree() == expected_relation.degree()
    assert relation.cardinality() == expected_relation.cardinality()
    assert relation.header == header
