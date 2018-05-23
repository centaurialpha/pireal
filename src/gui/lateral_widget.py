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

import os

from PyQt5.QtWidgets import QTreeWidget
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QSplitter
from PyQt5.QtWidgets import QTreeWidgetItem
from PyQt5.QtWidgets import QAbstractItemView
from PyQt5.QtWidgets import QVBoxLayout

from PyQt5.QtQuickWidgets import QQuickWidget

from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QUrl

from src.gui.main_window import Pireal
from src.core import settings


class LateralWidget(QSplitter):
    """
    Widget que contiene la lista de relaciones y la lista de relaciones
    del resultado de consultas
    """

    relationClicked = pyqtSignal(int)
    relationSelectionChanged = pyqtSignal(int)

    resultClicked = pyqtSignal(int)
    resultSelectionChanged = pyqtSignal(int)

    newRowsRequested = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setOrientation(Qt.Vertical)
        # Lista de relaciones de la base de datos
        self._relations_list = RelationListQML()
        self._relations_list.set_title(self.tr("Relaciones"))
        self.addWidget(self._relations_list)
        # Lista de relaciones del resultado de consultas
        self._results_list = RelationListQML()
        self._results_list.set_title(self.tr("Resultados"))
        self.addWidget(self._results_list)

        Pireal.load_service("lateral_widget", self)

        self._relations_list.itemClicked.connect(
            lambda i: self.relationClicked.emit(i))
        #         self._relations_list.row()))
        # self._relations_list.itemSelectionChanged.connect(
        #     lambda: self.relationSelectionChanged.emit(
        #         self._relations_list.row()))
        self._results_list.itemClicked.connect(
            lambda i: self.resultClicked.emit(i))
        #         self._results_list.row()))
        # self._results_list.itemSelectionChanged.connect(
        #     lambda: self.resultSelectionChanged.emit(
        #         self._results_list.row()))

    @property
    def relation_list(self):
        return self._relations_list

    @property
    def result_list(self):
        return self._results_list


class RelationListQML(QWidget):

    itemClicked = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        vbox = QVBoxLayout(self)
        vbox.setContentsMargins(0, 0, 0, 0)
        view = QQuickWidget()
        qml = os.path.join(settings.QML_PATH, "ListRelation.qml")
        view.setSource(QUrl.fromLocalFile(qml))
        view.setResizeMode(QQuickWidget.SizeRootObjectToView)
        vbox.addWidget(view)

        self._root = view.rootObject()

        self._root.itemClicked.connect(
            lambda i: self.itemClicked.emit(i))

    def set_title(self, title):
        self._root.setTitle(title)

    def add_item(self, name, card, deg):
        self._root.addItem(name, card, deg)

    def clear_items(self):
        self._root.clear()

    def current_item(self):
        item = self._root.currentItem()
        name, index = None, None
        if item is not None:
            name, index = item.toVariant().values()
        return index, name

    def has_item(self):
        return self._root.hasItem()

    def current_text(self):
        return self._root.currentItemText()

    def current_index(self):
        return self._root.currentIndex()

    def update_cardinality(self, new_cardinality):
        self._root.setCardinality(new_cardinality)


class RelationList(QTreeWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.header().setObjectName("lateral")
        self.setRootIsDecorated(False)
        self.header().setDefaultAlignment(Qt.AlignHCenter)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setFrameShape(QTreeWidget.NoFrame)
        self.setFrameShadow(QTreeWidget.Plain)
        self.setAnimated(True)

    def select(self, fila):
        item = self.topLevelItem(fila)
        item.setSelected(True)

    def select_last(self):
        for i in range(self.topLevelItemCount()):
            item = self.topLevelItem(i)
            item.setSelected(False)
        self.select(self.topLevelItemCount() - 1)

    def select_first(self):
        self.select(0)

    def set_title(self, title):
        self.setHeaderLabel(title)

    def row(self):
        return self.indexOfTopLevelItem(self.currentItem())

    def add_item(self, text, numero_tuplas):
        """Agrega un item"""
        item = Item(text, str(numero_tuplas))
        item.setText(0, item.display_name)
        item.setToolTip(0, item.display_name)
        self.addTopLevelItem(item)

    def item_text(self, index):
        """Retorna el texto del item en el indice pasado"""
        item = self.topLevelItem(index)
        if item is None:
            item = self.topLevelItem(self.selectedIndexes()[0].row())
        text = item.text(0)
        return text.split()[0].strip()

    def remove_item(self, index):
        if index == -1:
            index = 0  # primer elemento
        self.takeTopLevelItem(index)

    def clear_items(self):
        """Elimina todos los items"""

        self.clear()

    def update_item(self, tuplas_count):
        item = self.current_item()
        item.ntuples = str(tuplas_count)
        item.setText(0, item.display_name)

    def current_item(self):
        """ Returns the current item in the tree. If item is None
        returns item in the index 0 """

        item = self.currentItem()
        if item is None:
            item = self.topLevelItem(0)
        return item


class Item(QTreeWidgetItem):

    def __init__(self, text, ntuplas):
        super(Item, self).__init__()
        self.name = text
        self.ntuples = ntuplas

    @property
    def display_name(self):
        return self.name + " [" + self.ntuples + "]"
