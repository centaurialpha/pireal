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
import logging

from pireal.core.file_manager import (
    get_basename_with_extension,
    generate_database,
    parse_database_content,
    detect_encoding
)
from pireal.core.relation import Relation

logger = logging.getLogger(__name__)


class DBError(Exception):
    pass


class DBIOError(DBError):
    pass


class DB:

    def __init__(self, path=None):
        self._dirty = False
        self._path = path
        self._relations = {}

    @property
    def relations(self) -> tuple:
        return tuple(self._relations.values())

    @property
    def relation_names(self) -> tuple:
        return tuple(self._relations.keys())

    def give_relation(self, name: str) -> Relation:
        if name not in self._relations:
            raise NameError(f'Relation {name} not found')
        return self._relations[name]

    def file_path(self) -> str:
        return self._path

    def display_name(self) -> str:
        if self.is_new():
            return 'new'
        return get_basename_with_extension(self._path)

    def is_dirty(self) -> bool:
        return self._dirty

    def is_new(self) -> bool:
        new = True
        if self._path is not None:
            if os.path.exists(self._path):
                new = False
        return new

    def add(self, relation: Relation):
        if relation.name in self._relations:
            raise NameError(f'Relation {relation.name} alredy exist')
        self._relations[relation.name] = relation
        self._dirty = True

    def remove_from_name(self, name: str):
        try:
            del self._relations[name]
        except KeyError:
            logger.warning(f'Relation {name} not exist, nothing to remove')
            return
        self._dirty = True

    def save(self, file_path=None):
        if file_path is not None:
            self._path = file_path
        logger.debug('Generating database in %s', self._path)
        db_content = generate_database(self._relations)
        with open(self._path, 'w') as fp:
            fp.write(db_content)
        self._dirty = False

    def load(self, file_path=None):
        if file_path is not None:
            self._path = file_path
        try:
            with open(self._path, 'rb') as fp:
                content = fp.read()
            encoding = detect_encoding(content)
            content = content.decode(encoding)
        except (IOError, UnicodeDecodeError) as reason:
            logger.exception('Could not open file: %s', self._path)
            raise DBIOError(reason)
        db_content = parse_database_content(content)
        self._load_relations_from_content(db_content)

    def _load_relations_from_content(self, content: list):
        for table in content:
            relation_name = table['name']
            header = table['header']
            tuples = table['tuples']

            relation = Relation()
            relation.name = relation_name
            relation.header = header

            for t in tuples:
                relation.insert(t)

            self.add(relation)

        self._dirty = False

    def __iter__(self):
        for name, relation in self._relations.items():
            yield name, relation

    def __getitem__(self, key):
        return self._relations[key]

    def __len__(self):
        return len(self._relations)

    def __repr__(self):
        return (
            f'DB(name={self.display_name()} '
            f'path={self.file_path()} '
            f'relations={len(self)})'
        )
