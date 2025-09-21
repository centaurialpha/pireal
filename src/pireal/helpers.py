from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont, QFontDatabase, QIcon, QPainter, QPixmap

ROOT = Path(__file__).parent
FONT_PATH = str(ROOT / "resources" / "images" / "font-awesome.otf")


class Font:
    _instance = None

    def __init__(self, font_path: str = FONT_PATH):
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id == -1:
            raise RuntimeError("No se pudo cargar la fuente")

        self.family = QFontDatabase.applicationFontFamilies(font_id)[0]

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = Font()
        return cls._instance

    def font(self, size: int = 12) -> QFont:
        return QFont(self.family, size)

    def icon(self, char: str, size: int = 14, color: str = "black") -> QIcon:
        font = QFont(self.family)
        font.setPixelSize(size)

        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.GlobalColor.transparent)

        painter = QPainter(pixmap)
        painter.setFont(font)
        painter.setPen(QColor(color))
        painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, char)
        painter.end()

        return QIcon(pixmap)
