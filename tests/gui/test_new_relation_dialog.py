from unittest import mock
import pytest

from src.gui.dialogs.new_relation_dialog import NewRelationDialog


@pytest.fixture
def dialog():
    module = 'src.gui.view.CONFIG.get'
    with mock.patch(module):
        w = NewRelationDialog()
        return w


@pytest.mark.testgui
@pytest.mark.parametrize(
    'row_to_insert, expected',
    [
        (1, 1),
        (3, 3),
        (44, 44)
    ]
)
def test_add_tuple(qtbot, dialog, row_to_insert, expected):
    qtbot.addWidget(dialog)
    for i in range(row_to_insert):
        dialog._NewRelationDialog__add_tuple()
    assert dialog._view.model().rowCount() == expected


@pytest.mark.testgui
@pytest.mark.parametrize(
    'columns_to_insert, expected',
    [
        (1, 3),  # Ya existen 2 columnas por defecto ('Field 1', 'Field 2')
        (3, 5),
        (41, 43)
    ]
)
def test_add_column(qtbot, dialog, columns_to_insert, expected):
    qtbot.addWidget(dialog)
    for i in range(columns_to_insert):
        dialog._NewRelationDialog__add_column()
    assert dialog._view.model().columnCount() == expected

@pytest.mark.testgui
@pytest.mark.parametrize(
    'columns_to_insert, to_delete, expected',
    [
        (0, 1, 2),
        (3, 1, 4),
        (10, 6, 6)
    ]
)
def test_delete_column(qtbot, dialog, columns_to_insert, to_delete, expected):
    qtbot.addWidget(dialog)
    for _ in range(columns_to_insert):
        dialog._NewRelationDialog__add_column()
    for _ in range(to_delete):
        dialog._NewRelationDialog__delete_column()

    assert dialog._view.model().columnCount() == expected
