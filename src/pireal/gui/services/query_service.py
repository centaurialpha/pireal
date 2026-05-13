import logging
from pathlib import Path

from PyQt6.QtWidgets import (
    QFileDialog,
    QMessageBox,
)

from pireal import translations as tr
from pireal.core.db import DB
from pireal.core.pireal_file import (
    File,
    is_example_file,
)
from pireal.core.relation import (
    DivisionIncompatibleError,
    UnionCompatibleError,
)
from pireal.gui.lateral_widget import (
    LateralWidget,
    RelationItemType,
)
from pireal.gui.query_widget import (
    EditorWidget,
    QueryWidget,
)
from pireal.gui.status_bar import StatusBar
from pireal.gui.table_widget import TableWidget
from pireal.interpreter.evaluator import (
    Evaluator,
    UndefinedRelationError,
)
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
        logger.debug("Opening query: '%s'", filename or "<dialog>")
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
            self._last_folder,
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

    def _show_runtime_error(self, msg: str) -> None:
        status_bar = Registry.get("status-bar", StatusBar)
        status_bar.show_message(msg, timeout=0, error=True)

    def execute(self) -> None:
        logger.debug("Executing queries")
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
            logger.warning("Query parse error (line %s): %s", err.lineno, err)
            editor.editor.highlight_error(err.lineno, message=str(err))
            return

        try:
            results = Evaluator(self._db.relations_dict()).evaluate(tree)
        except UndefinedRelationError as err:
            logger.warning("Undefined relation (line %s): %s", err.lineno, err)
            editor.editor.highlight_error(err.lineno, message=str(err))
            return
        except (
            UndefinedAttributeError,
            DuplicateRelationNameError,
            DivisionIncompatibleError,
            UnionCompatibleError,
        ) as err:
            logger.error("Query evaluation error: %s", err)
            self._show_runtime_error(str(err))
            return

        # Ejecución exitosa: limpiar cualquier error previo de runtime
        status_bar = Registry.get("status-bar", StatusBar)
        status_bar.show_message("", timeout=0)

        for name, relation in results.items():
            self._db.load(relation)
            self._db.add_query_result(name)
            table_widget.add_table_to_results(relation)
            lateral_widget.add_item(relation, RelationItemType.Result)

        lateral_widget.select_result(len(results) - 1)

        logger.info("Queries executed successfully: %d result(s)", len(results))

    def confirm_close(self) -> bool:
        """
        Pregunta al usuario qué hacer con las queries modificadas.
        Retorna False si el usuario canceló, True si puede proceder.
        """
        from pireal.gui.main_window import Pireal

        query_widget = Registry.get("query-widget", QueryWidget)
        unsaved = [
            w
            for i in range(query_widget._editor_tabs.count())
            if isinstance((w := query_widget._editor_tabs.widget(i)), EditorWidget)
            and (doc := w.editor.document()) is not None
            and doc.isModified()
            and not is_example_file(w.file)
        ]

        if not unsaved:
            return True

        names = ", ".join(e.file.display_name for e in unsaved)
        answer = QMessageBox.question(
            Pireal.instance(),
            tr.TR_UNSAVED_QUERIES_TITLE,
            tr.TR_UNSAVED_QUERIES_BODY.format(names=names),
            QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard | QMessageBox.StandardButton.Cancel,
        )
        if answer == QMessageBox.StandardButton.Cancel:
            return False
        if answer == QMessageBox.StandardButton.Save:
            for editor in unsaved:
                query_widget._editor_tabs.setCurrentWidget(editor)
                if not self.save():
                    return False
        return True
