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

import os

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QSplitter
from PyQt5.QtWidgets import QVBoxLayout

from PyQt5.QtQuickWidgets import QQuickWidget

from PyQt5.QtCore import Qt
from PyQt5.QtCore import QAbstractListModel
from PyQt5.QtCore import pyqtSignal as Signal
from PyQt5.QtCore import QUrl

from pireal import translations as tr
from pireal.core import settings


class RelationModel(QAbstractListModel):

    NameRole = Qt.UserRole + 1
    CardinalityRole = NameRole + 1
    DegreeRole = CardinalityRole + 1

    def __init__(self, parent=None):
        super().__init__(parent)
        self._data = None

    def set_data(self, data):
        self._data = data

    def rowCount(self, index):
        return len(self._data)

    def data(self, index, role=Qt.DisplayRole):
        try:
            data = self._data[index.row()]
        except IndexError:
            return None
        if role == Qt.DisplayRole:
            return data.name
        return None

    def roles(self):
        return {
            self.NameRole: b'name',
            self.CardinalityRole: b'cardinality',
            self.DegreeRole: b'degree'
        }


class LateralWidget(QSplitter):
    """
    Widget que contiene la lista de relaciones y la lista de relaciones
    del resultado de consultas
    """

    relationClicked = Signal(int)
    relationSelectionChanged = Signal(int)

    resultClicked = Signal(int)
    resultSelectionChanged = Signal(int)

    newRowsRequested = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setOrientation(Qt.Vertical)
        # Lista de relaciones de la base de datos
        self._relations_list = RelationListQML(self.parent)
        self._relations_list.set_title(tr.TR_RELATIONS)
        self.addWidget(self._relations_list)
        # Lista de relaciones del resultado de consultas
        self._results_list = RelationListQML(self.parent)
        self._results_list.set_title(tr.TR_TABLE_RESULTS)
        self.addWidget(self._results_list)

        self._relations_list.itemClicked.connect(
            lambda i: self.relationClicked.emit(i))
        self._results_list.itemClicked.connect(
            lambda i: self.resultClicked.emit(i))

    @property
    def relation_list(self):
        return self._relations_list

    @property
    def result_list(self):
        return self._results_list


# FIXME: corregir el tema cuando se use el modelo correctamente
class RelationListQML(QWidget):

    itemClicked = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        vbox = QVBoxLayout(self)
        vbox.setContentsMargins(0, 0, 0, 0)
        self._view = QQuickWidget()
        self._set_source()
        self._view.setResizeMode(QQuickWidget.SizeRootObjectToView)
        vbox.addWidget(self._view)

        self._root = self._view.rootObject()

        self._root.itemClicked.connect(lambda i: self.itemClicked.emit(i))
        parent._parent.pireal.themeChanged.connect(self._reload)

    def _set_source(self):
        qml = os.path.join(settings.QML_PATH, "ListRelation.qml")
        self._view.setSource(QUrl.fromLocalFile(qml))

    def _reload(self):
        self._view.setSource(QUrl())
        self._set_source()
        self._root = self._view.rootObject()

    def set_title(self, title):
        self._root.setTitle(title)

    def add_item(self, name, card, deg):
        self._root.addItem(name, card, deg)

    def clear_items(self):
        self._root.clear()

    def current_item(self):
        item = self._root.currentItem()
        name, index = None, None
        if item is not None:
            name, index = item.toVariant().values()
        return index, name

    def has_item(self):
        return self._root.hasItem()

    def current_text(self):
        return self._root.currentItemText()

    def current_index(self):
        return self._root.currentIndex()

    def update_cardinality(self, new_cardinality):
        self._root.setCardinality(new_cardinality)
