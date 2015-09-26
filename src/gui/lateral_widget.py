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
    QVBoxLayout,
    QWidget,
    QListWidget,
    QListWidgetItem,
    QMenu
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from src.gui.main_window import Pireal


class LateralWidget(QWidget):

    def __init__(self):
        super(LateralWidget, self).__init__()
        vbox = QVBoxLayout(self)
        vbox.setContentsMargins(0, 0, 0, 0)
        self._list_widget = QListWidget()

        vbox.addWidget(self._list_widget)

        Pireal.load_service("lateral", self)

        self._list_widget.setContextMenuPolicy(Qt.CustomContextMenu)

        self._list_widget.currentRowChanged[int].connect(self._change_item)
        self._list_widget.customContextMenuRequested['const QPoint'].connect(
            self.__show_context_menu)

    def __show_context_menu(self, point):
        """ Context menu """

        menu = QMenu()
        remove_table_act = menu.addAction(QIcon(":img/remove-rel"),
                                          self.tr("Eliminar Relación"))

        remove_table_act.triggered.connect(self.remove_table)

        menu.exec_(self.mapToGlobal(point))

    def _change_item(self, index):
        table = Pireal.get_service("container").table_widget
        table.stacked.setCurrentIndex(index)

    def add_item_list(self, items):
        if not self.isVisible():
            self.show()
        for i in items:
            item = QListWidgetItem(i)
            item.setTextAlignment(Qt.AlignHCenter)
            self._list_widget.addItem(item)

    def remove_table(self):
        container = Pireal.get_service("container")
        container.remove_relation()

    def clear_items(self):
        """ Remove all items and selections in the view """

        self._list_widget.clear()

    def get_relation_name(self):
        """ Returns the text of the item """

        item = self._list_widget.currentItem()
        if item is None:
            return False
        return item.text()

    def current_index(self):
        """ Returns the current index """

        return self._list_widget.currentRow()

    def remove_item(self, index):
        """ Removes the item from the given index in the list widget"""

        self._list_widget.takeItem(index)

lateral = LateralWidget()
