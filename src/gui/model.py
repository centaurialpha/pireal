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

from PyQt5.QtGui import (
    QColor,
    QFont
)
from PyQt5.QtCore import (
    QAbstractTableModel,
    Qt,
    QVariant,
    QModelIndex,
    pyqtSignal
)


class Model(QAbstractTableModel):
    """ Modelo """

    modelModified = pyqtSignal(bool)
    degreeChanged = pyqtSignal(int)
    cardinalityChanged = pyqtSignal(int)

    def __init__(self, relation_obj):
        QAbstractTableModel.__init__(self)
        self.__data = relation_obj
        self.modified = False
        self.editable = True

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
        row, col = index.row(), index.column()
        content = list(self.__data.content)
        if role == Qt.DisplayRole:
            return content[row][col]
        elif role == Qt.TextColorRole:
            value = content[row][col]
            if value == 'null':
                # Para las operaciones de left, right y full other join
                return QColor('red')
        elif role == Qt.FontRole:
            font = QFont()
            font.setPointSize(10)
            return font
        elif role == Qt.TextAlignmentRole:
            return Qt.AlignHCenter

    def setData(self, index, value, role):
        """ Método reimplementado.
        Este método actualiza el modelo """
        if index.isValid() and role == Qt.EditRole:
            modified = False
            # old_value = self.__data.content[index.row()][index.column()]
            old_value = list(self.__data.content)[index.row()][index.column()]
            if value != old_value:
                # Si son distintos los datos, actualizo
                self.__data.update(index.row(), index.column(), value)
                modified = True
            # Emito la señal
            self.dataChanged.emit(index, index)
            self.set_modified(modified)
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
            modified = False
            old_value = self.__data.header[section]
            if value != old_value:
                # Actualizo el nuevo dato
                self.__data.header[section] = value
                modified = True
            # Emito la señal
            self.headerDataChanged.emit(orientation, section, section)
            self.set_modified(modified)
            return True

    def flags(self, index):
        """ Método reimplementado.
        Permite la edición en el modelo """

        flags = QAbstractTableModel.flags(self, index)
        if self.editable:
            flags |= Qt.ItemIsEditable
        return flags

    def insertRow(self, position, tupla, index=QModelIndex()):
        """ Método reimplementado.
        Inserta una fila al final de la tabla y emite una señal con
        el nuevo valor de cardinalidad """

        self.beginInsertRows(QModelIndex(), position, position)
        self.__data.insert(tupla)
        self.cardinalityChanged.emit(self.__data.cardinality())
        self.set_modified(True)
        self.endInsertRows()

    def insertColumn(self, position, index=QModelIndex()):
        """ Método reimplementado.
        Inserta una columna al final de la tabla """

        self.beginInsertColumns(QModelIndex(), position, position)
        self.__data.append_column()
        self.set_modified(True)
        self.endInsertColumns()

    def removeRow(self, row, parent=QModelIndex()):
        """ Método reimplementado.
        Elimina una fila del modelo y emite una señal con el nuevo
        valor de cardinalidad """

        self.beginRemoveRows(QModelIndex(), row, row)
        data = list(self.__data.content)[row]
        self.__data.content.remove(data)
        self.cardinalityChanged.emit(self.__data.cardinality())
        self.set_modified(True)
        self.endRemoveRows()

    def removeColumn(self, col, parent=QModelIndex()):
        """ Método reimplementado.
        Elimina una columna del modelo """

        self.beginRemoveColumns(QModelIndex(), col, col)
        self.__data.remove_column(col)
        self.set_modified(True)
        self.endRemoveColumns()

    def set_modified(self, val):
        self.modified = val
        self.modelModified.emit(val)

    def clear(self):
        self.__data.content.clear()
