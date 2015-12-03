# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (
    QTableWidget,
    QTableWidgetItem,
    QAbstractItemView,
    QHeaderView
)
from PyQt5.QtCore import Qt


class Table(QTableWidget):

    def __init__(self, parent=None):
        super(Table, self).__init__(parent)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        #FIXME: Configurable
        self.verticalHeader().setVisible(False)


class Item(QTableWidgetItem):

    def __init__(self, parent=None):
        super(Item, self).__init__(parent)
        self.setFlags(self.flags() ^ Qt.ItemIsEditable)
