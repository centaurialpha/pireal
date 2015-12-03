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
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidgetItem,
    QSpacerItem,
    QSizePolicy,
    QMessageBox,
    QShortcut
)
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import (
    Qt,
    pyqtSignal
)
from src.gui.main_window import Pireal
from src.gui import table
from src import translations as tr
from src.core import relation


class NewRelationDialog(QDialog):
    dbModified = pyqtSignal(int)

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        #self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.setFocusPolicy(Qt.TabFocus)
        self.setFocus()
        self.setWindowTitle(tr.TR_RELATION_DIALOG_TITLE)
        vbox = QVBoxLayout(self)
        hbox = QHBoxLayout()
        self._line_relation_name = QLineEdit()
        self._line_relation_name.setPlaceholderText(tr.TR_RELATION_DIALOG_NAME)
        hbox.addWidget(self._line_relation_name)
        vbox.addLayout(hbox)

        vbox.addWidget(QLabel(tr.TR_RELATION_DIALOG_FIELDS))

        hbox = QHBoxLayout()
        btn_add_column = QPushButton(tr.TR_RELATION_DIALOG_ADD_COL)
        hbox.addWidget(btn_add_column)
        btn_add_tuple = QPushButton(tr.TR_RELATION_DIALOG_ADD_ROW)
        hbox.addWidget(btn_add_tuple)
        btn_remove_column = QPushButton(tr.TR_RELATION_DIALOG_DELETE_COL)
        hbox.addWidget(btn_remove_column)
        btn_remove_tuple = QPushButton(tr.TR_RELATION_DIALOG_DELETE_ROW)
        hbox.addWidget(btn_remove_tuple)
        vbox.addLayout(hbox)

        self._table = table.Table()
        vbox.addWidget(self._table)
        self._table.setRowCount(1)
        self._table.setColumnCount(2)
        self._table.setItem(0, 0, QTableWidgetItem(tr.TR_RELATION_DIALOG_F1))
        self._table.setItem(0, 1, QTableWidgetItem(tr.TR_RELATION_DIALOG_F2))

        hbox = QHBoxLayout()
        hbox.addItem(QSpacerItem(1, 0, QSizePolicy.Expanding))
        btn_ok = QPushButton(tr.TR_RELATION_DIALOG_BTN_OK)
        hbox.addWidget(btn_ok)
        btn_cancel = QPushButton(tr.TR_RELATION_DIALOG_BTN_CANCEL)
        btn_cancel.setObjectName("cancel")
        hbox.addWidget(btn_cancel)
        vbox.addLayout(hbox)

        # Connections
        kescape = QShortcut(QKeySequence(Qt.Key_Escape), self)
        kescape.activated.connect(lambda: self.done(1))
        btn_add_column.clicked.connect(self.__add_column)
        btn_remove_column.clicked.connect(self.__remove_column)
        btn_add_tuple.clicked.connect(self.__add_tuple)
        btn_remove_tuple.clicked.connect(self.__remove_tuple)
        btn_ok.clicked.connect(self.__create_table)
        btn_cancel.clicked.connect(lambda: self.done(1))

    def done(self, result):
        self.__result = result
        super(NewRelationDialog, self).done(self.__result)
        #self.emit(SIGNAL("dbModified(int)"), self.__result)
        self.dbModified.emit(self.__result)

    def __add_column(self):
        columns = self._table.columnCount()
        self._table.insertColumn(columns)

    def __remove_column(self):
        current = self._table.currentColumn()
        self._table.removeColumn(current)

    def __add_tuple(self):
        tuples = self._table.rowCount()
        self._table.insertRow(tuples)

    def __remove_tuple(self):
        current = self._table.currentRow()
        self._table.removeRow(current)

    def __create_table(self):
        # Name of relation
        name = self._line_relation_name.text()
        if not name.strip():
            QMessageBox.critical(self, "Error",
                                 tr.TR_RELATION_DIALOG_ERROR_NAME)
            return
        rows = self._table.rowCount()
        columns = self._table.columnCount()

        rel = relation.Relation()
        # Header of relation
        fields = []
        for i in range(columns):
            text = self._table.item(0, i).text()
            if not text.strip():
                QMessageBox.critical(self, "Error",
                                     tr.TR_RELATION_DIALOG_ADD_COL)
                return
            fields.append(text)

        rel.fields = fields

        # Data
        data = {}
        for row in range(1, rows):
            reg = []
            for column in range(columns):
                item = self._table.item(row, column)
                if item is None or not item.text().strip():
                    QMessageBox.critical(self, "Error",
                        tr.TR_RELATION_DIALOG_FIELD_EMPTY.format(
                            row + 1, column + 1))
                    return
                reg.append(self._table.item(row, column).text())
                data[row, column] = self._table.item(row, column).text()
            rel.insert(reg)
        # Add table and relation
        central = Pireal.get_service("central")
        table_widget = central.get_active_db().table_widget
        table_widget.add_table(rows - 1, columns, name, data, fields)
        table_widget.add_relation(name, rel)
        list_relation = central.get_active_db().lateral_widget
        list_relation.add_item(name, rows - 1)

        self.close()

    def showEvent(self, event):
        QDialog.showEvent(self, event)
        self._line_relation_name.setFocus()
