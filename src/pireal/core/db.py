# -*- coding: utf-8 -*-
#
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


from typing import Dict, List, Optional

from PyQt6.QtCore import QObject, pyqtSignal

from pireal.core.relation import Relation


class DB(QObject):
    hasModified = pyqtSignal(bool)
    databaseStateChanged = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self._relations: Dict[str, Relation] = {}
        self._query_results: List[str] = []

        self._modified = False
        self._is_active = False

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

    def remove(self, relation_name: str) -> None:
        del self._relations[relation_name]
        self.modified = True

    def clear(self) -> None:
        if not self._relations:
            return

        self._relations.clear()
        self.modified = True

    def get(self, relation_name: str) -> Optional[Relation]:
        return self._relations.get(relation_name)

    def update(self, relations: Dict[str, Relation]) -> None:
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

    def eval_query(self, expression: str, name: str) -> Relation:
        relation = eval(expression, {}, self._relations)
        relation.name = name
        self.add(relation)

        if name not in self._query_results:
            self._query_results.append(name)

        return relation

    def clear_query_results(self) -> None:
        for name in self._query_results[:]:
            if name in self._relations:
                self.remove(name)

        self._query_results.clear()
