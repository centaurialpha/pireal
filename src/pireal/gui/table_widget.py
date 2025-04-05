from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import QSplitter, QStackedWidget, QTabWidget

from pireal.core.relation import Relation
from pireal.gui.db import DB
from pireal.gui.lateral_widget import LateralWidget
from pireal.gui.model_view_delegate import create_view
from pireal.registry import Registry


class TableWidget(QSplitter):
    def __init__(self):
        super().__init__()
        self._tabs = QTabWidget()
        self._tabs.setDocumentMode(True)
        self.addWidget(self._tabs)

        self._stacked = QStackedWidget()
        self._tabs.addTab(self._stacked, "Workspace")

        self._stacked_results = QStackedWidget()
        self._tabs.addTab(self._stacked_results, "Results")

        lateral_widget = Registry.get("lateral-widget", LateralWidget)
        lateral_widget.resultClicked.connect(self._on_result_list_clicked)

    @pyqtSlot(int)
    def _on_result_list_clicked(self, index):
        self._stacked_results.setCurrentIndex(index)

    def add_table_to_workspace(self, relation: Relation, editable=True):
        db = Registry.get("db", DB)

        view = create_view(relation, editable=editable)
        db.add(relation)
        self._stacked.addWidget(view)
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
