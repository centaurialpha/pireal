from pathlib import Path

from PyQt6.QtGui import QFont, QFontDatabase

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

    def apply_to(self, widget, size: int = 12):
        widget.setFont(self.font(size))
