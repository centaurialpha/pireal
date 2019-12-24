import pytest
from unittest import mock

from pireal.gui.query_container import EditorWidget


@pytest.fixture
def editor_widget(qtbot):
    w = EditorWidget(None)
    return w


@pytest.mark.gui
def test_initial_state(editor_widget):
    assert not editor_widget.has_editors()


@pytest.mark.gui
def test_create_editor(editor_widget):
    m = mock.Mock(display_name='foo', path='/path/to/foo.txt')
    w = editor_widget.create_editor(m)

    assert editor_widget.has_editors()
    assert w.file is m


@pytest.mark.gui
def test_get_editor_by_filename(editor_widget):
    m1 = mock.Mock(display_name='foo', path='/path/to/foo.txt')
    m2 = mock.Mock(display_name='bar', path='/path/to/bar.txt')

    w1 = editor_widget.create_editor(m1)
    w2 = editor_widget.create_editor(m2)

    ew2 = editor_widget.get_editor_by_filename('/path/to/bar.txt')
    ew1 = editor_widget.get_editor_by_filename('/path/to/foo.txt')

    assert ew2 == w2
    assert ew1 == w1


@pytest.mark.gui
def test_get_editr_by_index(editor_widget):
    m1 = mock.Mock(display_name='foo', path='/path/to/foo.txt')
    m2 = mock.Mock(display_name='bar', path='/path/to/bar.txt')

    w1 = editor_widget.create_editor(m1)
    w2 = editor_widget.create_editor(m2)

    ew1 = editor_widget.get_editor_by_index(1)
    ew2 = editor_widget.get_editor_by_index(0)
    none = editor_widget.get_editor_by_index(3)

    assert ew1 == w2
    assert ew2 == w1
    assert none is None


@pytest.mark.gui
def test_is_editor_open(editor_widget):
    m1 = mock.Mock(display_name='foo', path='/path/to/foo.txt')
    m2 = mock.Mock(display_name='bar', path='/path/to/bar.txt')

    assert not editor_widget.is_open(m1)

    editor_widget.create_editor(m1)
    editor_widget.create_editor(m2)

    assert editor_widget.is_open(m1)
    assert editor_widget.is_open(m2)


@pytest.mark.gui
def test_remove_editor(editor_widget):
    m1 = mock.Mock(display_name='foo', path='/path/to/foo.txt')
    m2 = mock.Mock(display_name='bar', path='/path/to/bar.txt')

    w1 = editor_widget.create_editor(m1)
    w2 = editor_widget.create_editor(m2)

    assert len(editor_widget.editors()) == 2

    editor_widget.remove(w1)

    assert len(editor_widget.editors()) == 1
    assert editor_widget.editors()[0] == w2


@pytest.mark.gui
def test_remove_others(editor_widget):
    m1 = mock.Mock(display_name='foo', path='/path/to/foo.txt')
    m2 = mock.Mock(display_name='bar', path='/path/to/bar.txt')
    m3 = mock.Mock(display_name='foobar', path='/path/to/foobar.py')
    m4 = mock.Mock(display_name='barfoo', path='/path/to/barfoo.pdb')

    editor_widget.create_editor(m1)
    editor_widget.create_editor(m2)
    w3 = editor_widget.create_editor(m3)
    editor_widget.create_editor(m4)

    assert len(editor_widget.editors()) == 4

    editor_widget.set_current_editor(w3)

    editor_widget.remove_others()

    assert len(editor_widget.editors()) == 1
    assert editor_widget.editors()[0] == w3


@pytest.mark.gui
def test_remove_all(editor_widget, qtbot):
    m1 = mock.Mock(display_name='foo', path='/path/to/foo.txt')
    m2 = mock.Mock(display_name='bar', path='/path/to/bar.txt')

    editor_widget.create_editor(m1)
    editor_widget.create_editor(m2)

    assert len(editor_widget.editors()) == 2

    with qtbot.waitSignal(editor_widget.allTabsClosed):
        editor_widget.remove_all()

    assert len(editor_widget.editors()) == 0


@pytest.mark.gui
def test_on_modification_changed(editor_widget, qtbot):
    m1 = mock.Mock(display_name='foo', path='/path/to/foo.txt')

    w1 = editor_widget.create_editor(m1)

    assert editor_widget._tabs_editor.tabText(0) == 'foo'

    with qtbot.waitSignal(w1.modificationChanged) as blocker:
        qtbot.keyClicks(w1, 'escribiendo algo')

    assert blocker.args == [True]
    assert editor_widget._tabs_editor.tabText(0) == '● foo'
