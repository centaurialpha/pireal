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

import itertools
from PyQt5.QtWidgets import (
    QWidget,
    QSplitter,
    QVBoxLayout,
    QListWidget,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QHeaderView,
    QAbstractItemView,
    QStackedWidget
)
from PyQt5.QtCore import Qt, QEvent, pyqtSignal
from src.gui.main_window import Pireal
from src.gui.query_container import (
    editor
)
#from src.core import parser
    #pfile,
    #parser
#)


class QueryTabContainer(QTabWidget):

    def __init__(self):
        super(QueryTabContainer, self).__init__()
        self.setTabPosition(QTabWidget.South)
        self.setTabsClosable(True)
        self.setMovable(True)

        self.tabCloseRequested[int].connect(self.removeTab)

    def add_tab(self, widget, title):
        inserted_index = self.addTab(widget, title)
        self.setCurrentIndex(inserted_index)
        # Focus editor
        widget.set_focus()
        return inserted_index

    def tab_modified(self, modified):
        weditor = self.sender().editor()
        if modified:
            text = "{} \u2022".format(weditor.name)
            self.setTabText(self.currentIndex(), text)
        else:
            self.setTabText(self.currentIndex(), weditor.name)


class QueryContainer(QWidget):

    # Signals
    editorFocused = pyqtSignal(bool)
    editorModified = pyqtSignal(bool)

    def __init__(self, parent=None):
        super(QueryContainer, self).__init__(parent)
        box = QVBoxLayout(self)
        box.setContentsMargins(0, 0, 0, 0)

        self.vsplitter = QSplitter(Qt.Vertical)
        self.hsplitter = QSplitter(Qt.Horizontal)

        self._list_tables = QListWidget()
        self.hsplitter.addWidget(self._list_tables)

        self._stack_tables = QStackedWidget()
        self.hsplitter.addWidget(self._stack_tables)

        self._weditor = editor.Editor()
        self.vsplitter.addWidget(self._weditor)
        self._weditor.installEventFilter(self)
        self._weditor.modificationChanged[bool].connect(self._editor_modified)

        self.vsplitter.addWidget(self.hsplitter)
        box.addWidget(self.vsplitter)

        # Load service
        Pireal.load_service("query_container", self)

        self._list_tables.currentRowChanged[int].connect(
            lambda index: self._stack_tables.setCurrentIndex(index))

    def set_pfile(self, pfile):
        self._weditor.pfile = pfile

    def _editor_modified(self, modified):
        self.editorModified.emit(modified)

    def editor(self):
        return self._weditor

    def eventFilter(self, obj, event):
        if event.type() == QEvent.FocusIn:
            self.editorFocused.emit(True)
        elif event.type() == QEvent.FocusOut:
            self.editorFocused.emit(False)
        return QWidget.eventFilter(self, obj, event)

    def add_editor_text(self, text):
        self._weditor.setPlainText(text)

    def text(self):
        return self._weditor.toPlainText()

    def set_focus(self):
        self._weditor.setFocus()

    def add_list_items(self, items):
        self._list_tables.addItems(items)

    def add_new_table(self, rel, name):
        table = Table()
        table.setRowCount(0)
        table.setColumnCount(0)

        data = itertools.chain([rel.fields], rel.content)

        for row_data in data:
            row = table.rowCount()
            table.setColumnCount(len(row_data))
            for col, text in enumerate(row_data):
                item = QTableWidgetItem()
                item.setText(text)
                if row == 0:
                    table.setHorizontalHeaderItem(col, item)
                else:
                    table.setItem(row - 1, col, item)
            table.insertRow(row)
        table.removeRow(table.rowCount() - 1)
        self._stack_tables.addWidget(table)
        self._stack_tables.setCurrentIndex(self._stack_tables.count() - 1)

    #def add_container(self, filename=''):
        #if filename:
            ## PFile
            #_file = pfile.PFile(filename)
            #self._weditor.setPlainText(_file.read())
        #else:
            #_file = pfile.PFile()

            #self._list_tables.addItem()

    def showEvent(self, event):
        super(QueryContainer, self).showEvent(event)
        self.hsplitter.setSizes([1, self.width() / 3])


#FIXME: a otro modulo
class Table(QTableWidget):

    def __init__(self, parent=None):
        super(Table, self).__init__(parent)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        #FIXME: Configurable
        self.verticalHeader().setVisible(False)

#tab_container = QueryTabContainer()
