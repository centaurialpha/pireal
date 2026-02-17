# Copyright 2015-2025 - Gabriel Acosta <acostadariogabriel@gmail.com>
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
from typing import cast

from PyQt6.QtCore import QAbstractItemModel, QAbstractListModel, QModelIndex, QRect, Qt, pyqtSignal
from PyQt6.QtGui import QPainter
from PyQt6.QtWidgets import (
    QFrame,
    QLabel,
    QListView,
    QMenu,
    QSizePolicy,
    QSplitter,
    QStyle,
    QStyledItemDelegate,
    QStyleOptionViewItem,
    QVBoxLayout,
)

from pireal import translations as tr

RelationItem = namedtuple("RelationItem", "name cardinality degree")


# FIXME: mejores nombres
class RelationItemType(enum.Enum):
    Normal = "normal"
    Result = "result"


class RelationModel(QAbstractListModel):
    NameRole = Qt.ItemDataRole.UserRole + 1
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

    def rowCount(self, index: QModelIndex, parent) -> int:
        _ = parent
        return len(self._relations)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
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
            self.NameRole: b"name",
            self.CardinalityRole: b"cardinality",
            self.DegreeRole: b"degree",
        }


class RelationListView(QFrame):
    def __init__(self, header_text="", parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(3, 3, 3, 3)
        layout.setSpacing(0)
        header_lbl = QLabel(header_text)
        font = header_lbl.font()
        font.setPointSize(12)
        header_lbl.setFont(font)
        layout.addWidget(
            header_lbl,
            alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter,
        )
        self.view = QListView()
        layout.addWidget(self.view)


class RelationDelegate(QStyledItemDelegate):
    def paint(
        self,
        painter: QPainter | None,
        option: "QStyleOptionViewItem",
        index: QModelIndex,
    ) -> None:
        if painter is None:
            return

        model: QAbstractItemModel | None = index.model()
        if model is None:
            return

        model = cast(RelationModel, model)

        opt = QStyleOptionViewItem(option)
        self.initStyleOption(opt, index)

        relation_name = model.data(index, model.NameRole)
        cardinality = model.data(index, model.CardinalityRole)
        degree = model.data(index, model.DegreeRole)

        style = opt.widget.style()
        opt.text = ""
        if style is not None:
            style.drawControl(QStyle.ControlElement.CE_ItemViewItem, opt, painter, opt.widget)

        rect = opt.rect

        rect = rect.adjusted(5, 3, 5, -3)
        painter.save()

        font = painter.font()
        font.setBold(True)
        font.setPointSize(12)
        painter.setFont(font)
        painter.drawText(
            QRect(rect.left(), rect.top(), rect.width(), round(rect.height() / 3)),
            opt.displayAlignment,
            relation_name,
        )

        painter.restore()

        painter.drawText(
            QRect(rect.left(), rect.top(), rect.width(), rect.height()),
            opt.displayAlignment,
            "cardinality: " + str(cardinality),
        )

        painter.drawText(
            QRect(
                rect.left(),
                round(rect.top() + rect.height() / 2),
                rect.width(),
                round(rect.height() / 1.5),
            ),
            opt.displayAlignment,
            "degree: " + str(degree),
        )

    def sizeHint(self, option, index):
        size = super().sizeHint(option, index)
        size.setHeight(round(size.height() * 4.5))
        return size


class LateralWidget(QSplitter):
    relationClicked = pyqtSignal(int)
    resultClicked = pyqtSignal(int)
    deleteRelationRequested = pyqtSignal(int)

    def __init__(self):
        super().__init__(orientation=Qt.Orientation.Vertical)
        self._relations_list = RelationListView(tr.TR_RELATIONS)
        self._relations_model = RelationModel()
        self._relations_list.view.setModel(self._relations_model)
        self._relations_list.view.setItemDelegate(RelationDelegate())
        self.addWidget(self._relations_list)

        self._results_list = RelationListView(tr.TR_RESULTS)
        self._results_model = RelationModel()
        self._results_list.view.setModel(self._results_model)
        self._results_list.view.setItemDelegate(RelationDelegate())
        self.addWidget(self._results_list)

        self._models = {
            RelationItemType.Normal: self._relations_model,
            RelationItemType.Result: self._results_model,
        }

        self._relations_list.view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self._relations_list.view.customContextMenuRequested.connect(self._on_relations_context_menu)
        self._relations_list.view.clicked.connect(lambda index: self.relationClicked.emit(index.row()))
        self._results_list.view.clicked.connect(lambda index: self.resultClicked.emit(index.row()))

    def _on_relations_context_menu(self, pos):
        index = self._relations_list.view.indexAt(pos)
        if not index.isValid():
            return
        menu = QMenu(self)
        delete_action = menu.addAction(tr.TR_MENU_SCHEME_REMOVE_RELATION)
        if menu.exec(self._relations_list.view.viewport().mapToGlobal(pos)) and delete_action:
            self.deleteRelationRequested.emit(index.row())

    def remove_relation(self, index: int):
        self._relations_model.remove_relation(index)

    def add_item(self, relation, relation_type: RelationItemType) -> None:
        item = RelationItem(relation.name, relation.cardinality(), relation.degree())
        self._models[relation_type].add_relation(item)

    def clear(self):
        self._relations_model.clear()

    def clear_results(self):
        self._results_model.clear()
