# -*- coding: utf-8 -*-
#
# Copyright 2015 - Gabriel Acosta <acostadariogabriel@gmail.com>
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

# import re
import logging
from typing import (
    Tuple,
    List
)

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtWidgets import QHBoxLayout
# from PyQt5.QtWidgets import QSplitter
# from PyQt5.QtWidgets import QMessageBox
# from PyQt5.QtWidgets import QStackedWidget
from PyQt5.QtWidgets import QLabel
# from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLineEdit
# from PyQt5.QtWidgets import QAction
# from PyQt5.QtWidgets import QToolBar

# from PyQt5.QtCore import QSettings
# from PyQt5.QtCore import QSize

from PyQt5.QtCore import pyqtSlot as Slot
from PyQt5.QtCore import pyqtSignal as Signal

from pireal import translations as tr
from pireal.core import interpreter
from pireal.gui.query_container import editor
# from pireal.gui.query_container import tab_widget
# from pireal.core import settings
from pireal.core.pfile import File

logger = logging.getLogger(__name__)


class QueryContainer(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.hide()

        self._main_panel = parent
        vbox = QVBoxLayout(self)
        vbox.setContentsMargins(3, 0, 3, 0)
        vbox.setSpacing(0)
        self._editor_widget = EditorWidget(self)
        vbox.addWidget(self._editor_widget)
        self._search_widget = SearchWidget()
        vbox.addWidget(self._search_widget)
        self._search_widget.hide()

        self._editor_widget.allTabsClosed.connect(self.hide)

    def reload_editor_scheme(self):
        for weditor in self._editor_widget.editors():
            weditor.apply_scheme()
            weditor.reload_highlighter()

    def change_visibility(self):
        if self.isVisible():
            self._hide()
        else:
            self.show()

    def open_query(self, query_filepath=None):
        file_obj = File(query_filepath)
        if self._editor_widget.is_open(query_filepath):
            weditor = self._editor_widget.get_editor_by_filename(query_filepath)
            self._editor_widget.set_current_editor(weditor)
        else:
            weditor = self._editor_widget.create_editor(file_obj)
            if not file_obj.is_new():
                weditor.setPlainText(file_obj.read())

        if not self.isVisible():
            self.show()

    def execute_query(self):
        current_editor = self._editor_widget.current_editor()
        query = current_editor.toPlainText()
        relations = self._main_panel.central_view.all_relations()

        try:
            result = interpreter.parse(query)
        except interpreter.InvalidSyntaxError as reason:
            logger.exception('Invalid syntax error: %s', reason)
        except interpreter.MissingQuoteError as reason:
            logger.exception('Missing quote: %s', reason)
        except interpreter.ConsumeError as reason:
            logger.exception('Consume error: %s', reason)
        else:
            # Reset model
            self._main_panel.lateral_widget.clear_results()

            # FIXME: Mover a otro módulo (utils?). Quizás dependa del refactor del intérprete
            for relation_name, expression in result.items():
                new_relation = eval(expression, {}, relations)
                relations[relation_name] = new_relation
                self._main_panel.central_view.add_relation_to_results(new_relation, relation_name)
                self._main_panel.lateral_widget.add_item_to_results(
                    relation_name, new_relation.cardinality(), new_relation.degree())


class EditorWidget(QWidget):

    allTabsClosed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._opened_editors = {}
        self._new_queries_count = 1
        vbox = QVBoxLayout(self)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(0)
        self._tabs_editor = QTabWidget()
        self._tabs_editor.setTabsClosable(True)
        self._tabs_editor.setMovable(True)
        # self._tabs_editor.setDocumentMode(True)

        line_col_widget = QWidget()
        hbox = QHBoxLayout(line_col_widget)
        self._line_col_text = 'Lin: {} Col: {}'
        self._lbl_line_col = QLabel(self._line_col_text.format(0, 0))
        hbox.addWidget(self._lbl_line_col)
        self._tabs_editor.setCornerWidget(line_col_widget)
        vbox.addWidget(self._tabs_editor)

        self._tabs_editor.tabCloseRequested[int].connect(self.remove_tab)

    @Slot(int)
    def remove_tab(self, index):
        logger.debug('Removing editor tab with index: %s', index)
        weditor = self.get_editor_by_index(index)
        if weditor.modified:
            pass
        self.remove_editor(weditor)
        self._tabs_editor.removeTab(index)
        weditor.deleteLater()
        if not self._opened_editors:
            self._new_queries_count = 1
            self.allTabsClosed.emit()

    def remove_editor(self, weditor: editor.Editor):
        # FIXME:
        copy_dict = self._opened_editors.copy()
        for key in copy_dict.keys():
            if copy_dict[key] == weditor:
                logger.debug('Removing editor object (%s:%s)', weditor, key)
                del self._opened_editors[key]
                break

    def editors(self) -> Tuple[editor.Editor]:
        return self._opened_editors.values()

    def is_open(self, filepath: str) -> bool:
        try:
            self._opened_editors[filepath]
        except KeyError:
            return False
        return True

    def has_editors(self) -> bool:
        return len(self._opened_editors) > 0

    def unsaved_editors(self) -> List[editor.Editor]:
        unsaved_editors_list = []
        for weditor in self.editors():
            if weditor.modified:
                unsaved_editors_list.append(weditor)
        return unsaved_editors_list

    def current_editor(self) -> editor.Editor:
        return self._tabs_editor.currentWidget()

    def set_current_editor(self, weditor):
        self._tabs_editor.setCurrentWidget(weditor)

    def get_editor_by_index(self, index: int) -> editor.Editor:
        return self._tabs_editor.widget(index)

    def get_editor_by_filename(self, filename: str) -> editor.Editor:
        return self._opened_editors[filename]

    def create_editor(self, file_obj: File):
        weditor = editor.Editor(file_obj=file_obj)
        if file_obj.is_new():
            tab_title = 'New query({})'.format(self._new_queries_count)
            self._new_queries_count += 1
        else:
            tab_title = file_obj.display_name
        index = self._tabs_editor.addTab(weditor, tab_title)
        self._tabs_editor.setTabToolTip(index, file_obj.path)
        self._opened_editors[tab_title] = weditor

        weditor.lineColumnChanged[int, int].connect(self._update_line_column)

        weditor.setFocus()
        return weditor

    @Slot(int, int)
    def _update_line_column(self, lineno, colno):
        self._lbl_line_col.setText(self._line_col_text.format(lineno, colno))

#     @staticmethod
#     def parse_error(text):
#         """ Replaces quotes by <b></b> tag """

#         return re.sub(r"\'(.*?)\'", r"<b>\1</b>", text)


class SearchWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._parent = parent
        box = QHBoxLayout(self)
        box.setContentsMargins(0, 3, 1, 3)
        self._line_search = QLineEdit()
        box.addWidget(self._line_search)
        btn_find_previous = QPushButton(tr.TR_BTN_FIND_PREVIOUS)
        box.addWidget(btn_find_previous)
        btn_find_next = QPushButton(tr.TR_BTN_FIND_NEXT)
        box.addWidget(btn_find_next)

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
        weditor = self._parent.editor
        weditor.find_text(text, find_next=find_next, backward=backward)

    @property
    def search_text(self):
        return self._line_search.text()
