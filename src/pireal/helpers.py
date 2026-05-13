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

from PyQt6.QtCore import (
    QByteArray,
    QSize,
    Qt,
)
from PyQt6.QtGui import (
    QColor,
    QIcon,
    QPainter,
    QPixmap,
)
from PyQt6.QtSvg import QSvgRenderer


def svg_icon(path: Path, color: QColor, size: int = 16) -> QIcon:
    svg = path.read_text(encoding="utf-8").replace("currentColor", color.name())
    renderer = QSvgRenderer(QByteArray(svg.encode()))
    pixmap = QPixmap(QSize(size, size))
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    renderer.render(painter)
    painter.end()
    return QIcon(pixmap)
