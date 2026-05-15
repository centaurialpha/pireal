import logging
from pathlib import Path

from PyQt6.QtWidgets import (
    QFileDialog,
    QMessageBox,
)

from pireal import translations as tr
from pireal.core.db import DB
from pireal.core.pireal_file import (
    File,
    is_example_file,
)
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
        if not is_example_file(File(filepath)):
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
            logger.warning("Database file not found: %s", filename)
            QMessageBox.warning(
                self._parent,
                tr.TR_MSG_FILE_NOT_FOUND_TITLE,
                tr.TR_MSG_FILE_NOT_FOUND_BODY.format(filename),
            )
            self._recents.remove(filename)
            return False

        content = sanitize_data(file.read())
        file_is_example = is_example_file(file)
        editable = not file_is_example

        database_container = Registry.get("database-container", DatabaseContainer)
        database_container.create_database(content, editable=editable)

        self._db.file = file
        self._db.is_active = True

        self._check_olakase_names()

        if not file_is_example:
            self._remember_folder(filename)
            self._recents.add(filename)

        logger.info("Database opened: %s", filename)
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

        logger.info("New database created: %s", filepath)
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

        logger.info("Database closed")
        self._db.is_active = False
        return True

    def save(self) -> bool:
        if not self._db.is_active or not self._db.modified:
            return False
        if self._db.is_new:
            return self.save_as()
        self._db.save()

        logger.info("Database saved: '%s'", self._db.file.path if self._db.file is not None else "")
        return True

    def save_as(self) -> bool:
        if not self._db.is_active:
            return False

        filename, _ = QFileDialog.getSaveFileName(
            self._parent,
            tr.TR_MSG_SAVE_DB_AS,
            self._last_folder,
            "Pireal Database File (*.pdb)",
        )
        if not filename:
            return False

        if not filename.endswith(".pdb"):
            filename += ".pdb"

        self._db.file = File(filename)
        self._db.save()
        self._remember_folder(filename)

        logger.info("Database saved as: '%s'", self._db.file.path if self._db.file is not None else "")
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
        self._check_olakase_names()
        return True

    def _warn_one_db(self) -> None:
        QMessageBox.information(
            self._parent,
            tr.TR_MSG_INFORMATION,
            tr.TR_MSG_ONE_DB_AT_TIME,
        )

    def _check_olakase_names(self) -> None:
        from pireal.core.olakase import check_relation
        from pireal.gui.status_bar import StatusBar

        for name in self._db.relations_dict():
            if check_relation(name) is not None:
                status_bar = Registry.get("status-bar", StatusBar)
                status_bar.show_message("buena elección de nombre", timeout=5000)
                break
