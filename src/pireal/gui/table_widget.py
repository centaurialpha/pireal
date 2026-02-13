from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSplitter,
    QStackedWidget,
    QTabWidget,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from pireal.core.db import DB
from pireal.core.relation import Relation
from pireal.gui.lateral_widget import LateralWidget
from pireal.gui.model_view_delegate import create_view
from pireal.helpers import Font
from pireal.registry import Registry


class PlaceholderWidget(QWidget):
    def __init__(
        self,
        message: str = "🛸 Espacio vacío detectado. \n¿Cargamos la primera relación?",
        parent=None,
    ):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        placeholder_label = QLabel(message)
        placeholder_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        placeholder_label.setStyleSheet("font-size: 18px; color: #888;")

        placeholder_button = QPushButton("Nueva relación")
        placeholder_button.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                padding: 8px;
                border-radius: 8px;
                background-color: #4CAF50;
                color: white;
            }
            QPushButton:hover {
                background-color: #45A049;
            }
        """)
        layout.addWidget(placeholder_label)
        layout.addSpacing(15)
        layout.addWidget(placeholder_button)

        placeholder_button.clicked.connect(self._on_placeholder_button_clicked)

    @pyqtSlot()
    def _on_placeholder_button_clicked(self):
        from pireal.gui.controller import Controller

        controller = Registry.get("controller", Controller)
        controller.create_relation()


class _TableWidget(QSplitter):
    def __init__(self):
        super().__init__()
        self._tabs = QTabWidget()
        self._tabs.setDocumentMode(True)
        self.addWidget(self._tabs)

        self._stacked = QStackedWidget()
        self._tabs.addTab(self._stacked, "Workspace")

        self._stacked_results = QStackedWidget()
        self._tabs.addTab(self._stacked_results, "Results")

        self._show_placeholder()

        lateral_widget = Registry.get("lateral-widget", LateralWidget)
        lateral_widget.resultClicked.connect(self._on_result_list_clicked)

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
        for i in range(self._stacked.count()):
            if isinstance(self._stacked.widget(i), PlaceholderWidget):
                return True
        return False

    @pyqtSlot(int)
    def _on_result_list_clicked(self, index):
        self._stacked_results.setCurrentIndex(index)

    def add_table_to_workspace(self, relation: Relation, editable=True):
        db = Registry.get("db", DB)

        # Eliminar el placeholder
        # TODO: volver a agregar luego? entonces no deberia ser un attr,
        # crear función helper para agregar el placeholder (?)
        self._remove_placeholder()

        view = create_view(relation, editable=editable)
        db.add(relation)
        self._stacked.addWidget(view)
        self._stacked.setCurrentWidget(view)
        self._update_tab_text(index=0)

    def _update_tab_text(self, index: int) -> None:
        tab_bar = self._tabs.tabBar()
        if tab_bar is not None:
            count = (
                self._stacked.count() if index == 0 else self._stacked_results.count()
            )
            table_name = "Workspace" if index == 0 else "Results"
            text = f"{table_name}({count})"
            tab_bar.setTabText(index, text)

    def add_table_to_results(self, relation: Relation, editable=False):
        view = create_view(relation, editable=editable)
        self._stacked_results.addWidget(view)
        self._update_tab_text(index=1)


class TableWidget(QWidget):
    def __init__(self):
        super().__init__()
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
        self._stacked.addWidget(view)
        self._stacked.setCurrentWidget(view)

    def add_table_to_results(self, relation: Relation, editable=False):
        view = create_view(relation, editable=editable)
        self._stacked_results.addWidget(view)
        self._stacked_results.setCurrentWidget(view)

        # Auto-split
        if not self._stacked_results.isVisible():
            self._btn_split.setChecked(True)
