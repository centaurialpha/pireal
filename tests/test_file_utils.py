import os
import pytest

from pireal.core import file_utils


def test_read_file(tmpdir):
    fh = tmpdir.join('file_example.txt')
    fh.write('gélooÚuuu\n')
    assert file_utils.read_file(fh.strpath) == 'gélooÚuuu\n'


def test_write_file(tmpdir):
    fh = tmpdir.join('file_example.pdb')
    content = 'this\nis\nan\nexámplñeró'
    file_utils.write_file(fh.strpath, content)

    assert os.path.exists(fh.strpath)

    with open(fh) as f:
        assert f.read() == content


@pytest.mark.parametrize(
    'filepath, expected_basename',
    [
        ('/home/gabox/mi_archivo.algo', 'mi_archivo.algo'),
        ('/path/to/file.txt', 'file.txt'),
        ('file_sin_path.pdb', 'file_sin_path.pdb')
    ]
)
def test_get_basename(filepath, expected_basename):
    assert file_utils.get_basename(filepath) == expected_basename
