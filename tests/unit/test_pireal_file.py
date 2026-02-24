# Copyright 2015-2026 - Gabriel Acosta <acostadariogabriel@gmail.com>
#
# This file is part of Pireal.
#
# Pireal is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# any later version.
#
# Pireal is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Pireal; If not, see <http://www.gnu.org/licenses/>.

from pathlib import Path

import pytest

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
    from pireal.resources import sample

    f = File(sample("database.pdb"))
    assert is_example_file(f)


def test_is_example_file_false(tmp_path):
    f = File(str(tmp_path / "mydb.pdb"))
    assert not is_example_file(f)


def test_is_example_file_none():
    assert not is_example_file(None)


def test_exists_false_when_no_filename():
    assert not File().exists


def test_exists_false_when_file_missing():
    assert not File("/tmp/no_existe_este_archivo.pdb").exists


def test_exists_true_when_file_present(tmp_path):
    f = tmp_path / "db.pdb"
    f.write_text("data")
    assert File(str(f)).exists
