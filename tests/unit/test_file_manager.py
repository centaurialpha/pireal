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

from pireal.core import file_manager, relation
from pireal.utils import sanitize_data


@pytest.mark.parametrize(
    "filename, expected",
    [
        ("/home/gabo/archivo.py", ".py"),
        ("/path/path/blabla/file.extension", ".extension"),
        ("/hola/como/estas/que_onda.qda", ".qda"),
    ],
)
def test_get_extension(filename, expected):
    assert file_manager.get_extension(filename) == expected


@pytest.mark.parametrize(
    "filename, name",
    [
        ("/home/gabo/archivo.py", "archivo"),
        ("/path/path/blabla/file.extension", "file"),
        ("/hola/como/estas/que_onda.qda", "que_onda"),
    ],
)
def test_get_basename(filename, name):
    assert str(file_manager.get_basename(filename)) == name


@pytest.mark.parametrize(
    "filename, path",
    [
        (Path("/home/gabo/archivo.py"), Path("/home/gabo")),
        (Path("/path/path/blabla/file.extension"), Path("/path/path/blabla")),
        (Path("/hola/como/estas/que_onda.qda"), Path("/hola/como/estas")),
    ],
)
def test_get_path(filename, path):
    assert file_manager.get_path(filename) == path


def test_get_files_from_folder(tmp_path: Path):
    files = ("archivo.py", "archivo2.py", "archivo3.py")
    assert len(list(tmp_path.iterdir())) == 0
    for f in files:
        path = tmp_path / f
        path.write_text("Some content")
    assert len(list(tmp_path.iterdir())) == len(files)
    _files = file_manager.get_files_from_folder(tmp_path)
    assert len(_files) == len(files)


def test_generate_database():
    r = relation.Relation()
    r.header = ["id", "name"]
    data = {("1", "Gabriel"), ("23", "Rodrigo")}
    for d in data:
        r.insert(d)
    relations = {"persona": r}

    result = file_manager.generate_database(relations)

    # Verificar header
    assert result.startswith("@persona:id,name\n")
    # Verificar que ambas tuplas están presentes, sin asumir orden
    assert "1,Gabriel" in result
    assert "23,Rodrigo" in result


def test_sanitize_data():
    data = "@t1:a,b,c\n1234,hola,chau\n4321,chau,hola\n\n@t2:d,e,f,g\n4321,AAA,BBB,CCC\n"
    expected = {
        "tables": [
            {
                "header": ["a", "b", "c"],
                "name": "t1",
                "tuples": [("1234", "hola", "chau"), ("4321", "chau", "hola")],
            },
            {
                "header": ["d", "e", "f", "g"],
                "name": "t2",
                "tuples": [("4321", "AAA", "BBB", "CCC")],
            },
        ]
    }
    assert expected == sanitize_data(data)
