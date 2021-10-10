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
import logging
from collections import defaultdict

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QStackedWidget
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QShortcut

from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QSettings


from pireal import settings
from pireal.core import (
    file_manager,
    pfile,
)
from pireal.gui.main_window import Pireal
from pireal.gui import (
    start_page,
    database_container
)
from pireal.gui.dialogs import (
    preferences,
    new_relation_dialog,
)
from pireal.gui.dialogs.new_database_dialog import DBInputDialog
from pireal.gui.lateral_widget import RelationItemType
from pireal.dirs import DATA_SETTINGS
from pireal import translations as tr

# Logger
logger = logging.getLogger(__name__)


class CentralWidget(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        box = QVBoxLayout(self)
        box.setContentsMargins(0, 0, 0, 0)
        box.setSpacing(0)

        self.stacked = QStackedWidget()
        box.addWidget(self.stacked)

        self.created = False

        qsettings = QSettings(str(DATA_SETTINGS), QSettings.IniFormat)
        # Acá cacheo la última carpeta accedida
        self._last_open_folder = qsettings.value('last_open_folder', type=str)
        self._recent_dbs = qsettings.value('recent_databases', type=list)

        Pireal.load_service("central", self)

        esc_short = QShortcut(QKeySequence(Qt.Key_Escape), self)
        esc_short.activated.connect(self._hide_search)

    def _hide_search(self):
        db_container = self.get_active_db()
        if db_container is None:
            return
        query_container = db_container.query_container
        if query_container is not None:
            query_container.set_editor_focus()

    @property
    def recent_databases(self) -> list:
        return self._recent_dbs

    def remember_recent_database(self, path: str):
        # TODO: FEISIMO
        if path.endswith('pireal/resources/samples/database.pdb'):
            return

        if path in self._recent_dbs:
            self._recent_dbs.remove(path)
        logger.debug('adding %s to recent databases', path)
        self._recent_dbs.insert(0, path)

    def remove_db_from_recents(self, path: str):
        if path in self._recent_dbs:
            logger.debug('removing %s from recent databases', path)
            self._recent_dbs.remove(path)

    @property
    def last_open_folder(self):
        return self._last_open_folder

    def rdb_to_pdb(self):
        from src.gui import rdb_pdb_tool
        dialog = rdb_pdb_tool.RDBPDBTool(self)
        dialog.exec_()

    def create_database(self):
        """Show a wizard widget to create a new database,
        only have one database open at time."""

        if self.created:
            return self.__say_about_one_db_at_time()
        db_filepath = DBInputDialog.ask_db_name(parent=self)
        if not db_filepath:
            logger.debug('database name not provided')
            return

        pireal = Pireal.get_service('pireal')
        db_container = database_container.DatabaseContainer()
        pfile_object = pfile.File(db_filepath)
        db_container.pfile = pfile_object
        self.add_widget(db_container)
        pireal.change_title(file_manager.get_basename(db_filepath))
        self.created = True
        logger.debug('database=%s has been created', db_filepath)

    def __say_about_one_db_at_time(self):
        logger.warning("Oops! One database at a time please")
        QMessageBox.information(self,
                                tr.TR_MSG_INFORMATION,
                                tr.TR_MSG_ONE_DB_AT_TIME)

    def open_database(self, filename='', remember=True):
        """ This function opens a database and set this on the UI """
        logger.debug('Triying to open database...')
        if self.created:
            return self.__say_about_one_db_at_time()

        # If not filename provide, then open dialog to select
        if not filename:
            logger.debug('Filename not provided')
            if self._last_open_folder is None:
                directory = os.path.expanduser("~")
            else:
                directory = self._last_open_folder
            filter_ = settings.get_extension_filter('.pdb')
            filename, _ = QFileDialog.getOpenFileName(
                self,
                tr.TR_OPEN_DATABASE,
                directory, filter_
            )
            # If is canceled, return
            if not filename:
                logger.debug('File not selected, bye!')
                return

        # If filename provide
        try:
            logger.debug("Triying to open the database file %s", filename)
            # Read pdb file
            pfile_object = pfile.File(filename)
            db_data = pfile_object.read()
            # Create a dict to manipulate data more easy
            db_data = self.__sanitize_data(db_data)
            logger.debug('Database loaded successful')
        except Exception as reason:
            logger.exception('The database file could not be opened: %s', filename)
            QMessageBox.information(
                self,
                tr.TR_MSG_DB_NOT_OPENED,
                str(reason)
            )
            return

        # Create a database container widget
        db_container = database_container.DatabaseContainer()

        try:
            db_container.create_database(db_data)
        except Exception as reason:
            logger.exception('Error creating the database')
            QMessageBox.information(self, 'Error', str(reason))
            return

        pireal = Pireal.get_service('pireal')
        pireal.status_bar.show_message(tr.TR_STATUS_DB_LOADED.format(filename))

        # Set the PFile object to the new database
        db_container.pfile = pfile_object
        # Add data base container to stacked
        self.add_widget(db_container)
        # Database name
        db_name = file_manager.get_basename(filename)
        # Update title with the new database name, and enable some actions
        pireal.status_bar.show_message(tr.TR_STATUS_DB_CONNECTED.format(db_name))
        if remember:
            # Add to recent databases
            self.remember_recent_database(filename)
            # Remember the folder
            self._last_open_folder = file_manager.get_path(filename)
        self.created = True

    def open_query(self, filename='', remember=True):
        if not filename:
            if self._last_open_folder is None:
                directory = os.path.expanduser("~")
            else:
                directory = self._last_open_folder
            filter_ = settings.get_extension_filter('.pqf')
            filename, _ = QFileDialog.getOpenFileName(
                self,
                tr.TR_MSG_OPEN_QUERY,
                directory,
                filter_
            )
            if not filename:
                return
        # Si @filename no es False
        # Cacheo la carpeta accedida
        if remember:
            self._last_open_folder = file_manager.get_path(filename)
        # FIXME: mejorar éste y new_query
        self.new_query(filename)

    def save_query(self, editor=None):
        db = self.get_active_db()
        if db is None:
            return
        fname = db.save_query(editor)
        if fname:
            pireal = Pireal.get_service('pireal')
            pireal.status_bar.show_message(tr.TR_STATUS_QUERY_SAVED.format(fname))

    def save_query_as(self):
        db = self.get_active_db()
        if db is None:
            return
        db.save_query_as()

    def __sanitize_data(self, data):
        """
        Este método convierte el contenido de la base de datos a un
        diccionario para un mejor manejo despues
        """

        # FIXME: controlar cuando al final de la línea hay una coma
        data_dict = defaultdict(list)
        for line_count, line in enumerate(data.splitlines()):
            # Ignore blank lines
            if not line.strip():
                continue
            if line.startswith("@"):
                # Header de una relación
                tpoint = line.find(":")
                if tpoint == -1:
                    raise Exception("Syntax error in {}".format(
                        line_count + 1))
                table_name, line = line.split(":")
                table_name = table_name[1:].strip()
                table_dict = {}
                table_dict["name"] = table_name
                table_dict["header"] = list(map(str.strip, line.split(",")))
                table_dict["tuples"] = set()
            else:
                # Tuplas de la relación
                for lline in csv.reader([line]):
                    tupla = tuple(map(str.strip, lline))
                    table_dict["tuples"].add(tupla)
            if not table_dict["tuples"]:
                data_dict["tables"].append(table_dict)
        return data_dict

    def remove_last_widget(self):
        """ Remove last widget from stacked """

        widget = self.stacked.widget(self.stacked.count() - 1)
        self.stacked.removeWidget(widget)

    def close_query(self):
        db = self.get_active_db()
        if db is None:
            return
        db.query_container.close_query()

    def close_database(self):
        """ Close the database and return to the main widget """

        db = self.get_active_db()
        query_container = db.query_container

        if db.modified:
            ret = QMessageBox.question(
                self,
                tr.TR_MSG_SAVE_CHANGES,
                tr.TR_MSG_SAVE_CHANGES_BODY,
                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
            )
            if ret == QMessageBox.Cancel:
                return
            if ret == QMessageBox.Yes:
                self.save_database()

        # Check if editor is modified
        query_widget = query_container.currentWidget()
        if query_widget is not None:
            weditor = query_widget.get_editor()
            if weditor is not None:
                # TODO: duplicate code, see tab widget
                if weditor.modified:
                    ret = QMessageBox.question(
                        self,
                        tr.TR_MSG_FILE_MODIFIED,
                        tr.TR_MSG_FILE_MODIFIED_BODY.format(weditor.name),
                        QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
                    )
                    if ret == QMessageBox.Cancel:
                        return
                    if ret == QMessageBox.Yes:
                        self.save_query(weditor)

        self.stacked.removeWidget(db)

        pireal = Pireal.get_service("pireal")
        pireal.change_title()  # Título en la ventana principal 'Pireal'
        self.created = False
        del db

    def new_query(self, filename=''):
        db_container = self.get_active_db()
        db_container.new_query(filename)
        # Enable editor actions
        # FIXME: refactoring

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

        pireal = Pireal.get_service('pireal')
        pireal.status_bar.show_message(tr.TR_STATUS_DB_SAVED.format(filename))

        db.modified = False

    def save_database_as(self):
        db = self.get_active_db()
        if db is None:
            return
        filter_ = settings.get_extension_filter('.pdb')
        filename, _ = QFileDialog.getSaveFileName(
            self,
            tr.TR_MSG_SAVE_DB_AS,
            db.pfile.filename,
            filter_
        )
        if not filename:
            return
        # Get relations
        relations = db.table_widget.relations
        # Content
        content = file_manager.generate_database(relations)
        # Si no se provee la extensión, le agrego
        if not os.path.splitext(filename)[1]:
            filename += '.pdb'
        db.pfile.save(content, filename)
        pireal = Pireal.get_service('pireal')
        pireal.status_bar.show_message(tr.TR_STATUS_DB_SAVED.format(db.pfile.filename))

        db.modified = False

    def remove_relation(self):
        db = self.get_active_db()
        if db is None:
            return
        if db.delete_relation():
            db.modified = True

    def create_relation(self):
        def _create_relation(relation, relation_name):
            db = self.get_active_db()
            lateral = Pireal.get_service("lateral_widget")
            table = db.create_table(relation, relation_name)
            db.table_widget.add_table(relation, relation_name, table)
            relation.name = relation_name
            lateral.add_item(relation, rtype=RelationItemType.Normal)
            db.modified = True

        db = self.get_active_db()
        if db is None:
            return
        dialog = new_relation_dialog.NewRelationDialog(self)
        dialog.created.connect(_create_relation)
        dialog.show()

    def load_relation(self, filename=''):
        """ Load Relation file """

        if not filename:
            if self._last_open_folder is None:
                directory = os.path.expanduser("~")
            else:
                directory = self._last_open_folder

            filter_ = settings.SUPPORTED_FILES.split(';;')[-1]
            filenames = QFileDialog.getOpenFileNames(
                self,
                tr.TR_MSG_OPEN_RELATION,
                directory,
                filter_)[0]

            if not filenames:
                return

        # Save folder
        self._last_open_folder = file_manager.get_path(filenames[0])
        db_container = self.get_active_db()
        if db_container.load_relation(filenames):
            db_container.modified = True

    def add_start_page(self):
        """ This function adds the Start Page to the stacked widget """

        sp = start_page.StartPage()
        self.add_widget(sp)

    def show_settings(self):
        """ Show settings dialog on stacked """

        settings_dialog = preferences.SettingsDialog(self)
        settings_dialog.exec_()

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
        lateral = Pireal.get_service("lateral_widget")
        if lateral.relation_list.has_item() == 0:
            return
        # rname = lateral.relation_list.item_text(lateral.relation_list.row())
        rname = lateral.relation_list.current_text()
        from src.gui.dialogs.edit_relation_dialog import EditRelationDialog
        dialog = EditRelationDialog(rname, self)
        tw = self.get_active_db().table_widget
        dialog.sendData.connect(tw.insert_rows)
        dialog.show()

    def add_column(self):
        tw = self.get_active_db().table_widget
        tw.add_column()

    def delete_tuple(self):
        lateral = Pireal.get_service("lateral_widget")
        if lateral.relation_list.has_item() == 0:
            return
        r = QMessageBox.question(
            self,
            tr.TR_MSG_REMOVE_TUPLES,
            tr.TR_MSG_REMOVE_TUPLES_BODY,
            QMessageBox.Yes | QMessageBox.Cancel
        )
        if r == QMessageBox.Cancel:
            return
        tw = self.get_active_db().table_widget
        tw.delete_tuple()

    def delete_column(self):
        tw = self.get_active_db().table_widget
        tw.delete_column()

    def search(self):
        query_container = self.get_active_db().query_container
        query_container.search()


central = CentralWidget()
