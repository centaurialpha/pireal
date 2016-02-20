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

from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QStackedWidget,
)

from src.gui import custom_table
from src.gui.main_window import Pireal


class TableWidget(QWidget):

    def __init__(self):
        super(TableWidget, self).__init__()

        vbox = QVBoxLayout(self)
        vbox.setContentsMargins(0, 0, 0, 0)

        self.relations = {}

        # Stack
        self.stacked = QStackedWidget()
        vbox.addWidget(self.stacked)

    def count(self):
        return self.stacked.count()

    def remove_table(self, index):
        widget = self.stacked.widget(index)
        self.stacked.removeWidget(widget)
        del widget

    def remove_relation(self, name):
        del self.relations[name]

    def add_relation(self, name, rela):
        if self.relations.get(name, None) is None:
            self.relations[name] = rela
            return True
        return False

    def add_table(self, rows, columns, name, data, fields):
        """ Add new table from New Relation Dialog """

        ptable = custom_table.Table()
        ptable.setRowCount(rows)
        ptable.setColumnCount(columns)
        ptable.setHorizontalHeaderLabels(fields)

        for k, v in list(data.items()):
            item = custom_table.Item()
            item.setText(v)
            ptable.setItem(k[0], k[1], item)

        self.stacked.addWidget(ptable)
        self.stacked.setCurrentIndex(self.count() - 1)
        central = Pireal.get_service("central")
        active_db = central.get_active_db()
        active_db.modified = True