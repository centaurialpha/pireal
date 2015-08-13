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
    QWidget,
    QHBoxLayout,
    QSplitter
)
from PyQt4.QtCore import Qt
from src.gui.main_window import Pireal


class CentralWidget(QWidget):

    def __init__(self):
        super(CentralWidget, self).__init__()
        box = QHBoxLayout(self)
        box.setContentsMargins(0, 0, 0, 0)

        # Splitters
        self._splitter_horizontal = QSplitter(Qt.Horizontal)
        self._splitter_vertical = QSplitter(Qt.Vertical)
        self._splitter_vertical.addWidget(self._splitter_horizontal)

        box.addWidget(self._splitter_vertical)

        # Load service
        Pireal.load_service("central", self)

    def load_lateral_widget(self, lateral):
        self._splitter_horizontal.addWidget(lateral)

    def load_table_widget(self, table):
        self._splitter_horizontal.addWidget(table)

    def load_editor_widget(self, editor):
        self._splitter_vertical.addWidget(editor)

    def showEvent(self, event):
        QWidget.showEvent(self, event)
        width = self.width() / 2
        height = self.height() / 6
        self._splitter_horizontal.setSizes([height, width])

central = CentralWidget()
