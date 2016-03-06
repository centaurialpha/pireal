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
    QPushButton
)
from PyQt5.QtGui import QStandardItem

from src.gui import custom_table


class RelationEditor(QDialog):

    def __init__(self, relation, parent=None):
        super(RelationEditor, self).__init__(parent)
        self._relation = relation
        self.setWindowTitle(self.tr("Relation Editor"))
        self.resize(700, 500)
        box = QVBoxLayout(self)

        # Buttons layout
        box_btns = QHBoxLayout()
        add_tuple_btn = QPushButton(self.tr("Add Tuple"))
        box_btns.addWidget(add_tuple_btn)
        remove_tuple_btn = QPushButton(self.tr("Remove Tuple"))
        box_btns.addWidget(remove_tuple_btn)
        add_column_btn = QPushButton(self.tr("Add Column"))
        box_btns.addWidget(add_column_btn)
        remove_column_btn = QPushButton(self.tr("Remove Column"))
        box_btns.addWidget(remove_column_btn)
        box.addLayout(box_btns)

        # Table
        self.table = custom_table.Table()
        box.addWidget(self.table)
        self.setup_table()

    def setup_table(self):
        model = self.table.model()
        model.setHorizontalHeaderLabels(self._relation.header)
        row_count = 0
        for row in self._relation.content:
            for col_count, data in enumerate(row):
                item = QStandardItem(data)
                model.setItem(row_count, col_count, item)
            row_count += 1
#from PyQt5.QtWidgets import (
    #QDialog,
    #QVBoxLayout,
    #QHBoxLayout,
    #QTableWidget,
    #QTableWidgetItem,
    #QPushButton,
    #QSizePolicy,
    #QSpacerItem,
    #QHeaderView,
    #QLineEdit
#)
#from PyQt5.QtGui import (
    #QBrush,
    #QColor
#)
#from PyQt5.QtCore import pyqtSignal

#from src.gui import custom_table
#from src import translations as tr


#class EditRelationDialog(QDialog):
    #tableChanged = pyqtSignal('QString')

    #def __init__(self, item, table_name, parent=None):
        #super(EditRelationDialog, self).__init__(parent)
        #title = tr.TR_RELATION_EDIT_DIALOG_TITLE + ' [' + table_name + ']'
        #self.setWindowTitle(title)
        #self.resize(650, 450)
        #box = QVBoxLayout(self)
        #box.setContentsMargins(5, 5, 5, 5)
        ## Name
        #self._line_relation_name = QLineEdit(table_name)
        #self._line_relation_name.setSelection(0, len(table_name))
        #box.addWidget(self._line_relation_name)

        ## Table
        #self.previous_table = item
        #self.new_table = self.__load_table(item)
        #box.addWidget(self.new_table)

        #self.modified = False
        ## Buttons
        ## Left
        #hbox_buttons = QHBoxLayout()
        #hbox = QHBoxLayout()
        #btn_add_row = QPushButton(tr.TR_RELATION_DIALOG_ADD_ROW)
        #hbox.addWidget(btn_add_row)
        #btn_delete_row = QPushButton(tr.TR_RELATION_DIALOG_DELETE_ROW)
        #hbox.addWidget(btn_delete_row)
        #hbox_buttons.addLayout(hbox)

        ## Right
        #hbox = QHBoxLayout()
        #hbox.addItem(QSpacerItem(1, 0, QSizePolicy.Expanding))
        #btn_save = QPushButton(tr.TR_RELATION_DIALOG_BTN_OK)
        #hbox.addWidget(btn_save)
        #btn_cancel = QPushButton(tr.TR_RELATION_DIALOG_BTN_CANCEL)
        #hbox.addWidget(btn_cancel)
        #hbox_buttons.addLayout(hbox)

        #box.addLayout(hbox_buttons)

        ## Connections
        #btn_save.clicked.connect(self.__save)
        #btn_cancel.clicked.connect(self.close)
        #btn_add_row.clicked.connect(self.__insert_row)
        #btn_delete_row.clicked.connect(self.__delete_row)
        #self.new_table.cellChanged[int, int].connect(self.__on_cell_changed)

    #def __insert_row(self):
        #nrows = self.new_table.rowCount()
        #self.new_table.insertRow(nrows)

    #def __delete_row(self):
        #if self.new_table.selectedItems():
            #row = self.new_table.currentIndex().row()
            #self.new_table.removeRow(row)

    #def __save(self):

        ##FIXME: mejor forma de hacerlo?
        #if self.modified:
            #nrows = self.new_table.rowCount()
            #ncols = self.new_table.columnCount()

            ## Clear items
            #for i in reversed(range(self.previous_table.rowCount())):
                #self.previous_table.removeRow(i)

            ## Set new row count
            #self.previous_table.setRowCount(nrows)

            ## Populate table with new items
            #for i in range(nrows):
                #for j in range(ncols):
                    #text = self.new_table.item(i, j).text()
                    #item = table.Item()
                    #item.setText(text)
                    #self.previous_table.setItem(i, j, item)

            ## Emit signal
            #self.tableChanged.emit(self._line_relation_name.text())

        #self.close()

    #def __on_cell_changed(self, row, column):
        #item = self.new_table.item(row, column)
        #item.setBackground(QBrush(QColor("#f95959")))
        #item.setForeground(QBrush(QColor("white")))
        #item.setSelected(False)
        #self.modified = True

    #def __load_table(self, table):
        #new_table = QTableWidget()
        #new_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        #nrows = table.rowCount()
        #ncols = table.columnCount()

        #new_table.setRowCount(nrows)
        #new_table.setColumnCount(ncols)

        ## Get texts from horizontal header
        #hlabels = [table.horizontalHeaderItem(i).text() for i in range(ncols)]
        ## Set horizontal header
        #new_table.setHorizontalHeaderLabels(hlabels)

        #for i in range(nrows):
            #for j in range(ncols):
                #old_item = table.item(i, j)
                #new_item = QTableWidgetItem()
                #new_item.setText(old_item.text())
                #new_table.setItem(i, j, new_item)

        #return new_table
#