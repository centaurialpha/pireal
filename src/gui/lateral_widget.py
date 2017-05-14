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
    QTreeWidget,
    QTreeWidgetItem,
    QAbstractItemView,
)
from PyQt5.QtCore import Qt


class LateralWidget(QTreeWidget):

    def __init__(self, parent=None):
        super(LateralWidget, self).__init__(parent)
        self.setAlternatingRowColors(True)
        self.setHeaderLabel(self.tr("Relations"))
        self.header().setDefaultAlignment(Qt.AlignHCenter)
        # Multiple selection
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)

    def row(self):
        return self.indexOfTopLevelItem(self.currentItem())

    def add_item(self, text, ntuples):
        item = Item()
        item.name = text
        item.ntuples = str(ntuples)
        item.setText(0, item.display_name)
        item.setToolTip(0, item.display_name)
        self.addTopLevelItem(item)

    def item_text(self, index):
        """ Return text of item in the index  """

        text = self.topLevelItem(index).text(0)
        return text.split()[0].strip()

    def clear_items(self):
        """ Remove all items and selections in the view """

        self.clear()

    def update_item(self, tuple_count):
        item = self.current_item()
        item.ntuples = str(tuple_count)
        item.setText(0, item.display_name)

    def current_item(self):
        """ Returns the current item in the tree. If item is None
        returns item in the index 0 """

        item = self.currentItem()
        if item is None:
            item = self.topLevelItem(0)
        return item


class Item(QTreeWidgetItem):

    def __init__(self):
        super(Item, self).__init__()
        self.ntuples = 0
        self.name = ''

    @property
    def display_name(self):
        return self.name + " [" + self.ntuples + "]"
