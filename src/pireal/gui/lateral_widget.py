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
from PyQt6.QtGui import QColor, QFont, QFontMetrics, QPainter, QPalette
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QListView,
    QMenu,
    QSizePolicy,
    QSplitter,
    QStyle,
    QStyledItemDelegate,
    QStyleOptionViewItem,
    QVBoxLayout,
    QWidget,
)

from pireal import translations as tr

RelationItem = namedtuple("RelationItem", "name cardinality degree")


class _EmptyListView(QListView):
    """QListView que muestra un mensaje placeholder cuando el modelo está vacío."""

    def __init__(self, empty_text: str, parent=None):
        super().__init__(parent)
        self._empty_text = empty_text

    def paintEvent(self, e):
        super().paintEvent(e)
        model = self.model()
        if model is None or model.rowCount() > 0:
            return
        viewport = self.viewport()
        if viewport is None:
            return
        painter = QPainter(viewport)
        painter.save()
        painter.setPen(self.palette().color(QPalette.ColorRole.PlaceholderText))
        painter.drawText(
            viewport.rect(),
            Qt.AlignmentFlag.AlignCenter,
            self._empty_text,
        )
        painter.restore()


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


class _CountBadge(QWidget):
    _PADDING_H = 6
    _PADDING_V = 2

    def __init__(self, parent=None):
        super().__init__(parent)
        self._count = 0
        self.hide()
        fm = self.fontMetrics()
        self.setFixedHeight(fm.height() + self._PADDING_V * 2)

    def set_count(self, count: int) -> None:
        self._count = count
        if count > 0:
            fm = self.fontMetrics()
            w = fm.horizontalAdvance(str(count)) + self._PADDING_H * 2
            self.setFixedWidth(w)
            self.show()
        else:
            self.hide()
        self.update()

    def paintEvent(self, a0) -> None:
        if self._count == 0:
            return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        color = self.palette().color(QPalette.ColorRole.PlaceholderText)
        bg = QColor(color)
        bg.setAlpha(35)
        painter.setBrush(bg)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 3, 3)

        painter.setPen(color)
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, str(self._count))


class _SectionHeader(QWidget):
    def __init__(self, text: str, parent=None):
        super().__init__(parent)
        self._count = 0
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 6, 8, 4)

        label = QLabel(text.upper())
        fm = label.fontMetrics()
        font = label.font()
        font.setPointSize(max(7, fm.height() // 2))
        font.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, 1.5)
        font.setBold(True)
        label.setFont(font)
        label.setStyleSheet(f"color: {label.palette().color(QPalette.ColorRole.PlaceholderText).name()};")
        layout.addWidget(label)
        layout.addStretch()

        self._badge = _CountBadge()
        layout.addWidget(self._badge)

    def set_model(self, model: "RelationModel") -> None:
        model.rowsInserted.connect(lambda *_: self._badge.set_count(model.rowCount()))
        model.rowsRemoved.connect(lambda *_: self._badge.set_count(model.rowCount()))
        model.modelReset.connect(lambda: self._badge.set_count(0))

    def paintEvent(self, a0) -> None:
        super().paintEvent(a0)
        painter = QPainter(self)
        color = self.palette().color(QPalette.ColorRole.Mid)
        color.setAlpha(80)
        painter.setPen(color)
        painter.drawLine(0, self.height() - 1, self.width(), self.height() - 1)


class __SectionHeader(QWidget):
    def __init__(self, text: str, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 6, 8, 4)

        label = QLabel(text.upper())
        fm = label.fontMetrics()
        font = label.font()
        font.setPointSize(max(7, fm.height() // 2))
        font.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, 1.5)
        font.setBold(True)
        label.setFont(font)

        palette = label.palette()
        label.setStyleSheet(f"color: {palette.color(QPalette.ColorRole.PlaceholderText).name()};")
        layout.addWidget(label)
        layout.addStretch()

    def set_model(self, model: "RelationModel") -> None:
        model.rowsInserted.connect(lambda *_: self._update_count(model))
        model.rowsRemoved.connect(lambda *_: self._update_count(model))
        model.modelReset.connect(lambda: self._update_count(model))
        self._update_count(model)

    def _update_count(self, model: "RelationModel") -> None:
        self._count = model.rowCount()
        self.update()

    def paintEvent(self, a0) -> None:
        super().paintEvent(a0)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # línea separadora abajo
        color = self.palette().color(QPalette.ColorRole.Mid)
        color.setAlpha(80)
        painter.setPen(color)
        painter.drawLine(0, self.height() - 1, self.width(), self.height() - 1)

        if self._count == 0:
            return

        # badge
        text = str(self._count)
        fm = self.fontMetrics()
        padding_h, padding_v = 6, 2
        badge_w = fm.horizontalAdvance(text) + padding_h * 2
        badge_h = fm.height() + padding_v * 2
        x = self.width() - badge_w - 8
        y = (self.height() - badge_h) // 2
        badge_rect = QRect(x, y, badge_w, badge_h)

        accent = self.palette().color(QPalette.ColorRole.PlaceholderText)
        bg = QColor(accent)
        bg.setAlpha(35)
        painter.setBrush(bg)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(badge_rect, 3, 3)

        painter.setPen(accent)
        painter.setFont(self.font())
        painter.drawText(badge_rect, Qt.AlignmentFlag.AlignCenter, text)


class RelationListView(QFrame):
    def __init__(self, header_text="", empty_text="", parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(3, 3, 3, 3)
        layout.setSpacing(0)
        self._header = _SectionHeader(header_text)
        layout.addWidget(self._header)
        self.view = _EmptyListView(empty_text)
        layout.addWidget(self.view)

    def set_model(self, model: "RelationModel") -> None:
        self.view.setModel(model)
        self._header.set_model(model)


class RelationDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        if painter is None:
            return

        model = cast(RelationModel, index.model())
        if model is None:
            return

        opt = QStyleOptionViewItem(option)
        self.initStyleOption(opt, index)
        opt.text = ""

        is_selected = bool(opt.state & QStyle.StateFlag.State_Selected)
        is_hover = bool(opt.state & QStyle.StateFlag.State_MouseOver)
        palette = opt.palette
        rect = opt.rect.adjusted(4, 3, -4, -3)

        painter.save()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        if is_selected:
            bg = palette.color(QPalette.ColorRole.Highlight)
            bg.setAlpha(25)
            painter.fillRect(opt.rect, bg)
        elif is_hover:
            bg = palette.color(QPalette.ColorRole.Highlight)
            bg.setAlpha(10)
            painter.fillRect(opt.rect, bg)

        if is_selected:
            name_color = palette.color(QPalette.ColorRole.Highlight)
            meta_color = palette.color(QPalette.ColorRole.Highlight)
            meta_color.setAlpha(180)
        else:
            name_color = palette.color(QPalette.ColorRole.Text)
            meta_color = palette.color(QPalette.ColorRole.PlaceholderText)

        text_rect = rect.adjusted(10, 4, -8, -4)

        name_font = QFont(painter.font())
        name_font.setBold(True)
        name_height = QFontMetrics(name_font).height()

        meta_font = QFont(painter.font())
        meta_font.setPointSize(meta_font.pointSize() - 1)
        meta_height = QFontMetrics(meta_font).height()

        top = text_rect.top() + (text_rect.height() - name_height - meta_height) // 2

        name = model.data(index, model.NameRole)
        cardinality = model.data(index, model.CardinalityRole)
        degree = model.data(index, model.DegreeRole)

        painter.setFont(name_font)
        painter.setPen(name_color)
        painter.drawText(
            QRect(text_rect.left(), top, text_rect.width(), name_height), Qt.AlignmentFlag.AlignVCenter, name
        )

        painter.setFont(meta_font)
        painter.setPen(meta_color)
        painter.drawText(
            QRect(text_rect.left(), top + name_height, text_rect.width(), meta_height),
            Qt.AlignmentFlag.AlignVCenter,
            f"{cardinality} tuples · {degree} attrs",
        )

        painter.restore()

    def sizeHint(self, option, index):
        name_font = QFont(option.font)
        name_font.setBold(True)
        name_height = QFontMetrics(name_font).height()
        meta_font = QFont(option.font)
        meta_font.setPointSize(meta_font.pointSize() - 1)
        meta_height = QFontMetrics(meta_font).height()
        size = super().sizeHint(option, index)
        size.setHeight(name_height + meta_height + 26)
        return size

    def _paint(
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
        if is_selected:
            meta_color = palette.color(QPalette.ColorRole.HighlightedText)
            meta_color.setAlpha(180)
        else:
            meta_color = palette.color(QPalette.ColorRole.PlaceholderText)

        rect = opt.rect.adjusted(12, 4, -8, -4)
        name_font = QFont(painter.font())
        name_font.setBold(True)
        name_height = QFontMetrics(name_font).height()

        meta_font = QFont(painter.font())
        meta_font.setPointSize(meta_font.pointSize() - 1)
        meta_height = QFontMetrics(meta_font).height()

        top = rect.top() + (rect.height() - name_height - meta_height) // 2

        painter.save()

        name = model.data(index, model.NameRole)
        cardinality = model.data(index, model.CardinalityRole)
        degree = model.data(index, model.DegreeRole)
        meta = f"{cardinality} tuples - {degree} attributes"

        painter.setFont(name_font)
        painter.setPen(name_color)
        painter.drawText(QRect(rect.left(), top, rect.width(), name_height), Qt.AlignmentFlag.AlignVCenter, name)

        painter.setFont(meta_font)
        painter.setPen(meta_color)
        painter.drawText(
            QRect(rect.left(), top + name_height, rect.width(), meta_height), Qt.AlignmentFlag.AlignVCenter, meta
        )
        painter.restore()

    def _sizeHint(self, option, index):
        size = super().sizeHint(option, index)
        name_font = QFont(option.font)
        name_font.setBold(True)
        name_height = QFontMetrics(name_font).height()
        meta_font = QFont(option.font)
        meta_font.setPointSize(meta_font.pointSize() - 1)
        meta_height = QFontMetrics(meta_font).height()
        size.setHeight(name_height + meta_height + 14)
        return size


class LateralWidget(QSplitter):
    relationClicked = pyqtSignal(int)
    resultClicked = pyqtSignal(int)
    deleteRelationRequested = pyqtSignal(int)

    def __init__(self):
        super().__init__(orientation=Qt.Orientation.Vertical)
        self._relations_list = RelationListView(tr.TR_RELATIONS, tr.TR_NO_RELATIONS)
        self._relations_model = RelationModel()
        self._relations_list.set_model(self._relations_model)
        self._relations_list.view.setItemDelegate(RelationDelegate())
        self.addWidget(self._relations_list)

        self._results_list = RelationListView(tr.TR_RESULTS, tr.TR_NO_RESULTS)
        self._results_model = RelationModel()
        self._results_list.set_model(self._results_model)
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
        viewport = self._relations_list.view.viewport()
        if viewport is None:
            return
        menu = QMenu(self)
        delete_action = menu.addAction(tr.TR_MENU_SCHEME_REMOVE_RELATION)
        action = menu.exec(viewport.mapToGlobal(pos))
        if action == delete_action:
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

    def relation_name_by_index(self, index: int) -> str:
        return self._relations_model.relation_by_index(index).name

    def select_relation(self, index: int) -> None:
        self._select_in_view(self._relations_list.view, index)

    def select_result(self, index: int) -> None:
        self._select_in_view(self._results_list.view, index)

    def _select_in_view(self, view, index: int) -> None:
        model = view.model()
        if model is None or model.rowCount() == 0:
            return
        idx = model.index(index, 0)
        view.setCurrentIndex(idx)
