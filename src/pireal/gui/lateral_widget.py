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

import enum
from collections import namedtuple

from PyQt5.QtWidgets import QListView
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QSplitter
from PyQt5.QtWidgets import QStyledItemDelegate
from PyQt5.QtWidgets import QStyleOptionViewItem
from PyQt5.QtWidgets import QStyle
from PyQt5.QtWidgets import QSizePolicy

from PyQt5.QtCore import (
    Qt,
    QRect,
    QModelIndex
)
from PyQt5.QtCore import QAbstractListModel
from PyQt5.QtCore import pyqtSignal as Signal

from pireal.gui.main_window import Pireal
from pireal import translations as tr


RelationItem = namedtuple('RelationItem', 'name cardinality degree')


class RelationItemType(enum.Enum):
    Normal = 'normal'
    Result = 'result'


class RelationModel(QAbstractListModel):

    NameRole = Qt.UserRole + 1
    CardinalityRole = NameRole + 1
    DegreeRole = CardinalityRole + 1

    def __init__(self, parent=None):
        super().__init__(parent)
        self._relations = []

    def add_relation(self, relation: RelationItem):
        relations_len = len(self._relations)

        self.beginInsertRows(QModelIndex(), relations_len, relations_len)
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

    def rowCount(self, index):
        return len(self._relations)

    def data(self, index, role=Qt.DisplayRole):
        try:
            relation_item = self._relations[index.row()]
        except IndexError:
            return None

        if role == self.NameRole:
            return relation_item.name
        elif role == self.CardinalityRole:
            return relation_item.cardinality
        elif role == self.DegreeRole:
            return relation_item.degree

        return None

    def roles(self):
        return {
            self.NameRole: b'name',
            self.CardinalityRole: b'cardinality',
            self.DegreeRole: b'degree'
        }


class RelationDelegate(QStyledItemDelegate):

    def paint(self, painter, option, index):
        opt = QStyleOptionViewItem(option)
        self.initStyleOption(opt, index)

        model = index.model()
        relation_name = model.data(index, model.NameRole)
        cardinality = model.data(index, model.CardinalityRole)
        degree = model.data(index, model.DegreeRole)

        opt.text = ''
        opt.widget.style().drawControl(QStyle.CE_ItemViewItem, opt, painter, opt.widget)

        rect = opt.rect

        rect = rect.adjusted(5, 3, 5, -3)
        painter.save()

        font = painter.font()
        font.setBold(True)
        font.setPointSize(12)
        painter.setFont(font)
        painter.drawText(
            QRect(rect.left(), rect.top(), rect.width(), rect.height() / 3),
            opt.displayAlignment, relation_name
        )

        painter.restore()

        painter.drawText(
            QRect(rect.left(), rect.top(), rect.width(), rect.height()),
            opt.displayAlignment, 'cardinality: ' + str(cardinality)
        )

        painter.drawText(
            QRect(rect.left(), rect.top() + rect.height() / 2, rect.width(), rect.height() / 1.5),
            opt.displayAlignment, 'degree: ' + str(degree)
        )

    def sizeHint(self, option, index):
        size = super().sizeHint(option, index)
        size.setHeight(size.height() * 4.5)
        return size


class RelationListView(QFrame):

    def __init__(self, header_text='', parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(3, 3, 3, 3)
        header_lbl = QLabel(header_text)
        font = header_lbl.font()
        font.setPointSize(12)
        header_lbl.setFont(font)
        layout.addWidget(header_lbl, alignment=Qt.AlignHCenter | Qt.AlignVCenter)
        self.view = QListView()
        layout.addWidget(self.view)


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
        self._relations_list = RelationListView(tr.TR_RELATIONS)
        self._relations_model = RelationModel()
        self._relations_list.view.setModel(self._relations_model)
        self._relations_list.view.setItemDelegate(RelationDelegate())
        self.addWidget(self._relations_list)
        # Lista de relaciones del resultado de consultas
        self._results_list = RelationListView(tr.TR_RESULTS)
        self._results_model = RelationModel()
        self._results_list.view.setModel(self._results_model)
        self._results_list.view.setItemDelegate(RelationDelegate())
        self.addWidget(self._results_list)

        self._models = {
            RelationItemType.Normal: self._relations_model,
            RelationItemType.Result: self._results_model
        }

        self._relations_list.view.clicked.connect(lambda i: self.relationClicked.emit(i.row()))
        self._results_list.view.clicked.connect(lambda i: self.resultClicked.emit(i.row()))

        Pireal.load_service("lateral_widget", self)

    def current_index(self):
        index = self._relations_list.view.currentIndex()
        return index.row()

    def current_text(self):
        index = self.current_index()
        relation = self._relations_model.relation_by_index(index)
        return relation.name

    def remove_relation(self, index):
        self._relations_model.remove_relation(index)

    def add_item(self, relation, rtype: RelationItemType.Normal):
        """Add relation to list of relations or results depending on rtype"""
        item = RelationItem(
            relation.name,
            relation.cardinality(),
            relation.degree())

        self._models[rtype].add_relation(item)

    def clear(self):
        """Clear list of relations"""
        self._relations_model.clear()

    def clear_results(self):
        """Clear list of results"""
        self._results_model.clear()
