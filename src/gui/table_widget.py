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
    QMdiSubWindow,
    QVBoxLayout,
    QSplitter,
    QListWidget,
    QStackedWidget
)


class TableWidget(QWidget):

    def __init__(self):
        super(TableWidget, self).__init__()
        vbox = QVBoxLayout(self)
        vbox.setContentsMargins(0, 0, 0, 0)

        # Splitter
        self._splitter = QSplitter()

        # List of names of tables/relations
        self._list_tables = QListWidget()
        self._splitter.addWidget(self._list_tables)
        # Stack
        self.stacked = QStackedWidget()
        self._splitter.addWidget(self.stacked)

        vbox.addWidget(self._splitter)

    def showEvent(self, event):
        QWidget.showEvent(self, event)
        self._splitter.setSizes([self.height(), self.width()])


class MdiDB(QMdiSubWindow):

    def __init__(self):
        super(MdiDB, self).__init__()
        self.table_widget = TableWidget()
        self.setWidget(self.table_widget)
