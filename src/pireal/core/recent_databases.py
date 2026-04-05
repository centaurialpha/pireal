# Copyright 2015-2026 - Gabriel Acosta <acostadariogabriel@gmail.com>
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

from pathlib import Path

from pireal.resources import sample
from pireal.settings import MAX_RECENT_DATABASES


class RecentDatabases:
    def __init__(self, items: list[str] | None = None):
        self._items: list[str] = items or []

    def add(self, filepath: str) -> None:
        if self._is_example(filepath):
            return
        normalized = self._normalize(filepath)
        if normalized in self._items:
            self._items.remove(normalized)
        self._items.insert(0, normalized)
        self._items = self._items[:MAX_RECENT_DATABASES]

    def remove(self, filepath: str) -> None:
        normalized = self._normalize(filepath)
        if normalized in self._items:
            self._items.remove(normalized)

    def all(self) -> list[str]:
        return self._items.copy()

    def __contains__(self, filepath: str) -> bool:
        return self._normalize(filepath) in self._items

    def __len__(self) -> int:
        return len(self._items)

    @staticmethod
    def _normalize(filepath: str) -> str:
        return str(Path(filepath).resolve())

    @staticmethod
    def _is_example(filepath: str) -> bool:
        return Path(filepath).resolve() == Path(sample("database.pdb")).resolve()
