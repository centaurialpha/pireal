from pathlib import Path

from PyQt6.QtCore import QObject

from pireal.dirs import EXAMPLES_DIR


class File(QObject):
    def __init__(self, filename: str = "", display_name: str = ""):
        super().__init__()
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


def is_example_file(file: File | None) -> bool:
    if file is None:
        return False
    try:
        Path(file.path).resolve().relative_to(EXAMPLES_DIR.resolve())
        return True
    except ValueError:
        return False
