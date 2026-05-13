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
    QSettings,
    Qt,
    pyqtSlot,
)
from PyQt6.QtWidgets import QSplitter

from pireal.core.db import DB
from pireal.core.relation_loader import load_relations
from pireal.dirs import DATA_SETTINGS
from pireal.gui.lateral_widget import (
    LateralWidget,
    RelationItemType,
)
from pireal.gui.model_view_delegate import (
    Delegate,
    RelationModel,
    View,
)
from pireal.gui.query_widget import QueryWidget
from pireal.gui.right_pane import RightPane
from pireal.gui.status_bar import StatusBar
from pireal.gui.table_widget import TableWidget
from pireal.registry import Registry


def create_view(relation, *, editable=False):
    view = View()
    model = RelationModel(relation)
    model.editable = editable
    view.setModel(model)
    view.setItemDelegate(Delegate())
    return view


class DatabaseContainer(QSplitter):
    def __init__(self, orientation=Qt.Orientation.Horizontal):
        super().__init__(orientation)
        lateral_widget = Registry.get("lateral-widget", LateralWidget)
        right_pane = Registry.get("right-pane", RightPane)
        table_widget = Registry.get("table-widget", TableWidget)
        query_widget = Registry.get("query-widget", QueryWidget)

        self.addWidget(lateral_widget)
        self.addWidget(right_pane)

        self._database = Registry.get("db", DB)

        lateral_widget.relationClicked.connect(self._on_relation_clicked)
        table_widget.sqlRequested.connect(query_widget._show_sql)
        table_widget.treeRequested.connect(query_widget._show_tree)
        self._database.relationsChanged.connect(query_widget.update_completer)
        self._database.databaseStateChanged.connect(self._on_db_state_for_status)

    @pyqtSlot(bool)
    def _on_db_state_for_status(self, active: bool) -> None:
        status_bar = Registry.get("status-bar", StatusBar)
        if active and self._database.file:
            status_bar.update_db_name(self._database.file.display_name)
        else:
            status_bar.update_db_name("")

    def create_database(self, data):
        table_widget = Registry.get("table-widget", TableWidget)
        lateral_widget = Registry.get("lateral-widget", LateralWidget)

        relations = list(load_relations(data))
        for relation in relations:
            self._database.load(relation)
            table_widget.add_table_to_workspace(relation)
            lateral_widget.add_item(relation, RelationItemType.Normal)

        last = len(relations) - 1
        lateral_widget.select_relation(last)
        table_widget.show_relation_at(last)

    def add_relations(self, data):
        table_widget = Registry.get("table-widget", TableWidget)
        lateral_widget = Registry.get("lateral-widget", LateralWidget)

        relations = list(load_relations(data))
        for relation in relations:
            self._database.add(relation)
            table_widget.add_table_to_workspace(relation)
            lateral_widget.add_item(relation, RelationItemType.Normal)

        last = len(relations) - 1
        lateral_widget.select_relation(last)
        table_widget.show_relation_at(last)

    @pyqtSlot(int)
    def _on_relation_clicked(self, row: int):
        table_widget = Registry.get("table-widget", TableWidget)
        table_widget.show_relation_at(row)

    def showEvent(self, a0):
        super().showEvent(a0)
        qsettings = QSettings(str(DATA_SETTINGS), QSettings.Format.IniFormat)
        hsizes = qsettings.value("hsplitter_sizes", None)
        if hsizes is not None:
            self.restoreState(hsizes)
        else:
            self.setSizes([round(self.width() / 10), round(self.width() / 3)])

    def save_state(self) -> None:
        qsettings = QSettings(str(DATA_SETTINGS), QSettings.Format.IniFormat)
        qsettings.setValue("hsplitter_sizes", self.saveState())
