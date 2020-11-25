import os

import pytest

from pireal.core.file_utils import File, FileNameError


@pytest.mark.parametrize(
    'path, expected',
    [
        (None, 'Untitled'),
        ('/home/path/to/thefile.txt', 'thefile.txt'),
        ('thefile.pdb', 'thefile.pdb'),
    ]
)
def test_displayname(monkeypatch, path, expected):
    monkeypatch.setattr(os, 'access', lambda *args: True)
    file = File(path=path)
    assert file.display_name == expected



@pytest.mark.parametrize(
    'path, expected',
    [
        ('/home/gabox/thefile.pdb', 'thefile.pdb (read-only)'),
        ('thefile.pdb', 'thefile.pdb (read-only)')
    ]
)
def test_display_name_read_only(monkeypatch, path, expected):
    monkeypatch.setattr(os, 'access', lambda *args: False)
    file = File(path=path)
    assert file.display_name == expected


def test_is_new(tmp_path):
    basedir = tmp_path / "test_is_new"
    basedir.mkdir()
    path = basedir / "test.pdb"

    file = File(path=path)
    assert file.is_new

    # Create file
    path.write_text(' ')

    file = File(path=path)
    assert not file.is_new


def test_read(tmp_path):
    base_dir = tmp_path / "test_read"
    base_dir.mkdir()
    filepath = base_dir / "test.txt"
    text = "this is\na\nexample"
    filepath.write_text(text)

    file = File(path=filepath)

    assert file.read() == text


def test_save_no_path(tmp_path):
    base_dir = tmp_path / 'test_save'
    base_dir.mkdir()
    filepath = base_dir / 'test.pdb'
    text = "this\nis\na\nexample"

    assert not filepath.exists()

    file = File()

    file.save(content=text, path=filepath)

    assert filepath.exists()


def test_save(tmpdir):
    filepath = tmpdir.join('test.txt')
    text = "this\nis\na\nexample"

    file = File(path=filepath)
    assert not filepath.exists()

    file.save(content=text)

    assert filepath.exists()


def test_save_no_path():
    file = File()

    with pytest.raises(FileNameError):
        file.save(content='jejeje')
