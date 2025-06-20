# -*- coding: utf-8 -*-
#
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

import structlog
from PyQt6.QtCore import QSettings, pyqtSlot
from PyQt6.QtWidgets import (
    QFileDialog,
    QMessageBox,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from pireal import translations as tr
from pireal.core.db import DB
from pireal.core.pireal_file import File
from pireal.dirs import DATA_SETTINGS, EXAMPLE_DB_FILENAME
from pireal.gui.database_container import DatabaseContainer
from pireal.gui.dialogs.new_db_dialog import NewDBInputDialog
from pireal.gui.dialogs.new_relation_dialog import NewRelationDialog
from pireal.gui.lateral_widget import LateralWidget, RelationItemType
from pireal.gui.table_widget import TableWidget
from pireal.registry import Registry
from pireal.utils import sanitize_data


class Controller(QWidget):
    """
    The main controller for the Pireal app.

    This class manage the core functionality  of the application.
    """

    def __init__(self):
        super().__init__()
        self._logger = structlog.get_logger().bind(component=self.__class__.__name__)

        box = QVBoxLayout(self)
        box.setContentsMargins(1, 1, 1, 1)

        self._stack = QStackedWidget()
        box.addWidget(self._stack)

        qsettings = QSettings(str(DATA_SETTINGS), QSettings.Format.IniFormat)
        self._last_open_folder: str = qsettings.value(
            "last_open_folder", type=str
        ) or str(Path.home())
        self._recent_databases: list[str] = qsettings.value(
            "recent_databases", type=list
        )

        self._logger.info("intialized")

    def add_widget(self, widget):
        index = self._stack.indexOf(widget)
        if index == -1:
            index = self._stack.addWidget(widget)
        self._stack.setCurrentIndex(index)

    @property
    def recent_databases(self) -> list[str]:
        return self._recent_databases.copy()

    def _remember_folder(self, filepath: str):
        """Actualiza la última carpeta usada basada en la ruta del archivo"""
        if filepath:
            folder = str(Path(filepath).parent)
            self._last_open_folder = folder

            qsettings = QSettings(str(DATA_SETTINGS), QSettings.Format.IniFormat)
            qsettings.setValue("last_open_folder", folder)

    def add_db_to_recents(self, db_filepath: str) -> None:
        if Path(db_filepath).resolve() == EXAMPLE_DB_FILENAME.resolve():
            self._logger.debug("skipping_example_db", filepath=db_filepath)
            return

        self._logger.info(
            "adding_to_recent_databases",
            filepath=db_filepath,
            current_count=len(self.recent_databases),
        )

        normalized_path = str(Path(db_filepath).resolve())

        if normalized_path in self._recent_databases:
            self._recent_databases.remove(normalized_path)

        self._recent_databases.insert(0, normalized_path)
        self._recent_databases = self._recent_databases[:10]  # FIXME: constant

        self._logger.debug(
            "recent_databases_updated",
            filepath=normalized_path,
            new_count=len(self.recent_databases),
        )

    @pyqtSlot()
    def create_database(self):
        db = Registry.get("db", DB)

        if db.is_active:
            self._show_one_database_warning()
            return

        database_filepath = NewDBInputDialog.ask_db_name(parent=self)
        if database_filepath is None:
            return

        db.is_active = True

        database_widget = Registry.get("database-container", DatabaseContainer)
        self.add_widget(database_widget)

    @pyqtSlot()
    def open_database(self, filename: str | Path = ""):
        """
        - si ya hay una db abierta, avisar y no hacer nada.
        - si no se proporciona un archivo, abrir el file dialog para seleccionar.
        - leer el archivo y sanitizar la data.
        - crear la db en el database container
        - agregar el container al stack
        - mostrar un mensaje en la toolbar del archivo abierto.
        - actualizar el titulo de la ventana con el nombre del archivo.
        - agregar la db a la lista de recientes.
        """

        if isinstance(filename, Path):
            filename = str(filename)

        db = Registry.get("db", DB)
        if db.is_active:
            self._logger.warning("database_already_active")
            self._show_one_database_warning()
            return

        if not filename:
            self._logger.info("filename_not_provided")
            filename, _ = QFileDialog.getOpenFileName(
                self, "Ola", self._last_open_folder, ""
            )
            if not filename:
                self._logger.info("filename_not_selected")
                return

        self._logger.info("opening_database", filename=filename)
        file = File(filename)
        content = sanitize_data(file.read())

        database_container = Registry.get("database-container", DatabaseContainer)
        database_container.create_database(content)
        self.add_widget(database_container)

        self._remember_folder(filename)
        self.add_db_to_recents(filename)

        db.is_active = True
        self._logger.info("database_opened")

    @pyqtSlot()
    def close_database(self):
        db = Registry.get("db", DB)

        if db.modified:
            value = QMessageBox.question(
                self,
                tr.TR_MSG_SAVE_CHANGES,
                tr.TR_MSG_SAVE_CHANGES_BODY,
                QMessageBox.StandardButton.Yes
                | QMessageBox.StandardButton.No
                | QMessageBox.StandardButton.Cancel,
            )
        db.is_active = False

    @pyqtSlot()
    def open_query(self, filename="", remember=True):
        if not filename:
            filename, _ = QFileDialog.getOpenFileName(
                self, "open quiery", self._last_open_folder, ""
            )
            if not filename:
                return

        self._remember_folder(filename)
        self.new_query(filename)

    @pyqtSlot()
    def new_query(self, filename: str = ""):
        database_widget = Registry.get("database-container", DatabaseContainer)
        database_widget.new_query(filename)

    @pyqtSlot()
    def save_query(self):
        pass

    @pyqtSlot()
    def save_query_as(self):
        pass

    @pyqtSlot()
    def close_query(self):
        pass

    @pyqtSlot()
    def execute_queries(self) -> None:
        database_widget = Registry.get("database-container", DatabaseContainer)
        database_widget.execute_queries()

    @pyqtSlot()
    def create_relation(self):
        def _create(relation, relation_name):
            relation.name = relation_name

            lateral_widget = Registry.get("lateral-widget", LateralWidget)
            table_widget = Registry.get("table-widget", TableWidget)

            table_widget.add_table_to_workspace(relation)
            lateral_widget.add_item(relation, relation_type=RelationItemType.Normal)

        new_relation_dialog = NewRelationDialog()
        new_relation_dialog.created.connect(_create)
        new_relation_dialog.exec()

    def _show_one_database_warning(self):
        QMessageBox.information(
            self, "ola", "Solo se puede tener una base de datos abierta a la vez."
        )
