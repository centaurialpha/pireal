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

from PyQt4.QtGui import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QSpacerItem,
    QSizePolicy
)
from PyQt4.QtCore import SIGNAL
from src.gui.main_window import Pireal


class NewRelationDialog(QDialog):

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setWindowTitle(self.tr("Nueva Relación"))
        vbox = QVBoxLayout(self)
        hbox = QHBoxLayout()
        self._line_relation_name = QLineEdit()
        hbox.addWidget(QLabel(self.tr("Nombre:")))
        hbox.addWidget(self._line_relation_name)
        vbox.addLayout(hbox)

        vbox.addWidget(QLabel(
            self.tr("La primera fila corresponde a los campos")))

        hbox = QHBoxLayout()
        btn_add_column = QPushButton(self.tr("Agregar Columna"))
        hbox.addWidget(btn_add_column)
        btn_add_tuple = QPushButton(self.tr("Agregar Tupla"))
        hbox.addWidget(btn_add_tuple)
        btn_remove_column = QPushButton(self.tr("Eliminar Columna"))
        hbox.addWidget(btn_remove_column)
        btn_remove_tuple = QPushButton(self.tr("Eliminar Tupla"))
        hbox.addWidget(btn_remove_tuple)
        vbox.addLayout(hbox)

        self._table = QTableWidget()
        vbox.addWidget(self._table)
        self._table.setRowCount(1)
        self._table.setColumnCount(2)
        self._table.setItem(0, 0, QTableWidgetItem("Campo 1"))
        self._table.setItem(0, 1, QTableWidgetItem("Campo 2"))

        hbox = QHBoxLayout()
        hbox.addItem(QSpacerItem(1, 0, QSizePolicy.Expanding))
        btn_ok = QPushButton(self.tr("Aceptar"))
        hbox.addWidget(btn_ok)
        btn_cancel = QPushButton(self.tr("Cancelar"))
        hbox.addWidget(btn_cancel)
        vbox.addLayout(hbox)

        # Connections
        self.connect(btn_add_column, SIGNAL("clicked()"),
            self.__add_column)
        self.connect(btn_remove_column, SIGNAL("clicked()"),
            self.__remove_column)
        self.connect(btn_add_tuple, SIGNAL("clicked()"),
            self.__add_tuple)
        self.connect(btn_remove_tuple, SIGNAL("clicked()"),
            self.__remove_tuple)
        self.connect(btn_ok, SIGNAL("clicked()"),
            self.__create_table)
        self.connect(btn_cancel, SIGNAL("clicked()"),
            self.close)

    def __add_column(self):
        columns = self._table.columnCount()
        self._table.insertColumn(columns)

    def __remove_column(self):
        current = self._table.currentColumn()
        self._table.removeColumn(current)

    def __add_tuple(self):
        tuples = self._table.rowCount()
        self._table.insertRow(tuples)

    def __remove_tuple(self):
        current = self._table.currentRow()
        self._table.removeRow(current)

    def __create_table(self):
        name = self._line_relation_name.text()
        rows = self._table.rowCount()
        columns = self._table.columnCount()

        # Generator
        #fields = (self._table.item(0, i).text() for i in range(columns))

        data = {}
        for row in range(rows):
            for column in range(columns):
                data[row, column] = self._table.item(row, column).text()

        table_widget = Pireal.get_service("db")
        table_widget.add_table(rows - 1, columns, name, data)

        self.close()