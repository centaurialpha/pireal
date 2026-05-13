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
    QPoint,
    QRect,
    QSize,
    Qt,
    pyqtSignal,
    pyqtSlot,
)
from PyQt6.QtGui import (
    QColor,
    QFont,
    QPainter,
    QPalette,
    QPolygon,
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
from pireal.helpers import svg_icon
from pireal.registry import Registry
from pireal.resources import icon


class _RunPill(QWidget):
    clicked = pyqtSignal()
    _PADDING_H = 12
    _PADDING_V = 4

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setToolTip("Run queries (F5)")
        fm = self.fontMetrics()
        icon_w = fm.height()
        gap = 6
        text_w = fm.horizontalAdvance("Run")
        w = self._PADDING_H * 2 + icon_w + gap + text_w
        h = fm.height() + self._PADDING_V * 2
        self.setFixedSize(w, h)
        self._success_color: QColor | None = None
        self._hovered = False
        self._refresh_color()
        get_theme_manager().themeChanged.connect(lambda _: self._refresh_color())

    def _refresh_color(self) -> None:
        self._success_color = get_theme_manager().current_scheme.editor.get(EditorColorRole.SUCCESS)
        self.update()

    def mousePressEvent(self, a0) -> None:
        if a0 is not None and a0.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(a0)

    def enterEvent(self, event) -> None:
        self._hovered = True
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, a0) -> None:
        self._hovered = False
        self.update()
        super().leaveEvent(a0)

    def paintEvent(self, a0) -> None:
        if self._success_color is None:
            return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        bg = QColor(self._success_color)
        bg.setAlpha(60 if self._hovered else 35)
        painter.setBrush(bg)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 1, 1)

        fm = self.fontMetrics()
        icon_h = fm.height()
        total_w = icon_h + 6 + fm.horizontalAdvance("Run")
        x = (self.width() - total_w) // 2
        y_center = self.height() // 2

        icon_rect = QRect(x, y_center - icon_h // 2, icon_h, icon_h)
        painter.setPen(self._success_color)

        # Triángulo play
        points = [
            icon_rect.topLeft() + QPoint(2, 1),
            icon_rect.bottomLeft() + QPoint(2, -1),
            QPoint(icon_rect.right() - 1, y_center),
        ]

        painter.setBrush(self._success_color)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawPolygon(QPolygon(points))

        font = painter.font()
        font.setWeight(QFont.Weight.Medium)
        painter.setFont(font)
        painter.setPen(self._success_color)
        text_x = x + icon_h + 6
        painter.drawText(
            QRect(text_x, 0, fm.horizontalAdvance("Run"), self.height()), Qt.AlignmentFlag.AlignVCenter, "Run"
        )

        painter.restore() if False else None


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
        layout.setSpacing(1)

        # Toolbar
        toolbar = QHBoxLayout()
        toolbar.setContentsMargins(0, 0, 0, 0)
        toolbar.addStretch()

        self._btn_split = self._make_tool_btn("Toggle split view")
        self._btn_split.setCheckable(True)
        self._btn_split.toggled.connect(self._on_split_toggled)
        toolbar.addWidget(self._btn_split)

        self._btn_sql = self._make_tool_btn("Show SQL")
        self._btn_sql.clicked.connect(self.sqlRequested.emit)
        toolbar.addWidget(self._btn_sql)

        self._btn_tree = self._make_tool_btn("Show execution tree")
        self._btn_tree.clicked.connect(self.treeRequested.emit)
        toolbar.addWidget(self._btn_tree)

        sep = QWidget()
        sep.setFixedSize(1, 14)
        sep.setAutoFillBackground(True)
        palette = sep.palette()
        color = self.palette().color(QPalette.ColorRole.Mid)
        color.setAlpha(80)
        palette.setColor(QPalette.ColorRole.Window, color)
        sep.setPalette(palette)
        toolbar.addSpacing(4)
        toolbar.addWidget(sep)
        toolbar.addSpacing(4)

        self._btn_run = self._make_tool_btn("Run queries (F5)")
        self._btn_run.clicked.connect(self._on_run_queries)
        toolbar.addWidget(self._btn_run)

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
        self._stacked.setCurrentIndex(index)

    def _make_tool_btn(self, tooltip: str, size: int = 16) -> QToolButton:
        btn = QToolButton()
        btn.setToolTip(tooltip)
        btn.setIconSize(QSize(size, size))
        btn.setFixedSize(28, 28)
        return btn

    def changeEvent(self, a0: QEvent | None) -> None:
        super().changeEvent(a0)
        if a0 is not None and a0.type() == QEvent.Type.PaletteChange:
            self._refresh_icons()

    def _refresh_icons(self) -> None:
        normal = self.palette().color(self.palette().ColorRole.ButtonText)
        success = get_theme_manager().current_scheme.editor.get(EditorColorRole.SUCCESS)

        self._btn_split.setIcon(svg_icon(icon("columns-2.svg"), normal))
        self._btn_sql.setIcon(svg_icon(icon("code.svg"), normal))
        self._btn_tree.setIcon(svg_icon(icon("network.svg"), normal))
        self._btn_run.setIcon(svg_icon(icon("play.svg"), success))

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

        success_bg = QColor(success)
        success_bg.setAlpha(45)
        success_hover = QColor(success)
        success_hover.setAlpha(70)

        run_style = f"""
            QToolButton {{
                border: none;
                border-radius: 4px;
                background-color: {success_bg.name(QColor.NameFormat.HexArgb)};
            }}
            QToolButton:hover {{
                background-color: {success_hover.name(QColor.NameFormat.HexArgb)};
            }}
        """

        for btn in (self._btn_split, self._btn_sql, self._btn_tree):
            btn.setStyleSheet(tool_btn_style)

        self._btn_run.setStyleSheet(run_style)

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
        return any(isinstance(self._stacked.widget(i), PlaceholderWidget) for i in range(self._stacked.count()))

    @pyqtSlot(int)
    def _on_result_list_clicked(self, index):
        self._stacked_results.setCurrentIndex(index)

    def add_table_to_workspace(self, relation: Relation, editable=True):
        self._remove_placeholder()
        view = create_view(relation, editable=editable)
        self._relation_widgets[relation.name] = view
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
            if widget is not None:
                self._stacked_results.removeWidget(widget)
                widget.deleteLater()
        self._btn_split.setChecked(False)

    def clear(self):
        # limpiar workspace
        while self._stacked.count() > 0:
            widget = self._stacked.widget(0)
            if widget is not None:
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
