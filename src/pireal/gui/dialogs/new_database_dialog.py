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

from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QStyle,
    QVBoxLayout,
)

from pireal import (
    dirs,
    translations as tr,
)


class _DBInputDialog(QDialog):
    def __init__(self, parent=None, default_location="", default_name=""):
        super().__init__(parent)

        self.setWindowTitle("Seleccionar Base de Datos")
        self.resize(500, 200)

        # Crear el layout principal
        main_layout = QVBoxLayout()

        # Campo para el nombre de la DB
        db_name_layout = QHBoxLayout()
        db_name_label = QLabel("Nombre DB:")
        self.db_name_input = QLineEdit(default_name)
        db_name_layout.addWidget(db_name_label)
        db_name_layout.addWidget(self.db_name_input)
        main_layout.addLayout(db_name_layout)

        # Separador
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        main_layout.addWidget(line)

        # Campo para la ubicación
        location_layout = QHBoxLayout()
        location_label = QLabel("Location:")
        self.location_input = QLineEdit(default_location)
        self.location_input.setReadOnly(True)
        browse_button = QPushButton("...")
        browse_button.setMaximumWidth(30)
        browse_button.clicked.connect(self.browse_folder)
        location_layout.addWidget(location_label)
        location_layout.addWidget(self.location_input)
        location_layout.addWidget(browse_button)
        main_layout.addLayout(location_layout)

        # Separador
        line2 = QFrame()
        line2.setFrameShape(QFrame.Shape.HLine)
        line2.setFrameShadow(QFrame.Shadow.Sunken)
        main_layout.addWidget(line2)

        # Campo para la ruta completa
        full_path_layout = QHBoxLayout()
        full_path_label = QLabel("Ruta Completa:")
        self.full_path_input = QLineEdit()
        self.full_path_input.setReadOnly(True)
        full_path_layout.addWidget(full_path_label)
        full_path_layout.addWidget(self.full_path_input)
        main_layout.addLayout(full_path_layout)

        # Botones OK y Cancel
        button_layout = QHBoxLayout()
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addStretch()
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        main_layout.addLayout(button_layout)

        # Añadir espaciador
        main_layout.addStretch()

        # Conectar señales para actualizar la ruta completa
        self.db_name_input.textChanged.connect(self.update_full_path)

        # Inicializar la ruta completa si hay valores por defecto
        if default_location or default_name:
            self.update_full_path()

        self.setLayout(main_layout)

    @pyqtSlot()
    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Seleccionar Carpeta")
        if folder:
            self.location_input.setText(folder)
            self.update_full_path()

    @pyqtSlot()
    def update_full_path(self):
        location = self.location_input.text()
        db_name = self.db_name_input.text()

        if location and db_name:
            # Asegurarse de que el nombre de la DB termine en .db si no tiene extensión
            if not db_name.endswith(".db"):
                db_name = f"{db_name}.db"

            full_path = os.path.join(location, db_name)
            self.full_path_input.setText(full_path)
        else:
            self.full_path_input.setText("")

    def get_full_path(self):
        """Retorna la ruta completa seleccionada"""
        return self.full_path_input.text()

    def get_db_name(self):
        """Retorna el nombre de la base de datos"""
        return self.db_name_input.text()

    def get_location(self):
        """Retorna la ubicación seleccionada"""
        return self.location_input.text()

    @staticmethod
    def ask_db_name(parent=None, default_location="", default_name=""):
        """
        Método estático que muestra el diálogo y retorna la ruta completa.

        Args:
            parent: Widget padre
            default_location: Ubicación por defecto
            default_name: Nombre de DB por defecto

        Returns:
            tuple: (ruta_completa, ubicación, nombre_db) si se acepta el diálogo
                   (None, None, None) si se cancela
        """
        dialog = _DBInputDialog(parent, default_location, default_name)
        result = dialog.exec()

        if result == QDialog.DialogCode.Accepted:
            return (dialog.get_full_path(), dialog.get_location(), dialog.get_db_name())
        else:
            return (None, None, None)


PIREAL_DB_EXTENSION = ".pdb"


class _DBInputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(tr.TR_DB_DIALOG_TITLE)
        self.setMinimumWidth(500)
        layout = QFormLayout(self)
        layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        self._line_db_name = QLineEdit()
        layout.addRow(tr.TR_DB_DIALOG_DB_NAME, self._line_db_name)
        self._line_db_location = QLineEdit()
        self._line_db_location.setText(str(dirs.DATABASES_DIR))
        self._line_db_location.setReadOnly(True)
        choose_dir_action = self._line_db_location.addAction(
            self.style().standardIcon(QStyle.StandardPixmap.SP_DirIcon),
            QLineEdit.ActionPosition.TrailingPosition,
        )
        layout.addRow(tr.TR_DB_DIALOG_DB_LOCATION, self._line_db_location)
        #        self._line_db_path = QLineEdit()
        self._line_db_path.setReadOnly(True)
        layout.addRow(tr.TR_DB_DIALOG_DB_FILENAME, self._line_db_path)
        self._line_db_path.setText(str(dirs.DATABASES_DIR))

        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel,
            Qt.Orientation.Horizontal,
        )
        layout.addWidget(button_box)
        self._button_ok = button_box.button(QDialogButtonBox.StandardButton.Ok)

        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        choose_dir_action.triggered.connect(self._choose_db_dir)
        self._line_db_name.textChanged.connect(self._update_db_path)
        self._line_db_location.textChanged.connect(self._update_db_path)
        self._line_db_name.textChanged.connect(self._validate)

    @pyqtSlot()
    def _update_db_path(self):
        db_name = self._line_db_name.text().strip()
        if db_name:
            db_name += PIREAL_DB_EXTENSION
        db_path = os.path.join(self._line_db_location.text(), db_name)
        self._line_db_path.setText(db_path)

    @property
    def db_path(self) -> str:
        return self._line_db_path.text()

    @pyqtSlot()
    def _choose_db_dir(self):
        location = QFileDialog.getExistingDirectory(self, tr.TR_DB_DIALOG_SELECT_FOLDER)
        if location:
            self._line_db_location.setText(location)
            # TODO: update PIREAL_DATABASES in settings

    @classmethod
    def ask_db_name(cls, parent=None) -> str:
        dialog = cls(parent=parent)
        ret = dialog.exec()
        if ret:
            return dialog.db_path
        return ""

    def _validate(self):
        exist = os.path.exists(self._line_db_path.text().strip())
        self._button_ok.setEnabled(not exist)
