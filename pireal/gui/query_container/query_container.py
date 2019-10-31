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
from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QSplitter
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QStackedWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QToolBar

from PyQt5.QtCore import Qt
from PyQt5.QtCore import QSettings
from PyQt5.QtCore import QSize

from PyQt5.QtCore import pyqtSignal as Signal

from pireal import translations as tr
from pireal.core.interpreter import parser
from pireal.core.interpreter.exceptions import (
    InvalidSyntaxError,
    MissingQuoteError,
    DuplicateRelationNameError,
    ConsumeError
)
from pireal.gui.query_container import editor
from pireal.gui.query_container import tab_widget
from pireal.core import settings


class QueryContainer(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        vbox = QVBoxLayout(self)
        self._editor_widget = EditorWidget(self)
        vbox.addWidget(self._editor_widget)
        self._search_widget = SearchWidget()
        vbox.addWidget(self._search_widget)

    def change_visibility(self):
        if self.isVisible():
            self._hide()
        else:
            self.show()


class EditorWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._opened_editors = {}
        vbox = QVBoxLayout(self)
        vbox.setContentsMargins(0, 0, 0, 0)
        self._tabs_editor = QTabWidget()
        vbox.addWidget(self._tabs_editor)

    def is_open(self, filepath) -> bool:
        try:
            self._opened_editors[filepath]
        except KeyError:
            return False
        return True

    def current_editor(self):
        return self._tabs_editor.currentWidget()

    def create_editor(self, title=''):
        weditor = editor.Editor()
        self._tabs_editor.addTab(weditor, title)
        return weditor

# class QueryContainer(QWidget):
#     saveEditor = Signal(object)

#     def __init__(self, parent=None):
#         super(QueryContainer, self).__init__(parent)
#         self.db_container = parent
#         box = QVBoxLayout(self)
#         self.setObjectName("query_container")
#         box.setContentsMargins(0, 10, 0, 0)
#         box.setSpacing(0)

#         self.__nquery = 1

#         # Tab
#         self._tabs = tab_widget.TabWidget()
#         self._tabs.tabBar().setObjectName("tab_query")
#         self._tabs.setAutoFillBackground(True)
#         p = self._tabs.palette()
#         p.setColor(p.Window, Qt.white)
#         self._tabs.setPalette(p)
#         box.addWidget(self._tabs)

#         self.relations = {}

#         # self._hide()

#         # Connections
#         # self._tabs.tabCloseRequested.connect(self.__hide)
#         self._tabs.saveEditor.connect(self.__on_save_editor)

#     def set_focus_editor_tab(self, index):
#         self._tabs.setCurrentIndex(index)

#     def current_index(self):
#         """ This property holds the index position of the current tab page """

#         return self._tabs.currentIndex()

#     def tab_text(self, index):
#         """
#         Returns the label text for the tab on the page at position index
#         """

#         return self._tabs.tabText(index)

#     def change_visibility(self):
#         if self.isVisible():
#             self._hide()
#         else:
#             self.show()

#     def _hide(self):
#         if self.count() == 0:
#             self.hide()
#             # Disable query actions
#             # FIXME: mejorar esto, mover a otro lado?
#             pireal = self.db_container.central.pireal
#             pireal.set_enabled_query_actions(False)
#             pireal.set_enabled_editor_actions(False)

#     def _add_operator_to_editor(self):
#         data = self.sender().data()
#         widget = self._tabs.currentWidget()
#         tc = widget.get_editor().textCursor()
#         tc.insertText(data + ' ')

#     def get_unsaved_queries(self):
#         weditors = []
#         for index in range(self.count()):
#             weditor = self._tabs.widget(index).get_editor()
#             if weditor.modified:
#                 weditors.append(weditor)
#         return weditors

#     def count(self):
#         return self._tabs.count()

#     def add_tab(self, widget, title):
#         if not self.isVisible():
#             self.show()

#         index = self._tabs.addTab(widget, title)
#         # Focus editor
#         weditor = widget.get_editor()
#         weditor.setFocus()
#         self._tabs.setCurrentIndex(index)
#         self._tabs.setTabToolTip(index, weditor.filename)

#         widget.editorModified[bool].connect(
#             lambda value: self._tabs.tab_modified(self.sender(), value))

#         return widget

#     def is_open(self, id_):
#         for index in range(self._tabs.count()):
#             weditor = self._tabs.widget(index).get_editor()
#             if weditor.filename == id_:
#                 return index
#         return -1

#     def currentWidget(self):
#         return self._tabs.currentWidget()

#     def __on_save_editor(self, editor):
#         self.saveEditor.emit(editor)

#     def execute_queries(self, query=''):
#         """ This function executes queries """

#         # If text is selected, then this text is the query,
#         # otherwise the query is all text that has the editor
#         editor_widget = self.currentWidget().get_editor()
#         if editor_widget.textCursor().hasSelection():
#             query = "\n".join(
#                 editor_widget.textCursor().selectedText().splitlines())
#         else:
#             query = editor_widget.toPlainText()
#         relations = self.currentWidget().relations
#         table_widget = self.db_container.table_widget
#         # central = Pireal.get_service("central")
#         # table_widget = central.get_active_db().table_widget

#         # Restore
#         relations.clear()
#         self.currentWidget().clear_results()

#         editor_widget.show_run_cursor()

#         # Parse query
#         error = True
#         try:
#             result = parser.parse(query)
#         except MissingQuoteError as reason:
#             title = tr.TR_SYNTAX_ERROR
#             text = self.parse_error(str(reason))
#         except InvalidSyntaxError as reason:
#             title = tr.TR_SYNTAX_ERROR
#             text = self.parse_error(str(reason) + "\n" + self.tr(
#                 "El error comienza con " + reason.character))
#         except DuplicateRelationNameError as reason:
#             title = tr.TR_NAME_DUPLICATED
#             text = tr.TR_RELATION_NAME_ALREADY_EXISTS.format(reason.rname)
#         except ConsumeError as reason:
#             title = tr.TR_SYNTAX_ERROR
#             text = self.parse_error(str(reason))
#         else:
#             error = False
#         if error:
#             QMessageBox.critical(self, title, text)
#             return
#         relations.update(table_widget.relations)
#         for relation_name, expression in result.items():
#             try:
#                 new_relation = eval(expression, {}, relations)
#             except Exception as reason:
#                 QMessageBox.critical(
#                     self,
#                     tr.TR_QUERY_ERROR,
#                     self.parse_error(str(reason))
#                 )
#                 return
#             relations[relation_name] = new_relation
#             self.__add_table(new_relation, relation_name)

#     def _highlight_error_in_editor(self, line_error, col=-1):
#         weditor = self.currentWidget().get_editor()
#         if weditor.hasFocus():
#             weditor.highlight_error(line_error)
#             if line_error != -1:
#                 cursor = weditor.textCursor()
#                 saved_col = cursor.positionInBlock()
#                 cursor.movePosition(cursor.Start)
#                 cursor.movePosition(cursor.Down, n=line_error - 1)
#                 if col != -1:
#                     cursor.movePosition(cursor.Right, n=col)
#                 else:
#                     cursor.movePosition(cursor.Right, n=saved_col)
#                 weditor.setTextCursor(cursor)

#     @staticmethod
#     def parse_error(text):
#         """ Replaces quotes by <b></b> tag """

#         return re.sub(r"\'(.*?)\'", r"<b>\1</b>", text)

#     def __add_table(self, rela, rname):
#         self.currentWidget().add_table(rela, rname)

#     def undo(self):
#         weditor = self.currentWidget().get_editor()
#         if weditor.hasFocus():
#             weditor.undo()

#     def redo(self):
#         weditor = self.currentWidget().get_editor()
#         if weditor.hasFocus():
#             weditor.redo()

#     def cut(self):
#         weditor = self.currentWidget().get_editor()
#         if weditor.hasFocus():
#             weditor.cut()

#     def copy(self):
#         weditor = self.currentWidget().get_editor()
#         if weditor.hasFocus():
#             weditor.copy()

#     def paste(self):
#         weditor = self.currentWidget().get_editor()
#         if weditor.hasFocus():
#             weditor.paste()

#     def comment(self):
#         weditor = self.currentWidget().get_editor()
#         if weditor.hasFocus():
#             weditor.comment()

#     def uncomment(self):
#         weditor = self.currentWidget().get_editor()
#         if weditor.hasFocus():
#             weditor.uncomment()

#     def search(self):
#         cw = self.currentWidget()
#         cw.show_search_widget()

#     def set_editor_focus(self):
#         cw = self.currentWidget()
#         if cw is not None:
#             cw.hide_search_widget()

# class QueryWidget(QWidget):
#     editorModified = Signal(bool)
#     # Editor positions
#     TOP_POSITION = 0
#     LEFT_POSITION = 1

#     def __init__(self, parent=None):
#         super(QueryWidget, self).__init__(parent)
#         self.db_container = parent
#         box = QVBoxLayout(self)
#         box.setContentsMargins(0, 0, 0, 0)

#         self._editor_splitter = QSplitter(Qt.Horizontal)
#         self.result_splitter = QSplitter(Qt.Vertical)

#         self._stack_tables = QStackedWidget()
#         self.result_splitter.addWidget(self._stack_tables)

#         self.relations = {}
#         # Editor widget
#         self._editor_widget = EditorWidget(self)
#         self._editor_widget.editorModified[bool].connect(
#             lambda modified: self.editorModified.emit(modified))
#         self._editor_splitter.addWidget(self._editor_widget)

#         box.addWidget(self._editor_splitter)

#     def show_relation(self, item):
#         # central_widget = Pireal.get_service("central")
#         central_widget = self.db_container.central
#         table_widget = central_widget.get_active_db().table_widget
#         rela = self.relations[item.name]
#         dialog = QDialog(self)
#         dialog.resize(700, 500)
#         dialog.setWindowTitle(item.name)
#         box = QVBoxLayout(dialog)
#         box.setContentsMargins(5, 5, 5, 5)
#         table = table_widget.create_table(rela, editable=False)
#         box.addWidget(table)
#         hbox = QHBoxLayout()
#         btn = QPushButton(tr.TR_MSG_OK)
#         btn.clicked.connect(dialog.close)
#         hbox.addStretch()
#         hbox.addWidget(btn)
#         box.addLayout(hbox)
#         dialog.show()

#     def save_sizes(self):
#         """ Save sizes of Splitters """

#         qsettings = QSettings(settings.SETTINGS_PATH, QSettings.IniFormat)
#         qsettings.setValue('result_splitter_query_sizes',
#                            self.result_splitter.saveState())
#         qsettings.setValue('editor_splitter_query_sizes',
#                            self._editor_splitter.saveState())

#     def get_editor(self):
#         return self._editor_widget.get_editor()

#     def showEvent(self, event):
#         super().showEvent(event)
#         # self.result_splitter.setSizes([1, self._result_list.width() * 0.1])

#     def clear_results(self):
#         # FIXME:
#         # central_widget = Pireal.get_service("central")
#         # lateral_widget = Pireal.get_service("lateral_widget")
#         central_widget = self.db_container.central
#         lateral_widget = self.db_container.lateral_widget
#         lateral_widget.result_list.clear_items()
#         table_widget = central_widget.get_active_db().table_widget
#         i = table_widget.stacked_result.count()
#         # i = self._stack_tables.count()
#         while i >= 0:
#             # widget = self._stack_tables.widget(i)
#             widget = table_widget.stacked_result.widget(i)
#             # self._stack_tables.removeWidget(widget)
#             table_widget.stacked_result.removeWidget(widget)
#             if widget is not None:
#                 widget.deleteLater()
#             i -= 1

#     def add_table(self, rela, rname):
#         # FIXME:
#         # central_widget = Pireal.get_service("central")
#         # lateral_widget = Pireal.get_service("lateral_widget")
#         central_widget = self.db_container.central
#         lateral_widget = self.db_container.lateral_widget
#         db = self.db_container
#         _view = db.create_table(rela, rname, editable=False)
#         table_widget = central_widget.get_active_db().table_widget
#         index = table_widget.stacked_result.addWidget(_view)
#         table_widget.stacked_result.setCurrentIndex(index)
#         lateral_widget.result_list.add_item(
#             rname, rela.cardinality(), rela.degree())
#         # lateral_widget.result_list.select_last()
#         table_widget._tabs.setCurrentIndex(1)

#     def show_search_widget(self):
#         self._editor_widget.show_search_widget()

#     def hide_search_widget(self):
#         self._editor_widget.hide_search_widget()


# class EditorWidget(QWidget):

#     TOOLBAR_ITEMS = [
#         'save_query',
#         '',
#         'undo_action',
#         'redo_action',
#         'cut_action',
#         'paste_action',
#     ]

#     editorModified = Signal(bool)

#     def __init__(self, parent=None):
#         QWidget.__init__(self, parent)
#         self.query_widget = parent
#         vbox = QVBoxLayout(self)
#         vbox.setContentsMargins(0, 0, 0, 0)
#         vbox.setSpacing(0)
#         self.setStyleSheet("outline: none")
#         hbox = QHBoxLayout()
#         # Position
#         self._column_str = "Col: {}"
#         self._column_lbl = QLabel(self._column_str.format(0))
#         # Toolbar
#         self._toolbar = QToolBar(self)
#         self._toolbar.setIconSize(QSize(16, 16))

#         pireal = self.query_widget.db_container.central.pireal
#         for action in self.TOOLBAR_ITEMS:
#             qaction = pireal.get_action(action)
#             if qaction is not None:
#                 self._toolbar.addAction(qaction)
#             else:
#                 self._toolbar.addSeparator()

#         vbox.addLayout(hbox)
#         # Editor
#         self._editor = editor.Editor()
#         vbox.addWidget(self._editor)
#         # Search widget
#         self._search_widget = SearchWidget(self)
#         self._search_widget.hide()
#         vbox.addWidget(self._search_widget)

#         # Editor connections
#         self._editor.customContextMenuRequested.connect(
#             self.__show_context_menu)
#         self._editor.modificationChanged[bool].connect(
#             lambda modified: self.editorModified.emit(modified))

#     @property
#     def editor(self):
#         return self._editor

#     def show_search_widget(self):
#         self._search_widget.show()
#         self._search_widget._line_search.setFocus()
#         self._search_widget._execute_search(self._search_widget.search_text)

#     def hide_search_widget(self):
#         self._search_widget.hide()
#         self._search_widget._line_search.clear()

#     def _update_column_label(self):
#         col = str(self._editor.textCursor().columnNumber() + 1)
#         self._column_lbl.setText(self._column_str.format(col))

#     def get_editor(self):
#         return self._editor

#     def __show_context_menu(self, point):
#         popup_menu = self._editor.createStandardContextMenu()

#         undock_editor = QAction(tr.TR_UNDOCK, self)
#         popup_menu.insertAction(popup_menu.actions()[0],
#                                 undock_editor)
#         popup_menu.insertSeparator(popup_menu.actions()[1])
#         undock_editor.triggered.connect(self.__undock_editor)

#         popup_menu.exec_(self.mapToGlobal(point))

#     def __undock_editor(self):
#         new_editor = editor.Editor()
#         actual_doc = self._editor.document()
#         new_editor.setDocument(actual_doc)
#         new_editor.resize(900, 400)
#         # Set text cursor
#         tc = self._editor.textCursor()
#         new_editor.setTextCursor(tc)
#         # Set title
#         # db = Pireal.get_service("central").get_active_db()
#         db = self.query_widget.db_container
#         qc = db.query_container
#         new_editor.setWindowTitle(qc.tab_text(qc.current_index()))
#         new_editor.show()

#     def __on_undo_available(self, value):
#         """ Change state of undo action """
#         # TODO:
#         # pireal = self.query_widget.db_container.central.pireal
#         # action = pireal.get_action("undo_action")
#         # action.setEnabled(value)
#         pass

#     def __on_redo_available(self, value):
#         """ Change state of redo action """
#         # TODO:
#         # pireal = self.query_widget.db_container.central.pireal
#         # action = pireal.get_action("redo_action")
#         # action.setEnabled(value)
#         pass

#     def __on_copy_available(self, value):
#         """ Change states of cut and copy action """

#         # TODO:
#         # cut_action = Pireal.get_action("cut_action")
#         # cut_action.setEnabled(value)
#         # copy_action = Pireal.get_action("copy_action")
#         # copy_action.setEnabled(value)
#         pass


class SearchWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._parent = parent
        box = QHBoxLayout(self)
        # box.setContentsMargins(0, 3, 0, 3)
        # box.setSpacing(0)
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