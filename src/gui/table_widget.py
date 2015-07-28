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
    QVBoxLayout,
    QStackedWidget,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView
)
#from PyQt4.QtCore import (
    #Qt,
    #SIGNAL
#)
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

    def add_table(self, rows, columns, name, data, fields):
        table = Table()
        table.setRowCount(rows)
        table.setColumnCount(columns)
        table.setHorizontalHeaderLabels(fields)

        for k, v in list(data.items()):
            item = QTableWidgetItem()
            item.setText(v)
            table.setItem(k[0] - 1, k[1], item)

        self.stacked.addWidget(table)
        self.stacked.setCurrentIndex(self.stacked.count() - 1)
        lateral = Pireal.get_service("lateral")
        lateral.add_item_list([name])

    def add_new_table(self, rel, name):
        import itertools

        table = Table()
        table.setRowCount(0)
        table.setColumnCount(0)

        data = itertools.chain([rel.fields], rel.content)

        for row_data in data:
            row = table.rowCount()
            table.setColumnCount(len(row_data))
            for col, text in enumerate(row_data):
                item = QTableWidgetItem()
                item.setText(text)
                if row == 0:
                    table.setHorizontalHeaderItem(col, item)
                else:
                    table.setItem(row - 1, col, item)
            table.insertRow(row)
        table.removeRow(table.rowCount() - 1)
        self.stacked.addWidget(table)
        self.stacked.setCurrentIndex(self.stacked.count() - 1)
        lateral = Pireal.get_service("lateral")
        lateral.add_item_list([name])

    def remove_table(self, index):
        table = self.stacked.widget(index)
        self.stacked.removeWidget(table)

    def add_table_from_rdb_content(self, content):
        lateral = Pireal.get_service("lateral")
        lateral.show()
        for line in content.splitlines():
            if line.startswith('@'):
                table = Table()
                name = line.split(':')[0][1:]
                lateral.add_item_list([name])
                fields = line.split(':')[-1].split(',')[:-1]
                table.setColumnCount(len(fields))
                table.setHorizontalHeaderLabels(fields)
                self.stacked.addWidget(table)
            else:
                row = table.rowCount()
                for e, i in enumerate(line.split(',')):
                    item = QTableWidgetItem()
                    item.setText(i)
                    table.setItem(row - 1, e, item)
                table.insertRow(row)


class Table(QTableWidget):

    def __init__(self, parent=None):
        super(Table, self).__init__(parent)
        self.horizontalHeader().setResizeMode(QHeaderView.ResizeToContents)
