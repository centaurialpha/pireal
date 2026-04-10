import logging
from pathlib import Path

from PyQt6.QtWidgets import QFileDialog, QMessageBox

from pireal import translations as tr
from pireal.core.db import DB
from pireal.core.pireal_file import File, is_example_file
from pireal.core.recent_databases import RecentDatabases
from pireal.gui.database_container import DatabaseContainer
from pireal.gui.dialogs.db_from_text_dialog import DBFromTextDialog
from pireal.gui.dialogs.new_db_dialog import NewDBInputDialog
from pireal.registry import Registry
from pireal.utils import sanitize_data

logger = logging.getLogger(__name__)


class DatabaseService:
    def __init__(self, db: DB, recents: RecentDatabases, last_folder: str = "", parent_widget=None):
        self._db = db
        self._recents = recents
        self._parent = parent_widget
        self._last_folder = last_folder or str(Path.home())

    def _remember_folder(self, filepath: str) -> None:
        self._last_folder = str(Path(filepath).parent)

    @property
    def last_folder(self) -> str:
        return self._last_folder

    def open(self, filename: str = "") -> bool:
        if self._db.is_active:
            self._warn_one_db()
            return False

        if not filename:
            filename, _ = QFileDialog.getOpenFileName(
                self._parent,
                tr.TR_OPEN_DB,
                self.last_folder,
                "Pireal Database (*.pdb)",
            )
            if not filename:
                return False

        logger.info("Opening database '%s'", filename)
        file = File(filename)
        if not file.exists:
            QMessageBox.warning(
                self._parent,
                tr.TR_MSG_FILE_NOT_FOUND_TITLE,
                tr.TR_MSG_FILE_NOT_FOUND_BODY.format(filename),
            )
            return False

        content = sanitize_data(file.read())

        database_container = Registry.get("database-container", DatabaseContainer)
        database_container.create_database(content)

        self._db.file = file
        self._db.is_active = True

        self._remember_folder(filename)
        self._recents.add(filename)

        logger.info("Database opened")
        return True

    def create(self) -> bool:
        if self._db.is_active:
            self._warn_one_db()
            return False

        filepath = NewDBInputDialog.ask_db_name(parent=self._parent)
        if filepath is None:
            return False

        self._db.file = File(filepath)
        self._db.is_active = True
        return True

    def close(self) -> bool:
        if not self._db.is_active:
            return False

        if self._db.modified and not is_example_file(self._db.file):
            answer = QMessageBox.question(
                self._parent,
                tr.TR_MSG_SAVE_CHANGES,
                tr.TR_MSG_SAVE_CHANGES_BODY,
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel,
            )
            if answer == QMessageBox.StandardButton.Cancel:
                return False
            if answer == QMessageBox.StandardButton.Yes:
                self.save()

        self._db.is_active = False
        return True

    def save(self) -> bool:
        if not self._db.is_active or not self._db.modified:
            return False
        if self._db.is_new:
            return self.save_as()
        self._db.save()
        return True

    def save_as(self) -> bool:
        if not self._db.is_active:
            return False

        filename, _ = QFileDialog.getSaveFileName(
            self._parent,
            tr.TR_MSG_SAVE_DB_AS,
            "",
            "Pireal Database File (*.pdb)",
        )
        if not filename:
            return False

        if not filename.endswith(".pdb"):
            filename += ".pdb"

        self._db.file = File(filename)
        self._db.save()
        self._remember_folder(filename)

        return True

    def create_from_text(self) -> bool:
        if self._db.is_active:
            self._warn_one_db()
            return False

        dialog = DBFromTextDialog(self._parent)
        if dialog.exec() != DBFromTextDialog.DialogCode.Accepted:
            return False

        data = dialog.parsed_data()
        if not data:
            return False

        database_container = Registry.get("database-container", DatabaseContainer)
        database_container.create_database(data)
        self._db.is_active = True
        return True

    def _warn_one_db(self) -> None:
        QMessageBox.information(
            self._parent,
            tr.TR_MSG_INFORMATION,
            tr.TR_MSG_ONE_DB_AT_TIME,
        )
