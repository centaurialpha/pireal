import pytest

from pireal.core import file_manager
from pireal.core import relation


@pytest.mark.parametrize(
    'filename, expected',
    [
        ('/home/gabo/archivo.py', '.py'),
        ('/path/path/blabla/file.extension', '.extension'),
        ('/hola/como/estas/que_onda.qda', '.qda')
    ]
)
def test_get_extension(filename, expected):
    assert file_manager.get_extension(filename) == expected


@pytest.mark.parametrize(
    'filename, name',
    [
        ('/home/gabo/archivo.py', 'archivo'),
        ('/path/path/blabla/file.extension', 'file'),
        ('/hola/como/estas/que_onda.qda', 'que_onda')
    ]
)
def test_get_basename(filename, name):
    assert file_manager.get_basename(filename) == name


@pytest.mark.parametrize(
    'filename, path',
    [
        ('/home/gabo/archivo.py', '/home/gabo'),
        ('/path/path/blabla/file.extension', '/path/path/blabla'),
        ('/hola/como/estas/que_onda.qda', '/hola/como/estas')
    ]
)
def test_get_path(filename, path):
    assert file_manager.get_path(filename) == path


def test_get_files_from_folder(tmpdir):
    files = (
        'archivo.py',
        'archivo2.py',
        'archivo3.py'
    )
    assert len(tmpdir.listdir()) == 0
    for f in files:
        path = tmpdir.join(f)
        path.write("Some content")
    assert len(tmpdir.listdir()) == len(files)
    _files = file_manager.get_files_from_folder(tmpdir.strpath)
    assert len(_files) == len(files)


def test_generate_database():
    # FIXME: arreglar
    r = relation.Relation()
    r.header = ['id', 'name']
    data = {
        ("1", "Gabriel"),
        ("23", "Rodrigo")
    }
    for d in data:
        r.insert(d)

    relations = {'persona': r}
    expected = "@persona:id,name\n1,Gabriel\n23,Rodrigo\n"

    # assert expected in file_manager.generate_database(relations)
