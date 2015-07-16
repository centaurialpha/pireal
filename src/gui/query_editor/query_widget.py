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

from PyQt4.QtGui import (
    #QDockWidget,
    QTabWidget,
    QWidget,
    QColor,
    QMessageBox,
    QVBoxLayout
)
from PyQt4.QtCore import (
    SIGNAL,
    Qt
)
from src.gui.query_editor import editor
from src.gui.main_window import Pireal
from src.core import (
    parser,
    rfile
)


class QueryWidget(QWidget):

    def __init__(self):
        super(QueryWidget, self).__init__()
        self.__nrelation = 1
        self.__nquery = 1
        box = QVBoxLayout(self)
        # Tabs
        self.tab = QTabWidget()
        self.tab.setTabsClosable(True)
        self.tab.setMovable(True)
        box.addWidget(self.tab)

        Pireal.load_service("query_widget", self)

        # Connections
        self.connect(self.tab, SIGNAL("tabCloseRequested(int)"),
                     self.removeTab)
        self.connect(self.tab, SIGNAL("tabCloseRequested(int)"),
                     self._check_count)

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
            name = qfile.filename + str(self.__nquery)
            self.__nquery += 1
        qeditor.rfile = qfile
        index = self.tab.addTab(qeditor, name)
        self.tab.setCurrentIndex(index)

        self.connect(qeditor, SIGNAL("modificationChanged(bool)"),
                     self.__editor_modified)

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
                self.__nrelation += 1
            expression = parser.convert_to_python(line.strip())
            try:
                rel = eval(expression, table.relations)
            except Exception as reason:
                QMessageBox.critical(self, self.tr("Error en consulta"),
                                     reason.__str__())
                return
            table.add_new_table(rel, relation_name)
            table.relations[relation_name] = rel

    def __editor_modified(self, modified):
        """ This function changes the text color of the tab when
        it receives the signal *modificationChanged(bool)*

        :param modified: Boolean value sent by the signal
        """

        if modified:
            self.tab.tabBar().setTabTextColor(self.tab.currentIndex(),
                                              QColor(Qt.red))
        else:
            self.tab.tabBar().setTabTextColor(self.tab.currentIndex(),
                                              QColor(Qt.black))
        editor = self.tab.currentWidget()
        editor.modified = modified

    def removeTab(self, index):
        # Current editor instance
        editor = self.tab.widget(index)
        #editor = self.tab.currentWidget()
        if editor.modified:
            flags = QMessageBox.Yes
            flags |= QMessageBox.No
            flags |= QMessageBox.Cancel
            r = QMessageBox.information(self, self.tr("Archivo modificado"),
                                        self.tr("El archivo <b>{}</b> "
                                                "tiene cambios sin guardar. "
                                                "Quieres guardarlos?").format(
                                                    editor.filename), flags)
            if r == QMessageBox.Cancel:
                return
            if r == QMessageBox.Yes:
                print("Guardando")
            else:
                print("Saliendo...")
        self.tab.removeTab(index)

query_widget = QueryWidget()
