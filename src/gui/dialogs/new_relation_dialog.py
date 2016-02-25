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
    QAbstractItemView,
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    #QLabel,
    QLineEdit,
    QPushButton,
    #QTableWidgetItem,
    QSpacerItem,
    QSizePolicy,
    QMessageBox,
    QShortcut,
    QComboBox,
    QTableView,
    QItemDelegate,
    QHeaderView
)
from PyQt5.QtGui import (
    QKeySequence,
    QStandardItemModel,
    QValidator,
    QIntValidator
)
from PyQt5.QtCore import (
    Qt,
    pyqtSignal,
    QModelIndex
)
from src.gui.main_window import Pireal
#from src.gui import table
from src.core import relation


class NewRelationDialog(QDialog):
    dbModified = pyqtSignal(int)

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.resize(600, 400)
        #self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.setFocusPolicy(Qt.TabFocus)
        self.setFocus()
        self.setWindowTitle(self.tr("New Relation"))
        vbox = QVBoxLayout(self)
        hbox = QHBoxLayout()
        self._line_relation_name = QLineEdit()
        self._line_relation_name.setPlaceholderText(self.tr("Relation name"))
        hbox.addWidget(self._line_relation_name)
        vbox.addLayout(hbox)

        #vbox.addWidget(QLabel(tr.TR_RELATION_DIALOG_FIELDS))

        hbox = QHBoxLayout()
        btn_add_column = QPushButton(self.tr("Add Column"))
        hbox.addWidget(btn_add_column)
        btn_add_tuple = QPushButton(self.tr("Add Row"))
        hbox.addWidget(btn_add_tuple)
        btn_remove_column = QPushButton(self.tr("Delete Column"))
        hbox.addWidget(btn_remove_column)
        btn_remove_tuple = QPushButton(self.tr("Delete Row"))
        hbox.addWidget(btn_remove_tuple)
        vbox.addLayout(hbox)

        self._hbox = QHBoxLayout()
        for i in range(2):
            self.__add_combo_to_layout()
        vbox.addLayout(self._hbox)

        # Model
        model = QStandardItemModel(0, 2)
        # Table
        self._table = QTableView()
        self._table.setModel(model)
        # Horizontal Header
        header = Header()
        self._table.setHorizontalHeader(header)
        # Default section name
        header.model().setHeaderData(0, Qt.Horizontal, self.tr("Field 1"))
        header.model().setHeaderData(1, Qt.Horizontal, self.tr("Field 2"))
        # Delegate
        delegate = ItemDelegate()
        self._table.setItemDelegate(delegate)
        vbox.addWidget(self._table)

        # Button ok and cancel
        hbox = QHBoxLayout()
        hbox.addItem(QSpacerItem(1, 0, QSizePolicy.Expanding))
        btn_ok = QPushButton(self.tr("Ok"))
        hbox.addWidget(btn_ok)
        btn_cancel = QPushButton(self.tr("Cancel"))
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

    #def done(self, result):
        #self.__result = result
        #super(NewRelationDialog, self).done(self.__result)
        ##self.emit(SIGNAL("dbModified(int)"), self.__result)
        #self.dbModified.emit(self.__result)

    def __add_column(self):
        model = self._table.model()
        col_count = model.columnCount()
        model.insertColumn(col_count)
        self.__add_combo_to_layout()

    def __remove_column(self):
        model = self._table.model()
        column_to_remove = self._table.currentIndex().column()
        model.removeColumn(column_to_remove)
        self.__remove_from_layout(column_to_remove)
        self._table.resizeColumnToContents(0)

    def __add_tuple(self):
        model = self._table.model()
        row_count = model.rowCount()
        model.insertRow(row_count)

    def __remove_tuple(self):
        model = self._table.model()
        row_to_remove = self._table.currentIndex().row()
        model.removeRow(row_to_remove)

    def __add_combo_to_layout(self):
        combo = QComboBox()
        combo.addItems(["Select Type", "Char", "Numeric"])
        self._hbox.addWidget(combo)

        combo.activated[int].connect(self._current_index_combo_changed)

    def _current_index_combo_changed(self, index):
        index_of_combo_widget = self._hbox.indexOf(self.sender())
        delegate = self._table.itemDelegate()
        delegate.set_column_type(index_of_combo_widget, index)

    def __remove_from_layout(self, index):
        widget = self._hbox.takeAt(index).widget()
        widget.deleteLater()

    #def __validate_types(self):
        #data = {}
        #for index in range(self._hbox.count()):
            #combo = self._hbox.itemAt(index).widget()
            #if combo.currentIndex() == 0:
            #QMessageBox.critical(self, "Select type", "Please select type")
                #return {}
            #data[index] = combo.currentText()

        #return data

    def __create_table(self):
        # Name of relation
        name = self._line_relation_name.text()
        if not name.strip():
            QMessageBox.critical(self, "Error",
                                 self.tr("Relation name not specified."))
            return

        nrow = self._table.model().rowCount()
        ncolumn = self._table.model().columnCount()

        rel = relation.Relation()
        # Header of relation
        fields = []

        for i in range(ncolumn):
            text = self._table.model().horizontalHeaderItem(i).text()
            if not text.strip():
                QMessageBox.critical(self, "Error",
                                     self.tr("Add Column"))
                return
            fields.append(text)

        rel.fields = fields

        # Data
        data = {}
        for row in range(nrow):
            reg = []
            for column in range(ncolumn):
                item = self._table.model().item(row, column)
                if item is None or not item.text().strip():
                    QMessageBox.critical(self, "Error",
                        self.tr("Field {0}:{1} is empty!".format(
                            row + 1, column + 1)))
                    return
                reg.append(item.text())
                data[row, column] = item.text()
            rel.insert(reg)
        # Add table and relation
        central = Pireal.get_service("central")
        table_widget = central.get_active_db().table_widget
        table_widget.add_table(nrow, ncolumn, name, data, fields)
        table_widget.add_relation(name, rel)
        list_relation = central.get_active_db().lateral_widget
        list_relation.add_item(name, nrow)

        self.close()

    def showEvent(self, event):
        QDialog.showEvent(self, event)
        self._line_relation_name.setFocus()


class ItemDelegate(QItemDelegate):

    def __init__(self, parent=None):
        super(ItemDelegate, self).__init__(parent)
        # (index column, index type)
        self._cols_type = {}

    def set_column_type(self, index_col, index_type):
        self._cols_type[index_col] = index_type

    def createEditor(self, parent, option, index):
        editor = QLineEdit(parent)
        return editor

    def setEditorData(self, line, index):
        text = index.model().data(index, Qt.EditRole)
        line.setText(text)

    def setModelData(self, line, model, index):
        text = line.text()
        validator = QIntValidator()
        column = index.column()
        if self._cols_type[column] == 2:
            if validator.validate(text, 0)[0] == QValidator.Acceptable:
                model.setData(index, text)
        else:
            if not text.isdigit():
                model.setData(index, text)

    def updateEditorGeometry(self, line, option, index):
        line.setGeometry(option.rect)


class Header(QHeaderView):

    def __init__(self, orientation=Qt.Horizontal, parent=None):
        super(Header, self).__init__(orientation, parent)
        self.setSectionsClickable(True)
        self.setSectionResizeMode(QHeaderView.Stretch)
        self.setSelectionBehavior(QAbstractItemView.SelectColumns)
        self.line = QLineEdit(parent=self.viewport())
        self.line.setAlignment(Qt.AlignTop)
        self.line.setHidden(True)
        self.line.blockSignals(True)
        self.col = 0

        # Connections
        self.sectionDoubleClicked[int].connect(self._edit_header)
        self.sectionClicked[int].connect(self._select_header)
        self.line.editingFinished.connect(self._done_editing)

    def _select_header(self, index):
        #self.setSelection(True)
        pass

    def _edit_header(self, index):
        geo = self.line.geometry()
        geo.setWidth(self.sectionSize(index))
        geo.moveLeft(self.sectionViewportPosition(index))
        self.line.setGeometry(geo)

        self.line.setHidden(False)
        self.line.blockSignals(False)
        self.line.setFocus()
        self.col = index

    def _done_editing(self):
        self.line.blockSignals(True)
        self.line.setHidden(False)
        text = self.line.text()
        self.model().setHeaderData(self.col, Qt.Horizontal, text)
        self.line.setText("")
        self.line.hide()
        self.setCurrentIndex(QModelIndex())
