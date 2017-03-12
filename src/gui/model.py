# -*- coding: utf-8 -*-
#
# Copyright 2015-2017 - Gabriel Acosta <acostadariogabriel@gmail.com>
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

from PyQt5.QtCore import (
    QAbstractTableModel,
    Qt,
    QVariant,
    QModelIndex
)


class Model(QAbstractTableModel):
    """ Modelo """

    def __init__(self, relation_obj):
        QAbstractTableModel.__init__(self)
        self.__data = relation_obj
        self.modified = False

    def rowCount(self, parent=QModelIndex()):
        """ Método reimplementado.
        Devuelve el número de filas, o dicho de otra forma, la
        cardinalidad de la relación o tabla
        """
        return self.__data.cardinality()

    def columnCount(self, parent=QModelIndex()):
        """ Método reimplementado.
        Devuelve el número de columnas, o dicho de otra forma, el grado
        de la relación o tabla
        """
        return self.__data.degree()

    def data(self, index, role):
        if not index.isValid():
            return QVariant()
        if role == Qt.DisplayRole:
            return list(self.__data.content)[index.row()][index.column()]

    def setData(self, index, value, role):
        """ Método reimplementado.
        Este método actualiza el modelo """

        if index.isValid() and role == Qt.EditRole:
            self.__data.update(index.row(), index.column(), value)
            # Emito la señal
            self.dataChanged.emit(index, index)
            self.modified = True
            return True
        return False

    def headerData(self, section, orientation, role):
        """ Método reimplementado.
        Devuelve el nombre de las columnas """

        if role == Qt.DisplayRole:
            return self.__data.header[section]

    def setHeaderData(self, section, orientation, value, role):
        """ Método reimplementado.
        Actualiza el nombre de una columna """

        if role == Qt.DisplayRole:
            # Actualizo el nuevo dato
            self.__data.header[section] = value
            # Emito la señal
            self.headerDataChanged.emit(orientation, section, section)
            self.modified = True
            return True

    def flags(self, index):
        """ Método reimplementado.
        Permite la edición en el modelo """

        flags = QAbstractTableModel.flags(self, index)
        flags |= Qt.ItemIsEditable
        return flags

    def insertRow(self, position, index=QModelIndex()):
        self.beginInsertRows(QModelIndex(), position, position)
        # FIXME: ver esto
        self.__data.insert(['-' for i in range(self.__data.cardinality())])
        self.endInsertRows()

    def clear(self):
        self.__data.content.clear()
