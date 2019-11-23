from unittest import mock
import pytest

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
    dialog = NewRelationDialog()
    dialog.table.setHorizontalHeaderLabels(['id', 'name'])
    qtbot.addWidget(dialog)

    relation = Relation()
    relation.header = ['id', 'name']
    relation.insert('Value_0 Value_1')

    with mock.patch('pireal.gui.dialogs.new_relation_dialog.QMessageBox.warning') as mock_msg_box:
        mock_msg_box.assert_not_called()
        relation_result = dialog.create_relation()
        assert relation.header == relation_result.header
        assert relation.content == relation_result.content
