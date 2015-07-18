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

from PyQt4.QtGui import (
    QDockWidget,
    QListWidget,
    QListWidgetItem
)
from PyQt4.QtCore import (
    Qt,
    SIGNAL
)
from src.gui.main_window import Pireal


class LateralWidget(QDockWidget):

    def __init__(self):
        super(LateralWidget, self).__init__()
        self._list_widget = QListWidget()
        self.setWidget(self._list_widget)

        Pireal.load_service("lateral", self)

        self.connect(self._list_widget, SIGNAL("currentRowChanged(int)"),
                     self._change_item)

    def _change_item(self, index):
        table = Pireal.get_service("container").table_widget
        table.stacked.setCurrentIndex(index)

    def add_item_list(self, items):
        for i in items:
            item = QListWidgetItem(i)
            item.setTextAlignment(Qt.AlignHCenter)
            self._list_widget.addItem(item)

    def remove_table(self):
        table_widget = Pireal.get_service("container").table_widget
        current_index = self._list_widget.currentRow()
        table_widget.remove_table(current_index)
        self._list_widget.takeItem(current_index)

lateral = LateralWidget()
