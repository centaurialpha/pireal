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

import logging
from typing import Any

from PyQt6.QtCore import (
    QAbstractTableModel,
    QModelIndex,
    Qt,
    pyqtSlot as Slot,
)
from PyQt6.QtGui import (
    QBrush,
    QColor,
    QFont,
)
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QHeaderView,
    QInputDialog,
    QItemDelegate,
    QTableView,
)

from pireal import translations as tr
from pireal.core.db import DB
from pireal.gui.theme.manager import get_theme_manager
from pireal.registry import Registry

logger = logging.getLogger("gui.model_view_delegate")


# En model_view_delegate.py, agregar esta clase antes de View


class RelationModel(QAbstractTableModel):
    def __init__(self, relation_object):
        super().__init__()
        self.editable = True
        self.relation = relation_object
        self._dirty_cells: set[tuple[int, int]] = set()

        theme_manager = get_theme_manager()
        self._null_color = theme_manager.current_scheme.placeholder_text

        db = Registry.get("db", DB)

        db.hasModified.connect(self._on_db_modified)
        theme_manager.themeChanged.connect(self._on_theme_changed)

    @Slot(bool)
    def _on_db_modified(self, modified: bool) -> None:
        if not modified and self._dirty_cells:
            self._dirty_cells.clear()
            self.dataChanged.emit(
                self.index(0, 0),
                self.index(self.rowCount() - 1, self.columnCount() - 1),
            )

    def _on_theme_changed(self, scheme):
        self._null_color = scheme.placeholder_text

    def rowCount(self, parent: QModelIndex | None = None) -> int:
        """Devuelve la cardinalidad de la relación"""
        if parent is not None and parent.isValid():
            return 0
        return self.relation.cardinality()

    def columnCount(self, parent: QModelIndex | None = None):
        """Devuelve el grado de la relación"""
        if parent is not None and parent.isValid():
            return 0
        return self.relation.degree()

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None

        row, column = index.row(), index.column()
        data = self.relation.content
        is_dirty = (row, column) in self._dirty_cells

        if role in (Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole):
            return data[row][column]

        if is_dirty:
            if role == Qt.ItemDataRole.BackgroundRole:
                return QBrush(QColor(255, 185, 0, 50))
            if role == Qt.ItemDataRole.FontRole:
                font = QFont()
                font.setItalic(True)
                return font

        elif data[row][column] == "null":
            if role == Qt.ItemDataRole.ForegroundRole:
                return self._null_color
            if role == Qt.ItemDataRole.FontRole:
                font = QFont()
                font.setItalic(True)
                return font

        return None

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return self.relation.header[section]

    def setHeaderData(
        self, section: int, orientation: Qt.Orientation, value: Any, role: int = Qt.ItemDataRole.DisplayRole
    ) -> bool:
        if role == Qt.ItemDataRole.DisplayRole:
            old_value = self.relation.header[section]
            if value != old_value:
                self.relation.header[section] = value
                self.headerDataChanged.emit(orientation, section, section)
                return True
        return False

    def flags(self, index):
        flags = super().flags(index)
        if self.editable:
            flags |= Qt.ItemFlag.ItemIsEditable
        return flags

    def setData(self, index: QModelIndex, value: Any, role: int = Qt.ItemDataRole.DisplayRole):
        if index.isValid() and role == Qt.ItemDataRole.EditRole:
            current_value = self.data(index)
            if current_value != value:
                self.relation.update(index.row(), index.column(), value)
                self._dirty_cells.add((index.row(), index.column()))
                self.dataChanged.emit(index, index)
                if self.editable:
                    logger.debug(
                        "Editing %d:%d - Current: %s, New: %s",
                        index.row(),
                        index.column(),
                        current_value,
                        value,
                    )
                    db = Registry.get("db", DB)
                    db.modified = True
                return True
        return False


class View(QTableView):
    """Vista"""

    def __init__(self):
        super().__init__()
        self.setAlternatingRowColors(True)
        vheader = self.verticalHeader()
        if vheader is not None:
            vheader.hide()
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        # Scroll content per pixel
        self.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.setHorizontalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        header = self.horizontalHeader()
        if header is not None:
            header.setHighlightSections(False)

        self._apply_hover_style()

        theme_manager = get_theme_manager()
        theme_manager.themeChanged.connect(self._on_theme_changed)

    def _on_theme_changed(self, scheme):
        self._apply_hover_style()

    def _apply_hover_style(self):
        scheme = get_theme_manager().current_scheme

        alternate = scheme.alternate_base
        highlight = scheme.highlight

        hover = QColor(highlight)
        hover.setAlpha(30)
        selected = QColor(highlight)
        selected.setAlpha(45)

        header_bg = scheme.base
        header_border = QColor(scheme.text)
        header_border.setAlpha(20)

        self.setStyleSheet(f"""
            QTableView {{
                alternate-background-color: {alternate.name()};
                selection-background-color: {selected.name(QColor.NameFormat.HexArgb)};
                selection-color: {scheme.text.name()};
            }}
            QTableView::item:hover:!selected {{
                background-color: {hover.name(QColor.NameFormat.HexArgb)};
            }}
            QHeaderView::section {{
                background-color: {header_bg.name()};
                color: {scheme.text.name()};
                font-weight: bold;
                padding: 4px 10px;
                border: none;
                border-right: 1px solid {header_border.name(QColor.NameFormat.HexArgb)};
                border-bottom: 1px solid {header_border.name(QColor.NameFormat.HexArgb)};
            }}
            QHeaderView::section:last {{
                border-right: none;
            }}
            QHeaderView::section:hover {{
                background-color: {hover.name(QColor.NameFormat.HexArgb)};
            }}
        """)

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self.adjust_columns()

    def adjust_columns(self):
        """Resize all sections to content and user interactive"""
        header = self.horizontalHeader()
        if header is not None:
            for column in range(header.count()):
                header.setSectionResizeMode(column, QHeaderView.ResizeMode.ResizeToContents)
                width = header.sectionSize(column)
                header.setSectionResizeMode(column, QHeaderView.ResizeMode.Interactive)
                header.resizeSection(column, width)
            header.setMinimumHeight(36)


class Header(QHeaderView):
    def __init__(self, orientation=Qt.Orientation.Horizontal, parent=None):
        super().__init__(orientation, parent)
        self.editable = True
        self.setSectionsClickable(True)
        self.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        # Connections
        self.sectionDoubleClicked[int].connect(self._on_section_double_clicked)

    @Slot(int)
    def _on_section_double_clicked(self, index):
        if not self.editable:
            return
        name, ok = QInputDialog.getText(self, tr.TR_INPUT_DIALOG_HEADER_TITLE, tr.TR_INPUT_DIALOG_HEADER_BODY)
        if ok:
            model = self.model()
            if model is not None:
                model.setHeaderData(index, Qt.Orientation.Horizontal, name.strip())
                db = Registry.get("db", DB)
                db.modified = True


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
    if editable:
        header = Header()
        view.setHorizontalHeader(header)
    return view
