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
    QPushButton,
    QSpacerItem,
    QSizePolicy,
    QMessageBox,
    QHeaderView,
    QLineEdit,
    QAbstractItemView
)
from PyQt5.QtGui import QStandardItem
from PyQt5.QtCore import (
    Qt,
    QModelIndex
)

from src.gui import custom_table
from src.core import relation


class RelationEditor(QDialog):

    def __init__(self, relation, parent=None):
        super(RelationEditor, self).__init__(parent)
        self._relation = relation
        self._parent = parent
        self.data = None
        self.setWindowTitle(self.tr("Relation Editor"))
        self.resize(700, 500)
        box = QVBoxLayout(self)

        # Buttons layout
        box_btns = QHBoxLayout()
        add_tuple_btn = QPushButton(self.tr("Add Tuple"))
        box_btns.addWidget(add_tuple_btn)
        remove_tuple_btn = QPushButton(self.tr("Remove Tuple"))
        box_btns.addWidget(remove_tuple_btn)
        add_column_btn = QPushButton(self.tr("Add Column"))
        box_btns.addWidget(add_column_btn)
        remove_column_btn = QPushButton(self.tr("Remove Column"))
        box_btns.addWidget(remove_column_btn)
        box.addLayout(box_btns)

        # Table
        self.table = custom_table.Table()
        self.table.setHorizontalHeader(Header())
        box.addWidget(self.table)
        self.setup_table()

        # Save and cancel button
        hbox = QHBoxLayout()
        hbox.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding))
        btn_save = QPushButton(self.tr("Save"))
        hbox.addWidget(btn_save)
        btn_cancel = QPushButton(self.tr("Cancel"))
        hbox.addWidget(btn_cancel)
        box.addLayout(hbox)

        # Buttons connection
        add_tuple_btn.clicked.connect(self.__add_tuple)
        remove_tuple_btn.clicked.connect(self.__remove_tuple)
        add_column_btn.clicked.connect(self.__add_column)
        btn_save.clicked.connect(self.save)
        btn_cancel.clicked.connect(self.close)

    def __add_tuple(self):
        model = self.table.model()
        model.insertRow(model.rowCount())

    def __remove_tuple(self):
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

    def save(self):
        model = self.table.model()
        ncolumn = model.columnCount()
        nrow = model.rowCount()

        header = []

        # Update relation
        for i in range(ncolumn):
            header.append(model.horizontalHeaderItem(i).text())

        rela = relation.Relation()
        rela.header = header

        for row in range(nrow):
            tuple_ = []
            for column in range(ncolumn):
                item = model.item(row, column)
                tuple_.append(item.text())
            rela.insert(tuple_)

        # Update table
        #FIXME: this sucks!
        table = self._parent.get_active_db().table_widget.current_table()
        mmodel = table.model()
        row_count = 0
        for row in rela.content:
            for col_count, data in enumerate(row):
                item = QStandardItem(data)
                mmodel.setItem(row_count, col_count, item)
            row_count += 1

        self.data = rela
        self.close()

    def setup_table(self):
        model = self.table.model()
        model.setHorizontalHeaderLabels(self._relation.header)

        row_count = 0
        for row in self._relation.content:
            for col_count, data in enumerate(row):
                item = QStandardItem(data)
                model.setItem(row_count, col_count, item)
            row_count += 1


class Header(QHeaderView):

    def __init__(self, orientation=Qt.Horizontal, parent=None):
        super(Header, self).__init__(orientation, parent)
        self.setSectionsClickable(True)
        self.setSectionResizeMode(QHeaderView.Stretch)
        self.setSelectionBehavior(QAbstractItemView.SelectColumns)
        self.line = QLineEdit(parent=self.viewport())
        self.line.setAlignment(Qt.AlignTop)
        self.line.setHidden(True)
        self.line.blockSignals(True)
        self.col = 0

        # Connections
        self.sectionDoubleClicked[int].connect(self._edit_header)
        self.line.editingFinished.connect(self._done_editing)

    def _edit_header(self, index):
        current_text = self.model().headerData(index, Qt.Horizontal)
        geo = self.line.geometry()
        geo.setWidth(self.sectionSize(index))
        geo.moveLeft(self.sectionViewportPosition(index))
        self.line.setGeometry(geo)

        self.line.setHidden(False)
        self.line.blockSignals(False)
        self.line.setFocus()
        self.col = index
        self.line.setText(current_text)

    def _done_editing(self):
        self.line.blockSignals(True)
        self.line.setHidden(False)
        text = self.line.text()
        self.model().setHeaderData(self.col, Qt.Horizontal, text)
        self.line.setText("")
        self.line.hide()
        self.setCurrentIndex(QModelIndex())