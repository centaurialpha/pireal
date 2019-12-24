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

from pireal.core.relation import Relation


def generate_database(relations: dict) -> str:
    """
    {rela_name: rela_object}
    """
    content = ''
    for relation_name, relation in relations.items():
        first_line = '@{relation_name}:{header}\n'
        header = ','.join(relation.header)
        content += first_line.format(relation_name=relation_name, header=header)
        for t in relation.content:
            content += ','.join(t) + '\n'
        content += '\n'

    return content.strip()


def parse_database(text: str) -> dict:
    """
    @rela:a,b,c
    1,2,3
    4,5,6

    @rela2:d,f,g
    7,8,9
    """
    result = {}

    first_lines = map(str.rstrip, text.split('@')[1:])
    for line in first_lines:
        relation = {}
        content = line.splitlines()
        relation_name, header = content[0].split(':')
        # FIXME: En una semana no voy a entender esto
        relation['header'] = list(map(str.strip, header.split(',')))
        content.pop(0)
        relation['tuples'] = [tuple(map(str.strip, t.split(','))) for t in content]

        result[relation_name] = relation

    return result


def create_relations_from_parsed_db(db: dict) -> list:
    relations = []
    for relation_name, data in db.items():
        relation = Relation()
        relation.name = relation_name
        relation.header = data['header']

        for t in data['tuples']:
            relation.insert(t)

        relations.append(relation)

    return relations
