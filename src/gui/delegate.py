# -*- coding: utf-8 -*-
#
# Copyright 2015-2017 - Gabriel Acosta <acostadariogabriel@gmail.com>
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

from PyQt5.QtWidgets import QItemDelegate
from PyQt5.QtWidgets import QStyle
from PyQt5.QtWidgets import QApplication

from PyQt5.QtGui import QColor
from PyQt5.QtGui import QPalette
from PyQt5.QtGui import QPen

from PyQt5.QtCore import Qt, QSize


class Delegate(QItemDelegate):
    """ Delegado
    Asegura que al editar un campo no se envíe un dato vacío
    """

    def __init__(self, parent=None):
        super().__init__(parent)

    def setModelData(self, editor, model, index):
        data = editor.text().strip()
        if data:
            model.setData(index, data, Qt.EditRole)

    def setEditorData(self, editor, index):
        text = index.model().data(index, Qt.DisplayRole)
        editor.setText(text)

    def paint(self, painter, opt, index):
        if opt.state & QStyle.State_Selected:
            opt.palette.setColor(QPalette.Highlight, QColor("#fffde1"))
            painter.drawRect(opt.rect)
        opt.palette.setColor(QPalette.HighlightedText, Qt.black)
        super().paint(painter, opt, index)
