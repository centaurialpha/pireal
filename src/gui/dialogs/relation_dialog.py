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
    # QTableView,
    # QAbstractItemView,
    QPushButton,
    QSpacerItem,
    QSizePolicy,
    QMessageBox,
    QLineEdit
)

from src.gui import view


class RelationDialog(QDialog):
    """ Base class for creator and edit relation """

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setWindowTitle(self.tr("Relation Editor"))
        # Data
        self.data = None
        self.resize(700, 500)
        box = QVBoxLayout(self)
        # Relation name
        self.relation_name = QLineEdit()
        self.relation_name.setVisible(False)
        box.addWidget(self.relation_name)
        # Buttons
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
        # La tabla es la vista
        self.view = view.View()
        box.addWidget(self.view)
        # Custom header que puede ser editado
        header = view.Header()
        self.view.setHorizontalHeader(header)
        # self.table = QTableView()
        # self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        # self.table.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        # self.table.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        # Editable header
        # header = custom_table.Header()
        # self.table.setHorizontalHeader(header)
        # box.addWidget(self.table)
        # Save and cancel button
        hbox = QHBoxLayout()
        hbox.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding))
        save_btn = QPushButton(self.tr("Ok"))
        hbox.addWidget(save_btn)
        cancel_btn = QPushButton(self.tr("Cancel"))
        hbox.addWidget(cancel_btn)
        box.addLayout(hbox)

        # Connections
        save_btn.clicked.connect(self.save)
        cancel_btn.clicked.connect(self.close)
        add_tuple_btn.clicked.connect(self.__add_tuple)
        delete_tuple_btn.clicked.connect(self.__delete_tuple)
        add_column_btn.clicked.connect(self.__add_column)
        delete_column_btn.clicked.connect(self.__delete_column)

    def setup_table(self, rela):
        raise NotImplementedError

    def save(self):
        raise NotImplementedError

    def __add_tuple(self):
        model = self.view.model()
        model.insertRow(model.rowCount())

    def __delete_tuple(self):
        model = self.table.model()
        selection = self.table.selectionModel()
        if selection.hasSelection():
            r = QMessageBox.question(self,
                                     self.tr("Confirm tuple delete"),
                                     self.tr("Are you sure you want "
                                             "to delete the selected "
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

    def __delete_column(self):
        model = self.table.model()
        if model.columnCount() >= 2:
            model.takeColumn(model.columnCount() - 1)
