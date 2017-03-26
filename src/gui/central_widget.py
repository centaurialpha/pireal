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
import csv

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
    pfile,
)
from src.core.logger import Logger
from src.gui.main_window import Pireal
from src.gui import (
    start_page,
    database_container
)
from src.gui.dialogs import (
    preferences,
    new_relation_dialog,
    new_database_dialog
)
PSetting = settings.PSetting
# Logger
logger = Logger(__name__)


class CentralWidget(QWidget):
    # This signals is used by notificator
    databaseSaved = pyqtSignal('QString')
    querySaved = pyqtSignal('QString')
    databaseConected = pyqtSignal('QString')

    def __init__(self):
        QWidget.__init__(self)
        box = QVBoxLayout(self)
        box.setContentsMargins(0, 0, 0, 0)
        box.setSpacing(0)

        self.stacked = QStackedWidget()
        box.addWidget(self.stacked)

        self.created = False
        # Acá cacheo la última carpeta accedida
        self.__last_open_folder = None
        if PSetting.LAST_OPEN_FOLDER:
            self.__last_open_folder = PSetting.LAST_OPEN_FOLDER
        self.__recent_dbs = []
        if PSetting.RECENT_DBS:
            self.__recent_dbs = PSetting.RECENT_DBS

        Pireal.load_service("central", self)

    @property
    def recent_databases(self):
        return self.__recent_dbs

    @recent_databases.setter
    def recent_databases(self, database_file):
        if database_file in PSetting.RECENT_DBS:
            PSetting.RECENT_DBS.remove(database_file)
        PSetting.RECENT_DBS.insert(0, database_file)
        self.__recent_dbs = PSetting.RECENT_DBS

    @property
    def last_open_folder(self):
        return self.__last_open_folder

    def create_database(self):
        """ Show a wizard widget to create a new database,
        only have one database open at time.
        """

        if self.created:
            return self.__say_about_one_db_at_time()
        dialog = new_database_dialog.NewDatabaseDialog(self)
        dialog.created.connect(self.__on_wizard_finished)
        dialog.show()

    def __on_wizard_finished(self, *data):
        """ This slot execute when wizard to create a database is finished """

        pireal = Pireal.get_service("pireal")
        if data:
            db_name, location, fname = data
            # Create a new data base container
            db_container = database_container.DatabaseContainer()
            # Associate the file name with the PFile object
            pfile_object = pfile.File(fname)
            # Associate PFile object with data base container
            # and add widget to stacked
            db_container.pfile = pfile_object
            self.add_widget(db_container)
            # Set window title
            pireal.change_title(file_manager.get_basename(fname))
            # Enable db actions
            pireal.set_enabled_db_actions(True)
            pireal.set_enabled_relation_actions(True)
            self.created = True
            logger.debug("La base de datos ha sido creada con éxito")

    def __say_about_one_db_at_time(self):
        logger.info("Una base de datos a la vez")
        QMessageBox.information(self,
                                self.tr("Information"),
                                self.tr("You may only have one database"
                                        " open at time."))

    def open_database(self, filename='', remember=True):
        """ This function opens a database and set this on the UI """

        if self.created:
            return self.__say_about_one_db_at_time()

        # If not filename provide, then open dialog to select
        if not filename:
            if self.__last_open_folder is None:
                directory = os.path.expanduser("~")
            else:
                directory = self.__last_open_folder
            filter_ = settings.SUPPORTED_FILES.split(';;')[0]
            filename, _ = QFileDialog.getOpenFileName(self,
                                                      self.tr("Open Database"),
                                                      directory,
                                                      filter_)
            # If is canceled, return
            if not filename:
                return

        # If filename provide
        try:
            logger.debug("Intentando abrir el archivo {}".format(filename))
            # Read pdb file
            pfile_object = pfile.File(filename)
            db_data = pfile_object.read()
            # Create a dict to manipulate data more easy
            db_data = self.__sanitize_data(db_data)
        except Exception as reason:
            QMessageBox.information(self,
                                    self.tr("The file couldn't be open"),
                                    reason.__str__())
            logger.debug("Error al abrir el archivo {0}: '{1}'".format(
                filename, reason.__str__()))
            return

        # Create a database container widget
        db_container = database_container.DatabaseContainer()

        try:
            db_container.create_database(db_data)
        except Exception as reason:
            QMessageBox.information(self,
                                    self.tr("Error"),
                                    str(reason))
            logger.debug("Error al crear la base de datos: {}".format(
                reason.__str__()))
            return

        # Set the PFile object to the new database
        db_container.pfile = pfile_object
        # Add data base container to stacked
        self.add_widget(db_container)
        # Database name
        db_name = file_manager.get_basename(filename)
        # Update title with the new database name, and enable some actions
        pireal = Pireal.get_service("pireal")
        self.databaseConected.emit(self.tr("Conected to: {}".format(db_name)))
        pireal.set_enabled_db_actions(True)
        pireal.set_enabled_relation_actions(True)
        if remember:
            # Add to recent databases
            self.recent_databases = filename
            # Remember the folder
            self.__last_open_folder = file_manager.get_path(filename)
        self.created = True

    def open_query(self, filename='', remember=True):
        if not filename:
            if self.__last_open_folder is None:
                directory = os.path.expanduser("~")
            else:
                directory = self.__last_open_folder
            filter_ = settings.SUPPORTED_FILES.split(';;')[1]
            filename, _ = QFileDialog.getOpenFileName(self,
                                                      self.tr("Open Query"),
                                                      directory,
                                                      filter_)
            if not filename:
                return
        # Si @filename no es False
        # Cacheo la carpeta accedida
        if remember:
            self.__last_open_folder = file_manager.get_path(filename)
        # FIXME: mejorar éste y new_query
        self.new_query(filename)

    def save_query(self, editor=None):
        db = self.get_active_db()
        fname = db.save_query(editor)
        if fname:
            self.querySaved.emit(self.tr("Query saved: {}".format(fname)))

    def save_query_as(self):
        pass

    def __sanitize_data(self, data):
        """
        Este método convierte el contenido de la base de datos a un
        diccionario para un mejor manejo despues
        """

        # FIXME: controlar cuando al final de la línea hay una coma
        data_dict = {'tables': []}

        for line_count, line in enumerate(data.splitlines()):
            # Ignore blank lines
            if not line:
                continue
            if line.startswith('@'):
                # Esta línea es el header de una relación
                tpoint = line.find(':')
                if tpoint == -1:
                    raise Exception("Invalid syntax at line {}".format(
                        line_count + 1))

                table_name, line = line.split(':')
                table_name = table_name[1:].strip()
                table_dict = {}
                table_dict['name'] = table_name
                table_dict['header'] = list(map(str.strip, line.split(',')))

                table_dict['tuples'] = []

            else:
                for l in csv.reader([line]):
                    # Remove spaces
                    tupla = list(map(str.strip, l))
                    table_dict['tuples'].append(tupla)
            if not table_dict['tuples']:
                data_dict['tables'].append(table_dict)

        return data_dict

    def remove_last_widget(self):
        """ Remove last widget from stacked """

        widget = self.stacked.widget(self.stacked.count() - 1)
        self.stacked.removeWidget(widget)

    def close_database(self):
        """ Close the database and return to the main widget """

        db = self.get_active_db()
        query_container = db.query_container

        if db.modified:
            msgbox = QMessageBox(self)
            msgbox.setIcon(QMessageBox.Question)
            msgbox.setWindowTitle(self.tr("Save Changes?"))
            msgbox.setText(self.tr("The <b>{}</b> database has ben"
                                   " modified.<br>Do you want save "
                                   "your changes?".format(
                                       db.dbname())))
            cancel_btn = msgbox.addButton(self.tr("Cancel"),
                                          QMessageBox.RejectRole)
            msgbox.addButton(self.tr("No"),
                             QMessageBox.NoRole)
            yes_btn = msgbox.addButton(self.tr("Yes"),
                                       QMessageBox.YesRole)
            msgbox.exec_()
            r = msgbox.clickedButton()
            if r == cancel_btn:
                return
            if r == yes_btn:
                self.save_database()

        # Check if editor is modified
        query_widget = query_container.currentWidget()
        if query_widget is not None:
            weditor = query_widget.get_editor()
            if weditor is not None:
                # TODO: duplicate code, see tab widget
                if weditor.modified:
                    msgbox = QMessageBox(self)
                    msgbox.setIcon(QMessageBox.Question)
                    msgbox.setWindowTitle(self.tr("File modified"))
                    msgbox.setText(self.tr("The file <b>{}</b> has unsaved "
                                           "changes. You want to keep "
                                           "them?".format(
                                               weditor.name)))
                    cancel_btn = msgbox.addButton(self.tr("Cancel"),
                                                  QMessageBox.RejectRole)
                    msgbox.addButton(self.tr("No"),
                                     QMessageBox.NoRole)
                    yes_btn = msgbox.addButton(self.tr("Yes"),
                                               QMessageBox.YesRole)
                    msgbox.exec_()
                    r = msgbox.clickedButton()
                    if r == cancel_btn:
                        return
                    if r == yes_btn:
                        self.save_query(weditor)

        self.stacked.removeWidget(db)

        pireal = Pireal.get_service("pireal")
        pireal.set_enabled_db_actions(False)
        pireal.set_enabled_relation_actions(False)
        pireal.set_enabled_query_actions(False)
        pireal.set_enabled_editor_actions(False)
        pireal.change_title()  # Título en la ventana principal 'Pireal'
        self.created = False
        del db

    def new_query(self, filename=''):
        pireal = Pireal.get_service("pireal")
        db_container = self.get_active_db()
        db_container.new_query(filename)
        # Enable editor actions
        # FIXME: refactoring
        pireal.set_enabled_query_actions(True)
        zoom_in_action = Pireal.get_action("zoom_in")
        zoom_in_action.setEnabled(True)
        zoom_out_action = Pireal.get_action("zoom_out")
        zoom_out_action.setEnabled(True)
        paste_action = Pireal.get_action("paste_action")
        paste_action.setEnabled(True)
        comment_action = Pireal.get_action("comment")
        comment_action.setEnabled(True)
        uncomment_action = Pireal.get_action("uncomment")
        uncomment_action.setEnabled(True)

    def execute_queries(self):
        db_container = self.get_active_db()
        db_container.execute_queries()

    def execute_selection(self):
        db_container = self.get_active_db()
        db_container.execute_selection()

    def save_database(self):

        db = self.get_active_db()
        if not db.modified:
            return

        # Get relations dict
        relations = db.table_widget.relations
        # Generate content
        content = file_manager.generate_database(relations)
        db.pfile.save(data=content)
        filename = db.pfile.filename
        # Emit signal
        self.databaseSaved.emit(
            self.tr("Database saved: {}".format(filename)))

        db.modified = False

    def save_database_as(self):
        filter = settings.SUPPORTED_FILES.split(';;')[0]
        filename, _ = QFileDialog.getSaveFileName(self,
                                                  self.tr("Save Database As"),
                                                  settings.PIREAL_DATABASES,
                                                  filter)
        if not filename:
            return
        db = self.get_active_db()
        # Get relations
        relations = db.table_widget.relations
        # Content
        content = file_manager.generate_database(relations)
        # Si no se provee la extensión, le agrego
        if not os.path.splitext(filename)[1]:
            filename += '.pdb'
        db.pfile.save(content, filename)
        self.databaseSaved.emit(
            self.tr("Database saved: {}".format(db.pfile.filename)))

        db.modified = False

    def remove_relation(self):
        db = self.get_active_db()
        if db.delete_relation():
            db.modified = True

    def create_new_relation(self):
        def create_relation(relation, relation_name):
            db = self.get_active_db()
            table = db.create_table(relation, relation_name)
            db.table_widget.add_table(relation, relation_name, table)
            db.lateral_widget.add_item(relation_name, relation.cardinality())
            db.modified = True

        dialog = new_relation_dialog.NewRelationDialog(self)
        dialog.created.connect(create_relation)
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
        db_container = self.get_active_db()
        if db_container.load_relation(filenames):
            db_container.modified = True

    def add_start_page(self):
        """ This function adds the Start Page to the stacked widget """

        sp = start_page.StartPage()
        self.add_widget(sp)

    def show_settings(self):
        """ Show settings dialog on stacked """

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
        """ Return an instance of DatabaseContainer widget if the
        stacked contains an DatabaseContainer in last index or None if it's
        not an instance of DatabaseContainer """

        index = self.stacked.count() - 1
        widget = self.widget(index)
        if isinstance(widget, database_container.DatabaseContainer):
            return widget
        return None

    def get_unsaved_queries(self):
        query_container = self.get_active_db().query_container
        return query_container.get_unsaved_queries()

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

    def zoom_in(self):
        query_container = self.get_active_db().query_container
        query_container.zoom_in()

    def zoom_out(self):
        query_container = self.get_active_db().query_container
        query_container.zoom_out()

    def comment(self):
        query_container = self.get_active_db().query_container
        query_container.comment()

    def uncomment(self):
        query_container = self.get_active_db().query_container
        query_container.uncomment()

    def add_tuple(self):
        tw = self.get_active_db().table_widget
        tw.add_tuple()

    def add_column(self):
        tw = self.get_active_db().table_widget
        tw.add_column()

    def delete_tuple(self):
        tw = self.get_active_db().table_widget
        tw.delete_tuple()

    def delete_column(self):
        tw = self.get_active_db().table_widget
        tw.delete_column()


central = CentralWidget()
