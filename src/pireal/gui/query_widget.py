from typing import Optional

from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from pireal import translations as tr
from pireal.core.pireal_file import File
from pireal.gui.editor import Editor
from pireal.registry import Registry


class QueryWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        box = QVBoxLayout(self)
        box.setContentsMargins(0, 0, 0, 0)
        box.setSpacing(0)
        self._editor_tabs = QTabWidget()
        self._editor_tabs.setTabsClosable(True)
        self._editor_tabs.setMovable(True)
        self._editor_tabs.setTabPosition(QTabWidget.TabPosition.South)
        box.addWidget(self._editor_tabs)

        self._editor_tabs.tabCloseRequested.connect(self._on_tab_close_requested)

    def _on_tab_close_requested(self, index: int):
        editor = self._editor_tabs.widget(index)
        if not isinstance(editor, EditorWidget):
            return

        if editor.editor.document().isModified():
            from PyQt6.QtWidgets import QMessageBox

            ret = QMessageBox.question(
                self,
                "Archivo modificado",
                f"El archivo <b>{editor.file.display_name}</b> tiene cambios sin guardar. ¿Guardar antes de cerrar?",
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

    def add_editor(self, editor: "EditorWidget"):
        tab_text = editor.file.display_name
        index = self._editor_tabs.addTab(editor, tab_text)
        self._editor_tabs.setTabToolTip(index, editor.file.path)

    def create_editor(self, file: Optional[File] = None) -> "EditorWidget":
        editor = EditorWidget()
        if file is not None:
            editor.file = file
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
