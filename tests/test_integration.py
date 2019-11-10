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

from pireal.core.pfile import File
from pireal.core.file_manager import parse_database_content
from pireal.core.relation import Relation
from pireal.core.interpreter import parse

SAMPLES = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'samples')
SAMPLE_PDB_PATH = os.path.join(SAMPLES, 'database.pdb')
QUERY_PATH = os.path.join(SAMPLES, 'queries.pqf')


@pytest.mark.integration
def test_full_cycle():
    # Prepare DB
    db_file = File(path=SAMPLE_PDB_PATH)
    assert not db_file.is_new()
    db_content_parsed = parse_database_content(db_file.read())
    assert db_content_parsed
    tables = db_content_parsed['tables']
    relations = {}
    db_count = 0
    for table in tables:
        name = table['name']
        header = table['header']
        tuples = table['tuples']

        relation_obj = Relation()
        relation_obj.header = header
        for data in tuples:
            relation_obj.insert(data)

        relations[name] = relation_obj
        db_count += 1

    assert len(relations) == db_count
    # Prepare query
    query_file = File(path=QUERY_PATH)
    result = parse(query_file.read())

    # FIXME: esto se hace de la misma forma en execute_queries. Unificar
    relations_copy = dict(relations)
    query_count = db_count
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
