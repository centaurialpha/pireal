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

from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QPlainTextEdit
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QStyle
from PyQt5.QtWidgets import QMessageBox

from PyQt5.QtGui import QFont

from PyQt5.QtCore import pyqtSignal

from src.gui.main_window import Pireal
from src.core.settings import CONFIG


class EditRelationDialog(QDialog):

    sendData = pyqtSignal(list)

    def __init__(self, rname, parent=None):
        super().__init__(parent)
        self._rname = rname
        self.setWindowTitle(self.tr("Editor - {}".format(rname)))
        self.resize(400, 300)
        self.setModal(True)
        vbox = QVBoxLayout(self)
        desc = QLabel(
            self.tr("Ingresar los datos separados por comas y las tuplas\n"
                    "separadas por un salto de línea."))
        vbox.addWidget(desc)
        self._editor = QPlainTextEdit()
        font, size = CONFIG.get("fontFamily"), CONFIG.get("fontSize")
        if font is None:
            font, size = CONFIG._get_font()
        f = QFont(font, size)
        self._editor.setFont(f)
        vbox.addWidget(self._editor)
        self._editor.setCursorWidth(3)
        self._editor.setPlaceholderText("1,Gabriel,Python")

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        btn_accept = QPushButton(self.tr("Agregar Tuplas"))
        btn_accept.setIcon(
            self.style().standardIcon(QStyle.SP_DialogApplyButton))
        hbox.addWidget(btn_accept)
        btn_cancel = QPushButton(self.tr("Cancelar"))
        btn_cancel.setIcon(
            self.style().standardIcon(QStyle.SP_DialogCancelButton))
        hbox.addWidget(btn_cancel)

        vbox.addLayout(hbox)

        btn_cancel.clicked.connect(self.close)
        btn_accept.clicked.connect(self._on_accept)

    def _on_accept(self):
        central = Pireal.get_service("central")
        table_widget = central.get_active_db().table_widget
        relation = table_widget.relations[self._rname]
        lines = self._editor.toPlainText().splitlines()
        tuples = [tuple(t.split(",")) for t in lines]
        for e, t in enumerate(tuples):
            if len(t) != relation.degree():
                QMessageBox.critical(
                    self,
                    "Error",
                    self.tr("La relación <b>{}</b> es de grado <b>{}</b>.<br> "
                            "Ingresaste <b>{}</b> datos a la "
                            "tupla <b>{}</b> :/".format(
                                self._rname,
                                relation.degree(), len(t), e + 1)))
                return
        self.sendData.emit(tuples)
        self.close()
