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

from PyQt5.QtCore import Qt

from src.gui.main_window import Pireal


class LateralWidget(QSplitter):
    """
    Widget que contiene la lista de relaciones y la lista de relaciones
    del resultado de consultas
    """

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

        Pireal.load_service("lateral_widget", self)

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
