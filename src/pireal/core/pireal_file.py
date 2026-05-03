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

from importlib.resources import files
from pathlib import Path


class File:
    def __init__(self, filename: str = "", display_name: str = ""):
        self._filename = Path(filename) if filename else None
        self._display_name = display_name

    @property
    def is_new(self) -> bool:
        return self._filename is None

    @property
    def display_name(self) -> str:
        if self._display_name:
            return self._display_name
        return self._filename.name if self._filename else "Untitled"

    @property
    def path(self) -> str:
        return str(self._filename) if self._filename else ""

    @property
    def exists(self) -> bool:
        return self._filename is not None and self._filename.exists()

    def read(self):
        if self._filename is None:
            return ""

        return self._filename.read_text(encoding="utf-8")

    def save(self, data, path=None):
        if path:
            self._filename = Path(path)
        if self._filename is None:
            raise ValueError("No filename set")

        self._filename.write_text(data, encoding="utf-8")
        self._display_name = ""


def is_example_file(file: File | Path | str | None) -> bool:
    if file is None:
        return False

    path = Path(file.path) if isinstance(file, File) else Path(file)
    examples_dir = Path(str(files("pireal") / "resources" / "samples"))

    try:
        path.resolve().relative_to(examples_dir)
        return True
    except ValueError:
        return False
