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

from PyQt5.QtWidgets import QSplitter

from PyQt5.QtCore import Qt
from PyQt5.QtCore import QAbstractListModel
from PyQt5.QtCore import pyqtSignal as Signal

from src import translations as tr
from src.gui.main_window import Pireal
from src.gui import qml_interface


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
        self.setOrientation(Qt.Vertical)
        # Lista de relaciones de la base de datos
        self._relations_list = RelationListQML()
        self._relations_list.set_title(tr.TR_RELATIONS)
        self.addWidget(self._relations_list)
        # Lista de relaciones del resultado de consultas
        self._results_list = RelationListQML()
        self._results_list.set_title(tr.TR_TABLE_RESULTS)
        self.addWidget(self._results_list)

        Pireal.load_service("lateral_widget", self)

        self._relations_list.itemClicked.connect(
            lambda i: self.relationClicked.emit(i))
        #         self._relations_list.row()))
        # self._relations_list.itemSelectionChanged.connect(
        #     lambda: self.relationSelectionChanged.emit(
        #         self._relations_list.row()))
        self._results_list.itemClicked.connect(
            lambda i: self.resultClicked.emit(i))
        #         self._results_list.row()))
        # self._results_list.itemSelectionChanged.connect(
        #     lambda: self.resultSelectionChanged.emit(
        #         self._results_list.row()))

    @property
    def relation_list(self):
        return self._relations_list

    @property
    def result_list(self):
        return self._results_list


class RelationListQML(qml_interface.QMLInterface):

    source = "ListRelation.qml"

    itemClicked = Signal(int)

    def initialize(self):
        self.root.itemClicked.connect(self.itemClicked.emit)

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
