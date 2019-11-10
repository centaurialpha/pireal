import os

import pytest

from pireal.core.settings import EXAMPLES
from pireal.core.pfile import File
from pireal.core.file_manager import parse_database_content
from pireal.core.relation import Relation
from pireal.core.interpreter import parse


SAMPLE_PDB_PATH = os.path.join(EXAMPLES, 'database.pdb')
QUERY_PATH = os.path.join(EXAMPLES, 'queries.pqf')


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
