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

from PyQt6.QtCore import (
    QEvent,
    QSize,
    Qt,
    pyqtSignal,
    pyqtSlot,
)
from PyQt6.QtGui import (
    QColor,
    QPalette,
)
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
from pireal.core.relation import Relation
from pireal.gui.lateral_widget import LateralWidget
from pireal.gui.model_view_delegate import create_view
from pireal.gui.theme.manager import get_theme_manager
from pireal.gui.theme.schema import EditorColorRole
from pireal.gui.widgets import TogglePill
from pireal.helpers import svg_icon
from pireal.registry import Registry
from pireal.resources import icon


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
        self._pending_relations: list[tuple[Relation, bool]] = []

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(1)

        # Toolbar
        toolbar = QHBoxLayout()
        toolbar.setContentsMargins(0, 0, 0, 0)
        toolbar.addStretch()

        self._pill_relations = TogglePill("Relations", checked=True)
        self._pill_results = TogglePill("Results", checked=False)

        self._pill_relations.toggled.connect(self._on_relations_toggled)
        self._pill_results.toggled.connect(self._on_results_toggled)

        toolbar.addWidget(self._pill_relations)
        toolbar.addSpacing(1)
        toolbar.addWidget(self._pill_results)

        toolbar.addSpacing(6)
        sep = QWidget()
        sep.setFixedSize(1, 14)
        sep.setAutoFillBackground(True)
        palette = sep.palette()
        color = self.palette().color(QPalette.ColorRole.Mid)
        color.setAlpha(80)
        palette.setColor(QPalette.ColorRole.Window, color)
        sep.setPalette(palette)
        toolbar.addWidget(sep)
        toolbar.addSpacing(4)

        self._btn_sql = self._make_tool_btn(tr.TR_TOOLTIP_SHOW_SQL)
        self._btn_sql.clicked.connect(self.sqlRequested.emit)
        toolbar.addWidget(self._btn_sql)

        self._btn_tree = self._make_tool_btn(tr.TR_TOOLTIP_SHOW_TREE)
        self._btn_tree.clicked.connect(self.treeRequested.emit)
        toolbar.addWidget(self._btn_tree)

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

        self._refresh_icons()

    def show_relation_at(self, index: int) -> None:
        # self._stacked.setCurrentIndex(index)
        if index < 0 or index >= len(self._pending_relations):
            return
        relation, editable = self._pending_relations[index]
        if relation.name not in self._relation_widgets:
            self._remove_placeholder()
            view = create_view(relation, editable=editable)
            self._relation_widgets[relation.name] = view
            self._stacked.addWidget(view)
        self._stacked.setCurrentWidget(self._relation_widgets[relation.name])

    def _make_toggle_btn(self, label: str) -> QToolButton:
        btn = QToolButton()
        btn.setText(label)
        btn.setCheckable(True)
        btn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextOnly)
        btn.setFixedHeight(22)

        return btn

    def _make_tool_btn(self, tooltip: str, size: int = 16) -> QToolButton:
        btn = QToolButton()
        btn.setToolTip(tooltip)
        btn.setIconSize(QSize(size, size))
        btn.setFixedSize(28, 28)
        return btn

    @pyqtSlot(bool)
    def _on_relations_toggled(self, checked: bool) -> None:
        if not checked and not self._pill_results.is_checked:
            self._pill_relations.set_checked(True)
            return
        self._stacked.setVisible(checked)
        if checked and self._stacked_results.isVisible():
            self._splitter.setSizes([1, 1])

    @pyqtSlot(bool)
    def _on_results_toggled(self, checked: bool) -> None:
        if not checked and not self._pill_relations.is_checked:
            self._pill_results.set_checked(True)
            return
        self._stacked_results.setVisible(checked)
        if checked and self._stacked.isVisible():
            self._splitter.setSizes([1, 1])

    def changeEvent(self, a0: QEvent | None) -> None:
        super().changeEvent(a0)
        if a0 is not None and a0.type() == QEvent.Type.PaletteChange:
            self._refresh_icons()

    def _refresh_icons(self) -> None:
        normal = self.palette().color(self.palette().ColorRole.ButtonText)
        success = get_theme_manager().current_scheme.editor.get(EditorColorRole.SUCCESS)

        # self._btn_split.setIcon(svg_icon(icon("columns-2.svg"), normal))
        self._btn_sql.setIcon(svg_icon(icon("code.svg"), normal))
        self._btn_tree.setIcon(svg_icon(icon("network.svg"), normal))
        # self._btn_run.setIcon(svg_icon(icon("play.svg"), success))

        hover = self.palette().color(self.palette().ColorRole.Highlight)
        hover.setAlpha(35)
        hover_hex = hover.name(QColor.NameFormat.HexArgb)

        tool_btn_style = f"""
            QToolButton {{
                border: none;
                border-radius: 4px;
                background: transparent;
            }}
            QToolButton:hover {{
                background-color: {hover_hex};
            }}
            QToolButton:checked {{
                background-color: {hover_hex};
            }}
        """

        highlight = self.palette().color(QPalette.ColorRole.Highlight)
        highlight.setAlpha(35)
        highlight_hex = highlight.name(QColor.NameFormat.HexArgb)
        highlight_checked = self.palette().color(QPalette.ColorRole.Highlight)
        highlight_checked.setAlpha(70)
        highlight_checked_hex = highlight_checked.name(QColor.NameFormat.HexArgb)
        fg = self.palette().color(QPalette.ColorRole.ButtonText).name()
        fg_dim = self.palette().color(QPalette.ColorRole.PlaceholderText).name()

        pill_style = f"""
            QToolButton {{
                border: none;
                border-radius: 10px;
                padding: 0px 8px;
                color: {fg_dim};
                background: transparent;
                font-size: 11px;
            }}
            QToolButton:hover {{
                background-color: {highlight_hex};
                color: {fg};
            }}
            QToolButton:checked {{
                background-color: {highlight_checked_hex};
                color: {fg};
            }}
        """
        self._pill_relations.setStyleSheet(pill_style)
        self._pill_results.setStyleSheet(pill_style)
        success_bg = QColor(success)
        success_bg.setAlpha(45)
        success_hover = QColor(success)
        success_hover.setAlpha(70)

        # run_style = f"""
        #     QToolButton {{
        #         border: none;
        #         border-radius: 4px;
        #         background-color: {success_bg.name(QColor.NameFormat.HexArgb)};
        #     }}
        #     QToolButton:hover {{
        #         background-color: {success_hover.name(QColor.NameFormat.HexArgb)};
        #     }}
        # """

        for btn in (self._btn_sql, self._btn_tree):
            btn.setStyleSheet(tool_btn_style)

        # self._btn_run.setStyleSheet(run_style)

    @pyqtSlot()
    def _on_run_queries(self):
        from pireal.gui.controller import Controller

        Registry.get("controller", Controller).execute_queries()

    def _on_split_toggled(self, checked: bool):
        if checked:
            self._stacked_results.show()
            self._splitter.setSizes([1, 1])
        else:
            self._stacked_results.hide()

    def toggle_split(self):
        self._pill_results.set_checked(not self._pill_results.is_checked)

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
        return any(isinstance(self._stacked.widget(i), PlaceholderWidget) for i in range(self._stacked.count()))

    @pyqtSlot(int)
    def _on_result_list_clicked(self, index):
        self._stacked_results.setCurrentIndex(index)

    def add_table_to_workspace(self, relation: Relation, editable=True):
        self._pending_relations.append((relation, editable))

    def add_table_to_results(self, relation: Relation, editable=False):
        view = create_view(relation, editable=editable)
        self._stacked_results.addWidget(view)
        self._stacked_results.setCurrentWidget(view)

        # Auto-split
        if not self._stacked_results.isVisible():
            self._pill_results.set_checked(True)

    def clear_results(self):
        while self._stacked_results.count() > 0:
            widget = self._stacked_results.widget(0)
            if widget is not None:
                self._stacked_results.removeWidget(widget)
                widget.deleteLater()
        self._pill_results.set_checked(False)

    def clear(self):
        # limpiar workspace
        while self._stacked.count() > 0:
            widget = self._stacked.widget(0)
            if widget is not None:
                self._stacked.removeWidget(widget)
                widget.deleteLater()
        self._relation_widgets.clear()
        self._pending_relations.clear()
        self.clear_results()
        self._show_placeholder()

    def remove_relation(self, relation_name: str):
        widget = self._relation_widgets.pop(relation_name, None)
        if widget is None:
            return
        self._stacked.removeWidget(widget)
        widget.deleteLater()
        self._pending_relations = [(r, e) for r, e in self._pending_relations if r.name != relation_name]
        if self._stacked.count() == 0:
            self._show_placeholder()
