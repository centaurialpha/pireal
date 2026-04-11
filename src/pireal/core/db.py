# Copyright 2015-2025 - Gabriel Acosta <acostadariogabriel@gmail.com>
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


from PyQt6.QtCore import QObject, pyqtSignal

from pireal.core.file_manager import generate_database
from pireal.core.pireal_file import File
from pireal.core.relation import Relation


class DB(QObject):
    hasModified = pyqtSignal(bool)
    databaseStateChanged = pyqtSignal(bool)
    relationsChanged = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self._relations: dict[str, Relation] = {}
        self._query_results: list[str] = []

        self._modified = False
        self._is_active = False

        self._file: File | None = None

    @property
    def file(self) -> File | None:
        return self._file

    @file.setter
    def file(self, value: File | None) -> None:
        self._file = value

    @property
    def is_active(self) -> bool:
        return self._is_active

    @is_active.setter
    def is_active(self, value: bool) -> None:
        if value != self._is_active:
            if not value:
                # Solo limpiar cuando se desactiva
                self.clear()
            self._is_active = value
            self.databaseStateChanged.emit(value)

    def add(self, relation: Relation) -> None:
        self._relations[relation.name] = relation
        self.modified = True
        self.relationsChanged.emit(list(self._relations.keys()))

    def load(self, relation: Relation) -> None:
        """Cargar relación sin marcar como modificado (para carga inicial)"""
        self._relations[relation.name] = relation
        self.relationsChanged.emit(list(self._relations.keys()))

    def remove(self, relation_name: str) -> None:
        del self._relations[relation_name]
        self.modified = True

    def clear(self) -> None:
        if not self._relations:
            return

        self._relations.clear()
        self.relationsChanged.emit([])

    def get(self, relation_name: str) -> Relation | None:
        return self._relations.get(relation_name)

    def update(self, relations: dict[str, Relation]) -> None:
        for name, relation in relations.items():
            is_new = name not in self._relations
            self._relations[name] = relation

            if is_new:
                # emitir señal?
                pass
        # FIXME: modified?

    @property
    def relations(self) -> list[Relation]:
        return list(self._relations.values())

    @property
    def count(self) -> int:
        return len(self._relations)

    @property
    def modified(self) -> bool:
        return self._modified

    @modified.setter
    def modified(self, has_modified: bool) -> None:
        if has_modified != self._modified:
            self._modified = has_modified
            self.hasModified.emit(has_modified)

    def __contains__(self, relation_name: str) -> bool:
        return relation_name in self._relations

    def __len__(self) -> int:
        return self.count

    def relations_dict(self) -> dict[str, Relation]:
        return dict(self._relations)

    def clear_query_results(self) -> None:
        for name in self._query_results[:]:
            if name in self._relations:
                self.remove(name)

        self._query_results.clear()

    @property
    def is_new(self) -> bool:
        return self._file is None

    def save(self) -> bool:
        if self._file is None:
            return False

        content = generate_database(self._relations)
        self._file.save(content)
        self.modified = False
        return True

    def add_query_result(self, name: str) -> None:
        self._query_results.append(name)
