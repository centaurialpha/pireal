# -*- coding: utf-8 -*-
#
# Copyright 2015-2018 - Gabriel Acosta <acostadariogabriel@gmail.com>
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

from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QMessageBox

from PyQt5.QtCore import QProcess

from src.core import settings
from src.gui.main_window import Pireal


class RDBPDBTool(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(self.tr("WinRDBI DB File to PDB"))
        self.setModal(True)
        self.setMinimumWidth(600)

        self._process = QProcess(self)
        self._process.setProgram("python")
        self._process.finished.connect(self._on_finished)

        vbox = QVBoxLayout(self)
        hbox = QHBoxLayout()
        hbox.addWidget(QLabel(self.tr("Ubicación del .rdb:")))
        self._line_location = QLineEdit()
        self._line_location.setReadOnly(True)
        choose_location = self._line_location.addAction(
            self.style().standardIcon(
                self.style().SP_DirIcon), QLineEdit.TrailingPosition)
        hbox.addWidget(self._line_location)
        vbox.addLayout(hbox)
        aviso = QLabel(
                self.tr(
                    "<b><i>El archivo será guardado en el mismo directorio "
                    "que el original.</i></b>"))
        f = aviso.font()
        f.setPointSize(10)
        aviso.setFont(f)
        vbox.addWidget(aviso)
        self._check_open = QCheckBox(self.tr("Abrir la BD al finalizar"))
        vbox.addWidget(self._check_open)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        start_btn = QPushButton(self.tr("Convertir!"))
        hbox.addWidget(start_btn)
        cancel_btn = QPushButton(self.tr("Salir"))
        hbox.addWidget(cancel_btn)
        vbox.addLayout(hbox)

        choose_location.triggered.connect(self._select_rdb_file)
        start_btn.clicked.connect(self._start_convertion)
        cancel_btn.clicked.connect(self.close)

    def _start_convertion(self):
        rdb_filename = self._line_location.text()

        tool = os.path.join(settings.ROOT_DIR, "rdb_to_pdb")

        args = [tool, rdb_filename]
        self._process.setArguments(args)
        self._process.start()

    def _on_finished(self, code, status):
        if status == QProcess.NormalExit == code:
            QMessageBox.information(
                self, self.tr("Completado!"),
                self.tr("Todo ha salido muy bien!"))
            if self._check_open.isChecked():
                central = Pireal.get_service("central")
                rdb = os.path.splitext(self._line_location.text())[0]
                pdb = rdb + ".pdb"
                central.open_database(pdb)
                self.close()
        else:
            QMessageBox.critical(
                self, "Error", "El proceso no se ha completado")

    def _select_rdb_file(self):
        filename = QFileDialog.getOpenFileName(
            self, self.tr("Selecciona el arhico RDB"),
            "~", "RDB Files (*.rdb)")[0]
        if filename:
            self._line_location.setText(filename)
            # pdb_name = os.path.basename(os.path.splitext(filename)[0])
            # self._line_name.setText(pdb_name + ".pdb")
