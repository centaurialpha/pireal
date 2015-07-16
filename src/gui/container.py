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
from PyQt4.QtGui import (
    QVBoxLayout,
    QStackedWidget,
    QInputDialog,
    QFileDialog,
    QMessageBox,
    QSplitter
)
from PyQt4.QtCore import Qt
from src.gui.main_window import Pireal
from src.gui import (
    start_page,
    table_widget,
    new_relation_dialog
)
from src.core import (
    settings,
    file_manager
)
#FIXME: refactoring


class Container(QSplitter):

    def __init__(self, orientation=Qt.Vertical):
        super(Container, self).__init__(orientation)
        self._data_bases = []
        self.__filename = ""
        vbox = QVBoxLayout(self)
        vbox.setContentsMargins(0, 0, 0, 0)
        self.__created = False
        # Stacked
        self.stacked = QStackedWidget()
        vbox.addWidget(self.stacked)

        # Table
        self.table_widget = table_widget.TableWidget()

        Pireal.load_service("container", self)

    def create_data_base(self, filename=''):
        """ This function opens or creates a database

        :param filename: Database filename
        """

        if self.__created:
            QMessageBox.critical(self, self.tr("Error"),
                                 self.tr("Solo puede tener una base de datos "
                                         "abierta a la vez."))
            return
        from_file = False
        if not filename:
            db_name, ok = QInputDialog.getText(self, self.tr("Nueva DB"),
                                               self.tr("Nombre:"))
            if not ok:
                return
        else:
            from_file = True
            # Read database from file
            try:
                data = file_manager.open_database(filename)
            except Exception as reason:
                QMessageBox.critical(self, self.tr("Error!"),
                                     reason.__str__())
                return
            # This is intended to give support multiple database
            for name, files in data.items():
                db_name = name
        # Remove the start page
        self.stacked.removeWidget(self.stacked.widget(0))
        self.stacked.addWidget(self.table_widget)
        pireal = Pireal.get_service("pireal")
        # Title
        pireal.change_title(db_name)
        if from_file:
            self.load_relation(files)
        # Enable QAction's
        pireal.enable_disable_db_actions()
        self.__created = True

    def create_new_relation(self):
        dialog = new_relation_dialog.NewRelationDialog(self)
        dialog.show()

    def new_query(self, filename=''):
        query_widget = Pireal.get_service("query_widget")
        self.addWidget(query_widget)
        if not query_widget.isVisible():
            query_widget.show()
        pireal = Pireal.get_service("pireal")
        pireal.enable_disable_query_actions()
        query_widget.new_query(filename)

    def show_start_page(self):
        sp = start_page.StartPage()
        self.stacked.addWidget(sp)

    def close_db(self):
        widget = self.stacked.currentWidget()
        if isinstance(widget, table_widget.TableWidget):
            self.close()

    def save_query(self):
        query_widget = Pireal.get_service("query_widget")
        # Editor instance
        editor = query_widget.get_active_editor()
        if editor.rfile.is_new:
            return self.save_query_as(editor)
        content = editor.toPlainText()
        editor.rfile.write(content)
        editor.document().setModified(False)

    def open_file(self):
        directory = os.path.expanduser("~")
        filename = QFileDialog.getOpenFileName(self, self.tr("Abrir Archivo"),
                                               directory, settings.RFILES,
                                               QFileDialog.DontUseNativeDialog)
        if not filename:
            return
        ext = file_manager.get_extension(filename)
        if ext == '.pqf':
            # Query file
            self.new_query(filename)
        else:
            self.create_data_base(filename)

    def save_query_as(self, editor=None):
        if editor is None:
            query_widget = Pireal.get_service("query_widget")
            editor = query_widget.get_active_editor()
        directory = os.path.expanduser("~")
        filename = QFileDialog.getSaveFileName(self,
                                               self.tr("Guardar Archivo"),
                                               directory)
        if not filename:
            return
        content = editor.toPlainText()
        editor.rfile.write(content, filename)
        editor.document().setModified(False)

    def load_relation(self, filenames=[]):
        """ Load relation from file """

        import csv
        from PyQt4.QtGui import QTableWidgetItem, QTableWidget
        from src.core import relation

        if not filenames:
            native_dialog = QFileDialog.DontUseNativeDialog
            directory = os.path.expanduser("~")
            filenames = QFileDialog.getOpenFileNames(self,
                                                     self.tr("Abrir Archivo"),
                                                     directory,
                                                     self.tr("Relaciones "
                                                     "{}").format(
                                                         settings.RFILES),
                                                     native_dialog)
            if not filenames:
                return
        lateral = Pireal.get_service("lateral")
        for filename in filenames:
            rel = relation.Relation(filename)
            relation_name = os.path.splitext(os.path.basename(filename))[0]
            self.table_widget.relations[relation_name] = rel
            table = QTableWidget()
            with open(filename, newline='') as f:
                table.setRowCount(0)
                table.setColumnCount(0)
                csv_reader = csv.reader(f)
                for row_data in csv_reader:
                    row = table.rowCount()
                    table.setColumnCount(len(row_data))
                    for column, data in enumerate(row_data):
                        item = QTableWidgetItem()
                        item.setText(data)
                        if row == 0:
                            table.setHorizontalHeaderItem(column, item)
                        else:
                            table.setItem(row - 1, column, item)
                    table.insertRow(row)
                table.removeRow(table.rowCount() - 1)
            self.table_widget.stacked.addWidget(table)
        #FIXME: names
        names = [os.path.splitext(os.path.basename(i))[0]
                 for i in filenames]
        lateral.add_item_list(names)
        lateral.show()

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


container = Container()
