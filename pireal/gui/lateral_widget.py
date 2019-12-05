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

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QSplitter
from PyQt5.QtWidgets import QVBoxLayout

from PyQt5.QtQuickWidgets import QQuickWidget

from PyQt5.QtCore import Qt
from PyQt5.QtCore import QModelIndex
from PyQt5.QtCore import QAbstractListModel
from PyQt5.QtCore import pyqtSignal as Signal
from PyQt5.QtCore import pyqtSlot as Slot
from PyQt5.QtCore import QUrl

from pireal import translations as tr
from pireal.core import settings

RelationItem = namedtuple('Relation', 'name cardinality degree')


class RelationModel(QAbstractListModel):

    NameRole = Qt.UserRole + 1
    CardinalityRole = Qt.UserRole + 2
    DegreeRole = Qt.UserRole + 3

    def __init__(self, parent=None):
        super().__init__(parent)
        self._relations = []

    def add_relation(self, relation: RelationItem):
        self.beginInsertRows(QModelIndex(), len(self._relations), len(self._relations))
        self._relations.append(relation)
        self.endInsertRows()

    def relation_by_index(self, index) -> RelationItem:
        return self._relations[index]

    def remove_relation(self, index: int):
        self.beginRemoveRows(QModelIndex(), index, index)
        self._relations.pop(index)
        self.endRemoveRows()

    def clear(self):
        self.beginResetModel()
        self._relations.clear()
        self.endResetModel()

    def rowCount(self, index=QModelIndex()):
        return len(self._relations)

    def data(self, index, role=Qt.DisplayRole):
        try:
            relation = self._relations[index.row()]
        except IndexError:
            return None
        if role == self.NameRole:
            return relation.name
        elif role == self.CardinalityRole:
            return relation.cardinality
        elif role == self.DegreeRole:
            return relation.degree
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

    relationClicked = Signal(int)
    relationClosed = Signal(int, str)
    resultClicked = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        # self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)
        self.parent = parent
        self.setOrientation(Qt.Vertical)
        self._relations_model = RelationModel()
        self._relations_view = RelationListQML(self._relations_model, closable=True, parent=self)
        self._relations_view.set_title(tr.TR_RELATIONS)
        self.addWidget(self._relations_view)
        self._results_model = RelationModel()
        self._results_view = RelationListQML(self._results_model, parent=self)
        self._results_view.set_title(tr.TR_TABLE_RESULTS)
        self.addWidget(self._results_view)

        self._relations_view.itemClicked[int].connect(self.relationClicked.emit)
        self._results_view.itemClicked[int].connect(self.resultClicked.emit)
        self._relations_view.itemClosed[int, str].connect(self.relationClosed.emit)

    @property
    def relations_view(self):
        return self._relations_view

    def add_item_to_relations(self, name: str, cardinality: int, degree: int):
        item = RelationItem(name, cardinality, degree)
        self._relations_model.add_relation(item)

    def add_item_to_results(self, name: str, cardinality: int, degree: int):
        item = RelationItem(name, cardinality, degree)
        self._results_model.add_relation(item)

    def clear_results(self):
        self._results_model.clear()


class RelationListQML(QWidget):

    itemClicked = Signal(int)
    itemClosed = Signal(int, str)

    def __init__(self, model, *, closable=False, parent=None):
        super().__init__(parent)
        self._parent = parent
        self._model = model
        vbox = QVBoxLayout(self)
        vbox.setContentsMargins(0, 0, 0, 0)
        self._view = QQuickWidget()
        self._view.rootContext().setContextProperty('relationModel', self._model)
        self._set_source()
        self._view.setResizeMode(QQuickWidget.SizeRootObjectToView)
        vbox.addWidget(self._view)

        self._root = self._view.rootObject()
        self._root.setClosable(closable)
        self._connect_signals()

    @property
    def model(self):
        return self._model

    def _connect_signals(self):
        self._root.itemClicked[int].connect(self.itemClicked.emit)
        self._root.itemClosed[int].connect(self._relation_closed)
        self._parent.parent._parent.pireal.themeChanged.connect(self._reload)

    @Slot(int)
    def _relation_closed(self, index):
        relation = self._model.relation_by_index(index)
        self.itemClosed.emit(index, relation.name)

    def _set_source(self):
        qml = os.path.join(settings.QML_PATH, "ListRelation.qml")
        self._view.setSource(QUrl.fromLocalFile(qml))

    def _reload(self):
        self._view.rootObject().deleteLater()
        self._view.setSource(QUrl())
        self._set_source()
        self._root = self._view.rootObject()
        self._connect_signals()

    def set_title(self, title):
        self._root.setTitle(title)

    # def sizeHint(self):
    #     return self._view.sizeHint()

    def resizeEvent(self, event):
        # print(self.sizeHint(), self.width())
        print(self._view.sizeHint(), self._view.width())
        super().resizeEvent(event)
