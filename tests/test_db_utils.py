# -*- coding: utf-8 -*-
#
# Copyright 2015-2020 - Gabriel Acosta <acostadariogabriel@gmail.com>
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

from pireal.core import db_utils
from pireal.core.relation import Relation


class FakeRelation:

    def __init__(self, header, content):
        self.header = header
        self.content = content


@pytest.fixture
def relations_fixture():
    r1 = Relation()
    r1.header = ['id', 'name']
    r1.insert(('2345', 'Mercedes'))
    r1.insert(('3123', 'Gabriel'))

    r2 = Relation()
    r2.header = ['id', 'skill']
    r2.insert(('3123', 'Python'))
    r2.insert(('2345', 'Rocks'))

    relations = {'people': r1, 'skills': r2}
    return relations


def test_generate_database(relations_fixture):
    expected = (
        '@people:id,name\n'
        '2345,Mercedes\n'
        '3123,Gabriel\n\n'
        '@skills:id,skill\n'
        '3123,Python\n'
        '2345,Rocks'
    )

    result = db_utils.generate_database(relations_fixture)
    assert result == expected


def test_parse_database():
    db_text = (
        '@people:id,  name\n'
        '2345,Mercedes\n'
        '3123,  Gabriel\n\n'
        '@skills: id, skill\n'
        '3123,Python\n'
        '2345,Rocks'
    )
    expected = {
        'people': {
            'header': ['id', 'name'],
            'tuples': [('2345', 'Mercedes'), ('3123', 'Gabriel')]
        },
        'skills': {
            'header': ['id', 'skill'],
            'tuples': [('3123', 'Python'), ('2345', 'Rocks')]
        }
    }
    result = db_utils.parse_database(db_text)
    assert result == expected


def test_create_relations_from_db_dict():
    db_dict = {
        'people': {
            'header': ['id', 'name'],
            'tuples': [('2345', 'Mercedes'), ('3123', 'Gabriel')]
        },
        'skills': {
            'header': ['id', 'skill'],
            'tuples': [('3123', 'Python'), ('2345', 'Rocks')]
        }
    }

    relations = db_utils.create_relations_from_parsed_db(db_dict)

    assert len(relations) == 2

    assert relations[0].name == 'people'
    assert relations[1].name == 'skills'
