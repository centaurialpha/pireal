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

import re

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QSplitter
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QStackedWidget
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLineEdit

from PyQt5.QtCore import Qt
from PyQt5.QtCore import QSettings

from PyQt5.QtCore import pyqtSignal as Signal
from pireal.interpreter import parser
from pireal.interpreter.exceptions import (
    InvalidSyntaxError,
    MissingQuoteError,
    DuplicateRelationNameError,
    ConsumeError
)
from pireal.gui.main_window import Pireal
from pireal.gui.query_container import editor
from pireal.gui.query_container import tab_widget
from pireal.gui.lateral_widget import RelationItemType

from pireal import translations as tr
from pireal.dirs import DATA_SETTINGS


class QueryContainer(QWidget):
    saveEditor = Signal(object)

    def __init__(self, parent=None):
        super(QueryContainer, self).__init__(parent)
        self._parent = parent
        box = QVBoxLayout(self)
        self.setObjectName("query_container")
        box.setContentsMargins(0, 0, 0, 0)
        box.setSpacing(0)
        # Regex for validate variable name
        self.__validName = re.compile(r'^[a-z_]\w*$')

        self.__nquery = 1

        # Tab
        self._tabs = tab_widget.TabWidget()
        self._tabs.tabBar().setObjectName("tab_query")
        box.addWidget(self._tabs)

        self.relations = {}

        self.__hide()

        # Connections
        self._tabs.tabCloseRequested.connect(self.__hide)
        self._tabs.saveEditor.connect(self.__on_save_editor)

    def close_query(self):
        if self.currentWidget() is not None:
            self._tabs.remove_tab(self.current_index())
            self.__hide()
            pireal = Pireal.get_service('pireal')
            pireal.status_bar._line_col_label.hide()

    def set_focus_editor_tab(self, index):
        self._tabs.setCurrentIndex(index)

    def current_index(self):
        """ This property holds the index position of the current tab page """

        return self._tabs.currentIndex()

    def tab_text(self, index):
        """
        Returns the label text for the tab on the page at position index
        """

        return self._tabs.tabText(index)

    def __hide(self):
        if self.count() == 0:
            self.hide()

    def _add_operator_to_editor(self):
        data = self.sender().data()
        widget = self._tabs.currentWidget()
        tc = widget.get_editor().textCursor()
        tc.insertText(data + ' ')

    def get_unsaved_queries(self):
        weditors = []
        for index in range(self.count()):
            weditor = self._tabs.widget(index).get_editor()
            if weditor.modified:
                weditors.append(weditor)
        return weditors

    def count(self):
        return self._tabs.count()

    def add_tab(self, widget, title):
        if not self.isVisible():
            self.show()

        index = self._tabs.addTab(widget, title)
        # Focus editor
        weditor = widget.get_editor()
        weditor.setFocus()
        self._tabs.setCurrentIndex(index)
        self._tabs.setTabToolTip(index, weditor.filename)

        widget.editorModified[bool].connect(
            lambda value: self._tabs.tab_modified(self.sender(), value))

        return widget

    def is_open(self, id_):
        for index in range(self._tabs.count()):
            weditor = self._tabs.widget(index).get_editor()
            if weditor.filename == id_:
                return index
        return -1

    def currentWidget(self):
        return self._tabs.currentWidget()

    def __on_save_editor(self, editor):
        self.saveEditor.emit(editor)

    def execute_queries(self, query=''):
        """ This function executes queries """

        # If text is selected, then this text is the query,
        # otherwise the query is all text that has the editor
        editor_widget = self.currentWidget().get_editor()
        if editor_widget.textCursor().hasSelection():
            query = "\n".join(
                editor_widget.textCursor().selectedText().splitlines())
        else:
            query = editor_widget.toPlainText()
        relations = self.currentWidget().relations
        central = Pireal.get_service("central")
        table_widget = central.get_active_db().table_widget

        # Restore
        relations.clear()
        self.currentWidget().clear_results()

        editor_widget.show_run_cursor()

        # Parse query
        error = True
        try:
            result = parser.parse(query)
        except MissingQuoteError as reason:
            title = tr.TR_SYNTAX_ERROR
            text = self.parse_error(str(reason))
        except InvalidSyntaxError as reason:
            title = tr.TR_SYNTAX_ERROR
            text = self.parse_error(str(reason) + "\n" + self.tr(
                "El error comienza con " + reason.character))
        except DuplicateRelationNameError as reason:
            title = tr.TR_NAME_DUPLICATED
            text = tr.TR_RELATION_NAME_ALREADY_EXISTS.format(reason.rname)
        except ConsumeError as reason:
            title = tr.TR_SYNTAX_ERROR
            text = self.parse_error(str(reason))
        else:
            error = False
        if error:
            QMessageBox.critical(self, title, text)
            return
        relations.update(table_widget.relations)
        for relation_name, expression in result.items():
            try:
                new_relation = eval(expression, {}, relations)
            except Exception as reason:
                QMessageBox.critical(
                    self,
                    tr.TR_QUERY_ERROR,
                    self.parse_error(str(reason))
                )
                return
            relations[relation_name] = new_relation
            self.__add_table(new_relation, relation_name)

    def _highlight_error_in_editor(self, line_error, col=-1):
        weditor = self.currentWidget().get_editor()
        if weditor.hasFocus():
            weditor.highlight_error(line_error)
            if line_error != -1:
                cursor = weditor.textCursor()
                saved_col = cursor.positionInBlock()
                cursor.movePosition(cursor.Start)
                cursor.movePosition(cursor.Down, n=line_error - 1)
                if col != -1:
                    cursor.movePosition(cursor.Right, n=col)
                else:
                    cursor.movePosition(cursor.Right, n=saved_col)
                weditor.setTextCursor(cursor)

    @staticmethod
    def parse_error(text):
        """ Replaces quotes by <b></b> tag """

        return re.sub(r"\'(.*?)\'", r"<b>\1</b>", text)

    def __add_table(self, rela, rname):
        self.currentWidget().add_table(rela, rname)

    def undo(self):
        weditor = self.currentWidget().get_editor()
        if weditor.hasFocus():
            weditor.undo()

    def redo(self):
        weditor = self.currentWidget().get_editor()
        if weditor.hasFocus():
            weditor.redo()

    def cut(self):
        weditor = self.currentWidget().get_editor()
        if weditor.hasFocus():
            weditor.cut()

    def copy(self):
        weditor = self.currentWidget().get_editor()
        if weditor.hasFocus():
            weditor.copy()

    def paste(self):
        weditor = self.currentWidget().get_editor()
        if weditor.hasFocus():
            weditor.paste()

    def zoom_in(self):
        weditor = self.currentWidget().get_editor()
        if weditor.hasFocus():
            weditor.zoom_in()

    def zoom_out(self):
        weditor = self.currentWidget().get_editor()
        if weditor.hasFocus():
            weditor.zoom_out()

    def comment(self):
        weditor = self.currentWidget().get_editor()
        if weditor.hasFocus():
            weditor.comment()

    def uncomment(self):
        weditor = self.currentWidget().get_editor()
        if weditor.hasFocus():
            weditor.uncomment()

    def search(self):
        cw = self.currentWidget()
        cw.show_search_widget()

    def set_editor_focus(self):
        cw = self.currentWidget()
        if cw is not None:
            cw.hide_search_widget()


class QueryWidget(QWidget):
    editorModified = Signal(bool)
    # Editor positions
    TOP_POSITION = 0
    LEFT_POSITION = 1

    def __init__(self):
        super(QueryWidget, self).__init__()
        box = QVBoxLayout(self)
        box.setContentsMargins(0, 0, 0, 0)

        self._editor_splitter = QSplitter(Qt.Horizontal)
        self.result_splitter = QSplitter(Qt.Vertical)

        self._stack_tables = QStackedWidget()
        self.result_splitter.addWidget(self._stack_tables)

        self.relations = {}
        # Editor widget
        self._editor_widget = EditorWidget(self)
        self._editor_widget.editorModified[bool].connect(
            lambda modified: self.editorModified.emit(modified))
        self._editor_splitter.addWidget(self._editor_widget)

        box.addWidget(self._editor_splitter)

    def show_relation(self, item):
        central_widget = Pireal.get_service("central")
        table_widget = central_widget.get_active_db().table_widget
        rela = self.relations[item.name]
        dialog = QDialog(self)
        dialog.resize(700, 500)
        dialog.setWindowTitle(item.name)
        box = QVBoxLayout(dialog)
        box.setContentsMargins(5, 5, 5, 5)
        table = table_widget.create_table(rela, editable=False)
        box.addWidget(table)
        hbox = QHBoxLayout()
        btn = QPushButton('Ok')
        btn.clicked.connect(dialog.close)
        hbox.addStretch()
        hbox.addWidget(btn)
        box.addLayout(hbox)
        dialog.show()

    def save_sizes(self):
        """ Save sizes of Splitters """

        qsettings = QSettings(str(DATA_SETTINGS), QSettings.IniFormat)
        qsettings.setValue('result_splitter_query_sizes',
                           self.result_splitter.saveState())
        qsettings.setValue('editor_splitter_query_sizes',
                           self._editor_splitter.saveState())

    def get_editor(self):
        return self._editor_widget.get_editor()

    def showEvent(self, event):
        super().showEvent(event)

    def clear_results(self):
        central_widget = Pireal.get_service("central")
        lateral_widget = Pireal.get_service("lateral_widget")
        lateral_widget.clear_results()
        table_widget = central_widget.get_active_db().table_widget
        i = table_widget.stacked_result.count()
        while i >= 0:
            widget = table_widget.stacked_result.widget(i)
            table_widget.stacked_result.removeWidget(widget)
            if widget is not None:
                widget.deleteLater()
            i -= 1

    def add_table(self, rela, rname):
        central_widget = Pireal.get_service("central")
        lateral_widget = Pireal.get_service("lateral_widget")
        db = central_widget.get_active_db()
        _view = db.create_table(rela, rname, editable=False)
        table_widget = central_widget.get_active_db().table_widget
        index = table_widget.stacked_result.addWidget(_view)
        table_widget.stacked_result.setCurrentIndex(index)
        rela.name = rname
        lateral_widget.add_item(rela, RelationItemType.Result)
        table_widget._tabs.setCurrentIndex(1)

    def show_search_widget(self):
        self._editor_widget.show_search_widget()

    def hide_search_widget(self):
        self._editor_widget.hide_search_widget()


class EditorWidget(QWidget):

    editorModified = Signal(bool)

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        vbox = QVBoxLayout(self)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(0)
        # Editor
        self._editor = editor.Editor()
        vbox.addWidget(self._editor)
        # Search widget
        self._search_widget = SearchWidget(self)
        self._search_widget.hide()
        vbox.addWidget(self._search_widget)

        # Editor connections
        self._editor.modificationChanged[bool].connect(
            lambda modified: self.editorModified.emit(modified))
        self._editor.cursorPositionChanged.connect(self._on_cursor_position_changed)

    def _on_cursor_position_changed(self):
        line = self._editor.textCursor().blockNumber() + 1
        col = self._editor.textCursor().columnNumber() + 1
        pireal = Pireal.get_service('pireal')
        pireal.status_bar.update_line_and_col(line, col)

    def show_search_widget(self):
        self._search_widget.show()
        self._search_widget._line_search.setFocus()
        self._search_widget._execute_search(self._search_widget.search_text)

    def hide_search_widget(self):
        self._search_widget.hide()
        self._search_widget._line_search.clear()

    def get_editor(self):
        return self._editor


class SearchWidget(QWidget):

    def __init__(self, parent=None):
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
        weditor = self._parent._editor
        weditor.find_text(text, find_next=find_next, backward=backward)

    @property
    def search_text(self):
        return self._line_search.text()
