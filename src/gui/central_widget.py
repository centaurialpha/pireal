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
from src.core.logger import PirealLogger
from src.gui.main_window import Pireal
from src.gui import (
    start_page,
    main_container
)
from src.gui.dialogs import (
    preferences,
    new_relation_dialog,
    database_wizard
)

# Logger
logger = PirealLogger(__name__)
CRITICAL = logger.critical
DEBUG = logger.debug

#FIXME: Refactoring


class CentralWidget(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        box = QVBoxLayout(self)
        box.setContentsMargins(0, 0, 0, 0)
        box.setSpacing(0)

        self.stacked = QStackedWidget()
        box.addWidget(self.stacked)

        #self.__ndb = 1
        self.__created = False
        self.__last_open_folder = None
        self.__recent_files = set()

        Pireal.load_service("central", self)

    def create_database_wizard(self):
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
        if not data:
            self.remove_last_widget()
        else:
            database_container = main_container.MainContainer()
            pfile_object = pfile.PFile(data['filename'])
            database_container.pfile = pfile_object
            self.add_widget(database_container)
            # Remove wizard
            self.stacked.removeWidget(wizard_widget)

        # Show menubar and toolbar
        pireal = Pireal.get_service("pireal")
        pireal.menuBar().setVisible(True)
        pireal.toolbar.setVisible(True)
        # Title
        pireal.change_title(file_manager.get_basename(data['filename']))
        # Enable db actions
        pireal.set_enabled_db_actions(True)
        self.__created = True

    def open_database(self, filename=''):
        # If not filename, then open dialog for select
        if not filename:
            if self.__last_open_folder is None:
                directory = os.path.expanduser("~")
            else:
                directory = self.__last_open_folder
            filename = QFileDialog.getOpenFileName(self,
                                                   self.tr("Open Database"),
                                                   directory,
                                                   settings.SUPPORTED_FILES)[0]
            # If is canceled, return
            if not filename:
                return

            # Remember the folder
            self.__last_open_folder = file_manager.get_path(filename)

        # Read pdb file
        with open(filename, mode='r') as f:
            db_data = f.read()

        # Add to recent databases
        self.__recent_files.add(filename)

        # Database name
        db_name = file_manager.get_basename(filename)

        database_container = main_container.MainContainer()
        pfile_object = pfile.PFile(filename)
        database_container.pfile = pfile_object
        database_container.create_database(self.__sanitize_data(db_data))
        self.add_widget(database_container)

        pireal = Pireal.get_service("pireal")
        pireal.change_title(db_name)
        pireal.set_enabled_db_actions(True)
        self.created = True

    def __sanitize_data(self, data):
        data_dict = {'tables': []}

        for line in data.splitlines():
            # Ignore blank lines
            if not line:
                continue
            if line.startswith('@'):
                table_name, line = line.split(':')
                table_name = table_name[1:].strip()
                fields = [tuple(f.split('/')) for f in line.split(',')]
                table_dict = {}
                table_dict['name'] = table_name
                table_dict['fields'] = [f[0] for f in fields]
                table_dict['types'] = [f[1] for f in fields]
                table_dict['tuples'] = []
            else:
                # Strip whitespace
                line = list(map(str.strip, line.split(',')))
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
                                             mcontainer.dbname())), flags)
                if r == QMessageBox.Cancel:
                    return
                if r == QMessageBox.Yes:
                    self.save_database()

            self.stacked.removeWidget(mcontainer)

            del mcontainer

            pireal = Pireal.get_service("pireal")
            pireal.set_enabled_db_actions(False)
            self.created = False

    def new_query(self, filename=''):
        if not self.created:
            QMessageBox.information(self, self.tr("Information"),
                                    self.tr("First create or open a database"))
            return
        pireal = Pireal.get_service("pireal")
        pireal.set_enabled_query_actions(True)
        main_container = self.get_active_db()
        main_container.new_query(filename)

    def execute_queries(self):
        main_container = self.get_active_db()
        main_container.execute_queries()

    def save_database(self):
        mcontainer = self.get_active_db()
        #if not mcontainer.modified:
            #return
        #if mcontainer.is_new():
            #return self.save_database_as(mcontainer)

        # Generate content
        relations = mcontainer.table_widget.relations
        relations_types = mcontainer.table_widget.relations_types
        content = file_manager.generate_database(relations, relations_types)
        mcontainer.pfile.write(content=content, new_fname='')
        mcontainer.modified = False

    def save_database_as(self, main_container=None):
        if main_container is None:
            main_container = self.get_active_db()

        filename = QFileDialog.getSaveFileName(self, self.tr("Save File"),
                                               main_container.dbname(),
                                               "Pireal database files"
                                               "(*.pdb)")[0]
        if not filename:
            return

        # Generate content
        relations = main_container.table_widget.relations
        print(relations)
        #content = file_manager.generate_database(relations)
        #main_container.pfile.write(content=content, new_fname=filename)

    def save_file(self):
        mcontainer = self.get_active_db()
        mcontainer.save_query()

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

            msg = self.tr("Open Relation File")
            filter_ = settings.SUPPORTED_FILES.split(';;')[-1]
            filenames = QFileDialog.getOpenFileNames(self, msg, directory,
                                                    filter_)[0]

            if not filenames:
                return

        # Save folder
        self.__last_open_folder = file_manager.get_path(filenames[0])
        main_container = self.get_active_db()
        main_container.load_relation(filenames)
        main_container.modified = True

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
        if isinstance(widget, main_container.MainContainer):
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
