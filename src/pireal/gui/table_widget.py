# Copyright 2015-2026 - Gabriel Acosta <acostadariogabriel@gmail.com>
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

from PyQt6.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt6.QtGui import QPalette
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSplitter,
    QStackedWidget,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from pireal import translations as tr
from pireal.core.db import DB
from pireal.core.relation import Relation
from pireal.gui.lateral_widget import LateralWidget
from pireal.gui.model_view_delegate import create_view
from pireal.helpers import Font
from pireal.registry import Registry


class PlaceholderWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(12)

        label = QLabel(tr.TR_PLACEHOLDER_NO_RELATIONS)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = label.font()
        font.setPointSize(font.pointSize() + 2)
        label.setFont(font)

        hint = QLabel(tr.TR_PLACEHOLDER_HINT)
        hint.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hint.setWordWrap(True)

        btn_new = QPushButton(tr.TR_PLACEHOLDER_BTN_NEW)
        btn_from_code = QPushButton(tr.TR_PLACEHOLDER_BTN_FROM_CODE)
        btn_from_code.setFlat(True)
        palette = btn_from_code.palette()
        link_color = palette.color(QPalette.ColorRole.Link).name()
        btn_from_code.setStyleSheet(f"color: {link_color};")

        btn_layout = QHBoxLayout()
        btn_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        btn_layout.setSpacing(8)
        btn_layout.addWidget(btn_new)
        btn_layout.addWidget(btn_from_code)

        layout.addWidget(label)
        layout.addWidget(hint)
        layout.addSpacing(8)
        layout.addLayout(btn_layout)

        btn_new.clicked.connect(self._on_new_relation)
        btn_from_code.clicked.connect(self._on_from_code)

    @pyqtSlot()
    def _on_new_relation(self):
        from pireal.gui.controller import Controller

        controller = Registry.get("controller", Controller)
        controller.create_relation()

    @pyqtSlot()
    def _on_from_code(self):
        from pireal.gui.controller import Controller

        controller = Registry.get("controller", Controller)
        controller.add_relations_from_text()


class TableWidget(QWidget):
    sqlRequested = pyqtSignal()
    treeRequested = pyqtSignal()

    def __init__(self):
        super().__init__()

        self._relation_widgets: dict[str, QWidget] = {}

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Toolbar
        toolbar = QHBoxLayout()
        toolbar.setContentsMargins(0, 0, 4, 0)
        toolbar.addStretch()
        fa = Font.instance()
        self._btn_split = QToolButton()
        self._btn_split.setAutoRaise(True)
        self._btn_split.setCheckable(True)
        self._btn_split.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        fa.apply_to(self._btn_split, size=12)
        self._btn_split.setText("\uf0db")
        self._btn_split.setToolTip("Toggle split view")
        self._btn_split.toggled.connect(self._on_split_toggled)
        toolbar.addWidget(self._btn_split)

        btn_sql = QToolButton()
        btn_sql.setAutoRaise(True)
        btn_sql.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        fa.apply_to(btn_sql, size=12)
        btn_sql.setText("\uf121")
        btn_sql.setToolTip("Show SQL")
        btn_sql.clicked.connect(self.sqlRequested.emit)
        toolbar.addWidget(btn_sql)

        btn_tree = QToolButton()
        btn_tree.setAutoRaise(True)
        btn_tree.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        fa.apply_to(btn_tree, size=12)
        btn_tree.setText("\uf0e8")
        btn_tree.setToolTip("Show Execution Tree")
        btn_tree.clicked.connect(self.treeRequested.emit)
        toolbar.addWidget(btn_tree)

        layout.addLayout(toolbar)

        self._splitter = QSplitter(Qt.Orientation.Horizontal)
        self._stacked = QStackedWidget()
        self._stacked_results = QStackedWidget()
        self._splitter.addWidget(self._stacked)
        self._splitter.addWidget(self._stacked_results)
        self._stacked_results.hide()
        layout.addWidget(self._splitter)

        self._show_placeholder()

        lateral_widget = Registry.get("lateral-widget", LateralWidget)
        lateral_widget.resultClicked.connect(self._on_result_list_clicked)

    def _on_split_toggled(self, checked: bool):
        if checked:
            self._stacked_results.show()
            self._splitter.setSizes([1, 1])
        else:
            self._stacked_results.hide()

    def toggle_split(self):
        if self._stacked_results.isVisible():
            self._stacked_results.hide()
        else:
            self._stacked_results.show()
            self._splitter.setSizes([1, 1])

    def _show_placeholder(self):
        if not self._has_placeholder():
            placeholder = PlaceholderWidget()
            self._stacked.addWidget(placeholder)
            self._stacked.setCurrentWidget(placeholder)

    def _remove_placeholder(self):
        for i in range(self._stacked.count()):
            widget = self._stacked.widget(i)
            if isinstance(widget, PlaceholderWidget):
                self._stacked.removeWidget(widget)
                widget.deleteLater()
                break

    def _has_placeholder(self) -> bool:
        return any(
            isinstance(self._stacked.widget(i), PlaceholderWidget)
            for i in range(self._stacked.count())
        )

    @pyqtSlot(int)
    def _on_result_list_clicked(self, index):
        self._stacked_results.setCurrentIndex(index)

    def add_table_to_workspace(self, relation: Relation, editable=True):
        db = Registry.get("db", DB)
        self._remove_placeholder()
        view = create_view(relation, editable=editable)
        db.add(relation)
        self._relation_widgets[relation.name] = view  # ← registrar
        self._stacked.addWidget(view)
        self._stacked.setCurrentWidget(view)

    def add_table_to_results(self, relation: Relation, editable=False):
        view = create_view(relation, editable=editable)
        self._stacked_results.addWidget(view)
        self._stacked_results.setCurrentWidget(view)

        # Auto-split
        if not self._stacked_results.isVisible():
            self._btn_split.setChecked(True)

    def clear_results(self):
        while self._stacked_results.count() > 0:
            widget = self._stacked_results.widget(0)
            self._stacked_results.removeWidget(widget)
            widget.deleteLater()

    def clear(self):
        # limpiar workspace
        while self._stacked.count() > 0:
            widget = self._stacked.widget(0)
            self._stacked.removeWidget(widget)
            widget.deleteLater()
        self.clear_results()
        self._show_placeholder()

    def remove_relation(self, relation_name: str):
        widget = self._relation_widgets.pop(relation_name, None)
        if widget is None:
            return
        self._stacked.removeWidget(widget)
        widget.deleteLater()
        if self._stacked.count() == 0:
            self._show_placeholder()
