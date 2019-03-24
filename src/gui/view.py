# -*- coding: utf-8 -*-
#
# Copyright 2015-2016 - Gabriel Acosta <acostadariogabriel@gmail.com>
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
    QTableView,
    QHeaderView,
    QLineEdit,
    QAbstractItemView,
    QMessageBox
)
from PyQt5.QtCore import (
    Qt,
    QModelIndex
)


class View(QTableView):
    """ Vista """

    def __init__(self):
        super(View, self).__init__()
        # self.setAlternatingRowColors(True)
        self.verticalHeader().hide()
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        # Scroll content per pixel
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.horizontalHeader().setHighlightSections(False)

    def resizeEvent(self, event):
        super(View, self).resizeEvent(event)
        self.adjust_columns()

    def adjust_columns(self):
        """ Resize all sections to content and user interactive """

        header = self.horizontalHeader()
        for column in range(header.count()):
            header.setSectionResizeMode(column, QHeaderView.ResizeToContents)
            width = header.sectionSize(column)
            header.setSectionResizeMode(column, QHeaderView.Interactive)
            header.resizeSection(column, width)
        self.horizontalHeader().setMinimumHeight(32)


class Header(QHeaderView):

    def __init__(self, orientation=Qt.Horizontal, parent=None):
        super(Header, self).__init__(orientation, parent)
        self.editable = True
        self.setSectionsClickable(True)
        self.setSectionResizeMode(QHeaderView.ResizeToContents)
        self.line = QLineEdit(parent=self.viewport())
        self.line.setAlignment(Qt.AlignTop)
        self.line.setHidden(True)
        self.line.blockSignals(True)
        self.col = 0

        # Connections
        self.sectionDoubleClicked[int].connect(self.__edit)
        self.line.editingFinished.connect(self.__done_editing)

    def __edit(self, index):
        if not self.editable:
            return
        geo = self.line.geometry()
        geo.setWidth(self.sectionSize(index))
        geo.moveLeft(self.sectionViewportPosition(index))
        current_text = self.model().headerData(index, Qt.Horizontal,
                                               Qt.DisplayRole)
        self.line.setGeometry(geo)
        self.line.setHidden(False)
        self.line.blockSignals(False)
        self.line.setText(str(current_text))
        self.line.setFocus()
        self.line.selectAll()
        self.col = index

    def __done_editing(self):
        text = self.line.text()
        if not text.strip():
            # No debe ser vacío
            QMessageBox.critical(self, "Error",
                                 self.tr("El campo no debe ser vacío"))
            self.line.hide()
            return
        self.line.blockSignals(True)
        self.line.setHidden(False)
        self.model().setHeaderData(self.col, Qt.Horizontal, text,
                                   Qt.DisplayRole)
        self.line.setText("")
        self.line.hide()
        self.setCurrentIndex(QModelIndex())
