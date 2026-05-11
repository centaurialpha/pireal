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

from dataclasses import dataclass

from PyQt6.QtCore import Qt
from PyQt6.QtGui import (
    QBrush,
    QColor,
    QFont,
    QPainter,
    QPalette,
    QPen,
)
from PyQt6.QtWidgets import (
    QComboBox,
    QDialog,
    QGraphicsLineItem,
    QGraphicsRectItem,
    QGraphicsScene,
    QGraphicsTextItem,
    QGraphicsView,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from pireal import translations as tr
from pireal.gui.model_view_delegate import (
    Delegate,
    RelationModel,
    View,
)
from pireal.gui.theme.manager import get_theme_manager
from pireal.gui.theme.schema import (
    EditorColorRole,
    blend_colors,
)
from pireal.gui.widgets import Pill
from pireal.interpreter.query_plan import (
    NodeState,
    QueryPlanEvaluator,
    QueryPlanNode,
)


class StatusPill(Pill):
    def __init__(self, parent=None):
        super().__init__(color_fn=self._current_color, parent=parent)
        self._state = "ready"  # "ready" | "step" | "completed"

    def _current_color(self) -> QColor:
        palette = self.palette()
        match self._state:
            case "step":
                return palette.color(QPalette.ColorRole.Highlight)
            case "completed":
                return get_theme_manager().current_scheme.editor.get(EditorColorRole.SUCCESS)
            case "error":
                return get_theme_manager().current_scheme.editor.get(EditorColorRole.ERROR)
            case _:
                return palette.color(QPalette.ColorRole.PlaceholderText)

    def set_ready(self) -> None:
        self._state = "ready"
        self._set_text(tr.TR_QUERY_PLAN_STATUS_READY)

    def set_step(self, current: int, total: int) -> None:
        self._state = "step"
        self._set_text(tr.TR_QUERY_PLAN_STEP_COUNT.format(current=current, total=total))

    def set_completed(self) -> None:
        self._state = "completed"
        self._set_text(tr.TR_QUERY_PLAN_COMPLETED)

    def set_error(self, msg: str) -> None:
        self._state = "error"
        self._set_text(f"Error: {msg}")

    def _set_text(self, text: str) -> None:
        self._text = text
        fm = self.fontMetrics()
        w = fm.horizontalAdvance(text) + self._PADDING_H * 2
        self.setFixedWidth(w)
        self.update()

    def paintEvent(self, a0) -> None:
        _ = a0
        if not self._text:
            return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        palette = self.palette()
        match self._state:
            case "step":
                color = palette.color(QPalette.ColorRole.Highlight)
            case "completed":
                color = get_theme_manager().current_scheme.editor.get(EditorColorRole.SUCCESS)
            case "error":
                color = get_theme_manager().current_scheme.editor.get(EditorColorRole.ERROR)
            case _:
                color = palette.color(QPalette.ColorRole.PlaceholderText)

        bg = QColor(color)
        bg.setAlpha(35)
        painter.setBrush(bg)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 3, 3)

        painter.setPen(color)
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, self._text)


class QueryPlanNodeItem(QGraphicsRectItem):
    """Graphical representation of a node in the plan"""

    NODE_WIDTH = 120
    NODE_HEIGHT = 60

    def __init__(self, plan_node: QueryPlanNode, x: float, y: float, on_click_callback):
        super().__init__(0, 0, self.NODE_WIDTH, self.NODE_HEIGHT)
        self.plan_node = plan_node
        self.on_click = on_click_callback
        self.setPos(x, y)

        self.setAcceptHoverEvents(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self.operator_text = QGraphicsTextItem(self)
        self.operator_text.setPlainText(plan_node.operator.value)
        font = QFont("Monospace", 18, QFont.Weight.Bold)
        self.operator_text.setFont(font)
        self.operator_text.setPos(10, 5)

        self.params_text = None
        if plan_node.params:
            self.params_text = QGraphicsTextItem(self)
            self.params_text.setPlainText(plan_node.params)
            font = QFont("Monospace", 9)
            self.params_text.setFont(font)
            # Truncar si es muy largo
            text = plan_node.params
            if len(text) > 15:
                text = text[:12] + "..."
            self.params_text.setPlainText(text)
            self.params_text.setPos(10, 35)

        self._update_style()

    def _update_style(self):
        theme = get_theme_manager().current_scheme
        is_dark = theme.window.lightness() < 128

        state_base_colors = {
            NodeState.PENDING: QColor(150, 150, 150),
            NodeState.EXECUTING: QColor(100, 150, 255),
            NodeState.EXECUTED: QColor(100, 200, 100),
            NodeState.ERROR: QColor(255, 100, 100),
        }

        base_color = state_base_colors[self.plan_node.state]

        bg_theme = theme.base

        if is_dark:
            bg = blend_colors(base_color, bg_theme, 0.3)  # 30% color, 70% fondo
            border = base_color
        else:
            bg = blend_colors(base_color, bg_theme, 0.2)  # 20% color, 80% fondo
            border = base_color.darker(130)

        self.setBrush(QBrush(bg))
        self.setPen(QPen(border, 2))

        text_color = theme.text
        self.operator_text.setDefaultTextColor(text_color)
        if self.params_text:
            self.params_text.setDefaultTextColor(text_color)

    def mousePressEvent(self, event):
        if self.on_click:
            self.on_click(self.plan_node)
        super().mousePressEvent(event)


@dataclass
class LayoutConfig:
    level_height: int = 100
    node_spacing: int = 40
    node_width: int = 120
    node_height: int = 60


class QueryPlanScene(QGraphicsScene):
    """Scene that draws the tree and handles interaction"""

    LEVEL_HEIGHT = 100
    NODE_SPACING = 40

    def __init__(self, plan_root: QueryPlanNode, config: LayoutConfig | None = None, on_node_clicked=None):
        super().__init__()
        self.plan_root = plan_root
        self.config = config or LayoutConfig()
        self.node_items = {}
        self.on_node_clicked = on_node_clicked
        self._build_tree()

    def _build_tree(self):
        """Build the tree by recursively positioning nodes"""
        positions = {}
        self._calculate_positions(self.plan_root, 0, 0, positions)
        self._draw_nodes(self.plan_root, positions)
        self._draw_edges(self.plan_root, positions)

    def _calculate_positions(self, node: QueryPlanNode, level: int, offset: float, positions: dict) -> float:
        """
        Calculates positions using a recursive algorithm.
        Returns the width used by this subtree.
        """

        if node.is_leaf():
            x = offset
            y = level * self.LEVEL_HEIGHT
            positions[id(node)] = (x, y)
            return QueryPlanNodeItem.NODE_WIDTH + self.NODE_SPACING

        child_offset = offset
        child_widths = []
        for child in node.children:
            width = self._calculate_positions(child, level + 1, child_offset, positions)
            child_widths.append(width)
            child_offset += width

        total_width = sum(child_widths)
        if node.children:
            first_child_x = positions[id(node.children[0])][0]
            last_child_x = positions[id(node.children[-1])][0]
            x = (first_child_x + last_child_x) / 2
        else:
            x = offset

        y = level * self.LEVEL_HEIGHT
        positions[id(node)] = (x, y)

        return total_width

    def _draw_nodes(self, node: QueryPlanNode, positions: dict):
        x, y = positions[id(node)]
        node_item = QueryPlanNodeItem(node, x, y, self.on_node_clicked)
        self.addItem(node_item)
        self.node_items[id(node)] = node_item

        for child in node.children:
            self._draw_nodes(child, positions)

    def _draw_edges(self, node: QueryPlanNode, positions: dict):
        """Draw lines connecting parents and children"""
        if node.is_leaf():
            return

        theme = get_theme_manager().current_scheme
        line_color = theme.text
        line_color.setAlpha(128)

        parent_x, parent_y = positions[id(node)]
        parent_center_x = parent_x + QueryPlanNodeItem.NODE_WIDTH / 2
        parent_bottom_y = parent_y + QueryPlanNodeItem.NODE_HEIGHT

        for child in node.children:
            child_x, child_y = positions[id(child)]
            child_center_x = child_x + QueryPlanNodeItem.NODE_WIDTH / 2

            line = QGraphicsLineItem(parent_center_x, parent_bottom_y, child_center_x, child_y)
            line.setPen(QPen(line_color, 2))
            self.addItem(line)
            line.setZValue(-1)

            self._draw_edges(child, positions)


class QueryPlanDialog(QDialog):
    def __init__(self, plans: list[QueryPlanNode], relations: dict, parent=None):
        super().__init__(parent)
        self.setWindowTitle(tr.TR_QUERY_PLAN_TITLE)
        self.resize(900, 700)

        self.plans = plans
        self.relations = relations
        self.evaluator: QueryPlanEvaluator
        self._execution_order = []
        self._current_step = 0

        layout = QVBoxLayout(self)

        selector_layout = QHBoxLayout()
        selector_layout.addWidget(QLabel(tr.TR_QUERY_PLAN_QUERY_LABEL))

        self.query_combo = QComboBox()
        for i, plan in enumerate(plans):
            label = plan.relation_name or f"Query {i + 1}"
            self.query_combo.addItem(label, i)
        self.query_combo.currentIndexChanged.connect(self._on_query_changed)
        selector_layout.addWidget(self.query_combo)
        selector_layout.addStretch()

        layout.addLayout(selector_layout)

        hbox = QHBoxLayout()
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        self.btn_step = QPushButton(tr.TR_QUERY_PLAN_BTN_STEP)
        self.btn_step.clicked.connect(self._step_forward)
        self.btn_run_all = QPushButton(tr.TR_QUERY_PLAN_BTN_RUN_ALL)
        self.btn_run_all.clicked.connect(self._run_all)
        self.btn_reset = QPushButton(tr.TR_QUERY_PLAN_BTN_RESET)
        self.btn_reset.clicked.connect(self._reset)
        buttons_layout.addWidget(self.btn_step)
        buttons_layout.addWidget(self.btn_run_all)
        buttons_layout.addWidget(self.btn_reset)

        status_layout = QHBoxLayout()
        self.status_label = StatusPill(self)
        self.status_label.set_ready()
        status_layout.addWidget(self.status_label)
        status_layout.addStretch()
        hbox.addLayout(status_layout)
        hbox.addLayout(buttons_layout)
        layout.addLayout(hbox)

        # Contenedor para el árbol (se recrea al cambiar query)
        self.tree_container = QWidget()
        self.tree_layout = QVBoxLayout(self.tree_container)
        self.tree_layout.setContentsMargins(0, 0, 0, 0)

        # Splitter
        self.splitter = QSplitter(Qt.Orientation.Vertical)
        self.splitter.addWidget(self.tree_container)

        # Tabla de resultados
        result_container = QWidget()
        result_layout = QVBoxLayout(result_container)
        result_layout.setContentsMargins(0, 0, 0, 0)

        self.result_label = QLabel(tr.TR_QUERY_PLAN_SELECT_NODE)
        result_layout.addWidget(self.result_label)

        self.result_view = View()
        result_layout.addWidget(self.result_view)

        self.splitter.addWidget(result_container)
        self.splitter.setSizes([500, 200])

        layout.addWidget(self.splitter)

        # Cargar primera query
        self._on_query_changed(0)

    def _on_query_changed(self, index):
        """Selected query change"""
        plan = self.plans[index]

        # Limpiar árbol anterior
        while self.tree_layout.count():
            item = self.tree_layout.takeAt(0)
            if item and (widget := item.widget()):
                widget.deleteLater()

        # Crear nuevo árbol
        self.evaluator = QueryPlanEvaluator(self.relations)
        self._execution_order = []
        self._current_step = 0
        self._build_execution_order(plan)

        self.scene = QueryPlanScene(plan, on_node_clicked=self._on_node_clicked)

        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.view.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.tree_layout.addWidget(self.view)

        # Ajustar vista
        self.scene.setSceneRect(self.scene.itemsBoundingRect().adjusted(-20, -20, 20, 20))
        self.view.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)

        # Resetear controles
        self.btn_step.setEnabled(True)
        self.status_label.set_ready()
        self.result_view.setModel(None)

        self.status_label.set_ready()

    def _build_execution_order(self, node: QueryPlanNode):
        """Build post-order (leaves first, root last)"""
        if node.is_leaf():
            self._execution_order.append(node)
            return

        # Primero los hijos
        for child in node.children:
            self._build_execution_order(child)

        # Luego este nodo
        self._execution_order.append(node)

    def _step_forward(self):
        if self._current_step >= len(self._execution_order):
            self.status_label.set_completed()
            self.btn_step.setEnabled(False)
            return

        node = self._execution_order[self._current_step]
        self._evaluate_and_show(node)
        self._current_step += 1
        self.status_label.set_step(self._current_step, len(self._execution_order))

        if self._current_step >= len(self._execution_order):
            self.btn_step.setEnabled(False)
            self.status_label.set_completed()

    def __step_forward(self):
        if self._current_step >= len(self._execution_order):
            self.status_label.set_step(self._current_step, len(self._execution_order))
            self.btn_step.setEnabled(False)
            return

        node = self._execution_order[self._current_step]
        self._evaluate_and_show(node)
        self._current_step += 1
        self.status_label.set_step(self._current_step, len(self._execution_order))

        if self._current_step >= len(self._execution_order):
            self.btn_step.setEnabled(False)
            self.status_label.set_completed()

    def _run_all(self):
        """Execute all the steps at once."""
        while self._current_step < len(self._execution_order):
            node = self._execution_order[self._current_step]
            self._evaluate_and_show(node, show_in_table=False)  # no actualizar tabla cada vez
            self._current_step += 1

        # Mostrar resultado final
        final_node = self._execution_order[-1]
        self._show_result(final_node)

        self.status_label.set_completed()
        self.btn_step.setEnabled(False)

    def _reset(self):
        self._current_step = 0
        self.evaluator.cache.clear()
        for node in self._execution_order:
            node.state = NodeState.PENDING
            node.result = None
            node.error = ""
            if id(node) in self.scene.node_items:
                self.scene.node_items[id(node)]._update_style()
        self.status_label.set_ready()
        self.btn_step.setEnabled(True)
        self.result_view.setModel(None)

    def _evaluate_and_show(self, node: QueryPlanNode, show_in_table=True):
        """Evaluate a node and update the display"""
        try:
            self.evaluator.evaluate(node)

            # Actualizar vista del nodo
            node_item = self.scene.node_items[id(node)]
            node_item._update_style()

            # Mostrar en tabla
            if show_in_table:
                self._show_result(node)

        except Exception as e:
            self.status_label.set_error(str(e))
            node_item = self.scene.node_items[id(node)]
            node_item._update_style()

    def _show_result(self, node: QueryPlanNode):
        """Displays the result of a node in the table"""
        if node.result is None:
            return

        op_name = f"{node.operator.value}"
        if node.params:
            op_name += f" ({node.params})"

        self.result_label.setText(
            tr.TR_QUERY_PLAN_RESULT_FORMAT.format(
                op=op_name, tuples=node.result.cardinality(), attrs=node.result.degree()
            )
        )

        model = RelationModel(node.result)
        self.result_view.setModel(model)
        self.result_view.setItemDelegate(Delegate())

    def _on_node_clicked(self, node: QueryPlanNode):
        if node.state == NodeState.EXECUTED:
            self._show_result(node)
        else:
            self._evaluate_and_show(node)
