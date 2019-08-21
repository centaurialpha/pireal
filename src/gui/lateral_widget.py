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
from collections import namedtuple

# from PyQt5.QtWidgets import QTreeWidget
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QSplitter
# from PyQt5.QtWidgets import QTreeWidgetItem
# from PyQt5.QtWidgets import QAbstractItemView
from PyQt5.QtWidgets import QVBoxLayout

from PyQt5.QtQuickWidgets import QQuickWidget

from PyQt5.QtCore import Qt
# from PyQt5.QtCore import QObject
from PyQt5.QtCore import QAbstractListModel
# from PyQt5.QtCore import pyqtProperty
from PyQt5.QtCore import pyqtSignal as Signal
from PyQt5.QtCore import pyqtSlot as Slot
from PyQt5.QtCore import QUrl
from PyQt5.QtCore import QModelIndex

from src import translations as tr
from src.gui.main_window import Pireal
from src.core import settings


RelationItem = namedtuple('Relation', 'name cardinality degree')


class RelationModel(QAbstractListModel):
    NameRole = Qt.UserRole + 1
    CardinalityRole = Qt.UserRole + 2
    DegreeRole = Qt.UserRole + 3

    def __init__(self, parent=None):
        super().__init__(parent)
        self._relations = []

    def add_item(self, item: RelationItem):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._relations.append(item)
        self.endInsertRows()

    def clear(self):
        self.beginResetModel()
        self._relations.clear()
        self.endResetModel()

    def rowCount(self, index=QModelIndex()):
        return len(self._relations)

    def data(self, index, role=Qt.DisplayRole):
        try:
            rel = self._relations[index.row()]
        except IndexError:
            return None
        if role == self.NameRole:
            return rel.name
        elif role == self.CardinalityRole:
            return rel.cardinality
        elif role == self.DegreeRole:
            return rel.degree
        return None

    def roleNames(self):
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

    # FIXME: puede que no necesite estas signals ya que la idea es usar el modelo

    # newRowsRequested = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setOrientation(Qt.Vertical)
        # Lista de relaciones de la base de datos
        self._relations_list_model = RelationModel()
        self._relations_list = RelationListQML(self._relations_list_model)
        self._relations_list.set_title(tr.TR_RELATIONS)
        self.addWidget(self._relations_list)
        # Lista de relaciones del resultado de consultas
        self._results_list_model = RelationModel()
        self._results_list = RelationListQML(self._results_list_model)
        self._results_list.set_title(tr.TR_TABLE_RESULTS)
        self.addWidget(self._results_list)

        Pireal.load_service("lateral_widget", self)

        # self._relations_list.itemClicked.connect(
        #     lambda i: self.relationClicked.emit(i))
        # self._results_list.itemClicked.connect(
        #     lambda i: self.resultClicked.emit(i))

    def add_relation_item(self, name: str, cardinality: int, degree: int):
        self._relations_list_model.add_item(RelationItem(name, cardinality, degree))

    def add_relation_result(self, name: str, cardinality: int, degree: int):
        self._results_list_model.add_item(RelationItem(name, cardinality, degree))

    def clear_relations(self):
        self._relations_list_model.clear()

    def clear_results(self):
        self._results_list_model.clear()


class RelationListQML(QWidget):

    # itemClicked = Signal(int)

    def __init__(self, model: RelationModel, parent=None):
        super().__init__(parent)
        vbox = QVBoxLayout(self)
        vbox.setContentsMargins(0, 0, 0, 0)
        view = QQuickWidget()
        view.rootContext().setContextProperty("relation_model", model)
        view.rootContext().setContextProperty("backend", self)
        qml = os.path.join(settings.QML_PATH, "ListRelation.qml")
        view.setSource(QUrl.fromLocalFile(qml))
        view.setResizeMode(QQuickWidget.SizeRootObjectToView)
        vbox.addWidget(view)

        self._root = view.rootObject()
        # self._root.itemClicked.connect(
        #     lambda i: self.itemClicked.emit(i))

    def set_title(self, title):
        self._root.setTitle(title)

    @Slot(int)
    def item_clicked(self, index):
        db = Pireal.get_service("central").get_active_db()
        if db is not None:
            db.relation_clicked(index)

    def add_item(self, name, card, deg):
        pass
    #     self._root.addItem(name, card, deg)

    def clear_items(self):
        pass
    #     self._root.clear()

    # def current_item(self):
    #     item = self._root.currentItem()
    #     name, index = None, None
    #     if item is not None:
    #         name, index = item.toVariant().values()
    #     return index, name

    # def has_item(self):
    #     return self._root.hasItem()

    # def current_text(self):
    #     return self._root.currentItemText()

    # def current_index(self):
    #     return self._root.currentIndex()

    # def update_cardinality(self, new_cardinality):
    #     self._root.setCardinality(new_cardinality)
