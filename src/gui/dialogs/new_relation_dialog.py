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
    QLineEdit,
    QPushButton,
    QSpacerItem,
    QSizePolicy
)
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtCore import Qt, pyqtSignal

from src.core import relation
from src.gui import view
from src.gui.main_window import Pireal


class NewRelationDialog(QDialog):

    created = pyqtSignal('PyQt_PyObject', 'QString')

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setWindowTitle(self.tr("Relation Creator"))
        # self.setModal(True)
        self.resize(700, 500)
        self.data = None
        box = QVBoxLayout(self)
        # Campo para el nombre de la relación
        self._line_relation_name = QLineEdit()
        self._line_relation_name.setPlaceholderText(self.tr("Relation Name"))
        box.addWidget(self._line_relation_name)
        hbox = QHBoxLayout()
        # Botones para agregar y eliminar tuplas/columnas
        btn_add_tuple = QPushButton(self.tr("Add Tuple"))
        hbox.addWidget(btn_add_tuple)
        btn_delete_tuple = QPushButton(self.tr("Delete Tuple"))
        hbox.addWidget(btn_delete_tuple)
        btn_add_column = QPushButton(self.tr("Add Column"))
        hbox.addWidget(btn_add_column)
        btn_delete_column = QPushButton(self.tr("Delete Column"))
        hbox.addWidget(btn_delete_column)
        box.addLayout(hbox)
        # Vista (tabla)
        self._view = view.View()
        box.addWidget(self._view)
        # Header personalizado para permitir ser editado
        header = view.Header()
        self._view.setHorizontalHeader(header)
        self._view.setModel(QStandardItemModel(0, 2))
        header.model().setHeaderData(0, Qt.Horizontal, self.tr("Field 1"))
        header.model().setHeaderData(1, Qt.Horizontal, self.tr("Field 2"))
        # Botones para crear/cancelar
        hhbox = QHBoxLayout()
        hhbox.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding))
        btn_create = QPushButton(self.tr("Create"))
        hhbox.addWidget(btn_create)
        btn_cancel = QPushButton(self.tr("Cancel"))
        hhbox.addWidget(btn_cancel)
        box.addLayout(hhbox)

        # Conexiones
        btn_add_tuple.clicked.connect(self.__add_tuple)
        btn_delete_tuple.clicked.connect(self.__delete_tuple)
        btn_add_column.clicked.connect(self.__add_column)
        btn_delete_column.clicked.connect(self.__delete_column)
        btn_cancel.clicked.connect(self.close)
        btn_create.clicked.connect(self._create)

    def __add_tuple(self):
        """ Agrega una tupla/fila al final de la tabla """

        model = self._view.model()
        model.insertRow(model.rowCount())

    def __delete_tuple(self):
        model = self._view.model()
        selection = self._view.selectionModel()

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
        model = self._view.model()
        model.insertColumn(model.columnCount())

    def __delete_column(self):
        model = self._view.model()
        if model.columnCount() >= 2:
            model.takeColumn(model.columnCount() - 1)

    def _create(self):

        relation_name = self._line_relation_name.text().strip()
        if not relation_name:
            QMessageBox.critical(self, "Error",
                                 self.tr("Relation name "
                                         "not specified"))
            return
        central = Pireal.get_service("central")
        if relation_name in central.get_active_db().table_widget.relations:
            QMessageBox.information(
                self,
                "Error",
                self.tr("Ya existe una relación con el nombre "
                        "<b>{}</b>.".format(relation_name))
            )
            return
        # Table model
        model = self._view.model()
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
                try:
                    if not item.text().strip():
                        raise Exception
                except:
                    QMessageBox.information(
                        self,
                        "Algo ha salido mal",
                        self.tr("Los espacios en blanco son tan aburridos :/."
                                "<br><br>Por favor ingrese un dato en la "
                                "fila <b>{}</b>, columna:<b>{}</b>".format(
                                    row + 1, column + 1)))
                    return
                tuples.append(item.text().strip())
            rela.insert(tuple(tuples))

        # Data
        # self.data = rela, relation_name
        self.created.emit(rela, relation_name)
        self.close()
