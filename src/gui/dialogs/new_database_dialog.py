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

import os
from PyQt5.QtWidgets import (
    QWizard,
    QWizardPage,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QStyle,
    QFileDialog
)
from PyQt5.QtCore import (
    pyqtSlot,
    pyqtSignal
)
from src.core import settings


class NewDatabaseDialog(QWizard):

    # La señal se emite cuando se crea la DB, es decir
    # cuando se clickea en el botón 'Crear' del diálogo
    created = pyqtSignal('QString', 'QString', 'QString')

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(self.tr("New Database Wizard"))
        self.addPage(FirstPage())

    def done(self, result):
        if result == 1:
            dbname = self.field("dbname")
            location = self.field("dblocation")
            filename = self.field("dbfilename")
            self.created.emit(dbname, location, filename)
        super().done(result)


class FirstPage(QWizardPage):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle("Nueva Base de Datos de Pireal")
        self.setSubTitle("A continuación elija el nombre y el destino de la DB")

        # Widgets
        box = QVBoxLayout(self)
        hbox = QHBoxLayout()
        hbox.addWidget(QLabel(self.tr("Database Name:")))
        self._database_name_line = QLineEdit()
        hbox.addWidget(self._database_name_line)
        box.addLayout(hbox)
        hbox = QHBoxLayout()
        hbox.addWidget(QLabel(self.tr("Location:")))
        self._database_location_line = QLineEdit()
        # Left action to change db location
        change_location_action = self._database_location_line.addAction(
            self.style().standardIcon(QStyle.SP_DirIcon), 1)
        self._database_location_line.setReadOnly(True)
        hbox.addWidget(self._database_location_line)
        box.addLayout(hbox)
        hbox = QHBoxLayout()
        hbox.addWidget(QLabel(self.tr("Filename:")))
        self._database_filename_line = QLineEdit()
        self._database_filename_line.setReadOnly(True)
        hbox.addWidget(self._database_filename_line)
        box.addLayout(hbox)

        # Register fields
        self.registerField("dbname*", self._database_name_line)
        self.registerField("dblocation", self._database_location_line)
        self.registerField("dbfilename", self._database_filename_line)

        self.__location_folder = settings.PIREAL_DATABASES
        self._database_filename_line.setText(self.__location_folder)
        self._database_location_line.setText(self.__location_folder)

        # Conexiones
        self._database_name_line.textChanged.connect(self._update_filename)
        change_location_action.triggered.connect(self.__select_location)

    @pyqtSlot()
    def __select_location(self):
        location = QFileDialog.getExistingDirectory(self,
                                                    self.tr("Select Folder"))
        if not location:
            return

        self._database_location_line.setText(location)
        self.__location_folder = os.path.join(self.__location_folder, location)

        self._database_filename_line.setText(os.path.join(
            location, self._database_name_line.text()))

    @pyqtSlot('QString')
    def _update_filename(self, filename):
        new_filename = os.path.join(self.__location_folder, filename)
        self._database_filename_line.setText(new_filename + '.pdb')
