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


from PyQt5.QtWidgets import QTreeWidget
from PyQt5.QtWidgets import QSplitter
from PyQt5.QtWidgets import QTreeWidgetItem
from PyQt5.QtWidgets import QAbstractItemView
from PyQt5.QtWidgets import QMenu

from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal

from src.gui.main_window import Pireal


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
        self._relations_list = RelationList()
        self._relations_list.set_title(self.tr("Relations"))
        self.addWidget(self._relations_list)
        # Lista de relaciones del resultado de consultas
        self._results_list = RelationList()
        self._results_list.set_title(self.tr("Result"))
        self.addWidget(self._results_list)

        self._relations_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self._relations_list.customContextMenuRequested.connect(self._menu)
        Pireal.load_service("lateral_widget", self)

        self._relations_list.itemClicked.connect(
            lambda: self.relationClicked.emit(
                self._relations_list.row()))
        self._relations_list.itemSelectionChanged.connect(
            lambda: self.relationSelectionChanged.emit(
                self._relations_list.row()))
        self._results_list.itemClicked.connect(
            lambda: self.resultClicked.emit(
                self._results_list.row()))
        self._results_list.itemSelectionChanged.connect(
            lambda: self.resultSelectionChanged.emit(
                self._results_list.row()))

    def _menu(self, position):
        if not self._relations_list.selectedItems():
            return
        menu = QMenu(self)
        edit_action = menu.addAction(self.tr("Insertar Tuplas"))
        edit_action.triggered.connect(self._edit_relation)
        menu.exec_(self.mapToGlobal(position))

    def _edit_relation(self):
        rname = self._relations_list.item_text(self._relations_list.row())
        from src.gui.dialogs.edit_relation_dialog import EditRelationDialog
        dialog = EditRelationDialog(rname, self)
        dialog.sendData.connect(lambda t: self.newRowsRequested.emit(t))
        dialog.show()

    @property
    def relation_list(self):
        return self._relations_list

    @property
    def result_list(self):
        return self._results_list


class RelationList(QTreeWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.header().setObjectName("lateral")
        self.setRootIsDecorated(False)
        self.header().setDefaultAlignment(Qt.AlignHCenter)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
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
        text = self.topLevelItem(index).text(0)
        return text.split()[0].strip()

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
