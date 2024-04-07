# -*- coding: utf-8 -*-
#
# Copyright 2015-2021 - Gabriel Acosta <acostadariogabriel@gmail.com>
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

from PyQt6.QtCore import QAbstractTableModel, QModelIndex, Qt
from PyQt6.QtCore import pyqtSlot as Slot
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QHeaderView,
    QInputDialog,
    QItemDelegate,
    QTableView,
)

from pireal import translations as tr
from pireal.gui.theme import get_color

logger = logging.getLogger("gui.model_view_delegate")


class RelationModel(QAbstractTableModel):
    def __init__(self, relation_object):
        super().__init__()
        self.editable = True
        self.relation = relation_object
        self._null_text_color = QColor(get_color("BrightText"))

    def rowCount(self, parent=QModelIndex()):
        """Devuelve la cardinalidad de la relación"""
        if parent.isValid():
            return 0
        return self.relation.cardinality()

    def columnCount(self, parent=QModelIndex()):
        """Devuelve el grado de la relación"""
        if parent.isValid():
            return 0
        return self.relation.degree()

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None

        row, column = index.row(), index.column()
        data = self.relation.content
        if role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole:
            return data[row][column]
        elif role == Qt.ItemDataRole.ForegroundRole:
            value = data[row][column]
            if value == "null":
                return self._null_text_color
        return None

    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole:
            return self.relation.header[section]

    def setHeaderData(self, section, orientation, value, role):
        if role == Qt.ItemDataRole.DisplayRole:
            old_value = self.relation.header[section]
            if value != old_value:
                self.relation.header[section] = value
                self.headerDataChanged.emit(orientation, section, section)
                return True

    def flags(self, index):
        flags = super().flags(index)
        if self.editable:
            flags |= Qt.ItemFlag.ItemIsEditable
        return flags

    def setData(self, index, value, role):
        if index.isValid() and role == Qt.ItemDataRole.EditRole:
            current_value = self.data(index)
            if current_value != value:
                self.relation.update(index.row(), index.column(), value)
                self.dataChanged.emit(index, index)
                logger.debug(
                    "Editing %d:%d - Current: %s, New: %s",
                    index.row(),
                    index.column(),
                    current_value,
                    value,
                )
                # FIXME: avisar que se ha modificado la base de datos
                return True
        return False


class View(QTableView):
    """Vista"""

    def __init__(self):
        super(View, self).__init__()
        # self.setAlternatingRowColors(CONFIG.get('alternatingRowColors'))
        self.verticalHeader().hide()
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        # Scroll content per pixel
        self.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.setHorizontalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.horizontalHeader().setHighlightSections(False)

    def resizeEvent(self, event):
        super(View, self).resizeEvent(event)
        self.adjust_columns()

    def adjust_columns(self):
        """Resize all sections to content and user interactive"""
        header = self.horizontalHeader()
        for column in range(header.count()):
            header.setSectionResizeMode(column, QHeaderView.ResizeMode.ResizeToContents)
            width = header.sectionSize(column)
            header.setSectionResizeMode(column, QHeaderView.ResizeMode.Interactive)
            header.resizeSection(column, width)
        self.horizontalHeader().setMinimumHeight(32)


class Header(QHeaderView):
    def __init__(self, orientation=Qt.Orientation.Horizontal, parent=None):
        super(Header, self).__init__(orientation, parent)
        self.editable = True
        self.setSectionsClickable(True)
        self.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        # Connections
        self.sectionDoubleClicked[int].connect(self._on_section_double_clicked)

    @Slot(int)
    def _on_section_double_clicked(self, index):
        if not self.editable:
            return
        name, ok = QInputDialog.getText(
            self, tr.TR_INPUT_DIALOG_HEADER_TITLE, tr.TR_INPUT_DIALOG_HEADER_BODY
        )
        if ok:
            self.model().setHeaderData(index, Qt.Orientation.Horizontal, name.strip())


class Delegate(QItemDelegate):
    """Delegado
    Asegura que al editar un campo no se envíe un dato vacío
    """

    def __init__(self, parent=None):
        super().__init__(parent)

    def setModelData(self, editor, model, index):
        data = editor.text().strip()
        if data:
            model.setData(index, data, Qt.ItemDataRole.EditRole)

    def setEditorData(self, editor, index):
        text = index.model().data(index, Qt.ItemDataRole.DisplayRole)
        editor.setText(text)


def create_view(relation, *, editable=False):
    view = View()
    model = RelationModel(relation)
    model.editable = editable
    view.setModel(model)
    view.setItemDelegate(Delegate())
    return view
