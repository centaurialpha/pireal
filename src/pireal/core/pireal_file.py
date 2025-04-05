from pathlib import Path

from PyQt6.QtCore import QFile, QIODevice, QObject, QStringConverter, QTextStream


class File(QObject):
    def __init__(self, filename: str = ""):
        super().__init__()
        self._is_new = True
        if filename:
            self._is_new = False
        self._filename = Path(filename) if filename else None

    @property
    def display_name(self) -> str:
        return self._filename.name if self._filename else "Untitled"

    @property
    def path(self) -> str:
        return str(self._filename)

    def read(self):
        file = QFile(str(self._filename))
        if not file.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text):
            raise IOError(f"Error al abrir el archivo: {file.errorString()}")

        stream = QTextStream(file)
        stream.setEncoding(QStringConverter.Encoding.Utf8)
        content = stream.readAll()
        return content

    def save(self, data, path=None):
        if path:
            self._filename = Path(path)
            self._is_new = False

        file = QFile(str(self._filename))
        if not file.open(
            QIODevice.OpenModeFlag.WriteOnly | QIODevice.OpenModeFlag.Truncate
        ):
            raise IOError(f"Error al abrir el archivo: {file.errorString()}")

        stream = QTextStream(file)
        stream.setEncoding(QStringConverter.Encoding.Utf8)
        _ = stream << data
        stream.flush()
        file.close()
