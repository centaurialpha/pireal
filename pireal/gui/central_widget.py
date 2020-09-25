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

import logging
import os

from PyQt5.QtCore import pyqtSlot as Slot
from PyQt5.QtCore import pyqtSignal as Signal
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QStackedLayout, QWidget

from pireal import translations as tr
from pireal.core import file_manager, settings, file_utils
from pireal.core.db import DB
from pireal.core.settings import DATA_SETTINGS, USER_SETTINGS
from pireal.gui import start_page
from pireal.gui.dialogs import new_relation_dialog
# from pireal.gui.dialogs.new_database_dialog import NewDBDialog
from pireal.gui.dialogs import DBInputDialog
from pireal.gui.dialogs import PreferencesDialog
# from pireal.gui.main_panel import MainPanel
from pireal.gui.database_panel import DBPanel
from pireal.dirs import DATABASES_DIR

# Logger
logger = logging.getLogger('gui.central_widget')


class CentralWidget(QWidget):

    dbOpened = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.pireal = parent
        self.db_panel: DBPanel = None
        self._stacked = QStackedLayout(self)
        if self.pireal is not None:
            self.add_start_page()
        self._last_open_folder: str = DATA_SETTINGS.value('lastOpenFolder')
        self._recent_dbs: list = DATA_SETTINGS.value('recentDbs', [], type=list)

    @property
    def recent_databases(self) -> list:
        return self._recent_dbs

    def remember_recent_database(self, path: str):
        if path in self._recent_dbs:
            self._recent_dbs.remove(path)
        self._recent_dbs.insert(0, path)

    def remove_db_from_recents(self, path: str):
        if path in self._recent_dbs:
            self._recent_dbs.remove(path)

    @property
    def last_open_folder(self) -> str:
        return self._last_open_folder

    @Slot(object)
    def _on_db_loaded(self, db):
        self.remove_start_page()
        self.pireal.update_title()
        self.pireal.show_status_message(f'Database {db.file_path()} loaded')
        self.remember_recent_file(db.file_path())

    def has_db(self) -> bool:
        return self.db_panel is not None

    def create_database(self):
        """Show a wizard widget to create a new empty database,
        only have one database open at time."""

        if self.has_db():
            return self._say_about_one_db_at_time()
        db_filepath = DBInputDialog.ask_db_name(parent=self)
        if db_filepath:
            logger.debug('Creating new DB as %s...', db_filepath)
            db = DB()
            self.db_panel = DBPanel(db, parent=self)
            self.remove_start_page()
            index = self._stacked.addWidget(self.db_panel)
            self._stacked.setCurrentIndex(index)

    def _say_about_one_db_at_time(self):
        logger.info("Oops! One database at a time please")
        QMessageBox.information(
            self,
            tr.TR_MSG_INFORMATION,
            tr.TR_MSG_ONE_DB_AT_TIME
        )

    def open_database(self, filename=''):
        if self.has_db():
            return self._say_about_one_db_at_time()
        # If not filename provide, then open dialog to select one
        if not filename:
            if self._last_open_folder is None:
                directory = os.path.expanduser('~')
            else:
                directory = self._last_open_folder
            filename, _ = QFileDialog.getOpenFileName(
                self,
                tr.TR_OPEN_DATABASE,
                directory,
                settings.get_extension_filter('.pdb')
            )
            # If is canceled, return
            if not filename:
                logger.info('File not selected, bye!')
                return

        try:
            db = DB.load_from_file(filename)
        except IOError as reason:
            QMessageBox.critical(self, tr.TR_MSG_ERROR, str(reason))
            return

        self.db_panel = DBPanel(db, parent=self)

        # First remove start page
        # FIXME: mejorar ?
        self.remove_start_page()

        index = self._stacked.addWidget(self.db_panel)
        self._stacked.setCurrentIndex(index)
        # Save last folder
        self._last_open_folder = file_utils.get_path(filename)
        # FIXME: considerar emitir una señal, mas testeable
        self.dbOpened.emit(filename)

        logger.debug('Connected to database: %s', db.display_name())

    def close_database(self):
        """ Close the database and return to the main widget """
        if not self.has_db():
            return
        if self.db_panel.db.is_dirty():
            reply = QMessageBox.question(
                self, tr.TR_MSG_SAVE_CHANGES,
                tr.TR_MSG_SAVE_CHANGES_BODY,
                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
            )
            actions = {
                QMessageBox.Cancel: lambda: None,
                QMessageBox.Yes: lambda: None,
                QMessageBox.No: lambda: None
            }
            actions[reply]()

        # TODO: ask for unsaved queries
        logger.info('Closing database %s', self.db_panel.db.display_name())
        self._stacked.removeWidget(self.db_panel)
        self.db_panel = None
        self.add_start_page()

    def save_database(self):
        if self.has_db():
            self._main_panel.save_database()

    def save_database_as(self):
        if self.has_db():
            self._main_panel.save_database_as()

    def create_relation(self):
        if not self.has_db():
            return
        dialog = new_relation_dialog.NewRelationDialog(self)
        if dialog.exec_():
            # Agregar a la tabla principal
            # agregar a la lista
            # ahora la DB fué modificada, notificar
            relation = dialog.get_data()
            self.db_panel.add_relation(relation)
            # self.db.add(relation)
            # main_panel = self.get_main_panel()
            # main_panel.load_relations()

    @Slot()
    def open_query(self, filename=''):
        if not self.has_db():
            logger.info('There is no active DB')
            return
        if not filename:
            directory = os.path.expanduser('~')  # FIXME: remember
            filenames, ok = QFileDialog.getOpenFileNames(
                self, tr.TR_OPEN_QUERY, directory, settings.get_extension_filter('.pqf')
            )
        else:
            filenames = [filename]
        for filename in filenames:
            self.db_panel.add_query(filename)

    def new_query(self):
        if not self.has_db():
            return
        self.db_panel.new_query()

    @Slot()
    def save_query(self, editor=None):
        if not self.has_db():
            return
        main_panel = self.get_main_panel()
        if editor is None:
            editor = main_panel.query_container.get_current_editor()
            if editor is None:
                return
        # Ok, we have an editor instance
        if editor.is_modified:
            if editor.file.is_new:
                return self.save_query_as()
            content = editor.toPlainText()
            editor.file.save(content)
            editor.document().setModified(False)

    def save_query_as(self):
        if not self.has_db():
            return
        main_panel = self.get_main_panel()
        editor = main_panel.query_container.get_current_editor()
        if editor is None:
            return
        if editor.file.path:
            save_folder = file_manager.get_path(editor.file.path)
        else:
            save_folder = self._last_open_folder
        filename, ok = QFileDialog.getSaveFileName(
            self,
            tr.TR_MENU_QUERY_SAVE_AS_QUERY,
            save_folder
        )
        if not ok:
            return
        content = editor.toPlainText()
        if not filename.endswith('.pqf'):
            filename = f'{filename}.pqf'
        editor.file.save(content, path=filename)
        editor.document().setModified(False)

    def close_query(self):
        if not self.has_db():
            return
        main_panel = self.get_main_panel()
        main_panel.close_query()

    def execute_query(self):
        if self.has_db():
            relations = self.db_panel.db._relations
            self.db_panel.query_widget.execute_query(relations)

    def add_start_page(self):
        """ This function adds the Start Page to the stacked widget """
        sp = start_page.StartPage(self)
        index = self._stacked.addWidget(sp)
        self._stacked.setCurrentIndex(index)

    def remove_start_page(self):
        start_page_widget = self._stacked.widget(0)
        if isinstance(start_page_widget, start_page.StartPage):
            self._stacked.removeWidget(start_page_widget)

    def show_preferences(self):
        """ Show settings dialog on stacked """

        preferences_dialog = PreferencesDialog(self)
        preferences_dialog.settingsChanged.connect(self._on_settings_changed)
        preferences_dialog.show()

    @Slot()
    def _on_settings_changed(self):
        if not self.has_db():
            return
        editors = self._main_panel.query_container.editor_widget.editors()
        if not editors:
            return
        logger.debug('updating settings in all editors')
        for editor in editors:
            # Update font
            editor.set_font(
                USER_SETTINGS.font_family,
                USER_SETTINGS.font_size
            )
            editor.set_highlight_line(USER_SETTINGS.highlight_current_line)
            editor.set_match_parenthesis(USER_SETTINGS.match_parenthesis)

    # def save_state(self):
    #     """Save splitter states"""
    #     if self.has_db():
    #         DATA_SETTINGS.setValue(
    #             'db_panel_state', self.db_panel.saveState())
    #         # DATA_SETTINGS.setValue(
    #         #     'query_container_state', main_panel._vertical_splitter.saveState())
