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
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtCore import Qt

from src.core import relation
from src.gui.dialogs import edit_relation_dialog


class NewRelationDialog(edit_relation_dialog.EditRelationDialog):

    def __init__(self, parent=None):
        super(NewRelationDialog, self).__init__(parent)
        self.setWindowTitle(self.tr("Relation Creator"))
        self.relation_name.setVisible(True)
        self.relation_name.setPlaceholderText(self.tr("Relation Name"))

    def setup_table(self):
        model = QStandardItemModel(0, 2)
        self.table.setModel(model)
        header = self.table.horizontalHeader()
        header.model().setHeaderData(0,
                                     Qt.Horizontal,
                                     self.tr("Field 1"))
        header.model().setHeaderData(1,
                                     Qt.Horizontal,
                                     self.tr("Field 2"))

    def save(self):
        relation_name = self.relation_name.text().strip()
        if not relation_name:
            QMessageBox.critical(self, "Error",
                                 self.tr("Relation name "
                                         "not specified"))
            return
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
                if item is None or item.text().strip():
                    QMessageBox.critical(self, "Error",
                                         self.tr("Field '{0}:{1}'"
                                                 "is empty!".format(
                                                     row + 1, column + 1)))
                    return
                tuples.append(item.text())
            rela.insert(tuples)

        # Data
        self.data = rela, relation_name
        self.close()


def create_relation():
    dialog = NewRelationDialog()
    dialog.setup_table()
    dialog.exec_()
    return dialog.data
