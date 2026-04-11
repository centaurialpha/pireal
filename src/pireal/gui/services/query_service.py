import logging
from pathlib import Path

from PyQt6.QtWidgets import QFileDialog

from pireal import translations as tr
from pireal.core.db import DB
from pireal.core.olakase import check_relation
from pireal.core.pireal_file import File
from pireal.gui.lateral_widget import LateralWidget, RelationItemType
from pireal.gui.query_widget import QueryWidget
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
from pireal.interpreter.parser import parse
from pireal.registry import Registry

logger = logging.getLogger(__name__)


class QueryService:
    def __init__(self, db: DB, last_folder: str = "", parent_widget=None):
        self._db = db
        self._parent = parent_widget
        self._last_folder = last_folder or str(Path.home())

    def _remember_folder(self, filepath: str) -> None:
        self._last_folder = str(Path(filepath).parent)

    @property
    def last_folder(self) -> str:
        return self._last_folder

    def new(self, filename: str = "") -> None:
        query_widget = Registry.get("query-widget", QueryWidget)

        if filename:
            from pireal.core.pireal_file import File

            file = File(filename)
            editor = query_widget.create_editor(file)
            editor.setText(file.read())
        else:
            query_widget.create_editor()

    def open(self, filename: str = "") -> None:
        if not filename:
            filename, _ = QFileDialog.getOpenFileName(
                self._parent,
                tr.TR_OPEN_QUERY,
                self.last_folder,
                "Pireal Query (*.pqf)",
            )
            if not filename:
                return
        self.new(filename)
        self._remember_folder(filename)

    def save(self) -> bool:
        query_widget = Registry.get("query-widget", QueryWidget)
        editor = query_widget.current_editor()
        if editor is None:
            return False
        if editor.file.is_new:
            return self.save_as()
        editor.file.save(editor.text())
        editor.saved()
        return True

    def save_as(self) -> bool:
        query_widget = Registry.get("query-widget", QueryWidget)
        editor = query_widget.current_editor()
        if editor is None:
            return False

        filename, _ = QFileDialog.getSaveFileName(
            self._parent,
            tr.TR_MSG_SAVE_QUERY_FILE,
            "",
            "Pireal Query File (*.pqf)",
        )
        if not filename:
            return False

        if not filename.endswith(".pqf"):
            filename += ".pqf"

        editor.file = File(filename)
        editor.file.save(editor.text())
        editor.saved()

        self._remember_folder(filename)

        return True

    def close(self) -> None:
        query_widget = Registry.get("query-widget", QueryWidget)
        query_widget.close_current_editor()

    def execute(self) -> None:
        query_widget = Registry.get("query-widget", QueryWidget)
        table_widget = Registry.get("table-widget", TableWidget)
        lateral_widget = Registry.get("lateral-widget", LateralWidget)

        editor = query_widget.current_editor()
        if editor is None:
            return

        queries = editor.text()
        lateral_widget.clear_results()
        self._db.clear_query_results()
        table_widget.clear_results()

        try:
            tree = parse(queries)
            editor.editor.highlight_error(-1)
            editor.editor.show_run_cursor()
        except (MissingQuoteError, InvalidSyntaxError, ConsumeError) as err:
            editor.editor.highlight_error(err.lineno, message=str(err))
            return

        try:
            results = Evaluator(self._db.relations_dict()).evaluate(tree)
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
            self._db.load(relation)
            self._db.add_query_result(name)
            table_widget.add_table_to_results(relation)
            lateral_widget.add_item(relation, RelationItemType.Result)

        for name in self._db.relations_dict():
            if check_relation(name) is not None:
                status_bar = Registry.get("status-bar", StatusBar)
                status_bar.show_message("buena elección de nombre", timeout=5000)
                break
