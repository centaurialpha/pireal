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
    QSplitter,
    QMessageBox
)
from PyQt5.QtCore import Qt
#from src.gui.main_window import Pireal
from src.gui import table_widget, lateral_widget
from src.core import pfile


class DBWidget(QSplitter):

    def __init__(self, orientation=Qt.Horizontal):
        QSplitter.__init__(self, orientation)
        self.lateral_widget = lateral_widget.LateralWidget()
        self.addWidget(self.lateral_widget)
        self.table_widget = table_widget.TableWidget()
        self.addWidget(self.table_widget)

    def create_database(self, filename=''):
        """ This function opens or creates a database """

        # Pireal File Object
        _file = pfile.PFile(filename)

        if filename:
            try:
                data = _file.read()
            except Exception as reason:
                QMessageBox.critical(self, "Error!", reason.__str__())
                return
            db_name = _file.name
            self.table_widget.add_data_base(data)
        else:
            db_name = "untitled_{}"

        return db_name

    @property
    def relations(self):
        return self.table_widget.relations

    def showEvent(self, event):
        QSplitter.showEvent(self, event)
        self.setSizes([1, self.width() / 3])