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
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QHeaderView
)
from PyQt5.QtGui import (
    QBrush,
    QColor
)

from src import translations as tr


class EditRelationDialog(QDialog):

    def __init__(self, item, table_name, parent=None):
        super(EditRelationDialog, self).__init__(parent)
        title = tr.TR_RELATION_EDIT_DIALOG_TITLE + ' [' + table_name + ']'
        self.setWindowTitle(title)
        self.resize(650, 450)
        box = QVBoxLayout(self)
        box.setContentsMargins(5, 5, 5, 5)
        self.previous_table = item
        self.new_table = self.__load_table(item)
        box.addWidget(self.new_table)

        # Buttons
        hbox = QHBoxLayout()
        hbox.addItem(QSpacerItem(1, 0, QSizePolicy.Expanding))
        btn_save = QPushButton(tr.TR_RELATION_DIALOG_BTN_OK)
        hbox.addWidget(btn_save)
        btn_cancel = QPushButton(tr.TR_RELATION_DIALOG_BTN_CANCEL)
        hbox.addWidget(btn_cancel)

        box.addLayout(hbox)

        # Connections
        btn_save.clicked.connect(self.__save)
        btn_cancel.clicked.connect(self.close)
        self.new_table.cellChanged[int, int].connect(self.__on_cell_changed)

    def __save(self):
        for i in range(self.previous_table.rowCount()):
            for j in range(self.previous_table.columnCount()):
                item = self.previous_table.item(i, j)
                new_text = self.new_table.item(i, j).text()
                item.setText(new_text)
        self.close()

    def __on_cell_changed(self, row, column):
        item = self.new_table.item(row, column)
        item.setBackground(QBrush(QColor("#f95959")))
        item.setForeground(QBrush(QColor("white")))
        item.setSelected(False)

    def __load_table(self, table):
        new_table = QTableWidget()
        new_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        nrows = table.rowCount()
        ncols = table.columnCount()

        new_table.setRowCount(nrows)
        new_table.setColumnCount(ncols)

        # Get texts from horizontal header
        hlabels = [table.horizontalHeaderItem(i).text() for i in range(ncols)]
        # Set horizontal header
        new_table.setHorizontalHeaderLabels(hlabels)

        for i in range(nrows):
            for j in range(ncols):
                old_item = table.item(i, j)
                new_item = QTableWidgetItem()
                new_item.setText(old_item.text())
                new_table.setItem(i, j, new_item)

        return new_table
