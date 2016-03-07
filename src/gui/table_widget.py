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
from PyQt5.QtGui import QStandardItem

from src.gui import (
    custom_table,
    fader_widget
)
from src.gui.main_window import Pireal


class TableWidget(QWidget):

    def __init__(self):
        super(TableWidget, self).__init__()

        vbox = QVBoxLayout(self)
        vbox.setContentsMargins(0, 0, 0, 0)

        self.relations = {}
        self.relations_types = {}

        # Stack
        self.stacked = StackedWidget()
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
        current_table = self.current_table()
        model = current_table.model()
        model.setHorizontalHeaderLabels(data.header)

        for row_count, row in enumerate(data.content):
            for col_count, data in enumerate(row):
                item = QStandardItem(data)
                item.setSelectable(False)
                model.setItem(row_count, col_count, item)

    def add_table(self, rela, name, types):
        """ Add new table from New Relation Dialog """

        ptable = custom_table.Table()
        model = ptable.model()
        model.setHorizontalHeaderLabels(rela.header)

        # Populate table
        row_count = 0
        for row in rela.content:
            for col_count, i in enumerate(row):
                item = QStandardItem(i)
                item.setSelectable(False)
                model.setItem(row_count, col_count, item)
                delegate = ptable.itemDelegate()
                delegate.data_types[col_count] = types[col_count]
            row_count += 1

        self.add_relation(name, rela)
        self.stacked.addWidget(ptable)

        central = Pireal.get_service("central")
        active_db = central.get_active_db()
        active_db.modified = True


class StackedWidget(QStackedWidget):

    def setCurrentIndex(self, index):
        self.fader_widget = fader_widget.FaderWidget(self.currentWidget(),
                                                     self.widget(index))
        QStackedWidget.setCurrentIndex(self, index)

    def show_display(self, index):
        self.setCurrentIndex(index)
