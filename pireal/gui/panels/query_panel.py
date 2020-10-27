# -*- coding: utf-8 -*-
#
# Copyright 2015-2020 - Gabriel Acosta <acostadariogabriel@gmail.com>
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
from typing import Iterator, Tuple

from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal as Signal
from PyQt5.QtCore import pyqtSlot as Slot
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import (QHBoxLayout, QLabel, QLineEdit, QMenu,
                             QMessageBox, QPushButton, QTabWidget, QVBoxLayout,
                             QWidget)

from pireal import translations as tr
from pireal.core import interpreter
from pireal.core.file_utils import File
from pireal.gui.editor import Editor

logger = logging.getLogger('gui.query_panel')


class QueryPanel(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.hide()

        self._db_panel = parent
        vbox = QVBoxLayout(self)
        vbox.setContentsMargins(3, 0, 3, 0)
        vbox.setSpacing(0)
        self.editor_widget = EditorWidget(self)
        vbox.addWidget(self.editor_widget)
        self._search_widget = SearchWidget()
        vbox.addWidget(self._search_widget)
        self._search_widget.hide()

        self.editor_widget.allTabsClosed.connect(self.hide)
        self._queries = {}

    def load_or_create_new_editor(self, filename: str = None):
        # First create a File object
        file = File(path=filename)

        editor = self.editor_widget.get_editor_by_filename(file.filename)
        if editor is None:
            # Create new editor
            editor = self.editor_widget.create_editor(file)
            if not file.is_new:
                editor.setPlainText(file.read())
        else:
            logger.debug('query=%s already open', file.filename)
            self.editor_widget.set_current_editor(editor)

        if not self.isVisible():
            self.setVisible(True)

    def reload_editor_scheme(self):
        for weditor in self.editor_widget.editors():
            weditor.apply_scheme()
            weditor.reload_highlighter()

    def change_visibility(self):
        if self.isVisible():
            self._hide()
        else:
            self.show()

    def get_current_editor(self) -> Editor:
        return self.editor_widget.current_editor()

    def save_query(self):
        pass

    def save_query_as(self):
        pass

    def execute_query(self, relations: dict):
        """
        steps:
        1. get current editor
        2. get current text (selected or all text)
        3. parse text aka query (cath all exceptions and show message box)
        4. get current active relations in DB
        5. clear current results (tables and list)
        6. evaluate individual query iterating over result in step 3
        7. get relations and send to db panel to create tables
        """
        current_editor = self.editor_widget.current_editor()
        if current_editor.textCursor().hasSelection():
            query = '\n'.join(current_editor.textCursor().selectedText().splitlines())
        else:
            query = current_editor.toPlainText()

        print(query)
        try:
            result = interpreter.parse(query)
        except interpreter.MissingQuoteError:
            logger.exception('missing quote error')
        except interpreter.InvalidSyntaxError:
            logger.exception('invalid syntax error')
        except interpreter.ConsumeError:
            logger.exception('consume error')
        else:
            # self._db_panel.clear_relations_list()
            self._db_panel.clear_relations_result_list()

            current_relations = dict(relations)
            for relation_name, expression in result.items():
                try:
                    new_relation = eval(expression, {}, current_relations)
                except Exception:
                    logger.exception('error during eval expression=%s', expression)
                    return
                new_relation.name = relation_name
                current_relations[relation_name] = new_relation

                self._db_panel.add_relation_to_results_list(new_relation)
                self._db_panel.add_relation_to_results(new_relation)


class EditorWidget(QWidget):
    allTabsClosed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._parent = parent
        self._opened_editors = []

        vbox = QVBoxLayout(self)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(0)

        self._tabs_editor = QTabWidget()
        self._tabs_editor.setTabsClosable(True)
        self._tabs_editor.setMovable(True)

        self._tabs_editor.setContextMenuPolicy(Qt.CustomContextMenu)
        self._tabs_editor.customContextMenuRequested.connect(self._show_menu)

        line_col_widget = QWidget()
        hbox = QHBoxLayout(line_col_widget)
        self._line_col_text = 'Lin: {} Col: {}'
        self._lbl_line_col = QLabel(self._line_col_text.format(0, 0))
        hbox.addWidget(self._lbl_line_col)
        self._tabs_editor.setCornerWidget(line_col_widget)
        vbox.addWidget(self._tabs_editor)

        self._tabs_editor.tabCloseRequested[int].connect(self.remove_tab)

    def _show_menu(self, qpoint):
        menu = QMenu()
        remove_all_act = menu.addAction('Remove All')
        remove_other_act = menu.addAction('Remove others')

        remove_all_act.triggered.connect(self.remove_all_tabs)
        remove_other_act.triggered.connect(self.remove_other)

        menu.exec_(QCursor.pos())

    @Slot(int)
    def remove_tab(self, index=-1):
        if index == -1:
            weditor = self.current_editor()
        else:
            weditor = self.get_editor_by_index(index)
        if weditor is None:
            return
        if weditor.is_modified:
            reply = QMessageBox.question(
                self,
                tr.TR_MSG_FILE_MODIFIED,
                tr.TR_MSG_FILE_MODIFIED_BODY.format(weditor.display_name),
                QMessageBox.Cancel | QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.Cancel:
                return
            if reply == QMessageBox.Yes:
                self._parent.save_query(weditor)

        self.remove(weditor)
        self._tabs_editor.removeTab(index)
        weditor.deleteLater()
        if not self._opened_editors:
            self.allTabsClosed.emit()

    def remove_all(self):
        logger.info('removing all tabs')
        for _ in range(self._tabs_editor.count()):
            self.remove_tab(0)

    def remove_others(self):
        logger.info('removing all tabs except this')
        current_index = self._tabs_editor.currentIndex()
        weditor = self.get_editor_by_index(current_index)
        self._tabs_editor.insertTab(0, weditor, self._tabs_editor.tabText(current_index))
        for _ in range(1, self._tabs_editor.count()):
            self.remove_tab(1)

    def remove(self, weditor: Editor):
        logger.debug('closing file: %s', weditor.display_name)
        self._opened_editors.remove(weditor)

    def editors(self) -> Tuple[Editor]:
        return tuple(self._opened_editors)

    def has_editors(self) -> bool:
        return len(self._opened_editors) > 0

    def is_open(self, filename: str) -> bool:
        found = False
        for weditor in self._opened_editors:
            if weditor.filename == filename:
                found = True
                break
        return found

    def unsaved_editors(self) -> Iterator[Editor]:
        for weditor in self.editors():
            if weditor.is_modified:
                yield weditor

    def current_editor(self) -> Editor:
        return self._tabs_editor.currentWidget()

    def set_current_editor(self, weditor):
        self._tabs_editor.setCurrentWidget(weditor)

    def get_editor_by_index(self, index: int) -> Editor:
        return self._tabs_editor.widget(index)

    def get_editor_by_filename(self, filename: str) -> Editor:
        found = None
        for weditor in self._opened_editors:
            if weditor.filename== filename:
                found = weditor
                break
        return found

    def create_editor(self, file: File):
        weditor = Editor(file=file)
        index = self._tabs_editor.addTab(weditor, file.filename)
        self._tabs_editor.setCurrentIndex(index)
        self._tabs_editor.setTabToolTip(index, file.filename)
        self._opened_editors.append(weditor)

        weditor.modificationChanged.connect(self._on_modification_changed)
        weditor.lineColumnChanged.connect(self._update_line_column)

        return weditor

    @Slot(bool)
    def _on_modification_changed(self, modified):
        weditor = self.sender()
        if modified:
            text = f'● {weditor.display_name}'
        else:
            text = f'{weditor.display_name}'
        index = self._tabs_editor.currentIndex()
        self._tabs_editor.setTabText(index, text)

    @Slot(int, int)
    def _update_line_column(self, lineno, colno):
        self._lbl_line_col.setText(self._line_col_text.format(lineno, colno))


class SearchWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._parent = parent
        box = QHBoxLayout(self)
        box.setContentsMargins(0, 3, 1, 3)
        self._line_search = QLineEdit()
        box.addWidget(self._line_search)
        self.btn_find_previous = QPushButton(tr.TR_BTN_FIND_PREVIOUS)
        box.addWidget(self.btn_find_previous)
        self.btn_find_next = QPushButton(tr.TR_BTN_FIND_NEXT)
        box.addWidget(self.btn_find_next)

        self._line_search.textChanged.connect(self._execute_search)
        self.btn_find_next.clicked.connect(self._find_next)
        self.btn_find_previous.clicked.connect(self._find_previous)

    def _find_next(self):
        self._execute_search(find_next=True)

    def _find_previous(self):
        self._execute_search(backward=True)

    def _execute_search(self, find_next=False, backward=False):
        text = self.search_text
        if not text:
            return
        weditor = self._parent.editor
        weditor.find_text(text, find_next=find_next, backward=backward)

    @property
    def search_text(self):
        return self._line_search.text()
