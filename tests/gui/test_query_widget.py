import pytest

from pireal.gui.query_widget import QueryWidget

pytestmark = pytest.mark.gui


@pytest.fixture
def query_widget(qtbot):
    widget = QueryWidget()
    qtbot.addWidget(widget)
    return widget


def test_current_editor_returns_active_tab(query_widget):
    query_widget.create_editor()
    e2 = query_widget.create_editor()

    # e2 es el último agregado, debería ser el activo
    assert query_widget.current_editor() is e2


def test_current_editor_after_switching_tab(query_widget):
    e1 = query_widget.create_editor()
    e2 = query_widget.create_editor()

    # Cambiar al primero
    query_widget._editor_tabs.setCurrentWidget(e1)

    assert query_widget.current_editor() is e1
    assert query_widget.current_editor() is not e2


def test_current_editor_returns_none_when_empty(query_widget):
    assert query_widget.current_editor() is None
