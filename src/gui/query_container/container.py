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
    QWidget,
    QSplitter,
    QVBoxLayout,
    QListWidget,
    QTableWidget
)
from PyQt5.QtCore import Qt
from src.gui.main_window import Pireal
from src.gui.query_container import (
    editor
)
from src.core import (
    pfile,
    parser
)


class QueryContainer(QWidget):

    def __init__(self, parent=None):
        super(QueryContainer, self).__init__(parent)
        box = QVBoxLayout(self)
        box.setContentsMargins(0, 0, 0, 0)

        self.vsplitter = QSplitter(Qt.Vertical)
        self.hsplitter = QSplitter(Qt.Horizontal)

        self._list_tables = QListWidget()
        self.hsplitter.addWidget(self._list_tables)

        self._tables = QTableWidget()
        self.hsplitter.addWidget(self._tables)

        self._weditor = editor.Editor()
        self.vsplitter.addWidget(self._weditor)

        self.vsplitter.addWidget(self.hsplitter)
        box.addWidget(self.vsplitter)

        # Load service
        Pireal.load_service("query_container", self)

    def add_container(self, filename=''):
        if filename:
            # PFile
            _file = pfile.PFile(filename)
            self._weditor.setPlainText(_file.read())
        else:
            _file = pfile.PFile()

    def execute_queries(self):
        text = self._weditor.toPlainText()
        mdi = Pireal.get_service("mdi")
        widgets = mdi.subWindowList(1)
        table_widget = widgets[0].widget().table_widget
        # Ignore comments
        for line in text.splitlines():
            if line.startswith('--'):
                continue
            expression = parser.convert_to_python(line.strip())
            relation = eval(expression, table_widget.relations)
            #self._list_tables.addItem()

    def showEvent(self, event):
        QSplitter.showEvent(self, event)
        self.hsplitter.setSizes([1, self.width() / 3])


container = QueryContainer()
