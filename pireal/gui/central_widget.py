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
# from PyQt5.QtWidgets import QShortcut

# from PyQt5.QtGui import QKeySequence
# from PyQt5.QtCore import Qt
# from PyQt5.QtCore import pyqtSignal as Signal
# from PyQt5.QtCore import pyqtSlot as Slot


from pireal import translations as tr
from pireal.core import settings
from pireal.core import file_manager
# from pireal.core import pfile
from pireal.core.relation import Relation

from pireal.gui import start_page
# from pireal.gui import database_container
from pireal.gui.main_panel import MainPanel

from pireal.gui.dialogs import preferences
from pireal.gui.dialogs import new_relation_dialog
from pireal.gui.dialogs import new_database_dialog

from pireal.core.settings import DATA_SETTINGS
from pireal.core.pfile import File
# Logger
logger = logging.getLogger(__name__)


class CentralWidget(QWidget):
    # This signals is used by notificator
    # databaseSaved = Signal(str)
    # querySaved = Signal(str)
    # databaseConected = Signal(str)

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.pireal = parent
        self._stacked = QStackedLayout(self)
        self._main_panel = None
        # Acá cacheo la última carpeta accedida
        self._last_open_folder = DATA_SETTINGS.value('ds/lastOpenFolder')
        self._recent_dbs = DATA_SETTINGS.value('ds/recentDbs', [])

        # if CONFIG.get("lastOpenFolder") is not None:
        #     self._last_open_folder = CONFIG.get("lastOpenFolder")
        # self._recent_dbs = []
        # if CONFIG.get("recentFiles"):
        #     self._recent_dbs = CONFIG.get("recentFiles")

    #     esc_short = QShortcut(QKeySequence(Qt.Key_Escape), self)
    #     esc_short.activated.connect(self._hide_search)

    # def _hide_search(self):
    #     db_container = self.get_active_db()
    #     if db_container is None:
    #         return
    #     query_container = db_container.query_container
    #     if query_container is not None:
    #         query_container.set_editor_focus()

    @property
    def recent_databases(self) -> list:
        return self._recent_dbs

    def add_to_recents(self, display_name: str, path: str):
        self._recent_dbs.append((display_name, path))
    # @recent_databases.setter
    # def recent_databases(self, database_file):
    #     recent_files = CONFIG.get("recentFiles")
    #     if database_file in recent_files:
    #         recent_files.remove(database_file)
    #     recent_files.insert(0, database_file)
    #     self._recent_dbs = recent_files

    @property
    def last_open_folder(self):
        return self._last_open_folder

    def has_main_panel(self):
        return self._main_panel is not None

    def create_database(self):
        """Show a wizard widget to create a new empty database,
        only have one database open at time."""

        if self.has_main_panel():
            return self._say_about_one_db_at_time()
        logger.debug('Creating a new empty database')
        dialog = new_database_dialog.NewDatabaseDialog(self)
        if dialog.exec_() == dialog.Accepted:
            self._main_panel = MainPanel(self)
            self.add_widget(self._main_panel)

    # @Slot(str, str, str)
    # def _on_wizard_finished(self, *data):
    #     """This slot execute when wizard to create a database is finished"""
    #     if
    #     if data:
    #         _, _, fname = data
    #         # Create a new data base container
    #         db_container = database_container.DatabaseContainer(self)
    #         # Associate the file name with the PFile object
    #         pfile_object = pfile.File(fname)
    #         # Associate PFile object with data base container
    #         # and add widget to stacked
    #         db_container.pfile = pfile_object
    #         self.add_widget(db_container)
    #         # Set window title
    #         self.pireal.change_title(file_manager.get_basename(fname))
    #         # Enable db actions
    #         self.pireal.set_enabled_db_actions(True)
    #         self.pireal.set_enabled_relation_actions(True)
    #         self.created = True
    #         logger.debug("La base de datos ha sido creada con éxito")

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
            filters = settings.SUPPORTED_FILES.split(';;')[0]
            filename, _ = QFileDialog.getOpenFileName(self, tr.TR_OPEN_DATABASE, directory, filters)
            # If is canceled, return
            if not filename:
                logger.info('File not selected, bye!')
                return
        # Save last folder
        self._last_open_folder = file_manager.get_path(filename)
        # If filename provide
        try:
            logger.debug('Triying to open the database: "%s"', filename)
            file_obj = File(filename)
            database_content = file_obj.read()
            if not database_content:
                logger.info('The file "%s" is empty', filename)
                QMessageBox.information(
                    self, tr.TR_MSG_INFORMATION, tr.TR_DB_FILE_EMPTY.format(filename))
                return
            database_content = file_manager.parse_database_content(database_content)
        except Exception:
            logger.exception('The database file could not be opened', exc_info=True)
            return

        # Create main panel for table view
        self._main_panel = MainPanel(self)
        self.add_widget(self._main_panel)

        # XXX: quizas eso se deba mover, por ahora lo hacemos acá
        for table in database_content.get('tables'):
            table_name = table['name']
            header = table['header']
            tuples = table['tuples']

            relation_obj = Relation()
            relation_obj.header = header

            for tuple_ in tuples:
                relation_obj.insert(tuple_)

            self._main_panel.central_view.add_relation(relation_obj, table_name)
            self._main_panel.lateral_widget.add_item_to_relations(
                table_name, relation_obj.cardinality(), relation_obj.degree())

        self.pireal.change_title(file_obj.display_name)

        self.add_to_recents(file_obj.display_name, file_obj.path)

        logger.debug('Connected to database: "%s"', file_obj.display_name)

    def open_query(self, filename=''):
        # TODO: se ha sacado el parámetro `remember`, debería ser una configuración
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
        self._main_panel.query_container.open_query()

    # def _open_database(self, filename='', remember=True):
    #     """ This function opens a database and set this on the UI """
    #     logger.debug('Triying to open database...')
    #     if self.created:
    #         return self._say_about_one_db_at_time()

    #     # If not filename provide, then open dialog to select
    #     if not filename:
    #         logger.debug('Filename not provided')
    #         if self._last_open_folder is None:
    #             directory = os.path.expanduser("~")
    #         else:
    #             directory = self._last_open_folder
    #         filter_ = settings.SUPPORTED_FILES.split(';;')[0]
    #         filename, _ = QFileDialog.getOpenFileName(
    #             self, tr.TR_OPEN_DATABASE, directory, filter_)
    #         # If is canceled, return
    #         if not filename:
    #             logger.debug('File not selected, bye!')
    #             return

    #     # If filename provide
    #     try:
    #         logger.debug("Triying to open the database file %s", filename)
    #         # Read pdb file
    #         pfile_object = pfile.File(filename)
    #         db_data = pfile_object.read()
    #         if not db_data:
    #             QMessageBox.warning(self, tr.TR_MSG_ERROR, tr.TR_DB_FILE_EMPTY.format(filename))
    #             logger.warning('The file \'%s\'is empty, aborting...', filename)
    #             return
    #         # Create a dict to manipulate data more easy
    #         db_data = file_manager.parse_database_content(db_data)
    #         logger.debug('Database loaded successful')
    #     except Exception as reason:
    #         logger.exception('The database file could not be opened: %s', filename)
    #         QMessageBox.information(
    #             self, tr.TR_MSG_DB_NOT_OPENED, str(reason))
    #         return

    #     # Create a database container widget
    #     db_container = database_container.DatabaseContainer(self)

    #     try:
    #         db_container.create_database(db_data)
    #     except Exception as reason:
    #         logger.exception('Error creating the database')
    #         QMessageBox.information(self, tr.TR_MSG_ERROR, str(reason))
    #         return

    #     # Set the PFile object to the new database
    #     db_container.pfile = pfile_object
    #     # Add data base container to stacked
    #     self.add_widget(db_container)
    #     # Database name
    #     db_name = file_manager.get_basename(filename)
    #     # Update title with the new database name, and enable some actions
    #     self.databaseConected.emit(tr.TR_NOTIFICATION_DB_CONNECTED.format(db_name))
    #     self.pireal.set_enabled_db_actions(True)
    #     self.pireal.set_enabled_relation_actions(True)
    #     if remember:
    #         # Add to recent databases
    #         self.recent_databases = filename
    #         # Remember the folder
    #         self._last_open_folder = file_manager.get_path(filename)
    #     self.created = True

    # def open_query(self, filename='', remember=True):
    #     if not filename:
    #         if self._last_open_folder is None:
    #             directory = os.path.expanduser("~")
    #         else:
    #             directory = self._last_open_folder
    #         filter_ = settings.SUPPORTED_FILES.split(';;')[1]
    #         filename, _ = QFileDialog.getOpenFileName(self,
    #                                                   tr.TR_OPEN_QUERY,
    #                                                   directory,
    #                                                   filter_)
    #         if not filename:
    #             return
    #     # Si @filename no es False
    #     # Cacheo la carpeta accedida
    #     if remember:
    #         self._last_open_folder = file_manager.get_path(filename)
    #     # FIXME: mejorar éste y new_query
    #     self.new_query(filename)

    # TODO
    # def save_query(self, editor=None):
    #     db = self.get_active_db()
    #     fname = db.save_query(editor)
    #     if fname:
    #         self.querySaved.emit(self.tr("Consulta guardada: {}".format(
    #             fname)))

    # def save_query_as(self):
    #     pass

    # def remove_last_widget(self):
    #     """ Remove last widget from stacked """

    #     widget = self._stacked.widget(self._stacked.count() - 1)
    #     self._stacked.removeWidget(widget)

    # def close_database(self):
    #     """ Close the database and return to the main widget """

    #     db = self.get_active_db()
    #     query_container = db.query_container

    #     if db.modified:
    #         msgbox = QMessageBox(self)
    #         msgbox.setIcon(QMessageBox.Question)
    #         msgbox.setWindowTitle(tr.TR_MSG_SAVE_CHANGES)
    #         msgbox.setText(tr.TR_MSG_SAVE_CHANGES_BODY)
    #         cancel_btn = msgbox.addButton(tr.TR_MSG_CANCEL, QMessageBox.RejectRole)
    #         msgbox.addButton(tr.TR_MSG_NO, QMessageBox.NoRole)
    #         yes_btn = msgbox.addButton(tr.TR_MSG_YES, QMessageBox.YesRole)
    #         msgbox.exec_()
    #         r = msgbox.clickedButton()
    #         if r == cancel_btn:
    #             return
    #         if r == yes_btn:
    #             self.save_database()

    #     # Check if editor is modified
    #     query_widget = query_container.currentWidget()
    #     if query_widget is not None:
    #         weditor = query_widget.get_editor()
    #         if weditor is not None:
    #             # TODO: duplicate code, see tab widget
    #             if weditor.modified:
    #                 msgbox = QMessageBox(self)
    #                 msgbox.setIcon(QMessageBox.Question)
    #                 msgbox.setWindowTitle(tr.TR_MSG_FILE_MODIFIED)
    #                 msgbox.setText(tr.TR_MSG_FILE_MODIFIED_BODY.format(weditor.name))
    #                 cancel_btn = msgbox.addButton(tr.TR_MSG_CANCEL, QMessageBox.RejectRole)
    #                 msgbox.addButton(tr.TR_MSG_NO, QMessageBox.NoRole)
    #                 yes_btn = msgbox.addButton(tr.TR_MSG_YES, QMessageBox.YesRole)
    #                 msgbox.exec_()
    #                 r = msgbox.clickedButton()
    #                 if r == cancel_btn:
    #                     return
    #                 if r == yes_btn:
    #                     self.save_query(weditor)

    #     self._stacked.removeWidget(db)

    #     self.pireal.set_enabled_db_actions(False)
    #     self.pireal.set_enabled_relation_actions(False)
    #     self.pireal.set_enabled_query_actions(False)
    #     self.pireal.set_enabled_editor_actions(False)
    #     self.pireal.change_title()  # Título en la ventana principal 'Pireal'
    #     self.created = False
    #     del db

    # def new_query(self, filename=''):
    #     db_container = self.get_active_db()
    #     db_container.new_query(filename)
    #     # Enable editor actions
    #     # FIXME: refactoring
    #     self.pireal.set_enabled_query_actions(True)
    #     # paste_action = Pireal.get_action("paste_action")
    #     # paste_action.setEnabled(True)
    #     # comment_action = Pireal.get_action("comment")
    #     # comment_action.setEnabled(True)
    #     # uncomment_action = Pireal.get_action("uncomment")
    #     # uncomment_action.setEnabled(True)
    #     # search_action = Pireal.get_action("search")
    #     # search_action.setEnabled(True)

    def execute_query(self):
        self._main_panel.execute_query()
    #     db_container = self.get_active_db()
    #     db_container.execute_queries()

    # def save_database(self):

    #     db = self.get_active_db()
    #     if not db.modified:
    #         return

    #     # Get relations dict
    #     relations = db.table_widget.relations
    #     # Generate content
    #     content = file_manager.generate_database(relations)
    #     db.pfile.save(data=content)
    #     filename = db.pfile.filename
    #     # Emit signal
    #     self.databaseSaved.emit(tr.TR_NOTIFICATION_DB_SAVED.format(filename))

    #     db.modified = False

    # def save_database_as(self):
    #     logger.debug('Triying to save as...')
    #     filter = settings.SUPPORTED_FILES.split(';;')[0]
    #     filename, _ = QFileDialog.getSaveFileName(self, tr.TR_MSG_SAVE_DB_AS,
    #                                               settings.PIREAL_DATABASES,
    #                                               filter)
    #     if not filename:
    #         logger.debug('Not filename provided, exiting.')
    #         return
    #     logger.debug('Filename provided: \'%s\'', filename)
    #     db = self.get_active_db()
    #     # Get relations
    #     relations = db.table_widget.relations
    #     # Content
    #     content = file_manager.generate_database(relations)
    #     # Si no se provee la extensión, le agrego
    #     if not os.path.splitext(filename)[1]:
    #         filename += '.pdb'
    #     db.pfile.save(content, filename)
    #     self.databaseSaved.emit(tr.TR_NOTIFICATION_DB_SAVED.format(db.pfile.filename))
    #     logger.debug('Database saved as: \'%s\'', filename)
    #     db.modified = False

    # def remove_relation(self):
    #     db = self.get_active_db()
    #     if db.delete_relation():
    #         db.modified = True

    def create_new_relation(self):
        dialog = new_relation_dialog.NewRelationDialog(self._main_panel)
        if dialog.exec_() == dialog.Accepted:
            relation_obj, relation_name = dialog.get_data()
            self._main_panel.central_view.add_relation(relation_obj, relation_name)
            rela_card = relation_obj.cardinality()
            rela_deg = relation_obj.degree()
            self._main_panel.lateral_widget.add_item_to_relations(
                relation_name, rela_card, rela_deg)
            # FIXME: database modified, signal!

    def add_start_page(self):
        """ This function adds the Start Page to the stacked widget """

        sp = start_page.StartPage(self)
        self.add_widget(sp)

    def show_settings(self):
        """ Show settings dialog on stacked """

        preferences_dialog = preferences.Preferences(self)
        preferences_dialog.show()
    #     # if isinstance(self.widget(1), preferences.Preferences):
    #     #     self.widget(1).close()
    #     # else:
    #     #     self.stacked.insertWidget(1, preferences_dialog)
    #     #     self.stacked.setCurrentIndex(1)

    #     # # Connect the closed signal
    #     # preferences_dialog.settingsClosed.connect(self._settings_closed)
    #     logger.debug('Showing preferences...')
    #     widget = preferences.Preferences(self)
    #     widget.show()

    # def widget(self, index):
    #     """ Returns the widget at the given index """

    #     return self._stacked.widget(index)

    def add_widget(self, widget):
        """ Appends and show the given widget to the Stacked """

        index = self._stacked.addWidget(widget)
        self._stacked.setCurrentIndex(index)

    # def _settings_closed(self):
    #     self._stacked.removeWidget(self.widget(1))
    #     self._stacked.setCurrentWidget(self._stacked.currentWidget())

    # def get_active_db(self):
    #     """ Return an instance of DatabaseContainer widget if the
    #     stacked contains an DatabaseContainer in last index or None if it's
    #     not an instance of DatabaseContainer """

    #     index = self._stacked.count() - 1
    #     widget = self.widget(index)
    #     if isinstance(widget, database_container.DatabaseContainer):
    #         return widget
    #     return None

    # def get_unsaved_queries(self):
    #     query_container = self.get_active_db().query_container
    #     return query_container.get_unsaved_queries()

    # def undo_action(self):
    #     query_container = self.get_active_db().query_container
    #     query_container.undo()

    # def redo_action(self):
    #     query_container = self.get_active_db().query_container
    #     query_container.redo()

    # def cut_action(self):
    #     query_container = self.get_active_db().query_container
    #     query_container.cut()

    # def copy_action(self):
    #     query_container = self.get_active_db().query_container
    #     query_container.copy()

    # def paste_action(self):
    #     query_container = self.get_active_db().query_container
    #     query_container.paste()

    # def comment(self):
    #     query_container = self.get_active_db().query_container
    #     query_container.comment()

    # def uncomment(self):
    #     query_container = self.get_active_db().query_container
    #     query_container.uncomment()

    # def add_tuple(self):
    #     lateral = self.get_active_db().lateral_widget
    #     if lateral.relation_list.has_item() == 0:
    #         return
    #     rname = lateral.relation_list.current_text()
    #     from pireal.gui.dialogs.edit_relation_dialog import EditRelationDialog
    #     dialog = EditRelationDialog(rname, self)
    #     tw = self.get_active_db().table_widget
    #     dialog.sendData.connect(tw.insert_rows)
    #     dialog.show()

    # def add_column(self):
    #     tw = self.get_active_db().table_widget
    #     tw.add_column()

    # def delete_tuple(self):
    #     lateral = self.get_active_db().lateral_widget
    #     if lateral.relation_list.has_item() == 0:
    #         return
    #     r = QMessageBox.question(
    #         self,
    #         tr.TR_MSG_REMOVE_TUPLES,
    #         tr.TR_MSG_REMOVE_TUPLES_BODY,
    #         QMessageBox.Yes | QMessageBox.Cancel)
    #     if r == QMessageBox.Cancel:
    #         return
    #     tw = self.get_active_db().table_widget
    #     tw.delete_tuple()

    # def delete_column(self):
    #     tw = self.get_active_db().table_widget
    #     tw.delete_column()

    # def search(self):
    #     query_container = self.get_active_db().query_container
    #     query_container.search()
