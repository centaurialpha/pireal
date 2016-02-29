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

from collections import OrderedDict

from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QToolBar,
    QSplitter,
    QStackedWidget,
    QMessageBox,
    #QTableWidgetItem,
)
from PyQt5.QtGui import (
    QStandardItem,
    QIcon
)
from PyQt5.QtCore import (
    Qt,
    QSize,
    pyqtSignal,
    QSettings
)

from src.core.logger import PirealLogger
from src.core import parser
from src.gui import (
    custom_table,
    list_widget,
    fader_widget
)
from src.gui.main_window import Pireal
#from src.gui import lateral_widget
from src.gui.query_container import (
    editor,
    tab_widget
)
from src.core import settings

# Logger
logger = PirealLogger(__name__)
DEBUG = logger.debug
ERROR = logger.error

ITEMS_TOOLBAR_OPERATORS = OrderedDict(
    [('select', ('Selection', 0x3c3)),
    ('project', ('Projection', 0x3a0)),
    ('njoin', ('Natural Join', 0x22c8)),
    ('product', ('Product', 0x58)),
    ('intersect', ('Intersection', 0x2229)),
    ('union', ('Union', 0x222a)),
    ('difference', ('Difference', 0x2d))]
)


class QueryContainer(QWidget):
    saveEditor = pyqtSignal('PyQt_PyObject')

    def __init__(self):
        super(QueryContainer, self).__init__()
        box = QVBoxLayout(self)
        box.setContentsMargins(0, 0, 0, 0)

        # Regex for validate variable name
        self.__validName = re.compile(r'^[a-z_]\w*$')

        self.__nquery = 1
        # Toolbar
        #toolbar = self.__load_toolbar()
        #box.addWidget(toolbar)

        # Tab
        self._tabs = tab_widget.TabWidget()
        box.addWidget(self._tabs)

        self.__hide()

        # Connections
        self._tabs.tabCloseRequested.connect(self.__hide)
        self._tabs.saveEditor['PyQt_PyObject'].connect(
            self.__on_save_editor)

    def __load_toolbar(self):
        toolbar = QToolBar(self)
        toolbar.setIconSize(QSize(14, 14))

        for key, value in ITEMS_TOOLBAR_OPERATORS.items():
            tooltip, action = value
            qaction = toolbar.addAction(chr(action))
            qaction.setIcon(QIcon(":img/{}".format(key)))
            qaction.setData(key)
            qaction.triggered.connect(self._add_operator_to_editor)
            qaction.setToolTip(tooltip)

        return toolbar

    def set_focus_editor_tab(self, index):
        self._tabs.setCurrentIndex(index)

    def __hide(self):
        if self.count() == 0:
            self.hide()
            # Disable query actions
            pireal = Pireal.get_service("pireal")
            pireal.set_enabled_query_actions(False)

    def _add_operator_to_editor(self):
        data = self.sender().data()
        widget = self._tabs.currentWidget()
        tc = widget.get_editor().textCursor()
        tc.insertText(data + ' ')

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

    def execute_queries(self):
        # Get the text from editor
        weditor = self.currentWidget().get_editor()
        text = weditor.toPlainText()

        central = Pireal.get_service("central")
        table_widget = central.get_active_db().table_widget

        # Ignore comments
        for line in text.splitlines():
            if line.startswith('--'):
                continue

            parts = line.split('=', 1)
            if len(parts) == 2 and self.__validName.match(parts[0].strip()):
                relation_name = parts[0].strip()
                line = parts[1].strip()
            else:
                relation_name = "query_{}".format(self.__nquery)
                self.__nquery += 1
            print(line)
            try:
                expression = parser.convert_to_python(line)
                rela = eval(expression, table_widget.relations)
            except Exception as reason:
                QMessageBox.critical(self,
                                     self.tr("Query Error"),
                                     reason.__str__())

            if table_widget.add_relation(relation_name, rela):
                self.__add_table(rela, relation_name)

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


class QueryWidget(QWidget):
    editorModified = pyqtSignal(bool)

    def __init__(self):
        super(QueryWidget, self).__init__()
        box = QVBoxLayout(self)
        box.setContentsMargins(0, 0, 0, 0)

        self._vsplitter = QSplitter(Qt.Vertical)
        self._hsplitter = QSplitter(Qt.Horizontal)

        self._result_list = list_widget.LateralWidget()
        self._hsplitter.addWidget(self._result_list)

        self._stack_tables = StackedWidget()
        self._hsplitter.addWidget(self._stack_tables)

        self._query_editor = editor.Editor()
        self._query_editor.modificationChanged[bool].connect(
            self.__editor_modified)
        self._vsplitter.addWidget(self._query_editor)

        self._vsplitter.addWidget(self._hsplitter)
        box.addWidget(self._vsplitter)

        # Connections
        self._result_list.currentRowChanged[int].connect(
            lambda index: self._stack_tables.show_display(index))

    def save_sizes(self):
        """ Save sizes of Splitters """

        qsettings = QSettings(settings.SETTINGS_PATH, QSettings.IniFormat)
        qsettings.setValue('hsplitter_query_sizes',
                           self._hsplitter.saveState())
        qsettings.setValue('vsplitter_query_sizes',
                           self._vsplitter.saveState())

    def get_editor(self):
        return self._query_editor

    def __editor_modified(self, modified):
        self.editorModified.emit(modified)

    def showEvent(self, event):
        super(QueryWidget, self).showEvent(event)
        self._hsplitter.setSizes([1, self.width() / 3])

    def add_table(self, rela, rname):
        wtable = custom_table.Table()

        #wtable.setColumnCount(len(rela.fields))
        wtable.model().setHorizontalHeaderLabels(rela.fields)

        for data in rela.content:
            nrow = wtable.model().rowCount()
            #wtable.insertRow(nrow)
            for col, text in enumerate(data):
                item = QStandardItem(text)
                wtable.model().setItem(nrow, col, item)

        index = self._stack_tables.addWidget(wtable)
        self._stack_tables.setCurrentIndex(index)

        self._result_list.addItem(rname)


class StackedWidget(QStackedWidget):

    def setCurrentIndex(self, index):
        self.fader_widget = fader_widget.FaderWidget(self.currentWidget(),
                                                     self.widget(index))
        QStackedWidget.setCurrentIndex(self, index)

    def show_display(self, index):
        self.setCurrentIndex(index)