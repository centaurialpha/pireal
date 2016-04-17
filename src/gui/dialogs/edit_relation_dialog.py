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

from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import (
    QStandardItem,
    QStandardItemModel
)

from src.core import relation
from src.gui.dialogs import relation_dialog


class EditRelationDialog(relation_dialog.RelationDialog):

    def __init__(self, parent=None):
        super(EditRelationDialog, self).__init__(parent)
        self.setWindowTitle(self.tr("Relation Editor"))

    def setup_table(self, rela):
        # Table model
        model = QStandardItemModel()
        self.table.setModel(model)
        # Set header
        model.setHorizontalHeaderLabels(rela.header)

        # Populate table
        for row_count, row in enumerate(rela.content):
            for col_count, data in enumerate(row):
                item = QStandardItem()
                item.setText(data)
                model.setItem(row_count, col_count, item)

    def save(self):
        # Table model
        model = self.table.model()
        # Row and column count
        nrow = model.rowCount()
        ncol = model.columnCount()
        # Create new relation object
        rela = relation.Relation()

        # Header
        try:
            header = []
            for i in range(ncol):
                text = model.horizontalHeaderItem(i).text().strip()
                header.append(text)
            rela.header = header
        except Exception as reason:
            QMessageBox.critical(self,
                                 self.tr("Header error"),
                                 str(reason))
            return

        # Load relation
        for row in range(nrow):
            tuples = []
            for column in range(ncol):
                item = model.item(row, column)
                if item is None or not item.text().strip():
                    QMessageBox.critical(self, "Error",
                                         self.tr("Field '{0}:{1}'"
                                                 "is empty!".format(
                                                     row + 1, column + 1)))
                    return
                tuples.append(item.text().strip())
            rela.insert(tuples)
        self.data = rela
        self.close()


def edit_relation(rela):
    dialog = EditRelationDialog()
    dialog.setup_table(rela)
    dialog.exec_()
    return dialog.data
