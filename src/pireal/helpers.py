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


from PyQt6.QtGui import QFont, QFontDatabase

from pireal.resources import font as get_font


class Font:
    _instance = None

    def __init__(self):
        font_id = QFontDatabase.addApplicationFont(get_font("font-awesome.otf"))
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
