from typing import Optional, cast

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

    def current_editor(self) -> "EditorWidget":
        current_widget = self._editor_tabs.currentWidget()
        if current_widget is None:
            current_widget = self.create_editor()
        return cast("EditorWidget", current_widget)


class EditorWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        vbox = QVBoxLayout(self)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(0)

        self.editor = Editor()
        vbox.addWidget(self.editor)

        self._search_widget = SearchWidget(self.editor)
        self._search_widget.hide()
        vbox.addWidget(self._search_widget)

        self._file: File

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
