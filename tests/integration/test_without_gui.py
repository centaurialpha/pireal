# -*- coding: utf-8 -*-
#
# Copyright 2015-2019 - Gabriel Acosta <acostadariogabriel@gmail.com>
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

from pireal.core.db import DB
from pireal.core.interpreter import parse

SAMPLES = Path().cwd() / 'samples'
SAMPLE_PDB_PATH = SAMPLES / 'database.pdb'
SAMPLE_PDB_WINDOWS_PATH = SAMPLES / 'database_windows.pdb'
QUERY_PATH = SAMPLES / 'queries.pqf'


@pytest.mark.integration
@pytest.mark.parametrize(
    'db_path',
    [SAMPLE_PDB_PATH, SAMPLE_PDB_WINDOWS_PATH]
)
def test_full_cycle(db_path):
    # Prepare DB
    db = DB.create_from_file(db_path)
    assert not db.is_new()
    assert len(db) > 0
    # Prepare query
    result = parse(QUERY_PATH.read_text())

    relations_copy = dict(db._relations)
    query_count = len(db)
    for query_name, query in result.items():
        new_relation = eval(query, {}, relations_copy)
        relations_copy[query_name] = new_relation

        query_count += 1

    assert len(relations_copy) == query_count

    # Assert relations
    q1 = relations_copy['q1']
    qq2 = relations_copy['qq2']

    assert q1.degree() == 7
    assert q1.cardinality() == 4

    assert qq2.degree() == 2
    assert qq2.cardinality() == 5
