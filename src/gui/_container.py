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
    QVBoxLayout,
    QStackedWidget,
    QFileDialog,
    QMessageBox,
    QSplitter,
)
from PyQt5.QtCore import (
    Qt,
    pyqtSignal
)
from src import translations as tr
from src.gui.main_window import Pireal
from src.gui import (
    start_page,
    table_widget
)
from src.gui.dialogs import new_relation_dialog, preferences
from src.core import (
    settings,
    file_manager,
    logger,
    pfile
    #relation
)
# FIXME: refactoring
log = logger.get_logger(__name__)
DEBUG = log.debug
ERROR = log.error


class Container(QSplitter):
    dbModified = pyqtSignal(int)
    currentFileSaved = pyqtSignal('QString')

    def __init__(self, orientation=Qt.Vertical):
        super(Container, self).__init__(orientation)
        self.__last_open_folder = None
        self.db_file = None
        self.__ndata_base = 1
        self.__filename = ""
        self.__created = False
        self.__modified = False
        vbox = QVBoxLayout(self)
        vbox.setContentsMargins(0, 0, 0, 0)
        # Stacked
        self.stacked = QStackedWidget()
        vbox.addWidget(self.stacked)

        # Table
        self.table_widget = table_widget.TableWidget()

        Pireal.load_service("container", self)

        # Connections
        self.dbModified[int].connect(self._database_modified)

    def create_data_base(self, filename=''):
        """ This function opens or creates a database

        :param filename: Database filename
        """

        if self.__created:
            QMessageBox.critical(self, "Error", tr.TR_CONTAINER_ERROR_DB)
            return

        # Pireal File
        _file = pfile.PFile(filename)

        if filename:
            try:
                data = _file.read()
            except Exception as reason:
                QMessageBox.critical(self, "Error!", reason.__str__())
                return
            db_name = _file.name
            # Add data base
            self.table_widget.add_data_base(data)
        else:
            db_name = "untitled_{}.pdb".format(self.__ndata_base)

        # Remove Start Page widget
        if isinstance(self.stacked.widget(0), start_page.StartPage):
            self.stacked.removeWidget(self.stacked.widget(0))
        self.stacked.addWidget(self.table_widget)
        # Title
        pireal = Pireal.get_service("pireal")
        pireal.change_title(db_name)
        self.__db_name = db_name
        # Enable QAction's
        pireal.enable_disable_db_actions()
        self.db_file = _file
        self.__created = True
        self.__ndata_base += 1
        # Add to recent files
        self.__add_to_recent(_file.filename)

    def __add_to_recent(self, filename):
        files = settings.get_setting('recentFiles', [])
        if filename not in files:
            files.insert(0, filename)
            del files[settings.PSettings.MAX_RECENT_FILES:]
            settings.set_setting('recentFiles', files)

    def get_db_name(self):
        return self.__db_name

    def open_recent_file(self):
        filename = self.sender().data()
        self.create_data_base(filename)

    def create_new_relation(self):
        dialog = new_relation_dialog.NewRelationDialog(self)

        dialog.dbModified[int].connect(self._database_modified)
        dialog.show()

    def _database_modified(self, value):
        if value == 0:
            self.__modified = True

    def remove_relation(self, items):
        pass
        #lateral = Pireal.get_service("lateral")
        #for item in items:
            #index = row()
        #rname = lateral.get_relation_name()
        #if not rname:
            #QMessageBox.critical(self, "Error",
                                 #tr.TR_CONTAINER_UNSELECTED_RELATIONSHIP)
            #return
        #r =QMessageBox.question(self, tr.TR_CONTAINER_CONFIRM_DELETE_REL_TITLE,
                                 #tr.TR_CONTAINER_CONFIRM_DELETE_REL.format(
                                     #rname), QMessageBox.Yes | QMessageBox.No)
        #if r == QMessageBox.No:
            #return
        #index = lateral.current_index()
        ## Remove table
        #self.table_widget.remove_table(index)
        ## Remove item from list widget
        #lateral.remove_item(index)

    def new_query(self, filename=''):
        query_widget = Pireal.get_service("query_widget")
        self.addWidget(query_widget)
        if not query_widget.isVisible():
            query_widget.show()
        pireal = Pireal.get_service("pireal")
        pireal.enable_disable_query_actions()
        query_widget.new_query(filename)

        query_widget.currentEditorSaved['PyQt_PyObject'].connect(
            self.save_query)

    @property
    def modified(self):
        return self.__modified

    def show_start_page(self):
        if settings.PSettings.SHOW_START_PAGE:
            # Add Start Page on stacked, index = 0
            sp = start_page.StartPage()
            self.stacked.insertWidget(0, sp)
            self.stacked.setCurrentIndex(0)

    def close_db(self):
        """ Close data base """

        widget = self.stacked.currentWidget()
        if isinstance(widget, table_widget.TableWidget):
            # Clear list of relations
            lateral = Pireal.get_service("lateral")
            lateral.clear_items()
            lateral.hide()
            # Close table widget
            self.stacked.removeWidget(widget)
            # Add start page
            self.show_start_page()

            self.__created = False

    def save_query(self, weditor=None):
        if not weditor:
            query_widget = Pireal.get_service("query_widget")
            # Editor instance
            weditor = query_widget.get_active_editor()
        if weditor.pfile.is_new:
            return self.save_query_as(weditor)
        content = weditor.toPlainText()
        weditor.pfile.write(content)
        weditor.document().setModified(False)

        self.currentFileSaved.emit(tr.TR_CONTAINER_FILE_SAVED.format(
                                   weditor.filename))

    def save_query_as(self, editor=None):
        if editor is None:
            query_widget = Pireal.get_service("query_widget")
            editor = query_widget.get_active_editor()
        directory = os.path.expanduser("~")
        filename = QFileDialog.getSaveFileName(self,
                                               tr.TR_CONTAINER_SAVE_FILE,
                                               directory)
        if not filename:
            return
        content = editor.toPlainText()
        editor.pfile.write(content, filename)
        editor.document().setModified(False)

    def save_data_base(self):

        directory = os.path.expanduser("~")
        filename = QFileDialog.getSaveFileName(self,
                                               tr.TR_CONTAINER_SAVE_DB,
                                               directory)
        if not filename:
            return

        # Generate content
        content = file_manager.generate_database(self.table_widget.relations)
        # Create the database on a pdb file
        self.db_file.write(content, filename + '.pdb')

    def open_file(self):

        if self.__last_open_folder is None:
            directory = os.path.expanduser("~")
        else:
            directory = self.__last_open_folder
        filename = QFileDialog.getOpenFileName(self, tr.TR_CONTAINER_OPEN_FILE,
                                               directory, settings.DBFILE)[0]
        if not filename:
            return
        # Save folder
        self.__last_open_folder = file_manager.get_path(filename)

        ext = file_manager.get_extension(filename)
        if ext == '.pqf':
            # Query file
            self.new_query(filename)
        else:
            self.create_data_base(filename)

    def convert_to_pdb(self):
        pass
        #directory = os.path.expanduser("~")
        #rdb_file = QFileDialog.getOpenFileName(self,
                                               #tr.TR_CONTAINER_OPEN_FILE,
                                               #directory,
                                               #"WinRDBI Database File (*.rdb)")
        #rdb_content = file_manager.read_rdb_file(rdb_file)
        #file_manager.convert_to_pdb(rdb_content)

    def load_relation(self, filenames=[]):
        """ Load relation from file """

        if not filenames:
            native_dialog = QFileDialog.DontUseNativeDialog
            if self.__last_open_folder is None:
                directory = os.path.expanduser("~")
            else:
                directory = self.__last_open_folder
            ffilter = settings.RFILES.split(';;')[-1]
            filenames = QFileDialog.getOpenFileNames(self,
                                                     tr.TR_CONTAINER_OPEN_FILE,
                                                     directory, ffilter,
                                                     native_dialog)
            if not filenames:
                return
            # Save folder
            self.__last_open_folder = file_manager.get_path(filenames[0])
            #self.__modified = True

        # Load tables
        self.table_widget.load_relation(filenames)
        # Emit signal
        self.dbModified.emit(0)

    def execute_queries(self):
        query_widget = Pireal.get_service("query_widget")
        query_widget.execute_queries()

    def undo_action(self):
        query_widget = Pireal.get_service("query_widget")
        query_widget.undo()

    def redo_action(self):
        query_widget = Pireal.get_service("query_widget")
        query_widget.redo()

    def cut_action(self):
        query_widget = Pireal.get_service("query_widget")
        query_widget.cut()

    def copy_action(self):
        query_widget = Pireal.get_service("query_widget")
        query_widget.copy()

    def paste_action(self):
        query_widget = Pireal.get_service("query_widget")
        query_widget.paste()

    def check_opened_query_files(self):
        query_widget = Pireal.get_service("query_widget")
        return query_widget.opened_files()

    def show_dialog(self, widget):
        if isinstance(self.stacked.widget(1), preferences.Preferences):
            self.stacked.widget(1).close()
        else:
            self.stacked.insertWidget(1, widget)
            self.stacked.setCurrentIndex(1)

        widget.settingsClosed.connect(self._settings_closed)

    def _settings_closed(self):
        self.stacked.removeWidget(self.stacked.widget(1))
        self.stacked.setCurrentWidget(self.stacked.currentWidget())


container = Container()
