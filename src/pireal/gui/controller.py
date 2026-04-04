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

import logging
from pathlib import Path

from PyQt6.QtCore import QSettings, pyqtSlot
from PyQt6.QtWidgets import QFileDialog, QMessageBox, QStackedWidget, QVBoxLayout, QWidget

from pireal import translations as tr
from pireal.core.db import DB
from pireal.core.pireal_file import File, is_example_file
from pireal.dirs import DATA_SETTINGS
from pireal.gui.database_container import DatabaseContainer
from pireal.gui.dialogs.new_db_dialog import NewDBInputDialog
from pireal.gui.dialogs.new_relation_dialog import NewRelationDialog
from pireal.gui.lateral_widget import LateralWidget, RelationItemType
from pireal.gui.query_widget import QueryWidget
from pireal.gui.table_widget import TableWidget
from pireal.registry import Registry
from pireal.resources import sample
from pireal.utils import sanitize_data

logger = logging.getLogger(__name__)


class Controller(QWidget):
    """
    The main controller for the Pireal app.

    This class manage the core functionality  of the application.
    """

    def __init__(self):
        super().__init__()

        box = QVBoxLayout(self)
        box.setContentsMargins(1, 1, 1, 1)

        self._stack = QStackedWidget()
        box.addWidget(self._stack)

        qsettings = QSettings(str(DATA_SETTINGS), QSettings.Format.IniFormat)
        self._last_open_folder: str = qsettings.value("last_open_folder", type=str) or str(Path.home())
        self._recent_databases: list[str] = qsettings.value("recent_databases", type=list)

        lateral_widget = Registry.get("lateral-widget", LateralWidget)
        db = Registry.get("db", DB)

        db.databaseStateChanged.connect(self._on_database_state_changed)
        lateral_widget.deleteRelationRequested.connect(self.remove_relation)

    @pyqtSlot()
    def add_relations_from_text(self):
        from pireal.gui.dialogs.db_from_text_dialog import DBFromTextDialog

        dialog = DBFromTextDialog(self)
        if dialog.exec() != DBFromTextDialog.DialogCode.Accepted:
            return

        data = dialog.parsed_data()
        if not data:
            return

        database_container = Registry.get("database-container", DatabaseContainer)
        database_container.create_database(data)

    def remove_from_recents(self, path: str):
        normalized = str(Path(path).resolve())
        if normalized in self._recent_databases:
            self._recent_databases.remove(normalized)

    @pyqtSlot(int)
    def remove_relation(self, index: int):
        lateral_widget = Registry.get("lateral-widget", LateralWidget)
        db = Registry.get("db", DB)

        relation_name = lateral_widget._relations_model.relation_by_index(index).name

        ret = QMessageBox.question(
            self,
            tr.TR_MENU_SCHEME_REMOVE_RELATION,
            tr.TR_MSG_REMOVE_RELATION.format(relation_name),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel,
        )
        if ret != QMessageBox.StandardButton.Yes:
            return

        db.remove(relation_name)
        lateral_widget.remove_relation(index)

        table_widget = Registry.get("table-widget", TableWidget)
        table_widget.remove_relation(relation_name)

    @pyqtSlot(bool)
    def _on_database_state_changed(self, active: bool):
        db = Registry.get("db", DB)
        if not active:
            lateral_widget = Registry.get("lateral-widget", LateralWidget)
            table_widget = Registry.get("table-widget", TableWidget)
            query_widget = Registry.get("query-widget", QueryWidget)

            lateral_widget.clear()
            lateral_widget.clear_results()
            table_widget.clear()
            query_widget.clear()
            db._file = None

            from pireal.gui.start_page import StartPage

            start_page = Registry.get("start-page", StartPage)
            self.add_widget(start_page)

    def add_widget(self, widget):
        index = self._stack.indexOf(widget)
        if index == -1:
            index = self._stack.addWidget(widget)
        self._stack.setCurrentIndex(index)

    @property
    def recent_databases(self) -> list[str]:
        return self._recent_databases.copy()

    def _remember_folder(self, filename: str):
        """Actualiza la última carpeta usada basada en la ruta del archivo"""
        if filename:
            filepath = Path(filename)
            folder = str(filepath.parent)
            if is_example_file(filepath):
                logger.debug("Skipping example folder: '%s'", folder)
                return

            self._last_open_folder = folder

            qsettings = QSettings(str(DATA_SETTINGS), QSettings.Format.IniFormat)
            qsettings.setValue("last_open_folder", folder)

    def add_db_to_recents(self, db_filepath: str) -> None:
        if Path(db_filepath).resolve() == Path(sample("database.pdb")).resolve():
            logger.debug("Skipping example database: '%s'", db_filepath)
            return

        logger.info(
            "Adding to recent databases, filepath='%s' - current_count='%d'",
            db_filepath,
            len(self.recent_databases),
        )

        normalized_path = str(Path(db_filepath).resolve())

        if normalized_path in self._recent_databases:
            self._recent_databases.remove(normalized_path)

        self._recent_databases.insert(0, normalized_path)
        self._recent_databases = self._recent_databases[:10]  # FIXME: constant

        logger.debug(
            "Recent databases updated, filepath='%s' - new_count='%d'",
            normalized_path,
            len(self.recent_databases),
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

        db.file = File(database_filepath)
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
            logger.warning("Database already active")
            self._show_one_database_warning()
            return

        if not filename:
            logger.info("Filename not provided")
            filename, _ = QFileDialog.getOpenFileName(
                self, tr.TR_OPEN_DB, self._last_open_folder, "Pireal Database (*.pdb)"
            )
            if not filename:
                logger.info("Filename not selected")
                return

        logger.info("Opening database '%s'", filename)
        file = File(filename)
        if not file.exists:
            QMessageBox.warning(
                self,
                tr.TR_MSG_FILE_NOT_FOUND_TITLE,
                tr.TR_MSG_FILE_NOT_FOUND_BODY.format(filename),
            )
            return
        content = sanitize_data(file.read())

        database_container = Registry.get("database-container", DatabaseContainer)
        database_container.create_database(content)
        self.add_widget(database_container)

        self._remember_folder(filename)
        self.add_db_to_recents(filename)

        db.file = file
        db.is_active = True
        logger.info("Database opened")

    @pyqtSlot()
    def close_database(self):
        db = Registry.get("db", DB)
        if not db.is_active:
            return

        if db.modified and not is_example_file(db.file):
            value = QMessageBox.question(
                self,
                tr.TR_MSG_SAVE_CHANGES,
                tr.TR_MSG_SAVE_CHANGES_BODY,
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel,
            )
            if value == QMessageBox.StandardButton.Cancel:
                return

            if value == QMessageBox.StandardButton.Yes:
                self.save_database()

        db.is_active = False

    @pyqtSlot()
    def open_query(self, filename="", remember=True):
        if not filename:
            filename, _ = QFileDialog.getOpenFileName(
                self, tr.TR_OPEN_QUERY, self._last_open_folder, "Pireal Query (*.qrf)"
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
        query_widget = Registry.get("query-widget", QueryWidget)
        editor = query_widget.current_editor()
        if editor is None:
            return
        if editor.file.is_new:
            return self.save_query_as()
        editor.file.save(editor.text())
        editor.saved()

    @pyqtSlot()
    def save_query_as(self):
        query_widget = Registry.get("query-widget", QueryWidget)
        editor = query_widget.current_editor()
        if editor is None:
            return
        filename, _ = QFileDialog.getSaveFileName(
            self,
            tr.TR_MSG_SAVE_QUERY_FILE,
            self._last_open_folder,
            "Pireal Query File (*.pqf)",
        )
        if not filename:
            return
        if not filename.endswith(".pqf"):
            filename += ".pqf"
        editor.file = File(filename)
        editor.file.save(editor.text())
        editor.saved()
        self._remember_folder(filename)

    @pyqtSlot()
    def close_query(self):
        query_widget = Registry.get("query-widget", QueryWidget)
        query_widget.close_current_editor()

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

    @pyqtSlot()
    def about_pireal(self):
        from pireal.gui.dialogs.about_dialog import AboutDialog

        dialog = AboutDialog(self)
        dialog.exec()

    def _show_one_database_warning(self):
        QMessageBox.information(self, "ola", "Solo se puede tener una base de datos abierta a la vez.")

    def save_database(self):
        db = Registry.get("db", DB)
        if not db.is_active or not db.modified:
            return

        if db.is_new:
            return self.save_database_as()

        db.save()

    def save_database_as(self):
        db = Registry.get("db", DB)
        if not db.is_active:
            return

        filename, _ = QFileDialog.getSaveFileName(
            self,
            tr.TR_MSG_SAVE_DB_AS,
            self._last_open_folder,
            "Pireal Database File (*.pdb)",
        )
        if not filename:
            return

        if not filename.endswith(".pdb"):
            filename += ".pdb"

        db._file = File(filename)
        db.save()
        self._remember_folder(filename)

    def create_database_from_text(self):
        db = Registry.get("db", DB)
        if db.is_active:
            self._show_one_database_warning()
            return

        from pireal.gui.dialogs.db_from_text_dialog import DBFromTextDialog

        dialog = DBFromTextDialog(self)
        if dialog.exec() != DBFromTextDialog.DialogCode.Accepted:
            return

        data = dialog.parsed_data()
        if not data:
            return

        database_container = Registry.get("database-container", DatabaseContainer)
        database_container.create_database(data)
        self.add_widget(database_container)
        db.is_active = True

    @pyqtSlot()
    def quit(self):
        from pireal.gui.main_window import Pireal

        Pireal.instance().close()

    @pyqtSlot()
    def show_tour(self):
        from pireal.gui.dialogs.tour_dialog import WelcomeDialog

        dialog = WelcomeDialog(self)
        dialog.exec()

    @pyqtSlot()
    def report_issue(self):
        from PyQt6.QtCore import QUrl
        from PyQt6.QtGui import QDesktopServices

        QDesktopServices.openUrl(QUrl("https://github.com/centaurialpha/pireal/issues"))

    @pyqtSlot()
    def about_qt(self):
        from PyQt6.QtWidgets import QApplication

        QApplication.aboutQt()

    @pyqtSlot()
    def send_feedback(self):
        from pireal.gui.dialogs.feedback_dialog import FeedbackDialog

        dialog = FeedbackDialog(self)
        dialog.exec()
