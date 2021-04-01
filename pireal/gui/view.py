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
    QAbstractItemView,
    QInputDialog,
)
from PyQt5.QtCore import (
    Qt,
    pyqtSlot as Slot,
)
from pireal import translations as tr


class View(QTableView):
    """ Vista """

    def __init__(self):
        super(View, self).__init__()
        # self.setAlternatingRowColors(CONFIG.get('alternatingRowColors'))
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

        # Connections
        self.sectionDoubleClicked[int].connect(self._on_section_double_clicked)

    @Slot(int)
    def _on_section_double_clicked(self, index):
        if not self.editable:
            return
        name, ok = QInputDialog.getText(
            self,
            tr.TR_INPUT_DIALOG_HEADER_TITLE,
            tr.TR_INPUT_DIALOG_HEADER_BODY
        )
        if ok:
            self.model().setHeaderData(index, Qt.Horizontal, name.strip())
