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
from PyQt6.QtWidgets import QMessageBox, QStackedWidget, QVBoxLayout, QWidget

from pireal import translations as tr
from pireal.core.db import DB
from pireal.core.recent_databases import RecentDatabases
from pireal.dirs import DATA_SETTINGS
from pireal.gui.database_container import DatabaseContainer
from pireal.gui.dialogs.about_dialog import AboutDialog
from pireal.gui.lateral_widget import LateralWidget
from pireal.gui.query_widget import QueryWidget
from pireal.gui.services.database_service import DatabaseService
from pireal.gui.services.query_service import QueryService
from pireal.gui.table_widget import TableWidget
from pireal.registry import Registry

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
        last_folder: str = qsettings.value("last_open_folder", type=str) or str(Path.home())
        recent_items = qsettings.value("recent_databases", defaultValue=[], type=list) or []
        self._recents = RecentDatabases(recent_items)

        lateral_widget = Registry.get("lateral-widget", LateralWidget)
        db = Registry.get("db", DB)

        self._db_service = DatabaseService(
            db=db,
            recents=self._recents,
            parent_widget=self,
            last_folder=last_folder,
        )

        self._query_service = QueryService(
            db=db,
            parent_widget=self,
            last_folder=last_folder,
        )

        db.databaseStateChanged.connect(self._on_database_state_changed)
        lateral_widget.deleteRelationRequested.connect(self.remove_relation)

    def set_recent_databases(self, paths: list[str]) -> None:
        self._recents = RecentDatabases(paths)

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
        self._recents.remove(path)

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
            db.file = None

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
        return self._recents.all()

    def add_db_to_recents(self, db_filepath: str) -> None:
        self._recents.add(db_filepath)

    @pyqtSlot()
    def create_database(self):
        if self._db_service.create():
            self.add_widget(Registry.get("database-container", DatabaseContainer))

    @pyqtSlot()
    def open_database(self, filename: str):
        if self._db_service.open(filename):
            self.add_widget(Registry.get("database-container", DatabaseContainer))

    @pyqtSlot()
    def close_database(self):
        self._db_service.close()

    def save_database(self):
        self._db_service.save()

    def save_database_as(self):
        self._db_service.save_as()

    def create_database_from_text(self):
        pass

    @pyqtSlot()
    def open_query(self, filename: str):
        self._query_service.open(filename)

    @pyqtSlot()
    def new_query(self, filename: str):
        self._query_service.new(filename)

    @pyqtSlot()
    def save_query(self):
        self._query_service.save()

    @pyqtSlot()
    def save_query_as(self):
        self._query_service.save_as()

    @pyqtSlot()
    def close_query(self):
        self._query_service.close()

    @pyqtSlot()
    def execute_queries(self) -> None:
        self._query_service.execute()

    @pyqtSlot()
    def create_relation(self):
        pass

    @pyqtSlot()
    def about_pireal(self):
        dialog = AboutDialog(self)
        dialog.exec()

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

    def save_state(self) -> None:
        qsettings = QSettings(str(DATA_SETTINGS), QSettings.Format.IniFormat)
        qsettings.setValue("recent_databases", self._recents.all())
        last_folder = self._db_service.last_folder or self._query_service.last_folder
        qsettings.setValue("last_open_folder", last_folder)
