# -*- coding: utf-8 -*-
#
# Copyright 2015-2022 - Gabriel Acosta <acostadariogabriel@gmail.com>
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
from pathlib import Path
from collections import defaultdict

from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QStackedWidget
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtGui import QShortcut

from PyQt6.QtGui import QKeySequence
from PyQt6.QtCore import Qt
from PyQt6.QtCore import QSettings

import pireal
from pireal.dirs import EXAMPLE_DB_FILENAME
from pireal import settings
from pireal.core import (
    file_manager,
    pfile,
)
from pireal.gui import start_page
from pireal.gui.database_container import DatabaseContainer
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
    """HOLA QUE ONDA"""

    def __init__(self):
        QWidget.__init__(self)
        box = QVBoxLayout(self)
        box.setContentsMargins(0, 0, 0, 0)
        box.setSpacing(0)

        self.stack = QStackedWidget()
        box.addWidget(self.stack)

        self.created = False

        qsettings = QSettings(str(DATA_SETTINGS), QSettings.Format.IniFormat)
        # Acá cacheo la última carpeta accedida
        self._last_open_folder = qsettings.value("last_open_folder", type=str)
        self._recent_db_containers = qsettings.value("recent_databases", type=list)

        esc_short = QShortcut(QKeySequence(Qt.Key.Key_Escape), self)
        esc_short.activated.connect(self._hide_search)

    def _hide_search(self):
        pireal_instance = pireal.get_pireal_instance()
        db_container = pireal_instance.db_container
        if db_container is None:
            return
        query_container = db_container.query_container
        if query_container is not None:
            query_container.set_editor_focus()

    @property
    def recent_databases(self) -> list[str]:
        return self._recent_db_containers

    def remember_recent_database(self, path: str | Path):
        if path == str(EXAMPLE_DB_FILENAME):
            return

        if path in self._recent_db_containers:
            self._recent_db_containers.remove(path)
        logger.debug("adding %s to recent databases", path)
        self._recent_db_containers.insert(0, path)

    def remove_db_container_from_recents(self, path: str):
        if path in self._recent_db_containers:
            logger.debug("removing %s from recent databases", path)
            self._recent_db_containers.remove(path)

    @property
    def last_open_folder(self):
        return self._last_open_folder

    def rdb_container_to_pdb_container(self):
        from src.gui import rdb_container_pdb_container_tool

        dialog = rdb_container_pdb_container_tool.Rdb_containerPdb_containerTool(self)
        dialog.exec_()

    def create_database(self):
        """Show a wizard widget to create a new database,
        only have one database open at time."""

        if self.created:
            return self.__say_about_one_db_container_at_time()
        db_container_filepath = DBInputDialog.ask_db_name(
            parent=self
        )
        if not db_container_filepath:
            logger.debug("database name not provided")
            return

        # # pireal = Pireal.get_service("pireal")
        # db_container = database_container.DatabaseContainer()
        # pfile_object = pfile.File(db_container_filepath)
        # db_container.pfile = pfile_object
        # self.add_widget(db_container)
        # pireal.change_title(file_manager.get_basename(db_container_filepath))
        # self.created = True
        # logger.debug("database=%s has been created", db_container_filepath)

    def __say_about_one_db_container_at_time(self):
        logger.warning("Oops! One database at a time please")
        QMessageBox.information(
            self, tr.TR_MSG_INFORMATION, tr.TR_MSG_ONE_db_container_AT_TIME
        )

    def open_database(self, filename="", remember=True):
        """This function opens a database and set this on the UI"""
        logger.debug("Triying to open database...")
        if self.created:
            return self.__say_about_one_db_container_at_time()

        # If not filename provide, then open dialog to select
        if not filename:
            logger.debug("Filename not provided")
            if self._last_open_folder is None:
                directory = os.path.expanduser("~")
            else:
                directory = self._last_open_folder
            filter_ = settings.get_extension_filter(".pdb_container")
            filename, _ = QFileDialog.getOpenFileName(
                self, tr.TR_OPEN_DATABASE, directory, filter_
            )
            # If is canceled, return
            if not filename:
                logger.debug("File not selected, bye!")
                return

        # If filename provide
        try:
            logger.debug("Triying to open the database file %s", filename)
            # Read pdb_container file
            pfile_object = pfile.File(filename)
            db_container_data = pfile_object.read()
            # Create a dict to manipulate data more easy
            db_container_data = self.__sanitize_data(db_container_data)
            logger.debug("Database loaded successful")
        except Exception as reason:
            logger.exception("The database file could not be opened: %s", filename)
            QMessageBox.information(self, tr.TR_MSG_DB_NOT_OPENED, str(reason))
            return

        db_container = DatabaseContainer()
        pireal_instance = pireal.get_pireal_instance()
        pireal_instance.db_container = db_container
        db_container.create_database(db_container_data)

        pireal_instance.status_bar.show_message(tr.TR_STATUS_DB_LOADED.format(filename))

        # Add data base container to stacked
        self.add_widget(db_container)

        # try:
        #     db_container.create_database(db_container_data)
        # except Exception as reason:
        #     logger.exception("Error creating the database")
        #     QMessageBox.information(self, "Error", str(reason))
        #     return

        # Set the PFile object to the new database
        # db_container.pfile = pfile_object
        # # Database name
        db_container_name = file_manager.get_basename(filename)
        # Update title with the new database name, and enable some actions
        pireal_instance.status_bar.show_message(
            tr.TR_STATUS_DB_CONNECTED.format(db_container_name)
        )
        if remember:
            # Add to recent databases
            self.remember_recent_database(filename)
            # Remember the folder
            self._last_open_folder = file_manager.get_path(filename)

        self.created = True

    def open_query(self, filename="", remember=True):
        if not filename:
            if self._last_open_folder is None:
                directory = os.path.expanduser("~")
            else:
                directory = self._last_open_folder
            filter_ = settings.get_extension_filter(".pqf")
            filename, _ = QFileDialog.getOpenFileName(
                self, tr.TR_MSG_OPEN_QUERY, directory, filter_
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
        pireal_instance = pireal.get_pireal_instance()
        db_container = pireal_instance.db_container
        if db_container is None:
            return
        fname = db_container.save_query(editor)
        if fname:
            pireal_instance.status_bar.show_message(
                tr.TR_STATUS_QUERY_SAVED.format(fname)
            )

    def save_query_as(self):
        pireal_instance = pireal.get_pireal_instance()
        db_container = pireal_instance.db_container
        if db_container is None:
            return
        db_container.save_query_as()

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
                    raise Exception("Syntax error in {}".format(line_count + 1))
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
        """Remove last widget from stacked"""

        widget = self.stack.widget(self.stack.count() - 1)
        self.stack.removeWidget(widget)

    def close_query(self):
        pireal_instance = pireal.get_pireal_instance()
        db_container = pireal_instance.db_container
        if db_container is None:
            return

        db_container.query_container.close_query()

    def close_database(self) -> None:
        """Close the database and return to the main widget"""

        pireal_instance = pireal.get_pireal_instance()
        db_container = pireal_instance.db_container
        if db_container is None:
            return

        query_container = db_container.query_container

        if db_container.modified:
            ret = QMessageBox.question(
                self,
                tr.TR_MSG_SAVE_CHANGES,
                tr.TR_MSG_SAVE_CHANGES_BODY,
                QMessageBox.Standardb_containerutton.Yes
                | QMessageBox.Standardb_containerutton.No
                | QMessageBox.Standardb_containerutton.Cancel,
            )
            if ret == QMessageBox.Standardb_containerutton.Cancel:
                return
            if ret == QMessageBox.Standardb_containerutton.Yes:
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
                        QMessageBox.Standardb_containerutton.Yes
                        | QMessageBox.Standardb_containerutton.No
                        | QMessageBox.Standardb_containerutton.Cancel,
                    )
                    if ret == QMessageBox.Standardb_containerutton.Cancel:
                        return
                    if ret == QMessageBox.Standardb_containerutton.Yes:
                        self.save_query(weditor)

        self.stack.removeWidget(db_container)

        pireal_instance.db_container = None
        pireal_instance = pireal.get_pireal_instance()
        pireal_instance.change_title()  # Título en la ventana principal 'Pireal'
        self.created = False

    def new_query(self, filename=""):
        pireal_instance = pireal.get_pireal_instance()
        db_container = pireal_instance.db_container
        if db_container is None:
            return

        db_container.new_query(filename)
        # Enable editor actions
        # FIXME: refactoring

    def execute_queries(self):
        pireal_instance = pireal.get_pireal_instance()
        db_container = pireal_instance.db_container
        if db_container is None:
            return

        db_container.execute_queries()

    def execute_selection(self):
        pireal_instance = pireal.get_pireal_instance()
        db_container = pireal_instance.db_container
        if db_container is None:
            return

        db_container.execute_selection()

    def save_database(self):
        pireal_instance = pireal.get_pireal_instance()
        db_container = pireal_instance.db_container
        if db_container is None:
            return

        if not db_container.modified:
            return

        # Get relations dict
        relations = db_container.table_widget.relations
        # Generate content
        content = file_manager.generate_database(relations)
        db_container.pfile.save(data=content)
        filename = db_container.pfile.filename

        pireal_instance = pireal.get_pireal_instance()
        pireal_instance.status_bar.show_message(
            tr.TR_STATUS_db_container_SAVED.format(filename)
        )

        db_container.modified = False

    def save_database_as(self):
        pireal_instance = pireal.get_pireal_instance()
        db_container = pireal_instance.db_container
        if db_container is None:
            return

        filter_ = settings.get_extension_filter(".pdb_container")
        filename, _ = QFileDialog.getSaveFileName(
            self, tr.TR_MSG_SAVE_db_container_AS, db_container.pfile.filename, filter_
        )
        if not filename:
            return
        # Get relations
        relations = db_container.table_widget.relations
        # Content
        content = file_manager.generate_database(relations)
        # Si no se provee la extensión, le agrego
        if not os.path.splitext(filename)[1]:
            filename += ".pdb_container"
        db_container.pfile.save(content, filename)
        pireal_instance.status_bar.show_message(
            tr.TR_STATUS_db_container_SAVED.format(db_container.pfile.filename)
        )

        db_container.modified = False

    def remove_relation(self):
        pireal_instance = pireal.get_pireal_instance()
        db_container = pireal_instance.db_container
        if db_container is None:
            return

        if db_container.delete_relation():
            db_container.modified = True

    def create_relation(self):
        pireal_instance = pireal.get_pireal_instance()
        db_container = pireal_instance.db_container
        if db_container is None:
            return

        def _create_relation(relation, relation_name):
            # lateral = Pireal.get_service("lateral_widget")
            table = db_container.create_table(relation, relation_name)
            db_container.table_widget.add_table(relation, relation_name, table)
            relation.name = relation_name
            db_container.lateral_widget.add_item(
                relation, rtype=RelationItemType.Normal
            )
            db_container.modified = True

        dialog = new_relation_dialog.NewRelationDialog(self)
        dialog.created.connect(_create_relation)
        dialog.show()

    def load_relation(self, filename=""):
        """Load Relation file"""

        filenames = []
        if not filename:
            if self._last_open_folder is None:
                directory = os.path.expanduser("~")
            else:
                directory = self._last_open_folder

            filter_ = settings.SUPPORTED_FILES.split(";;")[-1]
            filenames = QFileDialog.getOpenFileNames(
                self, tr.TR_MSG_OPEN_RELATION, directory, filter_
            )[0]

            if not filenames:
                return

        # Save folder
        self._last_open_folder = file_manager.get_path(filenames[0])
        pireal_instance = pireal.get_pireal_instance()
        db_container = pireal_instance.db_container
        if db_container is None:
            return

        if db_container.load_relation(filenames):
            db_container.modified = True

    def add_start_page(self):
        """This function adds the Start Page to the stacked widget"""

        sp = start_page.StartPage()
        self.add_widget(sp)

    def show_settings(self):
        """Show settings dialog on stacked"""

        settings_dialog = preferences.SettingsDialog(self)
        settings_dialog.exec()

    def widget(self, index):
        """Returns the widget at the given index"""

        return self.stack.widget(index)

    def add_widget(self, widget):
        """Appends and show the given widget to the Stacked"""

        index = self.stack.addWidget(widget)
        self.stack.setCurrentIndex(index)

    def _settings_closed(self):
        self.stack.removeWidget(self.widget(1))
        self.stack.setCurrentWidget(self.stack.currentWidget())

    # def get_active_db_container(self) -> database_container.DatabaseContainer | None:
    #     """Return an instance of DatabaseContainer widget if the
    #     stacked contains an DatabaseContainer in last index or None if it's
    #     not an instance of DatabaseContainer"""

    #     index = self.stack.count() - 1
    #     widget = self.widget(index)
    #     if isinstance(widget, database_container.DatabaseContainer):
    #         return widget
    #     return None

    def get_unsaved_queries(self):
        pireal_instance = pireal.get_pireal_instance()
        db_container = pireal_instance.db_container
        if db_container is None:
            return
        return db_container.query_container.get_unsaved_queries()

    def undo_action(self):
        pireal_instance = pireal.get_pireal_instance()
        db_container = pireal_instance.db_container
        if db_container is None:
            return
        db_container.query_container.undo()

    def redo_action(self):
        pireal_instance = pireal.get_pireal_instance()
        db_container = pireal_instance.db_container
        if db_container is None:
            return
        db_container.query_container.redo()

    def cut_action(self):
        pireal_instance = pireal.get_pireal_instance()
        db_container = pireal_instance.db_container
        if db_container is None:
            return
        db_container.query_container.cut()

    def copy_action(self):
        pireal_instance = pireal.get_pireal_instance()
        db_container = pireal_instance.db_container
        if db_container is None:
            return
        db_container.query_container.copy()

    def paste_action(self):
        pireal_instance = pireal.get_pireal_instance()
        db_container = pireal_instance.db_container
        if db_container is None:
            return
        db_container.query_container.paste()

    def zoom_in(self):
        pireal_instance = pireal.get_pireal_instance()
        db_container = pireal_instance.db_container
        if db_container is None:
            return
        db_container.query_container.zoom_in()

    def zoom_out(self):
        pireal_instance = pireal.get_pireal_instance()
        db_container = pireal_instance.db_container
        if db_container is None:
            return
        db_container.query_container.zoom_out()

    def comment(self):
        pireal_instance = pireal.get_pireal_instance()
        db_container = pireal_instance.db_container
        if db_container is None:
            return
        db_container.query_container.comment()

    def uncomment(self):
        pireal_instance = pireal.get_pireal_instance()
        db_container = pireal_instance.db_container
        if db_container is None:
            return
        db_container.query_container.uncomment()

    def add_tuple(self):
        pass
        # pireal_instance = pireal.get_pireal_instance()
        # lateral = Pireal.get_service("lateral_widget")
        # if lateral.relation_list.has_item() == 0:
        #     return
        # # rname = lateral.relation_list.item_text(lateral.relation_list.row())
        # rname = lateral.relation_list.current_text()
        # from src.gui.dialogs.edit_relation_dialog import EditRelationDialog

        # dialog = EditRelationDialog(rname, self)
        # tw = self.get_active_db_container().table_widget
        # dialog.sendData.connect(tw.insert_rows)
        # dialog.show()

    # def add_column(self):
    #     tw = self.get_active_db_container().table_widget
    #     tw.add_column()

    # def delete_tuple(self):
    #     lateral = Pireal.get_service("lateral_widget")
    #     if lateral.relation_list.has_item() == 0:
    #         return
    #     r = QMessageBox.question(
    #         self,
    #         tr.TR_MSG_REMOVE_TUPLES,
    #         tr.TR_MSG_REMOVE_TUPLES_BODY,
    #         QMessageBox.Standardb_containerutton.Yes |
    #         QMessageBox.Standardb_containerutton.Cancel,
    #     )
    #     if r == QMessageBox.Standardb_containerutton.Cancel:
    #         return
    #     tw = self.get_active_db_container().table_widget
    #     tw.delete_tuple()

    # def delete_column(self):
    #     tw = self.get_active_db_container().table_widget
    #     tw.delete_column()

    def search(self):
        pireal_instance = pireal.get_pireal_instance()
        db_container = pireal_instance.db_container
        if db_container is None:
            return
        db_container.query_container.search()
