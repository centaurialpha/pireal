# -*- coding: utf-8 -*-
#
# Copyright 2015 - Gabriel Acosta <acostadariogabriel@gmail.com>
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

from PyQt4.QtGui import (
    QMdiArea,
    QPixmap,
    QPainter
)
from src.gui.main_window import Pireal


class MdiArea(QMdiArea):

    def __init__(self):
        QMdiArea.__init__(self)

        Pireal.load_service("mdi", self)

    def paintEvent(self, event):
        """ Draw the logo in center """

        QMdiArea.paintEvent(self, event)
        logo = QPixmap(":img/logo")
        painter = QPainter(self.viewport())
        # Position
        pos_x = (self.width() - logo.width()) / 2
        pos_y = (self.height() - logo.height()) / 2
        # Opacity
        painter.setOpacity(0.04)
        painter.drawPixmap(pos_x, pos_y, logo)


mdi = MdiArea()
