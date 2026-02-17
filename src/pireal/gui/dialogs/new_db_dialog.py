# Copyright 2015-2025 - Gabriel Acosta <acostadariogabriel@gmail.com>
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


from pathlib import Path

from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QFileDialog, QFormLayout, QLineEdit, QStyle

from pireal import translations as tr
from pireal.dirs import DATABASES_DIR


class NewDBInputDialog(QDialog):
    def __init__(self, parent=None, location: str = "", name: str = ""):
        super().__init__(parent)
        self.setWindowTitle(tr.TR_DB_DIALOG_TITLE)
        self.setMinimumWidth(500)

        # Form
        layout = QFormLayout(self)
        self._line_db_name = QLineEdit()
        self._line_db_name.setText(name)
        self._line_db_location = QLineEdit()
        self._line_db_location.setText(location or str(DATABASES_DIR))
        self._line_db_location.setReadOnly(True)
        style = self.style()
        assert style is not None
        choose_dir_action = self._line_db_location.addAction(
            style.standardIcon(QStyle.StandardPixmap.SP_DirIcon),
            QLineEdit.ActionPosition.TrailingPosition,
        )
        self._line_db_filename = QLineEdit()
        self._line_db_filename.setReadOnly(True)
        self._line_db_filename.setText(self.filename())

        layout.addRow(tr.TR_DB_DIALOG_DB_NAME, self._line_db_name)
        layout.addRow(tr.TR_DB_DIALOG_DB_LOCATION, self._line_db_location)
        layout.addRow(tr.TR_DB_DIALOG_DB_FILENAME, self._line_db_filename)

        # Buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel,
            Qt.Orientation.Horizontal,
        )
        layout.addWidget(button_box)

        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        choose_dir_action.triggered.connect(self._choose_db_dir)
        self._line_db_name.textChanged.connect(self._update_db_filename)
        self._line_db_location.textChanged.connect(self._update_db_filename)

    def filename(self) -> str:
        db_name = self._line_db_name.text().strip()
        if db_name:
            db_name = f"{db_name}.pdb"
        return str(Path(self._line_db_location.text()) / db_name)

    @pyqtSlot()
    def _update_db_filename(self):
        self._line_db_filename.setText(self.filename())

    @pyqtSlot()
    def _choose_db_dir(self):
        location = QFileDialog.getExistingDirectory(self, tr.TR_DB_DIALOG_SELECT_FOLDER)
        if location:
            self._line_db_location.setText(location)

    @staticmethod
    def ask_db_name(parent=None, location: str = "", name: str = ""):
        dialog = NewDBInputDialog(parent, location, name)
        result = dialog.exec()

        if result == QDialog.DialogCode.Accepted and dialog._line_db_name.text().strip():
            return dialog._line_db_filename.text()
        return
