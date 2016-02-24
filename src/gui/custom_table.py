# -*- coding: utf-8 -*-

import re

from PyQt5.QtWidgets import (
    QTableView,
    QItemDelegate,
    QLineEdit,
    QHeaderView
)
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtCore import Qt


class Table(QTableView):

    def __init__(self):
        super(Table, self).__init__()
        # Stretch horizontal header
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # Model
        model = QStandardItemModel()
        self.setModel(model)
        # Item delegate
        delegate = ItemDelegate()
        self.setItemDelegate(delegate)


class ItemDelegate(QItemDelegate):

    def __init__(self, parent=None):
        super(ItemDelegate, self).__init__(parent)
        self.data_types = {}

    def createEditor(self, parent, option, index):
        editor = QLineEdit(parent)
        type_ = self.data_types.get(index.column())

        if type_ == 'numeric':
            regex = r"^\d*\.?\d*$"
        elif type_ == 'char':
            regex = r"^[a-zA-Z][a-zA-Z0-9]*?$"
        else:
            # Validate 0000/00/00, 00/00/00, 00/00/0000
            regex1 = "(\d{1,4})[/.-](\d{1,2})[/.-](\d{2,4})$"
            # Validate 00:00
            regex2 = "(24:00|2[0-3]:[0-5][0-9]|[0-1][0-9]:[0-5][0-9])"
            regex = '(' + regex1 + '|' + regex2 + ')'
        editor.regexp = re.compile(regex)
        editor.data_ok = False
        editor.textChanged.connect(self.__check_state)

        return editor

    def setEditorData(self, line, index):
        text = index.model().data(index, Qt.EditRole)
        line.setText(text)

    def setModelData(self, line, model, index):
        if line.data_ok:
            model.setData(index, line.text())

    def __check_state(self, text):
        line = self.sender()
        if line.regexp.match(text):
            color = "#c4df9b"
            line.data_ok = True
        else:
            color = "#f6989d"
            line.data_ok = False
        line.setStyleSheet(
            "QLineEdit { border: none; background-color: %s }" % color)