import pytest
from pathlib import Path
from pireal.core.pireal_file import File, is_example_file


def test_is_new_without_filename():
    f = File()
    assert f.is_new


def test_is_new_with_filename():
    f = File("/tmp/test.pdb")
    assert not f.is_new


def test_display_name_with_filename():
    f = File("/tmp/test.pdb")
    assert f.display_name == "test.pdb"


def test_display_name_override():
    f = File(display_name="untitled_1.pqf")
    assert f.display_name == "untitled_1.pqf"


def test_display_name_fallback():
    f = File()
    assert f.display_name == "Untitled"


def test_path_empty_when_no_filename():
    f = File()
    assert f.path == ""


def test_save_and_read(tmp_path: Path):
    filepath = tmp_path / "test.pdb"
    f = File(str(filepath))
    f.save("contenido de prueba")
    assert filepath.read_text(encoding="utf-8") == "contenido de prueba"
    assert f.read() == "contenido de prueba"


def test_save_raises_without_filename():
    f = File()
    with pytest.raises(ValueError):
        f.save("data")


def test_is_example_file_true(tmp_path):
    from pireal.dirs import EXAMPLES_DIR
    example_file = EXAMPLES_DIR / "database.pdb"
    f = File(str(example_file))
    assert is_example_file(f)


def test_is_example_file_false(tmp_path):
    f = File(str(tmp_path / "mydb.pdb"))
    assert not is_example_file(f)


def test_is_example_file_none():
    assert not is_example_file(None)
