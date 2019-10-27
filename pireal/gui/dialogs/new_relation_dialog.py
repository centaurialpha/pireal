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
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QSpacerItem
from PyQt5.QtWidgets import QSizePolicy

from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtCore import Qt

from pireal import translations as tr

from pireal.core import relation
from pireal.gui import view
# from pireal.gui.main_window import Pireal

logger = logging.getLogger(__name__)


class NewRelationDialog(QDialog):

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self._central = parent
        self.setWindowTitle(tr.TR_RELATION_DIALOG_TITLE)
        # self.setModal(True)
        self._data = None
        self.resize(700, 500)
        box = QVBoxLayout(self)
        # Campo para el nombre de la relación
        self._line_relation_name = QLineEdit()
        self._line_relation_name.setPlaceholderText(tr.TR_RELATION_DIALOG_NAME)
        box.addWidget(self._line_relation_name)
        hbox = QHBoxLayout()
        # Botones para agregar y eliminar tuplas/columnas
        btn_add_tuple = QPushButton(tr.TR_RELATION_DIALOG_ADD_TUPLE)
        hbox.addWidget(btn_add_tuple)
        btn_delete_tuple = QPushButton(tr.TR_RELATION_DIALOG_DELETE_TUPLE)
        hbox.addWidget(btn_delete_tuple)
        btn_add_column = QPushButton(tr.TR_RELATION_DIALOG_ADD_COLUMN)
        hbox.addWidget(btn_add_column)
        btn_delete_column = QPushButton(tr.TR_RELATION_DIALOG_DELETE_COLUMN)
        hbox.addWidget(btn_delete_column)
        box.addLayout(hbox)
        # Vista (tabla)
        self._view = view.View()
        box.addWidget(self._view)
        # Header personalizado para permitir ser editado
        header = view.Header()
        self._view.setHorizontalHeader(header)
        self._view.setModel(QStandardItemModel(0, 2))
        header.model().setHeaderData(0, Qt.Horizontal, tr.TR_RELATION_DIALOG_FIELD1)
        header.model().setHeaderData(1, Qt.Horizontal, tr.TR_RELATION_DIALOG_FIELD2)
        # Botones para crear/cancelar
        hhbox = QHBoxLayout()
        hhbox.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding))
        btn_create = QPushButton(tr.TR_RELATION_DIALOG_CREATE)
        hhbox.addWidget(btn_create)
        btn_cancel = QPushButton(tr.TR_MSG_CANCEL)
        hhbox.addWidget(btn_cancel)
        box.addLayout(hhbox)

        # Conexiones
        btn_add_tuple.clicked.connect(self.__add_tuple)
        btn_delete_tuple.clicked.connect(self.__delete_tuple)
        btn_add_column.clicked.connect(self.__add_column)
        btn_delete_column.clicked.connect(self.__delete_column)
        btn_cancel.clicked.connect(self.close)
        btn_create.clicked.connect(self._create)

    def get_data(self):
        return self._data

    def __add_tuple(self):
        """ Agrega una tupla/fila al final de la tabla """

        model = self._view.model()
        model.insertRow(model.rowCount())

    def __delete_tuple(self):
        model = self._view.model()
        selection = self._view.selectionModel()
        if selection.hasSelection():
            r = QMessageBox.question(
                self,
                tr.TR_RELATION_DIALOG_CONFIRM_DELETE_TUPLE,
                tr.TR_RELATION_DIALOG_CONFIRM_DELETE_TUPLE_BODY,
                QMessageBox.Yes | QMessageBox.No
            )
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
        if model.columnCount() > 2:
            model.takeColumn(model.columnCount() - 1)

    def _create(self):

        relation_name = self._line_relation_name.text().strip()
        if not relation_name:
            QMessageBox.information(self, tr.TR_MSG_ERROR,
                                    tr.TR_RELATION_DIALOG_EMPTY_RELATION_NAME)
            logger.debug('Relation name not specified')
            return
        # central = Pireal.get_service("central")
        if relation_name in self._central.get_active_db().table_widget.relations:
            QMessageBox.information(
                self,
                tr.TR_MSG_ERROR,
                tr.TR_RELATION_NAME_ALREADY_EXISTS.format(relation_name)
            )
            logger.debug('Relation already exists with this name')
            return
        logger.debug('Creating new relation: %s', relation_name)
        # Table model
        model = self._view.model()
        # Row and column count
        nrow = model.rowCount()
        ncol = model.columnCount()
        # Create new relation object
        rela = relation.Relation()

        # Header
        header = []
        for i in range(ncol):
            text = model.horizontalHeaderItem(i).text().strip()
            header.append(text)
        try:
            rela.header = header
        except relation.InvalidFieldNameError as reason:
            QMessageBox.critical(self,
                                 tr.TR_MSG_ERROR,
                                 str(reason))
            logger.warning('Invalid field name \'%s\'', reason.campo)
            return

        # Load relation
        for row in range(nrow):
            tuples = []
            for column in range(ncol):

                item = model.item(row, column)
                if item is None:
                    QMessageBox.information(
                        self,
                        tr.TR_MSG_ERROR,
                        tr.TR_RELATION_DIALOG_WHITESPACE.format(row + 1, column + 1))
                    logger.warning('Not data in \'%d:%d\'', row + 1, column + 1)
                    return
                data = item.text().strip()
                tuples.append(data)
            rela.insert(tuple(tuples))

        # Data
        self._data = (rela, relation_name)
        self.accept()
