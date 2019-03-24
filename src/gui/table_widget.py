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
    QTabWidget,
    QToolButton,
    QVBoxLayout,
    QStackedWidget,
    QMessageBox,
    QMenu
)
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtCore import Qt
from src.gui import (
    view,
    model,
    delegate
)
from src.core import relation
from src.gui.main_window import Pireal


class TableWidget(QSplitter):

    def __init__(self):
        super(TableWidget, self).__init__()

        # vbox = QVBoxLayout(self)
        # vbox.setContentsMargins(0, 0, 0, 0)

        self._tabs = QTabWidget()
        self._tabs.setAutoFillBackground(True)
        p = self._tabs.palette()
        p.setColor(p.Window, QColor("white"))
        self._tabs.setPalette(p)
        self._other_tab = QTabWidget()
        self._other_tab.setAutoFillBackground(True)
        self._other_tab.setPalette(p)
        self.addWidget(self._tabs)
        self.addWidget(self._other_tab)
        self.setSizes([1, 1])
        self._other_tab.hide()

        self.relations = {}

        # Stack
        self.stacked = QStackedWidget()
        self._tabs.addTab(self.stacked, "Workspace")
        self.stacked_result = QStackedWidget()
        self._tabs.addTab(self.stacked_result, self.tr("Resultados"))

        btn_split = QToolButton()
        btn_split.setToolTip(self.tr("Click para dividir la pantalla"))
        btn_split.setAutoRaise(True)
        btn_split.setIcon(QIcon(":img/split"))
        self._tabs.setCornerWidget(btn_split)
        btn_split.clicked.connect(self._split)
        btn_split = QToolButton()
        btn_split.setToolTip(self.tr("Click para juntar las pantallas"))
        btn_split.setAutoRaise(True)
        btn_split.setIcon(QIcon(":img/split"))
        btn_split.clicked.connect(self._unsplit)
        self._other_tab.setCornerWidget(btn_split)
        # self.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.customContextMenuRequested.connect(self._show_menu)

        lateral_widget = Pireal.get_service("lateral_widget")
        lateral_widget.resultClicked.connect(self._on_result_list_clicked)
        lateral_widget.resultSelectionChanged.connect(
            lambda index: self.stacked_result.setCurrentIndex(index))
        # lateral_widget.newRowsRequested.connect(self._insert_rows)

    def insert_rows(self, tuplas):
        current_view = self.current_table()
        if current_view is not None:
            model = current_view.model()
            for tupla in tuplas:
                model.insertRow(model.rowCount(), tupla)
        current_view.adjust_columns()

    def _on_result_list_clicked(self, index):
        self.stacked_result.setCurrentIndex(index)
        if not self._other_tab.isVisible():
            self._tabs.setCurrentIndex(1)

    def _unsplit(self):
        self._other_tab.hide()
        result_widget = self._other_tab.widget(0)
        self._tabs.addTab(result_widget, self.tr("Resultados"))
        self._tabs.cornerWidget().show()

    def _split(self):
        result_widget = self._tabs.widget(1)
        self._other_tab.addTab(result_widget, self.tr("Resultados"))
        self._other_tab.show()
        self.setSizes([1, 1])
        self._tabs.cornerWidget().hide()
        self.setOrientation(Qt.Horizontal)

    def _show_menu(self, position):
        menu = QMenu(self)

        if self.count() > 0:
            add_tuple_action = menu.addAction(self.tr("Agregar Tupla"))
            add_col_action = menu.addAction(self.tr("Add Column"))

            add_tuple_action.triggered.connect(self.add_tuple)
            add_col_action.triggered.connect(self.add_column)
            menu.addSeparator()

        add_relation_action = menu.addAction(self.tr("Create new Relation"))
        add_relation_action.triggered.connect(self.__new_relation)

        menu.exec_(self.mapToGlobal(position))

    def __new_relation(self):
        central_service = Pireal.get_service("central")
        central_service.create_new_relation()

    def count(self):
        return self.stacked.count()

    def remove_table(self, index):
        widget = self.stacked.widget(index)
        self.stacked.removeWidget(widget)
        del widget

    def current_table(self):
        return self.stacked.currentWidget()

    def remove_relation(self, name):
        del self.relations[name]

    def add_relation(self, name, rela):
        if self.relations.get(name, None) is None:
            self.relations[name] = rela
            return True
        return False

    def add_table(self, rela, name, table):
        """ Add new table from New Relation Dialog """

        self.add_relation(name, rela)
        self.stacked.addWidget(table)

    def add_tuple(self):
        current_view = self.current_table()
        if current_view is not None:
            model = current_view.model()
            model.insertRow(model.rowCount())

    def add_column(self):
        current_view = self.current_table()
        if current_view is not None:
            model = current_view.model()
            model.insertColumn(model.columnCount())

    def delete_tuple(self):
        current_view = self.current_table()
        if current_view is not None:
            model = current_view.model()
            selection = current_view.selectionModel()
            if selection.hasSelection():
                selection = selection.selection()
                rows = set([index.row() for index in selection.indexes()])
                rows = sorted(list(rows))
                previous = -1
                i = len(rows) - 1
                while i >= 0:
                    current = rows[i]
                    if current != previous:
                        model.removeRow(current)
                    i -= 1

    def delete_column(self):
        """ Elimina la/las columnas seleccionadas """

        current_view = self.current_table()
        if current_view is not None:
            model = current_view.model()
            selection = current_view.selectionModel()
            if selection.hasSelection():
                selection = selection.selection()
                columns = set(
                    [index.column() for index in selection.indexes()])
                columns = sorted(list(columns))
                previous = -1
                i = len(columns) - 1
                while i >= 0:
                    current = columns[i]
                    if current != previous:
                        model.removeColumn(current)
                    i -= 1

    def create_table(self, rela, editable=True):
        """ Se crea la vista y el modelo """

        _view = view.View()
        _model = model.Model(rela)
        if not editable:
            _model.editable = False
        _view.setModel(_model)
        _view.setItemDelegate(delegate.Delegate())
        _view.setHorizontalHeader(view.Header())
        return _view
