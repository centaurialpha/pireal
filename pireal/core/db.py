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

"""A container for Relation objects"""

import logging

from pireal.core.file_manager import (
    generate_database,
    parse_database_content,
)
from pireal.core.relation import Relation
from pireal.core.file_manager import File

logger = logging.getLogger('core.db')


class DBError(Exception):
    """Base para errores referidos a la base de datos"""


class DBFileNotFoundError(DBError):
    """Se lanza cuando no se encuentra el archivo de db"""


class DBInvalidFormatError(DBError):
    """Se lanza cuando el contenido de la db no cumple el formato"""


class DB:

    def __init__(self, path=None):
        self._dirty = False
        self._relations = {}
        self.file = File(path=path)

    @property
    def relations(self) -> tuple:
        return tuple(self._relations.values())

    @property
    def relation_names(self) -> tuple:
        return tuple(self._relations.keys())

    @classmethod
    def create_from_file(cls, filename):
        logger.debug('Creating DB from filename=%s', filename)
        db = cls(path=filename)
        try:
            db_content = db.file.read()
        except FileNotFoundError as e:
            logger.exception('Error reading the database. The file %s does not exists', filename)
            raise DBFileNotFoundError from e
        else:
            try:
                db_content = parse_database_content(db_content)
            except SyntaxError as reason:
                logger.exception('Error parsing the database.')
                raise DBInvalidFormatError(reason)

        for table in db_content:
            relation_name, header, tuples = table.values()
            relation = Relation()
            relation.name = relation_name
            relation.header = header

            for t in tuples:
                relation.insert(t)

            db.add(relation)

        db._dirty = False

        return db

    def give_relation(self, name: str) -> Relation:
        if name not in self._relations:
            raise NameError(f'Relation {name} not found')
        return self._relations[name]

    def display_name(self) -> str:
        return self.file.display_name

    def file_path(self) -> str:
        return self.file.path

    def is_new(self) -> bool:
        return self.file.is_new

    def is_dirty(self) -> bool:
        return self._dirty

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
        logger.debug('Generating database in %s', self.file.path)
        db_content = generate_database(self._relations)
        self.file.save(db_content, path=file_path)
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
