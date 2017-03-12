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
    QStackedWidget
)
from PyQt5.QtGui import (
    QStandardItem,
    QStandardItemModel
)
from PyQt5.QtCore import Qt

from src.gui import view, model


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

    def current_table(self):
        return self.stacked.currentWidget()

    def remove_relation(self, name):
        del self.relations[name]

    def add_relation(self, name, rela):
        if self.relations.get(name, None) is None:
            self.relations[name] = rela
            return True
        return False

    def update_table(self, data):
        print(data)
        """
        current_table = self.current_table()
        model = current_table.model()
        # Clear content
        model.clear()
        # Add new header and content

        model.setHorizontalHeaderLabels(data.header)

        for row_count, row in enumerate(data.content):
            for col_count, data in enumerate(row):
                item = QStandardItem(data)
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                model.setItem(row_count, col_count, item)

        # Ajustar las columnas de acuerdo al nuevo contenido
        current_table.adjust_columns()
        """
    def add_table(self, rela, name):
        """ Add new table from New Relation Dialog """

        # Create table
        table = self.create_table(rela)
        self.add_relation(name, rela)
        self.stacked.addWidget(table)

    def create_table(self, rela):
        """ Se crea la vista y el modelo """

        _view = view.View()
        _model = model.Model(rela)
        _view.setModel(_model)
        return _view
