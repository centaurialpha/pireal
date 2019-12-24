import os

import pytest

from pireal.core.file_manager import File


def test_is_new(tmpdir):
    f = File()
    assert f.is_new
    f = File(path='/path/no/existe')
    assert f.is_new
    fh = tmpdir.join('test')
    fh.write('algún contenido')
    f = File(path=fh)
    assert not f.is_new


@pytest.mark.parametrize(
    'filename, expected',
    [
        ('/path/to/file/mi_file.algo', 'mi_file.algo'),
        ('/hola/pirel/ueu/un_nombre_de_archivo_demasiado_largo.je', 'un_nombre_de_archivo_demasiado_largo.je'),
        (None, 'Untitled'),
    ]
)
def test_display_name_property(filename, expected):
    f = File(filename)
    assert f.display_name == expected


@pytest.mark.parametrize(
    'filename, expected',
    [
        ('/path/to/file/mi_file.algo', 'mi_file.algo'),
        ('/hola/pirel/ueu/un_nombre_de_archivo_demasiado_largo.je', 'un_nombre_de_archivo_demasiado_largo.je'),
        ('~/algo.pdb', 'algo.pdb')
    ]
)
def test_filename_property(filename, expected):
    f = File(filename)
    assert f.filename == expected


def test_save(tmpdir):
    fh = tmpdir.join('file_example.txt')
    fh2 = tmpdir.join('file_example_2.txt')
    f = File(path=fh)
    content = 'hóolá desde Pireal!'
    f.save(content)
    assert os.path.exists(f.path)
    f.save(content, path=fh2)
    assert f.path == fh2
    assert os.path.exists(f.path)

    with open(f.path) as fp:
        c = fp.read()
        assert c == content


def test_read(tmpdir):
    fh = tmpdir.join('file_example.txt')
    fh.write('gelouuuú')
    f = File(path=fh.strpath)
    content = f.read()
    assert content == 'gelouuuú'


def test_read_with_fileioerror(tmpdir):
    fh = tmpdir.join('file_example.txt')
    fh.write(' asdasd')
    f = File(path=fh.strpath)
    os.remove(fh)
    with pytest.raises(FileNotFoundError):
        f.read()
