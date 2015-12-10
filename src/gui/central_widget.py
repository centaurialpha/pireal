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

from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QStackedWidget,
    QFileDialog,
    QMessageBox
)

from src.core import (
    settings,
    file_manager,
    pfile
)
from src import translations as tr
from src.gui.main_window import Pireal
from src.gui import start_page, main_container
from src.gui.dialogs import (
    preferences,
    new_relation_dialog
)


class CentralWidget(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        box = QVBoxLayout(self)
        box.setContentsMargins(0, 0, 0, 0)

        self.stacked = QStackedWidget()
        box.addWidget(self.stacked)

        self.__ndb = 1
        self.__created = False
        self.__last_open_folder = None

        Pireal.load_service("central", self)

    def open_file(self, filename=''):
        if self.__last_open_folder is None:
            directory = os.path.expanduser("~")
        else:
            directory = self.__last_open_folder

        if not filename:
            filename = QFileDialog.getOpenFileName(self,
                                                   tr.TR_CENTRAL_OPEN_FILE,
                                                   directory,
                                                   settings.SUPPORTED_FILES)[0]
            if not filename:
                return

        # Save folder
        self.__last_open_folder = file_manager.get_path(filename)

        extension = file_manager.get_extension(filename)
        if extension == '.pqf':
            if not self.created:
                QMessageBox.information(self, tr.TR_CENTRAL_INFORMATION,
                                        tr.TR_CENTRAL_FIRST_CREATE_DB)
                return
            # Open a query file
        else:
            # Open a database file
            self.create_database(filename)

    def create_database(self, filename=''):
        """ This function opens or creates a database """

        # Only one database
        if self.created:
            QMessageBox.critical(self, "Error", tr.TR_CENTRAL_ERROR_DB)
            return

        # File
        ffile = pfile.PFile(filename)

        main = main_container.MainContainer(ffile)
        self.add_widget(main)

        if not filename:
            ffile.complete_name(self.__ndb, 'pdb')
            db_name = main.dbname()
            #db_name = main.dbname().format(self.__ndb, 'pdb')

        else:
            try:
                data = ffile.read()
            except Exception as reason:
                QMessageBox.critical(self, "Error", reason.__str__())
                return

            db_name = ffile.name
            main.create_database(data)

        pireal = Pireal.get_service("pireal")
        pireal.change_title(db_name)
        pireal.enable_disable_db_actions()
        self.created = True
        self.__ndb += 1

    def close_database(self):
        mcontainer = self.get_active_db()
        if mcontainer is not None:
            if mcontainer.modified:
                flags = QMessageBox.Cancel
                flags |= QMessageBox.No
                flags |= QMessageBox.Yes
                r = QMessageBox.question(self, tr.TR_CENTRAL_DB_UNSAVED_TITLE,
                                         tr.TR_CENTRAL_DB_UNSAVED_MSG.format(
                                             mcontainer.dbname()), flags)
                if r == QMessageBox.Cancel:
                    return
                if r == QMessageBox.Yes:
                    self.save_database()

            self.stacked.removeWidget(mcontainer)

            del mcontainer

            pireal = Pireal.get_service("pireal")
            pireal.enable_disable_db_actions(False)
            self.created = False

    def new_query(self):
        pireal = Pireal.get_service("pireal")
        pireal.enable_disable_query_actions()
        main_container = self.get_active_db()
        main_container.new_query()

    def execute_queries(self):
        main_container = self.get_active_db()
        main_container.execute_queries()

    def save_database(self):
        pass

    def remove_relation(self):
        main_container = self.get_active_db()
        main_container.delete_relation()

    def create_new_relation(self):
        dialog = new_relation_dialog.NewRelationDialog(self)
        dialog.show()

    def load_relation(self, filename=''):
        """ Load Relation file """

        if not filename:
            if self.__last_open_folder is None:
                directory = os.path.expanduser("~")
            else:
                directory = self.__last_open_folder

            msg = tr.TR_CENTRAL_OPEN_RELATION
            filter_ = settings.SUPPORTED_FILES.split(';;')[-1]
            filenames = QFileDialog.getOpenFileNames(self, msg, directory,
                                                    filter_)[0]

            if not filenames:
                return

        # Save folder
        self.__last_open_folder = file_manager.get_path(filenames[0])
        main_container = self.get_active_db()
        main_container.load_relation(filenames)

    def add_start_page(self):
        """ This function adds the Start Page to the stacked widget """

        sp = start_page.StartPage()
        self.add_widget(sp)

    #def add_main_container(self):
        #main = Pireal.get_service("main")
        #self.add_widget(main)

    def __get_created(self):
        return self.__created

    def __set_created(self, value):
        self.__created = value

    created = property(__get_created, __set_created)

    def show_settings(self):
        preferences_dialog = preferences.Preferences(self)

        if isinstance(self.widget(1), preferences.Preferences):
            self.widget(1).close()
        else:
            self.stacked.insertWidget(1, preferences_dialog)
            self.stacked.setCurrentIndex(1)

        # Connect the closed signal
        preferences_dialog.settingsClosed.connect(self._settings_closed)

    def widget(self, index):
        """ Returns the widget at the given index """

        return self.stacked.widget(index)

    def add_widget(self, widget):
        """ Appends and show the given widget to the Stacked """

        index = self.stacked.addWidget(widget)
        self.stacked.setCurrentIndex(index)

    def _settings_closed(self):
        self.stacked.removeWidget(self.widget(1))
        self.stacked.setCurrentWidget(self.stacked.currentWidget())

    def get_active_db(self):
        """ Return an instance of Main Conatainer widget if the
        stacked contains an Main Container in last index or None if it's
        not an instance of Main Container """

        index = self.stacked.count() - 1
        widget = self.widget(index)
        if isinstance(widget, main_container.MainContainer):
            return widget
        return None


central = CentralWidget()
