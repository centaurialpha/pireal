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

from PyQt5.QtWidgets import (
    QLabel,
    QTabWidget,
    QWidget,
    QMessageBox,
    QVBoxLayout
)
from PyQt5.QtCore import pyqtSignal
from src.gui.query_editor import editor
from src.gui.main_window import Pireal
from src.core import (
    parser,
    rfile
)
from src import translations as tr


class Tab(QTabWidget):

    def __init__(self):
        super(Tab, self).__init__()
        #self.currentChanged[int].connect(self._resize)

    #def _resize(self, v):
        #width = self.size().width() / self.count() - 18
        #self.setStyleSheet("QTabBar::tab { width: %spx; }" % width)


class QueryWidget(QWidget):
    currentEditorSaved = pyqtSignal('PyQt_PyObject')

    def __init__(self):
        super(QueryWidget, self).__init__()
        self.__nrelation = 1
        self.__nquery = 1
        self._cursor_position = "Lin: %s, Col: %s"
        self._cursor_position_widget = QLabel(self._cursor_position % (0, 0))

        box = QVBoxLayout(self)
        box.setContentsMargins(0, 0, 5, 0)
        # Tabs
        self.tab = Tab()
        #self.tab.setCornerWidget(self._cursor_position_widget)
        self.tab.setTabsClosable(True)
        self.tab.setMovable(True)
        box.addWidget(self.tab)

        Pireal.load_service("query_widget", self)

        # Connections
        self.tab.tabCloseRequested[int].connect(self.removeTab)
        self.tab.tabCloseRequested[int].connect(self._check_count)

    def showEvent(self, event):
        container = Pireal.get_service("container")
        self.setMinimumHeight(container.height() / 3)

    def get_active_editor(self):
        weditor = self.tab.currentWidget()
        return weditor

    def undo(self):
        self.get_active_editor().undo()

    def redo(self):
        self.get_active_editor().redo()

    def cut(self):
        self.get_active_editor().cut()

    def copy(self):
        self.get_active_editor().copy()

    def paste(self):
        self.get_active_editor().paste()

    def _check_count(self):
        """ Hide dock if count = 0 """

        if self.tab.count() == 0:
            pireal = Pireal.get_service("pireal")
            pireal.enable_disable_query_actions(False)
            self.hide()

    def new_query(self, filename=''):
        """ Add new query editor in QTabWidget """

        # New Editor instance
        qeditor = editor.Editor()
        if filename:
            # RFile
            qfile = rfile.RFile(filename)
            content = qfile.read()
            qeditor.setPlainText(content)
            name = qfile.get_name
        else:
            qfile = rfile.RFile()
            qfile.filename = qfile.filename + str(self.__nquery)
            name = qfile.filename
            self.__nquery += 1
        qeditor.rfile = qfile
        index = self.tab.addTab(qeditor, name)
        self.tab.setTabToolTip(index, qfile.filename)
        self.tab.setCurrentIndex(index)

        qeditor.modificationChanged[bool].connect(self.__editor_modified)
        qeditor.cursorPositionChanged[int, int].connect(
            self._update_cursor_position)
        qeditor.setFocus()

    def execute_queries(self):
        import re
        # Editor instance
        editor = self.tab.currentWidget()
        # Text
        text = editor.toPlainText()
        # Ignore comments
        table = Pireal.get_service("container").table_widget
        for line in text.splitlines():
            if line.startswith('--'):
                continue
            parts = line.split('=', 1)
            parts[0] = parts[0].strip()
            if re.match(r'^[_a-zA-Z]+[_a-zA-Z0-9]*$', parts[0]):
                relation_name, line = parts
            else:
                relation_name = 'rel_{}'.format(self.__nrelation)
            try:
                expression = parser.convert_to_python(line.strip())
                rel = eval(expression, table.relations)
                self.__nrelation += 1
            except Exception as reason:

            #try:
            #except Exception as reason:
                QMessageBox.critical(self, tr.TR_QUERY_ERROR, reason.__str__())
                return
            table.add_new_table(rel, relation_name)
            table.relations[relation_name] = rel

    def __editor_modified(self, modified):
        """ This function changes the text color of the tab when
        it receives the signal *modificationChanged(bool)*

        :param modified: Boolean value sent by the signal
        """

        editor = self.tab.currentWidget()
        editor_name = editor.rfile.get_name
        index = self.tab.currentIndex()
        if modified:
            text = "{} \u2022".format(editor_name)
            self.tab.setTabText(index, text)
        else:
            self.tab.setTabText(index, editor_name)
        editor.modified = modified

    def removeTab(self, index):
        # Current editor instance
        editor = self.tab.widget(index)
        if editor.modified:
            r = self.__file_modified_message(editor.filename)
            if r == QMessageBox.Cancel:
                return
            if r == QMessageBox.Yes:
                self.currentEditorSaved.emit(editor)
            else:
                print("Saliendo...")
        self.tab.removeTab(index)

    def _update_cursor_position(self, li, co):
        self._cursor_position_widget.setText(self._cursor_position % (li, co))

    def __file_modified_message(self, filename):
        flags = QMessageBox.Yes
        flags |= QMessageBox.No
        flags |= QMessageBox.Cancel
        r = QMessageBox.information(self, tr.TR_QUERY_FILE_MODIFIED,
                                    tr.TR_QUERY_FILE_MODIFIED_MSG.format(
                                        filename), flags)
        return r

    def opened_files(self):
        for i in range(self.tab.count()):
            weditor = self.tab.widget(i)
            if weditor.modified:
                r = self.__file_modified_message(weditor.filename)
                if r == QMessageBox.Cancel:
                    return False
                if r == QMessageBox.Yes:
                    print("Guardando")
                else:
                    print("Saliendo sin guardar")
        return True

query_widget = QueryWidget()
