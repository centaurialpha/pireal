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
    #QListWidget,
    #QListWidgetItem,
    QTreeWidget,
    QTreeWidgetItem,
    #QMenu,
    QAbstractItemView,
    #QMessageBox
)
#from PyQt5.QtGui import QIcon
from PyQt5.QtCore import (
    Qt,
    #pyqtSignal
)
#from src.gui.main_window import Pireal


class LateralWidget(QTreeWidget):

    #itemRemoved = pyqtSignal(int)
    #showEditRelation = pyqtSignal('QModelIndex')

    def __init__(self, parent=None):
        super(LateralWidget, self).__init__(parent)
        #self.setColumnCount(1)
        self.setAlternatingRowColors(True)
        self.setHeaderLabel(self.tr("Relations"))
        self.header().setDefaultAlignment(Qt.AlignHCenter)
        # Multiple selection
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        #self.setContextMenuPolicy(Qt.CustomContextMenu)
        # Connections
        #self.customContextMenuRequested['const QPoint'].connect(
            #self.__show_context_menu)

    def row(self):
        return self.indexOfTopLevelItem(self.currentItem())

    #def __show_context_menu(self, point):
        #""" Context menu """

        #menu = QMenu()
        #edit_action = menu.addAction(tr.TR_MENU_RELATION_EDIT_RELATION)
        #remove_action = menu.addAction(QIcon(":img/remove-rel"),
                                        #tr.TR_MENU_RELATION_DELETE_RELATION)

        #remove_action.triggered.connect(self._remove)
        #edit_action.triggered.connect(self._edit)

        #menu.exec_(self.mapToGlobal(point))

    def current_text(self):
        pass
        #return self.currentItem().text()

    def add_item(self, text, ntuples):
        item = QTreeWidgetItem()
        item.setText(0, text + " [" + ntuples + "]")
        self.addTopLevelItem(item)

    #def update_item(self):
        #item = self.topLevelItem(self.row())
        #print(item.text(0))

    def item_text(self, index):
        """ Return text of item in the index  """

        text = self.topLevelItem(index).text(0)
        return text.split()[0].strip()

    def clear_items(self):
        """ Remove all items and selections in the view """

        self.clear()
