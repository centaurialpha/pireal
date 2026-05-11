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


import logging

from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from pireal import translations as tr
from pireal.core.db import DB
from pireal.core.pireal_file import (
    File,
    is_example_file,
)
from pireal.gui.dialogs.query_plan_dialog import QueryPlanDialog
from pireal.gui.dialogs.sql_dialog import SQLDialog
from pireal.gui.editor import Editor
from pireal.gui.status_bar import StatusBar
from pireal.interpreter.exceptions import (
    ConsumeError,
    InvalidSyntaxError,
    MissingQuoteError,
)
from pireal.interpreter.lexer import Lexer
from pireal.interpreter.operator_pipeline import pipeline_text
from pireal.interpreter.parser import Parser
from pireal.interpreter.query_plan import QueryPlanBuilder
from pireal.interpreter.scanner import Scanner
from pireal.interpreter.sql_generator import SQLGenerator
from pireal.interpreter.tokens import SYMBOL_TO_KEYWORD
from pireal.registry import Registry
from pireal.settings import settings

logger = logging.getLogger(__name__)


class QueryWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self._untitled_count = 0
        self._symbol_mode_on = False

        box = QVBoxLayout(self)
        box.setContentsMargins(0, 0, 0, 0)
        box.setSpacing(0)
        self._editor_tabs = QTabWidget()
        self._editor_tabs.setTabsClosable(True)
        self._editor_tabs.setMovable(True)
        self._editor_tabs.setTabPosition(QTabWidget.TabPosition.South)

        box.addWidget(self._editor_tabs)

        self._editor_tabs.currentChanged.connect(self._on_tab_changed)
        self._editor_tabs.tabCloseRequested.connect(self._on_tab_close_requested)

        self.hide()

    def _on_cursor_moved(self, editor_widget: "EditorWidget") -> None:
        status_bar = Registry.get("status-bar", StatusBar)
        cursor = editor_widget.editor.textCursor()
        line = cursor.blockNumber() + 1
        col = cursor.columnNumber() + 1
        status_bar.update_line_col(line, col)
        self._update_pipeline(editor_widget, line)

    def _update_pipeline(self, editor_widget: "EditorWidget", current_line: int) -> None:
        status_bar = Registry.get("status-bar", StatusBar)

        text = editor_widget.text()
        if not text:
            status_bar.hide_pipeline()
            return

        try:
            tree = Parser(Lexer(Scanner(text))).parse()
        except Exception:
            status_bar.hide_pipeline()
            return

        # Rangos de bloques (0-based)
        lines_list = text.split("\n")
        assignments = tree.children
        blocks = []
        for idxi, assignment in enumerate(assignments):
            start = (assignment.rname.lineno or 1) - 1  # 0-based
            # el fin real es la línea donde está el ;
            end = start
            for idxj in range(start, len(lines_list)):
                if ";" in lines_list[idxj]:
                    end = idxj
                    break
            blocks.append((start, end, idxi))

        editor_widget.editor.set_query_blocks(blocks)

        # Encontrar el assignment cuyo rango de líneas incluye current_line
        target = None
        for assignment in tree.children:
            if assignment.rname.lineno is not None:
                if assignment.rname.lineno <= current_line:
                    target = assignment
                else:
                    break
        else:
            target = tree.children[-1] if tree.children else None

        if target is None:
            status_bar.hide_pipeline()
            return

        text_pipeline = pipeline_text(target)
        if text_pipeline:
            status_bar.show_pipeline(text_pipeline)
        else:
            status_bar.hide_pipeline()

    def set_symbol_mode(self, enabled: bool) -> None:
        self._symbol_mode_on = enabled
        editor = self.current_editor()
        if editor:
            editor.editor.toggle_symbol_mode(enabled)

        status_bar = Registry.get("status-bar", StatusBar)
        status_bar.show_symbol_mode(enabled)

    def _on_tab_changed(self, index: int) -> None:
        status_bar = Registry.get("status-bar", StatusBar)
        widget = self._editor_tabs.widget(index)
        if isinstance(widget, EditorWidget):
            cursor = widget.editor.textCursor()
            status_bar.update_line_col(cursor.blockNumber() + 1, cursor.columnNumber() + 1)
        else:
            status_bar.hide_line_col()

    def _on_tab_close_requested(self, index: int):
        editor = self._editor_tabs.widget(index)
        if not isinstance(editor, EditorWidget):
            return
        doc = editor.editor.document()
        if doc is not None and doc.isModified() and not is_example_file(editor.file):
            ret = QMessageBox.question(
                self,
                tr.TR_TAB_CLOSE_TITLE,
                tr.TR_TAB_CLOSE_BODY.format(name=editor.file.display_name),
                QMessageBox.StandardButton.Save
                | QMessageBox.StandardButton.Discard
                | QMessageBox.StandardButton.Cancel,
            )
            if ret == QMessageBox.StandardButton.Cancel:
                return
            if ret == QMessageBox.StandardButton.Save:
                from pireal.gui.controller import Controller

                controller = Registry.get("controller", Controller)
                controller.save_query()
        self._editor_tabs.removeTab(index)
        if self._editor_tabs.count() == 0:
            self.hide()

    def clear(self):
        self._editor_tabs.clear()
        self.hide()

    def add_editor(self, editor_widget: "EditorWidget"):
        status_bar = Registry.get("status-bar", StatusBar)
        editor_widget.editor.errorOccurred.connect(
            lambda line, msg: status_bar.show_message(f"Line {line}: {msg}", timeout=0, error=True)
        )
        editor_widget.editor.errorCleared.connect(lambda: status_bar.show_message("", timeout=0))
        editor_widget.editor.cursorPositionChanged.connect(lambda: self._on_cursor_moved(editor_widget))

        tab_text = editor_widget.file.display_name
        index = self._editor_tabs.addTab(editor_widget, tab_text)
        self._editor_tabs.setTabToolTip(index, editor_widget.file.path)
        self._editor_tabs.setCurrentIndex(index)

    def create_editor(self, file: File | None = None) -> "EditorWidget":
        editor = EditorWidget()
        if file is not None:
            editor.file = file
        else:
            self._untitled_count += 1
            editor.file = File(display_name=f"untitled_{self._untitled_count}.pqf")
        self.add_editor(editor)
        self.show()
        return editor

    def _show_tree(self):
        editor = self.current_editor()
        if editor is None:
            return
        queries = editor.text()
        if not queries.strip():
            return

        try:
            tree = Parser(Lexer(Scanner(queries))).parse()
            db = Registry.get("db", DB)

            # Contexto inicial: relaciones base
            context = db.relations_dict().copy()

            # Evaluar queries intermedios y agregarlos al contexto
            from pireal.interpreter.evaluator import Evaluator

            evaluator = Evaluator(context)
            results = evaluator.evaluate(tree)
            context.update(results)  # ahora context tiene base + intermedios

            # Construir plan de la última query
            builder = QueryPlanBuilder(context)
            plans = builder.build(tree)

            if plans:
                # Mostrar el último plan con contexto completo
                dialog = QueryPlanDialog(plans, context, self)
                dialog.exec()
        except (MissingQuoteError, InvalidSyntaxError, ConsumeError):
            pass
        except Exception:
            logger.exception("Unexpected error building query plan")

    def _show_sql(self):
        editor = self.current_editor()
        if editor is None:
            return
        queries = editor.text()
        if not queries.strip():
            return

        try:
            tree = Parser(Lexer(Scanner(queries))).parse()
            sql_queries = SQLGenerator(tree).generate()
            sql = "\n\n".join(f"-- {name}\n{sql}" for name, sql in sql_queries.items())
            dialog = SQLDialog(sql, self)
            dialog.exec()
        except (MissingQuoteError, InvalidSyntaxError, ConsumeError):
            pass  # sintáxis inválida, no mostrar nada
        except Exception:
            logger.exception("Unexpected error generating SQL")

    def current_editor(self) -> "EditorWidget | None":
        widget = self._editor_tabs.currentWidget()
        if isinstance(widget, EditorWidget):
            return widget
        return None

    def update_completer(self, relation_names: list[str]) -> None:
        for i in range(self._editor_tabs.count()):
            widget = self._editor_tabs.widget(i)
            if isinstance(widget, EditorWidget):
                widget.editor.completer.update_words(relation_names)

    def close_current_editor(self):
        index = self._editor_tabs.currentIndex()
        if index != -1:
            self._on_tab_close_requested(index)


class EditorWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        vbox = QVBoxLayout(self)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(0)

        self.editor = Editor()
        vbox.addWidget(self.editor)

        doc = self.editor.document()
        if doc is not None:
            doc.modificationChanged.connect(self._on_modification_changed)

        self._search_widget = SearchWidget(self.editor)
        self._search_widget.hide()
        vbox.addWidget(self._search_widget)

        self._file: File

    def _on_modification_changed(self, modified: bool):
        tabs = self._get_tabs()
        if tabs is None:
            return
        idx = tabs.indexOf(self)
        if idx == -1:
            return
        name = self.file.display_name
        tabs.setTabText(idx, f"{name} •" if modified else name)

    @property
    def file(self) -> File:
        return self._file

    @file.setter
    def file(self, file: File) -> None:
        self._file = file

    def text(self) -> str:
        content = self.editor.toPlainText()
        for symbol, keyword in SYMBOL_TO_KEYWORD.items():
            content = content.replace(symbol, keyword)
        return content

    def setText(self, text: str):
        self.editor.setPlainText(text)
        if settings.symbol_mode:
            self.editor.toggle_symbol_mode(True)
        document = self.editor.document()
        if document is not None:
            document.setModified(False)
        self.editor.modified = False

    def saved(self):
        self.editor.saved()
        # actualizar el título del tab sacando el bullet •
        tabs = self._get_tabs()
        if tabs is not None:
            idx = tabs.indexOf(self)
            if idx != -1:
                tabs.setTabText(idx, self.file.display_name)

    def _get_tabs(self):
        parent = self.parent()
        while parent is not None:
            if isinstance(parent, QTabWidget):
                return parent
            parent = parent.parent()
        return None


class SearchWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        box = QHBoxLayout(self)
        box.setContentsMargins(0, 3, 0, 3)
        box.setSpacing(0)
        self._line_search = QLineEdit()
        box.addWidget(self._line_search)
        btn_find_previous = QPushButton(tr.TR_BTN_FIND_PREVIOUS)
        box.addWidget(btn_find_previous)
        btn_find_next = QPushButton(tr.TR_BTN_FIND_NEXT)
        box.addWidget(btn_find_next)

        self._parent = parent

        self._line_search.textChanged.connect(self._execute_search)
        btn_find_next.clicked.connect(self._find_next)
        btn_find_previous.clicked.connect(self._find_previous)

    def _find_next(self):
        self._execute_search(find_next=True)

    def _find_previous(self):
        self._execute_search(backward=True)

    def _execute_search(self, find_next=False, backward=False):
        text = self.search_text
        if not text:
            return
        self._parent.find_text(text, find_next=find_next, backward=backward)

    @property
    def search_text(self):
        return self._line_search.text()
