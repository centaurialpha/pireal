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
from PyQt5.QtCore import pyqtSignal

from src.core import (
    settings,
    file_manager,
    pfile
)
from src.core.logger import PirealLogger
from src.gui.main_window import Pireal
from src.gui import (
    start_page,
    database_container
)
from src.gui.dialogs import (
    preferences,
    database_wizard,
    relation_manager
)

# Logger
logger = PirealLogger(__name__)
CRITICAL = logger.critical
DEBUG = logger.debug

# FIXME: Refactoring


class CentralWidget(QWidget):
    databaseSaved = pyqtSignal('QString')

    def __init__(self):
        QWidget.__init__(self)
        box = QVBoxLayout(self)
        box.setContentsMargins(0, 0, 0, 0)
        box.setSpacing(0)

        self.stacked = QStackedWidget()
        box.addWidget(self.stacked)

        self.__created = False
        self.__last_open_folder = None
        self.__recent_files = set()

        Pireal.load_service("central", self)

    def create_database(self):
        if self.__created:
            QMessageBox.information(self,
                                    self.tr("Information"),
                                    self.tr("You may only have one database"
                                            "open at time."))
            return
        wizard = database_wizard.DatabaseWizard(self)
        wizard.wizardFinished.connect(
            self.__on_wizard_finished)
        # Hide menubar and toolbar
        pireal = Pireal.get_service("pireal")
        pireal.menuBar().hide()
        pireal.toolbar.hide()
        # Add wizard widget to stacked
        self.add_widget(wizard)

    def __on_wizard_finished(self, data, wizard_widget):
        pireal = Pireal.get_service("pireal")
        if not data:
            self.remove_last_widget()
        else:
            db_container = database_container.DatabaseContainer()
            pfile_object = pfile.PFile(data['filename'])
            db_container.pfile = pfile_object
            self.add_widget(db_container)
            # Remove wizard
            self.stacked.removeWidget(wizard_widget)
            # Title
            pireal.change_title(file_manager.get_basename(data['filename']))
            # Enable db actions
            pireal.set_enabled_db_actions(True)
            pireal.set_enabled_relation_actions(True)
            self.__created = True

        # If data or not, show menubar and toolbar again
        # Show menubar and toolbar
        pireal.menuBar().setVisible(True)
        pireal.toolbar.setVisible(True)

    def open_database(self, filename=''):
        """ This function opens a database and set this on the UI """

        # If not filename provide, then open dialog to select
        if not filename:
            if self.__last_open_folder is None:
                directory = os.path.expanduser("~")
            else:
                directory = self.__last_open_folder
            filter_ = settings.SUPPORTED_FILES.split(';;')[0]
            filename = QFileDialog.getOpenFileName(self,
                                                   self.tr("Open Database"),
                                                   directory,
                                                   filter_)[0]
            # If is canceled, return
            if not filename:
                return

            # Remember the folder
            self.__last_open_folder = file_manager.get_path(filename)

        # If filename provide
        try:
            # Read pdb file
            pfile_object = pfile.PFile(filename)
            db_data = pfile_object.read()
            db_data = self.__sanitize_data(db_data)
        except Exception as reason:
            QMessageBox.information(self,
                                    self.tr("The file couldn't be open"),
                                    str(reason))
            return

        # Create a dict to manipulate data more easy
        # Create a database container widget
        db_container = database_container.DatabaseContainer()

        try:
            db_container.create_database(db_data)
        except Exception as reason:
            QMessageBox.information(self,
                                    self.tr("Error"),
                                    str(reason))
            return

        # Set the PFile object to the new database
        db_container.pfile = pfile_object
        # Add data base container to stacked
        self.add_widget(db_container)
        # Database name
        db_name = file_manager.get_basename(filename)
        # Update title with the new database name, and enable some actions
        pireal = Pireal.get_service("pireal")
        pireal.change_title(db_name)
        pireal.set_enabled_db_actions(True)
        pireal.set_enabled_relation_actions(True)
        # Add to recent files
        self.__recent_files.add(filename)
        self.created = True

    def open_query(self):
        filter_ = settings.SUPPORTED_FILES.split(';;')[1]
        filename = QFileDialog.getOpenFileName(self,
                                               self.tr("Open Query"),
                                               os.path.expanduser("~"),
                                               filter_)[0]
        if not filename:
            return
        # FIXME: mejorar éste y new_query
        self.new_query(filename)

    def save_query(self):
        pass

    def save_query_as(self):
        pass

    def __sanitize_data(self, data):
        """
        This function converts the data into a dictionary
        for better handling then.
        The argument 'data' is the content of the database.
        """

        # FIXME: controlar cuando al final de la línea hay una coma
        data_dict = {'tables': []}

        for line_count, line in enumerate(data.splitlines()):
            # Ignore blank lines
            if not line:
                continue
            if line.startswith('@'):
                tpoint = line.find(':')
                if tpoint == -1:
                    raise Exception("Invalid syntax at line {}".format(
                        line_count + 1))

                table_name, line = line.split(':')
                table_name = table_name[1:].strip()

                table_dict = {}
                table_dict['name'] = table_name
                table_dict['header'] = line.split(',')
                table_dict['tuples'] = []
            else:
                # Strip whitespace
                line = list(map(str.strip, line.split(',')))
                line = [l.strip() for l in line if l]
                if table_dict['name'] == table_name:
                    table_dict['tuples'].append(line)
            if not table_dict['tuples']:
                data_dict['tables'].append(table_dict)

        return data_dict

    def remove_last_widget(self):
        """ Remove last widget from stacked """

        widget = self.stacked.widget(self.stacked.count() - 1)
        self.stacked.removeWidget(widget)

    def close_database(self):
        """ Close the database and return to the main widget """

        mcontainer = self.get_active_db()
        if mcontainer is not None:
            if mcontainer.modified:
                flags = QMessageBox.Cancel
                flags |= QMessageBox.No
                flags |= QMessageBox.Yes
                r = QMessageBox.question(self, self.tr("Save Changes?"),
                                         self.tr("The <b>{}</b> database "
                                                 "has ben modified.<br>"
                                                 "Dou you want save your "
                                                 "changes?".format(
                                                     mcontainer.dbname())),
                                         flags)
                if r == QMessageBox.Cancel:
                    return
                if r == QMessageBox.Yes:
                    self.save_database()

            self.stacked.removeWidget(mcontainer)

            del mcontainer

            pireal = Pireal.get_service("pireal")
            pireal.set_enabled_db_actions(False)
            pireal.set_enabled_relation_actions(False)
            self.created = False

    def new_query(self, filename=''):
        if not self.created:
            QMessageBox.information(self, self.tr("Information"),
                                    self.tr("First create or open a database"))
            return
        pireal = Pireal.get_service("pireal")
        pireal.set_enabled_query_actions(True)
        db_container = self.get_active_db()
        db_container.new_query(filename)

    def execute_queries(self):
        db_container = self.get_active_db()
        db_container.execute_queries()

    def save_database(self):
        mcontainer = self.get_active_db()

        # Generate content
        relations = mcontainer.table_widget.relations
        relations_types = mcontainer.table_widget.relations_types
        content = file_manager.generate_database(relations, relations_types)
        mcontainer.pfile.write(content=content, new_fname='')
        mcontainer.modified = False
        filename = mcontainer.pfile.filename
        # Emit signal
        self.databaseSaved.emit(
            self.tr("Database saved: {}".format(filename)))

    def save_database_as(self, db_container=None):
        pass

    def remove_relation(self):
        db_container = self.get_active_db()
        db_container.delete_relation()

    def create_new_relation(self):
        db = self.get_active_db()
        data, name = relation_manager.create_or_edit_relation()
        db.table_widget.add_table(data, name)

    def edit_relation(self):
        db = self.get_active_db()
        lateral = db.lateral_widget
        selected_relation = lateral.selectedItems()[0].text(0)
        relation_text = selected_relation.split()[0].strip()
        rela = db.table_widget.relations[relation_text]
        data, _ = relation_manager.create_or_edit_relation(rela)
        if data is not None:
            # Update table
            db.table_widget.update_table(data)
            # Update relation
            db.table_widget.relations[relation_text] = data

    def load_relation(self, filename=''):
        """ Load Relation file """

        if not filename:
            if self.__last_open_folder is None:
                directory = os.path.expanduser("~")
            else:
                directory = self.__last_open_folder

            msg = self.tr("Open Relation File")
            filter_ = settings.SUPPORTED_FILES.split(';;')[-1]
            filenames = QFileDialog.getOpenFileNames(self, msg, directory,
                                                     filter_)[0]

            if not filenames:
                return

        # Save folder
        self.__last_open_folder = file_manager.get_path(filenames[0])
        db_container = self.get_active_db()
        db_container.load_relation(filenames)
        db_container.modified = True

    def add_start_page(self):
        """ This function adds the Start Page to the stacked widget """

        sp = start_page.StartPage()
        self.add_widget(sp)

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

    def add_tuple(self):
        db_container = self.get_active_db()
        db_container.add_tuple()

    def insert_tuple(self):
        db_container = self.get_active_db()
        db_container.insert_tuple()

    def delete_tuple(self):
        db_container = self.get_active_db()
        db_container.delete_tuple()

    @property
    def recent_files(self):
        return self.__recent_files

    def _settings_closed(self):
        self.stacked.removeWidget(self.widget(1))
        self.stacked.setCurrentWidget(self.stacked.currentWidget())

    def get_active_db(self):
        """ Return an instance of Main Conatainer widget if the
        stacked contains an Main Container in last index or None if it's
        not an instance of Main Container """

        index = self.stacked.count() - 1
        widget = self.widget(index)
        if isinstance(widget, database_container.DatabaseContainer):
            return widget
        return None

    def undo_action(self):
        query_container = self.get_active_db().query_container
        query_container.undo()

    def redo_action(self):
        query_container = self.get_active_db().query_container
        query_container.redo()

    def cut_action(self):
        query_container = self.get_active_db().query_container
        query_container.cut()

    def copy_action(self):
        query_container = self.get_active_db().query_container
        query_container.copy()

    def paste_action(self):
        query_container = self.get_active_db().query_container
        query_container.paste()


central = CentralWidget()
