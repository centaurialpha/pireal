# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (
    QTableWidget,
    QAbstractItemView,
    QHeaderView
)


class Table(QTableWidget):

    def __init__(self, parent=None):
        super(Table, self).__init__(parent)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        #FIXME: Configurable
        self.verticalHeader().setVisible(False)