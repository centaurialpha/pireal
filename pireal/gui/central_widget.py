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

import os
import logging

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QStackedLayout
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox

from PyQt5.QtCore import pyqtSlot as Slot
from pireal import translations as tr
from pireal.core import settings
from pireal.core import file_manager

from pireal.gui import start_page
from pireal.gui.main_panel import MainPanel

from pireal.gui.dialogs import preferences
from pireal.gui.dialogs import new_relation_dialog
from pireal.gui.dialogs import new_database_dialog

from pireal.core.settings import DATA_SETTINGS

# Logger
logger = logging.getLogger(__name__)


class CentralWidget(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.pireal = parent
        self._stacked = QStackedLayout(self)
        self._main_panel = None
        self.add_start_page()
        self._last_open_folder: str = DATA_SETTINGS.value('lastOpenFolder')
        self._recent_dbs: list = DATA_SETTINGS.value('recentDbs', [], type=list)

    @property
    def recent_databases(self) -> list:
        return self._recent_dbs

    def remember_recent_file(self, path: str):
        recents = self._recent_dbs
        if path in recents:
            recents.remove(path)
        recents.insert(0, path)
        self._recent_dbs = recents

    def remove_from_recents(self, path: str):
        if path in self._recent_dbs:
            self._recent_dbs.remove(path)

    @property
    def last_open_folder(self):
        return self._last_open_folder

    def _create_main_panel(self):
        if self._main_panel is not None:
            return
        self._main_panel = MainPanel(self)
        self._main_panel.dbLoaded.connect(self._on_db_loaded)
        self.add_widget(self._main_panel)

    @Slot(object)
    def _on_db_loaded(self, db):
        self.remove_start_page()
        self.pireal.update_title()
        self.remember_recent_file(db.file_path())

    def create_database(self):
        """Show a wizard widget to create a new empty database,
        only have one database open at time."""

        if self.has_main_panel():
            return self._say_about_one_db_at_time()
        logger.debug('Creating a new empty database')
        dialog = new_database_dialog.NewDatabaseDialog(self)
        if dialog.exec_() == dialog.Accepted:
            self._create_main_panel()
            self._main_panel.create_db(dialog.data['file_path'])

    def has_main_panel(self):
        return self._main_panel is not None

    def _say_about_one_db_at_time(self):
        logger.warning("Oops! One database at a time please")
        QMessageBox.information(self, tr.TR_MSG_INFORMATION, tr.TR_MSG_ONE_DB_AT_TIME)

    def open_database(self, filename=''):
        if self.has_main_panel():
            return self._say_about_one_db_at_time()
        # If not filename provide, then open dialog to select one
        if not filename:
            if self._last_open_folder is None:
                directory = os.path.expanduser('~')
            else:
                directory = self._last_open_folder
            filename, _ = QFileDialog.getOpenFileName(
                self, tr.TR_OPEN_DATABASE, directory, settings.get_extension_filter('.pdb'))
            # If is canceled, return
            if not filename:
                logger.info('File not selected, bye!')
                return
        # Create main panel for table view
        self._create_main_panel()
        self._main_panel.load_database(filename)
        # Save last folder
        self._last_open_folder = file_manager.get_path(filename)

        self.add_widget(self._main_panel)

    def open_query(self, filename=''):
        if not filename:
            directory = os.path.expanduser('~')
            # FIXME: hacer un settings.get_supported_files(query) o algo así
            filters = settings.SUPPORTED_FILES.split(';;')[1]
            filename, _ = QFileDialog.getOpenFileName(self, tr.TR_OPEN_QUERY, directory, filters)
            if not filename:
                return
        self._main_panel.query_container.open_query(filename)
        # TODO:
        # Tengo el filename, si ya está abierto, ir a ese tab
        # Sino, crear un nuevo editor con el contenido

    def new_query(self):
        pass

    def remove_main_panel(self):
        if not isinstance(self._stacked.currentWidget(), MainPanel):
            return
        self._stacked.removeWidget(self._stacked.currentWidget())
        self._main_panel = None
        self.add_start_page()
        self.pireal.update_title()

    def close_database(self):
        """ Close the database and return to the main widget """

        if self.has_main_panel():
            self._main_panel.close_database()
            self.remove_main_panel()

    def execute_query(self):
        if self.has_main_panel():
            self._main_panel.execute_query()

    def save_database(self):
        if self.has_main_panel():
            self._main_panel.save_database()

    def save_database_as(self):
        if self.has_main_panel():
            self._main_panel.save_database_as()

    def create_relation(self):
        dialog = new_relation_dialog.NewRelationDialog(self)
        if dialog.exec_():
            relation = dialog.get_data()
            self._main_panel.add_relation(relation)

    def add_start_page(self):
        """ This function adds the Start Page to the stacked widget """

        sp = start_page.StartPage(self)
        self.add_widget(sp)

    def remove_start_page(self):
        start_page_widget = self._stacked.widget(0)
        if isinstance(start_page_widget, start_page.StartPage):
            self._stacked.removeWidget(start_page_widget)

    def show_settings(self):
        """ Show settings dialog on stacked """

        preferences_dialog = preferences.Preferences(self)
        preferences_dialog.show()

    def add_widget(self, widget):
        """ Appends and show the given widget to the Stacked """

        index = self._stacked.addWidget(widget)
        self._stacked.setCurrentIndex(index)
