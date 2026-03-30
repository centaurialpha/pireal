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

from PyQt6.QtCore import QAbstractListModel, QModelIndex, QRect, Qt, pyqtSignal
from PyQt6.QtGui import QPainter, QPalette
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

    def rowCount(self, parent: QModelIndex | None = None) -> int:
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
        header_lbl = QLabel(header_text.upper())
        header_lbl.setObjectName("section_title")
        font = header_lbl.font()
        font.setPointSize(11)
        header_lbl.setFont(font)
        layout.addWidget(
            header_lbl,
            # alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter,
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

        model = cast(RelationModel, index.model())
        if model is None:
            return

        opt = QStyleOptionViewItem(option)
        self.initStyleOption(opt, index)
        opt.text = ""

        style = opt.widget.style()
        if style is not None:
            if opt.state & QStyle.StateFlag.State_Selected:
                highlight = opt.palette.color(QPalette.ColorRole.Highlight)
                highlight.setAlpha(150)
                opt.palette.setColor(QPalette.ColorRole.Highlight, highlight)

            style.drawControl(QStyle.ControlElement.CE_ItemViewItem, opt, painter, opt.widget)

        is_selected = bool(opt.state & QStyle.StateFlag.State_Selected)
        palette = opt.palette
        name_color = (
            palette.color(QPalette.ColorRole.HighlightedText) if is_selected else palette.color(QPalette.ColorRole.Text)
        )
        meta_color = palette.color(QPalette.ColorRole.PlaceholderText)

        rect = opt.rect.adjusted(12, 4, -8, -4)
        half = rect.height() // 2

        name = model.data(index, model.NameRole)
        cardinality = model.data(index, model.CardinalityRole)
        degree = model.data(index, model.DegreeRole)
        meta = f"{cardinality} tuples - {degree} attributes"

        painter.save()

        font = painter.font()
        font.setBold(True)
        painter.setFont(font)
        painter.setPen(name_color)
        painter.drawText(QRect(rect.left(), rect.top(), rect.width(), half), Qt.AlignmentFlag.AlignVCenter, name)

        font.setBold(False)
        font.setPointSize(font.pointSize() - 1)
        painter.setFont(font)
        painter.setPen(meta_color)
        painter.drawText(QRect(rect.left(), rect.top() + half, rect.width(), half), Qt.AlignmentFlag.AlignVCenter, meta)
        painter.restore()

    def sizeHint(self, option, index):
        size = super().sizeHint(option, index)
        size.setHeight(44)
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
        viewport = self._relations_list.view.viewport()
        if viewport is not None and menu.exec(viewport.mapToGlobal(pos)) and delete_action:
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
