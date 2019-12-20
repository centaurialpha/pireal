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


import os

import pytest

from pireal.core.db import DB
from pireal.core.relation import Relation
from pireal.core.interpreter import parse

SAMPLES = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'samples')
SAMPLE_PDB_PATH = os.path.join(SAMPLES, 'database.pdb')
SAMPLE_PDB_WINDOWS_PATH = os.path.join(SAMPLES, 'database_windows.pdb')
QUERY_PATH = os.path.join(SAMPLES, 'queries.pqf')


@pytest.mark.integration
def test_full_cycle():
    for database_filepath in (SAMPLE_PDB_PATH, SAMPLE_PDB_WINDOWS_PATH):
        # Prepare DB
        db = DB(path=database_filepath)
        assert not db.is_new()
        db.load()
        assert len(db) > 0
        # Prepare query
        with open(QUERY_PATH) as fp:
            result = parse(fp.read())

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
