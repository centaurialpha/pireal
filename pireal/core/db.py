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
import logging
from collections import OrderedDict

from pireal.core.file_manager import (
    get_basename_with_extension,
    generate_database,
    parse_database_content,
    detect_encoding
)

logger = logging.getLogger(__name__)


class DBIOError(Exception):
    pass


class DB:

    def __init__(self, path=None):
        self._dirty = False
        self._path = path
        self._relations = OrderedDict()

    @staticmethod
    def formats() -> str:
        return 'Pireal Database File *.pdb'

    def file_path(self) -> str:
        return self._path

    def display_name(self) -> str:
        return get_basename_with_extension(self._path)

    def is_dirty(self) -> bool:
        return self._dirty

    def is_new(self) -> bool:
        return self._path is None

    def add(self, name: str, relation):
        if name in self._relations:
            raise NameError('Relation %s alredy exist', name)
        self._relations[name] = relation
        self._dirty = True

    def remove_from_name(self, name: str):
        try:
            del self._relations[name]
        except KeyError:
            pass
        self._dirty = True

    def save(self):
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

        return parse_database_content(content)

    def __iter__(self):
        return iter(self._relations)

    def __len__(self):
        return len(self._relations)
