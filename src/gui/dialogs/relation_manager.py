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
    QTableView,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLineEdit,
    QSpacerItem,
    QSizePolicy,
    QMessageBox,
)
from PyQt5.QtGui import (
    QStandardItemModel,
    QStandardItem
)
from PyQt5.QtCore import Qt

from src.gui import custom_table
from src.core import relation


def create_or_edit_relation(rela=None):
    class RelationManager(QDialog):

        def __init__(self, parent=None):
            super(RelationManager, self).__init__(parent)
            self.resize(700, 500)
            box = QVBoxLayout(self)
            self.rela = rela
            self.data = None
            # Table
            self.table = QTableView()
            model = QStandardItemModel()
            self.table.setModel(model)

            if rela is not None:
                self.__setup_edit_relation(rela)
            else:
                self._relation_name = QLineEdit()
                box.addWidget(self._relation_name)
                self.__setup_new_relation()

            # Buttons layout
            box_btns = QHBoxLayout()
            add_tuple_btn = QPushButton(self.tr("Add Tuple"))
            box_btns.addWidget(add_tuple_btn)
            delete_tuple_btn = QPushButton(self.tr("Delete Tuple"))
            box_btns.addWidget(delete_tuple_btn)
            add_column_btn = QPushButton(self.tr("Add Column"))
            box_btns.addWidget(add_column_btn)
            delete_column_btn = QPushButton(self.tr("Delete Column"))
            box_btns.addWidget(delete_column_btn)
            box.addLayout(box_btns)

            # Editable header
            header = custom_table.Header()
            self.table.setHorizontalHeader(header)
            box.addWidget(self.table)

            # Save and cancel button
            hbox = QHBoxLayout()
            hbox.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding))
            save_btn = QPushButton(self.tr("Save"))
            hbox.addWidget(save_btn)
            cancel_btn = QPushButton(self.tr("Cancel"))
            hbox.addWidget(cancel_btn)
            box.addLayout(hbox)

            # Button connection
            save_btn.clicked.connect(self.__save)
            cancel_btn.clicked.connect(self.close)
            add_tuple_btn.clicked.connect(self.__add_tuple)
            delete_tuple_btn.clicked.connect(self.__delete_tuple)
            add_column_btn.clicked.connect(self.__add_column)

        def __save(self):
            rname = ''
            if self.rela is None:
                # New
                rname = self._relation_name.text()
                if not rname.strip():
                    QMessageBox.critical(self, "Error",
                                         self.tr("Relation name "
                                                 "not specified"))
                    return
            nrela = relation.Relation()
            model = self.table.model()
            ncolumn = model.columnCount()
            nrow = model.rowCount()

            # Header
            try:
                header = []
                for i in range(ncolumn):
                    text = model.horizontalHeaderItem(i).text()
                    header.append(text)
                nrela.header = header
            except Exception as reason:
                QMessageBox.critical(self,
                                     self.tr("Header error"),
                                     str(reason))
                return
            for row in range(nrow):
                tuples = []
                for column in range(ncolumn):
                    item = model.item(row, column)
                    if item is None:
                        QMessageBox.critical(self, "Error",
                                             self.tr("Field '{0}:{1}'"
                                                     "is empty!".format(
                                                         row + 1, column + 1)))
                        return
                    tuples.append(item.text())
                nrela.insert(tuples)

            self.data = nrela, rname
            self.close()

        def __setup_edit_relation(self, rela):
            self.setWindowTitle(self.tr("Relation Editor"))
            model = self.table.model()
            model.setHorizontalHeaderLabels(rela.header)

            for row_count, row in enumerate(rela.content):
                for col_count, data in enumerate(row):
                    item = QStandardItem()
                    item.setText(data)
                    model.setItem(row_count, col_count, item)

        def __setup_new_relation(self):
            self.setWindowTitle(self.tr("Relation Creator"))
            model = QStandardItemModel(0, 2)
            self.table.setModel(model)
            header = self.table.horizontalHeader()
            header.model().setHeaderData(0,
                                         Qt.Horizontal,
                                         self.tr("Field 1"))
            header.model().setHeaderData(1,
                                         Qt.Horizontal,
                                         self.tr("Field 2"))

        def __add_tuple(self):
            model = self.table.model()
            model.insertRow(model.rowCount())

        def __delete_tuple(self):
            model = self.table.model()
            selection = self.table.selectionModel()
            if selection.hasSelection():
                r = QMessageBox.question(self,
                                         self.tr("Confirm tuple delete"),
                                         self.tr("Are you sure you want to "
                                                 "to delete the selected"
                                                 "tuple(s)?"),
                                         QMessageBox.Yes | QMessageBox.No)
                if r == QMessageBox.Yes:
                    selection = selection.selection()
                    rows = set([index.row() for index in selection.indexes()])
                    rows = sorted(list(rows))
                    previous = -1
                    i = len(rows) - 1
                    while i >= 0:
                        current = rows[i]
                        if current != previous:
                            model.removeRows(current, 1)
                        i -= 1

        def __add_column(self):
            model = self.table.model()
            model.insertColumn(model.columnCount())

    manager = RelationManager()
    manager.exec_()
    return manager.data
