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
    QListWidgetItem,
    QStackedWidget,
    QTableWidget,
    QTableWidgetItem
)
from PyQt4.QtCore import (
    Qt,
    SIGNAL
)
from src.gui.main_window import Pireal


class TableWidget(QWidget):

    def __init__(self):
        super(TableWidget, self).__init__()

        vbox = QVBoxLayout(self)
        vbox.setContentsMargins(0, 0, 0, 0)

        self.relations = {}

        ## Splitter
        #self._splitter = QSplitter()

        ## List of names of tables/relations
        #self._list_tables = QListWidget()
        #self._splitter.addWidget(self._list_tables)
        ## Stack
        self.stacked = QStackedWidget()
        vbox.addWidget(self.stacked)

        #vbox.addWidget(self._splitter)

        #self.connect(self._list_tables, SIGNAL("currentRowChanged(int)"),
                     #self.__change_table)

    #def __change_table(self, index):
        #self.stacked.setCurrentIndex(index)

    def count(self):
        return self.stacked.count()

    def add_table(self, rows, columns, name, data):
        table = QTableWidget()
        table.setRowCount(rows)
        table.setColumnCount(columns)

        for k, v in list(data.items()):
            item = QTableWidgetItem()
            item.setText(v)
            if k[0] == 0:
                table.setHorizontalHeaderItem(k[1], item)
            else:
                table.setItem(k[0] - 1, k[1], item)
        #ntuples = " [ " + str(rows) + " ]"
        #item_list = QListWidgetItem(name + ntuples)
        #item_list.setTextAlignment(Qt.AlignHCenter)
        #self._list_tables.addItem(item_list)
        self.stacked.addWidget(table)
        self.stacked.setCurrentIndex(self.stacked.count() - 1)

    def add_new_table(self, rel, name):
        import itertools

        table = QTableWidget()
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

    def add_table_from_file(self):
        pass

    #def showEvent(self, event):
        #QWidget.showEvent(self, event)
        #self._splitter.setSizes([self.height(), self.width()])


#class MdiDB(QMdiSubWindow):

    #def __init__(self):
        #super(MdiDB, self).__init__()
        #self.table_widget = TableWidget()
        #self.setWidget(self.table_widget)

        #Pireal.load_service("db", self.table_widget)

    #def closeEvent(self, event):
        ## Disable QAction's
        #pireal = Pireal.get_service("pireal")
        #pireal.enable_disable_db_actions(False)
