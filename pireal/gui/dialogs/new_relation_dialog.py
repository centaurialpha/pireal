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

import logging

from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QDialogButtonBox
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QInputDialog

from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSlot as Slot

from pireal import translations as tr

from pireal.core.relation import Relation, InvalidFieldNameError


logger = logging.getLogger(__name__)


class NewRelationDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowTitle(tr.TR_RELATION_DIALOG_TITLE)
        self.setSizeGripEnabled(True)
        self.resize(650, 350)
        self._data = None

        vbox = QVBoxLayout(self)
        hbox = QHBoxLayout()
        hbox.addWidget(QLabel('Relation name:'))

        buttons_hbox = QHBoxLayout()
        btn_add_column = QPushButton('Add column')
        buttons_hbox.addWidget(btn_add_column)
        btn_delete_column = QPushButton('Delete column')
        buttons_hbox.addWidget(btn_delete_column)
        btn_add_row = QPushButton('Add row')
        buttons_hbox.addWidget(btn_add_row)
        btn_delete_row = QPushButton('Delete row')
        buttons_hbox.addWidget(btn_delete_row)

        self.line_relation_name = QLineEdit()
        hbox.addWidget(self.line_relation_name)
        vbox.addLayout(hbox)
        vbox.addLayout(buttons_hbox)

        self.table = QTableWidget()
        vbox.addWidget(self.table)
        self.table.horizontalHeader().sectionDoubleClicked.connect(self._edit_header)
        self.setup_empty_table()

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        vbox.addWidget(button_box)

        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        btn_add_column.clicked.connect(self.add_column)
        btn_add_row.clicked.connect(self.add_row)
        btn_delete_column.clicked.connect(self.delete_column)
        btn_delete_row.clicked.connect(self.delete_row)

    @property
    def relation_name(self) -> str:
        return self.line_relation_name.text().strip()

    @Slot(int)
    def _edit_header(self, index):
        item = self.table.horizontalHeaderItem(index)
        if item is None:
            value = self.table.model().headerData(index, Qt.Horizontal)
            item = QTableWidgetItem(str(value))
            self.table.setHorizontalHeaderItem(index, item)
        old_header = item.text()

        new_header, ok = QInputDialog.getText(
            self, tr.TR_RELATION_DIALOG_CHANGE_HEADER_LABEL,
            tr.TR_RELATION_DIALOG_HEADER_NAME, QLineEdit.Normal, old_header
        )
        if ok:
            item.setText(new_header)

    def get_data(self):
        return self._data

    def setup_empty_table(self):
        self.table.insertColumn(0)
        self.table.insertColumn(0)

        self.table.insertRow(0)

        for i in range(2):
            item = QTableWidgetItem()
            item.setText('Value_{}'.format(i))
            self.table.setItem(0, i, item)

    def create_relation(self):
        header = [self.table.model().headerData(i, Qt.Horizontal)
                  for i in range(self.table.columnCount())]
        relation = Relation()
        try:
            relation.header = header
        except InvalidFieldNameError as ex:
            QMessageBox.warning(None, 'Error', str(ex))
            return None
        for i in range(self.table.rowCount()):
            row_data = []
            for j in range(self.table.columnCount()):
                item_text = self.table.item(i, j).text().strip()
                if not item_text:
                    QMessageBox.warning(
                        None, 'Error', tr.TR_RELATION_DIALOG_WHITESPACE.format(i + 1, j + 1))
                    return None
                row_data.append(item_text)
            relation.insert(tuple(row_data))
        return relation

    def accept(self):
        relation = self.create_relation()
        if relation is not None:
            if not self.relation_name:
                QMessageBox.warning(
                    None, 'Error', tr.TR_RELATION_DIALOG_EMPTY_RELATION_NAME
                )
                self.line_relation_name.setFocus()
                self.line_relation_name.selectAll()
                return
            self._data = self.relation_name, relation
            QDialog.accept(self)

    @Slot()
    def add_column(self):
        self.table.insertColumn(self.table.columnCount())
        self._select_last_column()

    @Slot()
    def add_row(self):
        self.table.insertRow(self.table.rowCount())
        self._select_last_row()

    def _select_last_row(self):
        self.table.selectRow(self.table.rowCount() - 1)

    def _select_last_column(self):
        self.table.selectColumn(self.table.columnCount() - 1)

    @Slot()
    def delete_column(self):
        if self.table.columnCount() > 1:
            self.table.removeColumn(self.table.currentColumn())
            self._select_last_column()

    @Slot()
    def delete_row(self):
        if self.table.rowCount() > 1:
            self.table.removeRow(self.table.currentRow())
            self._select_last_row()
