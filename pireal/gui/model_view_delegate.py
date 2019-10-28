# -*- coding: utf-8 -*-
#
# Copyright 2015-2019 - Gabriel Acosta <acostadariogabriel@gmail.com>
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

from PyQt5.QtWidgets import QTableView
from PyQt5.QtWidgets import QHeaderView
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QAbstractItemView
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QItemDelegate
from PyQt5.QtWidgets import QStyle

from PyQt5.QtGui import QPalette
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QFont

from PyQt5.QtCore import QAbstractTableModel
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QModelIndex
from PyQt5.QtCore import pyqtSignal as Signal

from pireal import translations as tr
from pireal.core.settings import CONFIG

logger = logging.getLogger(__name__)


class RelationModel(QAbstractTableModel):

    def __init__(self, relation_object):
        super().__init__()
        self.editable = True
        self._relation = relation_object

    def rowCount(self, index):
        """Devuelve la cardinalidad de la relación"""
        return self._relation.cardinality()

    def columnCount(self, index):
        """Devuelve el grado de la relación"""
        return self._relation.degree()

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None

        row, column = index.row(), index.column()
        data = list(self._relation.content)
        if role == Qt.DisplayRole or role == Qt.EditRole:
            return data[row][column]
        elif role == Qt.TextColorRole:
            value = data[row][column]
            # FIXME: mejorar esto
            if value == 'null':
                return QColor('red')
        return None

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            return self._relation.header[section]

    def setHeaderData(self, section, orientation, value, role):
        if role == Qt.DisplayRole:
            old_value = self._relation.header[section]
            if value != old_value:
                self._relation.header[section] = value
                self.headerDataChanged.emit(orientation, section, section)
                return True

    def flags(self, index):
        flags = super().flags(index)
        if self.editable:
            flags |= Qt.ItemIsEditable
        return flags

    def setData(self, index, value, role):
        if index.isValid() and role == Qt.EditRole:
            current_value = self.data(index)
            if current_value != value:
                self._relation.update(index.row(), index.column(), value)
                self.dataChanged.emit(index, index)
                logger.debug('Editing %d:%d - Current: %s, New: %s',
                             index.row(), index.column(), current_value, value)
                # FIXME: avisar que se ha modificado la base de datos
                return True
        return False


class View(QTableView):
    """ Vista """

    def __init__(self):
        super(View, self).__init__()
        self.setAlternatingRowColors(CONFIG.get('alternatingRowColors'))
        self.verticalHeader().hide()
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        # Scroll content per pixel
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.horizontalHeader().setHighlightSections(False)

    def resizeEvent(self, event):
        super(View, self).resizeEvent(event)
        self.adjust_columns()

    def adjust_columns(self):
        """ Resize all sections to content and user interactive """

        header = self.horizontalHeader()
        for column in range(header.count()):
            header.setSectionResizeMode(column, QHeaderView.ResizeToContents)
            width = header.sectionSize(column)
            header.setSectionResizeMode(column, QHeaderView.Interactive)
            header.resizeSection(column, width)
        self.horizontalHeader().setMinimumHeight(32)


class Header(QHeaderView):

    def __init__(self, orientation=Qt.Horizontal, parent=None):
        super(Header, self).__init__(orientation, parent)
        self.editable = True
        self.setSectionsClickable(True)
        self.setSectionResizeMode(QHeaderView.ResizeToContents)
        self.line = QLineEdit(parent=self.viewport())
        self.line.setAlignment(Qt.AlignTop)
        self.line.setHidden(True)
        self.line.blockSignals(True)
        self.col = 0

        # Connections
        self.sectionDoubleClicked[int].connect(self.__edit)
        self.line.editingFinished.connect(self.__done_editing)

    def __edit(self, index):
        if not self.editable:
            return
        geo = self.line.geometry()
        geo.setWidth(self.sectionSize(index))
        geo.moveLeft(self.sectionViewportPosition(index))
        current_text = self.model().headerData(index, Qt.Horizontal,
                                               Qt.DisplayRole)
        self.line.setGeometry(geo)
        self.line.setHidden(False)
        self.line.blockSignals(False)
        self.line.setText(str(current_text))
        self.line.setFocus()
        self.line.selectAll()
        self.col = index

    def __done_editing(self):
        text = self.line.text()
        if not text.strip():
            # No debe ser vacío
            QMessageBox.critical(self, tr.TR_MSG_ERROR, tr.TR_HEADER_NOT_EMPTY)
            self.line.hide()
            return
        self.line.blockSignals(True)
        self.line.setHidden(False)
        self.model().setHeaderData(self.col, Qt.Horizontal, text,
                                   Qt.DisplayRole)
        self.line.setText("")
        self.line.hide()
        self.setCurrentIndex(QModelIndex())


class Delegate(QItemDelegate):
    """ Delegado
    Asegura que al editar un campo no se envíe un dato vacío
    """

    def __init__(self, parent=None):
        super().__init__(parent)

    def setModelData(self, editor, model, index):
        data = editor.text().strip()
        if data:
            model.setData(index, data, Qt.EditRole)

    def setEditorData(self, editor, index):
        text = index.model().data(index, Qt.DisplayRole)
        editor.setText(text)

    def paint(self, painter, opt, index):
        if opt.state & QStyle.State_Selected:
            opt.palette.setColor(QPalette.Highlight, QColor("#fffde1"))
            painter.drawRect(opt.rect)
        opt.palette.setColor(QPalette.HighlightedText, Qt.black)
        super().paint(painter, opt, index)

# class _Model(QAbstractTableModel):
#     """ Modelo """

#     modelModified = Signal(bool)
#     degreeChanged = Signal(int)
#     cardinalityChanged = Signal(int)

#     def __init__(self, relation_obj):
#         QAbstractTableModel.__init__(self)
#         self.__data = relation_obj
#         self.modified = False
#         self.editable = True

#     def rowCount(self, parent=QModelIndex()):
#         """ Método reimplementado.
#         Devuelve el número de filas, o dicho de otra forma, la
#         cardinalidad de la relación o tabla
#         """
#         return self.__data.cardinality()

#     def columnCount(self, parent=QModelIndex()):
#         """ Método reimplementado.
#         Devuelve el número de columnas, o dicho de otra forma, el grado
#         de la relación o tabla
#         """
#         return self.__data.degree()

#     def data(self, index, role):
#         if not index.isValid():
#             # return QVariant()
#             return None
#         row, col = index.row(), index.column()
#         content = list(self.__data.content)
#         if role == Qt.DisplayRole:
#             return content[row][col]
#         elif role == Qt.TextColorRole:
#             value = content[row][col]
#             if value == 'null':
#                 # Para las operaciones de left, right y full other join
#                 return QColor('red')
#         elif role == Qt.FontRole:
#             font = QFont()
#             font.setPointSize(10)
#             return font
#         elif role == Qt.TextAlignmentRole:
#             return Qt.AlignHCenter

#     def setData(self, index, value, role):
#         """ Método reimplementado.
#         Este método actualiza el modelo """
#         if index.isValid() and role == Qt.EditRole:
#             modified = False
#             # old_value = self.__data.content[index.row()][index.column()]
#             old_value = list(self.__data.content)[index.row()][index.column()]
#             if value != old_value:
#                 # Si son distintos los datos, actualizo
#                 self.__data.update(index.row(), index.column(), value)
#                 modified = True
#             # Emito la señal
#             self.dataChanged.emit(index, index)
#             self.set_modified(modified)
#             return True
#         return False

#     def headerData(self, section, orientation, role):
#         """ Método reimplementado.
#         Devuelve el nombre de las columnas """

#         if role == Qt.DisplayRole:
#             return self.__data.header[section]

#     def setHeaderData(self, section, orientation, value, role):
#         """ Método reimplementado.
#         Actualiza el nombre de una columna """

#         if role == Qt.DisplayRole:
#             modified = False
#             old_value = self.__data.header[section]
#             if value != old_value:
#                 # Actualizo el nuevo dato
#                 self.__data.header[section] = value
#                 modified = True
#             # Emito la señal
#             self.headerDataChanged.emit(orientation, section, section)
#             self.set_modified(modified)
#             return True

#     def flags(self, index):
#         """ Método reimplementado.
#         Permite la edición en el modelo """

#         flags = QAbstractTableModel.flags(self, index)
#         if self.editable:
#             flags |= Qt.ItemIsEditable
#         return flags

#     def insertRow(self, position, tupla, index=QModelIndex()):
#         """ Método reimplementado.
#         Inserta una fila al final de la tabla y emite una señal con
#         el nuevo valor de cardinalidad """

#         self.beginInsertRows(QModelIndex(), position, position)
#         self.__data.insert(tupla)
#         self.cardinalityChanged.emit(self.__data.cardinality())
#         self.set_modified(True)
#         self.endInsertRows()

#     def insertColumn(self, position, index=QModelIndex()):
#         """ Método reimplementado.
#         Inserta una columna al final de la tabla """

#         self.beginInsertColumns(QModelIndex(), position, position)
#         self.__data.append_column()
#         self.set_modified(True)
#         self.endInsertColumns()

#     def removeRow(self, row, parent=QModelIndex()):
#         """ Método reimplementado.
#         Elimina una fila del modelo y emite una señal con el nuevo
#         valor de cardinalidad """

#         self.beginRemoveRows(QModelIndex(), row, row)
#         data = list(self.__data.content)[row]
#         self.__data.content.remove(data)
#         self.cardinalityChanged.emit(self.__data.cardinality())
#         self.set_modified(True)
#         self.endRemoveRows()

#     def removeColumn(self, col, parent=QModelIndex()):
#         """ Método reimplementado.
#         Elimina una columna del modelo """

#         self.beginRemoveColumns(QModelIndex(), col, col)
#         self.__data.remove_column(col)
#         self.set_modified(True)
#         self.endRemoveColumns()

#     def set_modified(self, val):
#         self.modified = val
#         self.modelModified.emit(val)

#     def clear(self):
#         self.__data.content.clear()
