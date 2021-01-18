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

"""A container for Relation objects"""

import logging

from pireal.core import db_utils
from pireal.core.file_utils import File
from pireal.core.relation import Relation

logger = logging.getLogger('core.db')


class DBError(Exception):
    """Base class for DB errors"""


class RelationNotFound(DBError):
    """Raise when relation not exist in DB"""


class DB:

    def __init__(self, file: File = None):
        self._relations = {}
        self._dirty = False
        self.file = file

    def add(self, relation: Relation):
        """Add a Relation to DB"""
        rname = relation.name
        if rname in self._relations:
            raise NameError(f'Relation {rname} already exist')
        self._relations[rname] = relation
        self._dirty = True

    def get(self, name: str) -> Relation:
        """Return Relation object or fail"""
        if name not in self._relations:
            raise RelationNotFound(f'Relation {name} not found')
        return self._relations[name]

    def remove(self, name: str):
        """Remove Relation from DB"""
        if name not in self._relations:
            raise RelationNotFound(f'Relation {name} not found')
        del self._relations[name]

    def write_to_file(self, dst_path: str):
        """Serialize all relations to a file"""
        db_content = db_utils.generate_database(self._relations)
        if self.file is None:
            self.file = File(path=dst_path)

        self.file.save(content=db_content)
        self._dirty = False

    @classmethod
    def from_file(cls, filepath):
        """Create a DB object from a file"""
        file = File(path=filepath)
        db = cls(file=file)

        if file.is_new:
            return db

        try:
            text = file.read()
        except IOError:
            logger.exception('Error reading file')
            raise

        db_dict = db_utils.parse_database(text)

        relations = db_utils.create_relations_from_parsed_db(db_dict)

        for relation in relations:
            db.add(relation)

        db._dirty = False

        return db

    @property
    def dirty(self):
        return self._dirty

    @property
    def filename(self):
        return self.file.filename

    @property
    def display_name(self):
        return self.file.display_name

    @property
    def relations_dict(self):
        return self._relations

    @property
    def relations(self):
        return tuple(self._relations.values())

    @property
    def is_new(self):
        return self.file.is_new

    def __len__(self):
        return len(self._relations)

    def __repr__(self):
        return f'DB(name={self.display_name}, relations={len(self)})'

    def __iter__(self):
        for relation_name, relation in self._relations.items():
            yield relation_name, relation
