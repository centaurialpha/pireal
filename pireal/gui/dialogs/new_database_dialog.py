# -*- coding: utf-8 -*-
#
# Copyright 2015-2021 - Gabriel Acosta <acostadariogabriel@gmail.com>
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
from PyQt5.QtWidgets import QDialogButtonBox
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QStyle
from PyQt5.QtWidgets import QFileDialog

from PyQt5.QtCore import pyqtSlot as Slot
from PyQt5.QtCore import Qt

from pireal import translations as tr
from pireal import dirs

PIREAL_DB_EXTENSION = '.pdb'


class DBInputDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(tr.TR_DB_DIALOG_TITLE)
        self.setMinimumWidth(500)
        layout = QFormLayout(self)
        layout.setLabelAlignment(Qt.AlignRight)
        self._line_db_name = QLineEdit()
        layout.addRow(tr.TR_DB_DIALOG_DB_NAME, self._line_db_name)
        self._line_db_location = QLineEdit()
        self._line_db_location.setText(str(dirs.DATABASES_DIR))
        self._line_db_location.setReadOnly(True)
        choose_dir_action = self._line_db_location.addAction(
            self.style().standardIcon(QStyle.SP_DirIcon), QLineEdit.TrailingPosition)
        layout.addRow(tr.TR_DB_DIALOG_DB_LOCATION, self._line_db_location)
        self._line_db_path = QLineEdit()
        self._line_db_path.setReadOnly(True)
        layout.addRow(tr.TR_DB_DIALOG_DB_FILENAME, self._line_db_path)
        self._line_db_path.setText(str(dirs.DATABASES_DIR))

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal)
        layout.addWidget(button_box)
        self._button_ok = button_box.button(QDialogButtonBox.Ok)

        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        choose_dir_action.triggered.connect(self._choose_db_dir)
        self._line_db_name.textChanged.connect(self._update_db_path)
        self._line_db_location.textChanged.connect(self._update_db_path)
        self._line_db_name.textChanged.connect(self._validate)

    @Slot()
    def _update_db_path(self):
        db_name = self._line_db_name.text().strip()
        if db_name:
            db_name += PIREAL_DB_EXTENSION
        db_path = os.path.join(self._line_db_location.text(), db_name)
        self._line_db_path.setText(db_path)

    @property
    def db_path(self) -> str:
        return self._line_db_path.text()

    @Slot()
    def _choose_db_dir(self):
        location = QFileDialog.getExistingDirectory(self, tr.TR_DB_DIALOG_SELECT_FOLDER)
        if location:
            self._line_db_location.setText(location)
            # TODO: update PIREAL_DATABASES in settings

    @classmethod
    def ask_db_name(cls, parent=None) -> str:
        dialog = cls(parent=parent)
        ret = dialog.exec_()
        if ret:
            return dialog.db_path
        return ''

    def _validate(self):
        exist = os.path.exists(self._line_db_path.text().strip())
        self._button_ok.setEnabled(not exist)
