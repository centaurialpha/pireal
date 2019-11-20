# -*- coding: utf-8 -*-
#
# Copyright 2015-2019 - Gabriel Acosta <acostadariogabriel@gmail.com>
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

# import logging

from PyQt5.QtWidgets import QSplitter
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QMessageBox

from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSlot as Slot

from pireal import translations as tr
from pireal.gui.lateral_widget import LateralWidget
from pireal.gui.query_container.query_container import QueryContainer
from pireal.gui.table_widget import TableWidget


__main_panel = None


def MainPanel(*args, **kwargs):
    global __main_panel
    if __main_panel is None:
        mp = _MainPanel(*args, **kwargs)
        __main_panel = mp
    return __main_panel


class _MainPanel(QSplitter):

    def __init__(self, parent=None, orientation=Qt.Horizontal):
        super().__init__(orientation, parent)
        self._parent = parent
        # La UI se divide en 3
        self._lateral_widget = LateralWidget(self)
        self._central_view = CentralView(self)
        self._query_container = QueryContainer(self)

        self._vertical_splitter = QSplitter(Qt.Vertical)
        self._vertical_splitter.addWidget(self._central_view)
        self._vertical_splitter.addWidget(self._query_container)

        self.addWidget(self._lateral_widget)
        self.addWidget(self._vertical_splitter)
        self.setSizes([70, 1])
        self._vertical_splitter.setSizes([1, 70])

        # Connections
        self._parent.pireal.themeChanged.connect(self.query_container.reload_editor_scheme)
        self._lateral_widget.relationClicked.connect(self._on_relation_clicked)
        self._lateral_widget.relationClosed[int, str].connect(self._on_relation_closed)
        self._lateral_widget.resultClicked.connect(self._on_result_clicked)

    @Slot(int, str)
    def _on_relation_closed(self, index, name):
        self._central_view.remove_relation(index, name)

    @Slot(int)
    def _on_relation_clicked(self, index):
        self._central_view.set_current_relation(index)

    @Slot(int)
    def _on_result_clicked(self, index):
        self._central_view.set_current_result(index)

    @property
    def database_modified(self):
        return self._central_view.table_widget.modified

    # FIXME: FEO
    @database_modified.setter
    def database_modified(self, value: bool):
        self._central_view.table_widget.modified = value

    @property
    def lateral_widget(self):
        return self._lateral_widget

    @property
    def central_view(self):
        return self._central_view

    @property
    def query_container(self):
        return self._query_container

    def execute_query(self):
        self._query_container.execute_query()

    def close_database(self) -> bool:
        pass
        # Check if are database modified
        # if self.database_modified:

        #     reply = QMessageBox(
        #         self, tr.TR_MSG_SAVE_CHANGES, tr.TR_MSG_SAVE_CHANGES_BODY.format())
        # check if are query modified


class CentralView(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._main_panel = parent
        vbox = QVBoxLayout(self)
        vbox.setContentsMargins(0, 0, 0, 0)
        self._tabs = QTabWidget()
        self._tabs.setTabPosition(QTabWidget.East)
        self._tabs.setMovable(True)
        vbox.addWidget(self._tabs)
        self._table_widget = TableWidget(self)
        self.add_widget(self._table_widget, 'Relations')

    @property
    def table_widget(self):
        return self._table_widget

    def add_widget(self, widget, title=''):
        """Add widget in QTabWidget"""
        self._tabs.addTab(widget, title)

    def remove_relation(self, index: int, name: str):
        reply = QMessageBox.question(
            self, tr.TR_MSG_CONFIRMATION, tr.TR_MSG_REMOVE_RELATION.format(name),
            QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.No:
            return
        self._table_widget.remove_relation(index, name)
        self._main_panel.lateral_widget.relations_view.model.remove_relation(index)

    def add_relation(self, relation_obj, relation_name):
        self._table_widget.add_relation(relation_obj, relation_name)

    def add_relation_to_results(self, relation_obj, relation_name):
        self._table_widget.add_relation_to_results(relation_obj, relation_name)

    def set_current_relation(self, index: int):
        self._table_widget.set_current_relation(index)

    def set_current_result(self, index: int):
        self._table_widget.set_current_result(index)

    def all_relations(self) -> dict:
        """Return a shallow copy of relations"""
        return {**self._table_widget.relations}
