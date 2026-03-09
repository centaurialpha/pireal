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


import time

from PyQt6.QtCore import QSettings, Qt, pyqtSlot
from PyQt6.QtWidgets import QSplitter

from pireal.core.db import DB
from pireal.core.pireal_file import File
from pireal.core.relation import Relation
from pireal.dirs import DATA_SETTINGS
from pireal.gui.lateral_widget import LateralWidget, RelationItemType
from pireal.gui.model_view_delegate import Delegate, RelationModel, View
from pireal.gui.query_widget import QueryWidget
from pireal.gui.right_pane import RightPane
from pireal.gui.status_bar import StatusBar
from pireal.gui.table_widget import TableWidget
from pireal.interpreter.evaluator import Evaluator, UndefinedRelationError
from pireal.interpreter.exceptions import (
    ConsumeError,
    DuplicateRelationNameError,
    InvalidSyntaxError,
    MissingQuoteError,
    UndefinedAttributeError,
)
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
        status_bar = Registry.get("status-bar", StatusBar)

        self.addWidget(lateral_widget)
        self.addWidget(right_pane)

        self._relations: dict[str, Relation] = {}
        self._database = Registry.get("db", DB)

        lateral_widget.relationClicked.connect(self._on_relation_clicked)
        table_widget.sqlRequested.connect(query_widget._show_sql)
        table_widget.treeRequested.connect(query_widget._show_tree)
        self._database.relationsChanged.connect(query_widget.update_completer)
        self._database.databaseStateChanged.connect(self._on_db_state_for_status)
        self._database.databaseStateChanged.connect(
            lambda active: status_bar.update_db_name(
                self._database.file.display_name if active and self._database.file else ""
            )
        )

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
        for table in data.get("tables"):
            table_name = table.get("name")
            header = table.get("header")
            tuples = table.get("tuples")

            rela = Relation()
            rela.header = header

            for tup in tuples:
                rela.insert(tup)

            # FIXME: feo
            rela.name = table_name

            self._database.load(rela)

            # FIXME: acá se hace un add por lo tanto se modifica la db, utilizar load
            table_widget.add_table_to_workspace(rela)

            lateral_widget.add_item(rela, RelationItemType.Normal)

        self._database.modified = False

    @pyqtSlot(int)
    def _on_relation_clicked(self, row: int):
        table_widget = Registry.get("table-widget", TableWidget)
        table_widget._stacked.setCurrentIndex(row)

    def showEvent(self, a0):
        super().showEvent(a0)
        qsettings = QSettings(str(DATA_SETTINGS), QSettings.Format.IniFormat)
        hsizes = qsettings.value("hsplitter_sizes", None)
        if hsizes is not None:
            self.restoreState(hsizes)
        else:
            self.setSizes([round(self.width() / 10), round(self.width() / 3)])

    def new_query(self, filename: str) -> None:
        query_widget = Registry.get("query-widget", QueryWidget)

        if filename:
            file = File(filename)
            editor = query_widget.create_editor(file)
            content = file.read()
            editor.setText(content)
        else:
            query_widget.create_editor()

    def execute_queries(self):
        from pireal.interpreter.parser import parse

        db = Registry.get("db", DB)
        table_widget = Registry.get("table-widget", TableWidget)
        query_widget = Registry.get("query-widget", QueryWidget)
        lateral_widget = Registry.get("lateral-widget", LateralWidget)

        editor = query_widget.current_editor()
        queries = editor.text()
        editor.editor.show_run_cursor()

        # Limpiar resultados anteriores
        lateral_widget.clear_results()
        db.clear_query_results()
        table_widget.clear_results()

        try:
            tree = parse(queries)
            editor.editor.highlight_error(-1)
        except (MissingQuoteError, InvalidSyntaxError, ConsumeError) as err:
            editor.editor.highlight_error(err.lineno, message=str(err))
            return

        try:
            start = time.perf_counter()
            results = Evaluator(db.relations_dict()).evaluate(tree)
            elapsed_ms = round((time.perf_counter() - start) * 1000)
        except UndefinedRelationError as err:
            editor.editor.highlight_error(err.lineno, message=str(err))
            return
        except UndefinedAttributeError as err:
            status_bar = Registry.get("status-bar", StatusBar)
            status_bar.show_message(str(err))
            return
        except DuplicateRelationNameError as err:
            status_bar = Registry.get("status-bar", StatusBar)
            status_bar.show_message(str(err))
            return

        for name, relation in results.items():
            db.load(relation)
            db._query_results.append(name)
            table_widget.add_table_to_results(relation)
            lateral_widget.add_item(relation, RelationItemType.Result)

        status_bar = Registry.get("status-bar", StatusBar)
        status_bar.update_query_time(elapsed_ms)
