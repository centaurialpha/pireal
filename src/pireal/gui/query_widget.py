from typing import Optional

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from pireal import translations as tr
from pireal.core.pireal_file import File, is_example_file
from pireal.gui.editor import Editor
from pireal.gui.status_bar import StatusBar
from pireal.registry import Registry


class QueryWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self._untitled_count = 0
        box = QVBoxLayout(self)
        box.setContentsMargins(0, 0, 0, 0)
        box.setSpacing(0)
        self._editor_tabs = QTabWidget()
        self._editor_tabs.setTabsClosable(True)
        self._editor_tabs.setMovable(True)
        self._editor_tabs.setTabPosition(QTabWidget.TabPosition.South)

        # Line/col
        self._line_col_label = QLabel("Ln 1, Col 1")
        self._line_col_label.setContentsMargins(0, 0, 6, 0)
        self._line_col_label.hide()
        self._editor_tabs.setCornerWidget(
            self._line_col_label,
            Qt.Corner.TopRightCorner,  # TopRight = esquina sobre las tabs (que están abajo = BottomRight)
        )
        box.addWidget(self._editor_tabs)

        self._editor_tabs.currentChanged.connect(self._on_tab_changed)
        self._editor_tabs.tabCloseRequested.connect(self._on_tab_close_requested)

    def _on_tab_changed(self, index: int):
        widget = self._editor_tabs.widget(index)
        if isinstance(widget, EditorWidget):
            self._line_col_label.show()
            cursor = widget.editor.textCursor()
            self._update_line_col(cursor.blockNumber() + 1, cursor.columnNumber() + 1)
        else:
            self._line_col_label.hide()

    def _update_line_col(self, line: int, col: int):
        self._line_col_label.setText(f"Ln {line}, Col {col}")

    def _on_tab_close_requested(self, index: int):
        editor = self._editor_tabs.widget(index)
        if not isinstance(editor, EditorWidget):
            return
        if editor.editor.document().isModified() and not is_example_file(editor.file):
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

    def clear(self):
        self._editor_tabs.clear()

    def add_editor(self, editor_widget: "EditorWidget"):
        status_bar = Registry.get("status-bar", StatusBar)
        editor_widget.editor.errorOccurred.connect(
            lambda line, msg: status_bar.show_message(f"Line {line}: {msg}", timeout=0, error=True)
        )
        editor_widget.editor.errorCleared.connect(
            lambda: status_bar.show_message("", timeout=0)
        )
        editor_widget.editor.cursorPositionChanged.connect(
            lambda: self._update_line_col(
                editor_widget.editor.textCursor().blockNumber() + 1,
                editor_widget.editor.textCursor().columnNumber() + 1,
            )
        )

        tab_text = editor_widget.file.display_name
        index = self._editor_tabs.addTab(editor_widget, tab_text)
        self._editor_tabs.setTabToolTip(index, editor_widget.file.path)

    def create_editor(self, file: Optional[File] = None) -> "EditorWidget":
        editor = EditorWidget()
        if file is not None:
            editor.file = file
        else:
            self._untitled_count += 1
            editor.file = File(display_name=f"untitled_{self._untitled_count}.pqf")
        self.add_editor(editor)
        return editor

    def _show_tree(self):
        from pireal.gui.dialogs.tree_dialog import TreeDialog
        from pireal.interpreter.lexer import Lexer
        from pireal.interpreter.parser import Parser
        from pireal.interpreter.scanner import Scanner
        from pireal.interpreter.tree_builder import TreeBuilder

        queries = self.current_editor().text()
        if not queries.strip():
            return

        try:
            tree = Parser(Lexer(Scanner(queries))).parse()
            roots = TreeBuilder().build(tree)
            dialog = TreeDialog(roots, self)
            dialog.exec()
        except Exception:
            pass

    def _show_sql(self):
        from pireal.gui.dialogs.sql_dialog import SQLDialog
        from pireal.interpreter.lexer import Lexer
        from pireal.interpreter.parser import Parser
        from pireal.interpreter.scanner import Scanner
        from pireal.interpreter.sql_generator import SQLGenerator

        queries = self.current_editor().text()
        if not queries.strip():
            return

        try:
            tree = Parser(Lexer(Scanner(queries))).parse()
            sql_queries = SQLGenerator(tree).generate()
            sql = "\n\n".join(f"-- {name}\n{sql}" for name, sql in sql_queries.items())
            dialog = SQLDialog(sql, self)
            dialog.exec()
        except Exception as e:
            print(e)
            pass  # si hay error de sintaxis, no mostrar nada

    def current_editor(self) -> "EditorWidget | None":
        widget = self._editor_tabs.currentWidget()
        if isinstance(widget, EditorWidget):
            return widget
        return None

    def _current_editor(self) -> "EditorWidget":
        for i in range(self._editor_tabs.count()):
            widget = self._editor_tabs.widget(i)
            if isinstance(widget, EditorWidget):
                return widget
        return self.create_editor()

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

        self.editor.document().modificationChanged.connect(
            self._on_modification_changed
        )

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
        return self.editor.toPlainText()

    def setText(self, text: str):
        self.editor.setPlainText(text)

    def saved(self):
        self.editor.saved()
        # actualizar el título del tab sacando el bullet •
        tabs = self._get_tabs()
        if tabs is not None:
            idx = tabs.indexOf(self)
            if idx != -1:
                tabs.setTabText(idx, self.file.display_name)

    def _get_tabs(self):
        from PyQt6.QtWidgets import QTabWidget

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
