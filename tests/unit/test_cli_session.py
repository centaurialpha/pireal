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

import pytest

from pireal.cli.session import _execute_query
from tests.helpers import make_relation


@pytest.fixture
def base_relations():
    return {
        "students": make_relation(
            ["id", "name", "age"],
            [("1", "Gabriel", "25"), ("2", "Marisel", "30"), ("3", "Rodrigo", "25")],
        )
    }


def test_execute_valid_query(base_relations):
    results, err = _execute_query("q := project name (students);", base_relations)
    assert err is None
    assert "q" in results
    assert results["q"].cardinality() == 3


def test_execute_invalid_relation(base_relations):
    results, err = _execute_query("q := nonexistent;", base_relations)
    assert err is not None
    assert results == {}


def test_execute_syntax_error(base_relations):
    _, err = _execute_query("q := select (students);", base_relations)
    assert err is not None


def test_results_accumulate_across_calls(base_relations):
    session = dict(base_relations)

    r1, _ = _execute_query("young := select age=25 (students);", session)
    session.update(r1)

    r2, err = _execute_query("names := project name (young);", session)
    assert err is None
    assert "names" in r2
    assert r2["names"].cardinality() == 2


def test_handle_show_relation_not_found(capsys):
    from io import StringIO

    from rich.console import Console

    from pireal.cli.session import _handle_show_relation

    console = Console(file=StringIO())
    rels = {"students": make_relation(["id"], [("1",)])}
    # no debe explotar
    _handle_show_relation(console, rels, r"\r nonexistent")


def test_handle_show_relation_no_arg(capsys):
    from io import StringIO

    from rich.console import Console

    from pireal.cli.session import _handle_show_relation

    console = Console(file=StringIO())
    rels = {"students": make_relation(["id"], [("1",)])}
    _handle_show_relation(console, rels, r"\r")
