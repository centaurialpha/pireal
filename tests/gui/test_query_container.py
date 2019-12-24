import pytest
from unittest import mock

from pireal.core.file_manager import File
from pireal.gui.query_container import QueryContainer


@pytest.fixture
def query_container(qtbot):
    w = QueryContainer(parent=None)
    qtbot.addWidget(w)
    return w


@pytest.mark.gui
def test_create_new_query_file(query_container):
    file = query_container.get_or_create_query_file()
    assert not query_container._queries
    assert isinstance(file, File)


@pytest.mark.gui
def test_create_new_query_file_with_filename(query_container, tmpdir):
    fh = tmpdir.join('test.file')
    fh.write('')
    file = query_container.get_or_create_query_file(filename=fh)
    assert query_container.get_or_create_query_file(filename=fh) == file
