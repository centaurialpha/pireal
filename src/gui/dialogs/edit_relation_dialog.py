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
    QMessageBox,
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLineEdit,
    QSpacerItem,
    QSizePolicy
)
from src.gui import model, view
from src.core import relation
from src.gui.dialogs import relation_dialog


class EditRelationDialog(QDialog):

    def __init__(self, relation_obj, relation_name, parent=None):
        QDialog.__init__(self, parent)
        self.setWindowTitle(relation_name)
        self.resize(700, 500)
        box = QVBoxLayout(self)
        hbox = QHBoxLayout()
        btn_add_tuple = QPushButton(self.tr("Add Tuple"))
        hbox.addWidget(btn_add_tuple)
        btn_delete_tuple = QPushButton(self.tr("Delete Tuple"))
        hbox.addWidget(btn_delete_tuple)
        btn_add_column = QPushButton(self.tr("Add Column"))
        hbox.addWidget(btn_add_column)
        btn_delete_column = QPushButton(self.tr("Delete Column"))
        hbox.addWidget(btn_delete_column)
        box.addLayout(hbox)

        _view = view.View()
        _model = model.Model(relation_obj)
        _model.editable = True
        _view.setModel(_model)

        box.addWidget(_view)

        hhbox = QHBoxLayout()
        hhbox.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding))
        btn_save = QPushButton(self.tr("Ok"))
        hhbox.addWidget(btn_save)

        box.addLayout(hhbox)


"""
class EditRelationDialog(relation_dialog.RelationDialog):

    def __init__(self, parent=None):
        super(EditRelationDialog, self).__init__(parent)
        self.setWindowTitle(self.tr("Relation Editor"))

    def setup_table(self, rela):
        _model = model.Model(rela)
        _model.editable = True
        self.view.setModel(_model)

    def save(self):
        # Table model
        # model = self.table.model()
        # Row and column count
        # nrow = model.rowCount()
        # ncol = model.columnCount()
        # Create new relation object
        # rela = relation.Relation()

        # Header
        # try:
        #    header = []
        #    for i in range(ncol):
        #        text = model.horizontalHeaderItem(i).text().strip()
        #        header.append(text)
        #    rela.header = header
        # except Exception as reason:
        #    QMessageBox.critical(self,
        #                         self.tr("Header error"),
        #                         str(reason))
        #    return

        # Load relation
        # for row in range(nrow):
        #    tuples = []
        #    for column in range(ncol):
        #        item = model.item(row, column)
        #        if item is None or not item.text().strip():
        #            QMessageBox.critical(self, "Error",
        #                                 self.tr("Field '{0}:{1}'"
        #                                         "is empty!".format(
        #                                             row + 1, column + 1)))
        #            return
        #        text = item.text().strip()
        #        tuples.append(text)
        #    rela.insert(tuples)
        # self.data = rela
        # self.close()
        self.close()


def edit_relation(rela):
    dialog = EditRelationDialog()
    dialog.setup_table(rela)
    dialog.exec_()
    return dialog.data
"""