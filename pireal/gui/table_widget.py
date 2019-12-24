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

import logging

from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QSplitter
from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QStackedWidget
from PyQt5.QtWidgets import QStackedLayout

from PyQt5.QtCore import Qt

from pireal.gui.model_view_delegate import create_view

from pireal import translations as tr

logger = logging.getLogger('gui.table_widget')


class _BaseRelationWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.stack = QStackedLayout(self)

    def add(self, relation):
        pass


class RelationWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.relations = {}
        self._stack = QStackedLayout(self)

    def add(self, relation):
        view = create_view(relation)
        index = self._stack.addWidget(view)
        self._stack.setCurrentIndex(index)

    def set_current(self, index):
        self._stack.setCurrentIndex(index)


class ResultWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._stack = QStackedLayout(self)

    def add(self, relation):
        view = create_view(relation)
        index = self._stack.addWidget(view)
        self._stack.setCurrentIndex(index)

    def set_current(self, index):
        self._stack.setCurrentIndex(index)

    def clear(self):
        for _ in range(self._stack.count()):
            widget = self._stack.widget(0)
            w = self._stack.takeAt(0)
            print(w)
            self._stack.removeWidget(widget)


class TableWidget(QSplitter):

    def __init__(self, db=None, parent=None):
        super().__init__(parent)
        self.modified = False
        self._db = db
        # self._relations = {}  # relation_name: relation_object
        self._results = []
        self._tab_relations = QTabWidget()
        self._tab_relations.setAutoFillBackground(True)
        self._tab_results = QTabWidget()
        self._tab_results.setAutoFillBackground(True)
        self.addWidget(self._tab_relations)
        self.addWidget(self._tab_results)

        # Relation stack
        self._relation_stack = QStackedWidget()
        self._relation_stack.setAutoFillBackground(True)
        self._tab_relations.addTab(self._relation_stack, tr.TR_TABLE_WORKSPACE)
        # Empty widget
        self._empty_widget = QLabel('Create a new Relation')
        self._empty_widget.setAlignment(Qt.AlignCenter)
        self._relation_stack.addWidget(self._empty_widget)
        # Result stack
        self._result_stack = QStackedWidget()
        self._result_stack.setAutoFillBackground(True)
        self._tab_results.addTab(self._result_stack, tr.TR_TABLE_RESULTS)

        self.setSizes([1, 1])

    # @property
    # def relations(self) -> dict:
    #     return self._relations

    def count(self):
        return self._relation_stack.count()

    def count_results(self):
        return self._result_stack.count()

    def set_current_relation(self, index: int):
        self._relation_stack.setCurrentIndex(index)

    def set_current_result(self, index: int):
        self._result_stack.setCurrentIndex(index)

    # def add_relation(self, relation_obj, editable=True):
    #     table_view = self.create_table(relation_obj, editable=editable)
    #     self._relations[relation_obj] = table_view
    #     if self._relation_stack.widget(0) == self._empty_widget:
    #         self._relation_stack.removeWidget(self._empty_widget)
    #     self._relation_stack.addWidget(table_view)

    # def remove_relation(self, index):
    #     table_view = self._relation_stack.widget(index)
    #     model = table_view.model()
    #     del self._relations[model.relation]
    #     self._relation_stack.removeWidget(table_view)
    #     table_view.deleteLater()
    #     if self.count() == 0:
    #         self._relation_stack.addWidget(self._empty_widget)

    # def add_relation_to_results(self, relation_obj):
    #     if relation_obj.name not in self._results:
    #         table_view = self.create_table(relation_obj, editable=False)
    #         index = self._result_stack.addWidget(table_view)
    #         self._result_stack.setCurrentIndex(index)
    #         self._results.append(relation_obj.name)

    # def clear_results(self):
    #     for _ in range(self.count_results()):
    #         w = self._result_stack.widget(0)
    #         self._result_stack.removeWidget(w)
    #     self._results.clear()
