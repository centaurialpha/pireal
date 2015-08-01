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
    QSplitter,
    QTableWidget,
    QTableWidgetItem
)
from PyQt4.QtCore import (
    Qt,
    SIGNAL
)
from src.gui.main_window import Pireal
from src.gui import (
    start_page,
    table_widget,
    new_relation_dialog
)
from src.core import (
    settings,
    file_manager,
    logger,
    #relation
)
# FIXME: refactoring
log = logger.get_logger(__name__)
DEBUG = log.debug
ERROR = log.error


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
        if not filename:
            db_name, ok = QInputDialog.getText(self, self.tr("Nueva DB"),
                                               self.tr("Nombre:"))
            if not ok:
                return
        else:
            # From file
            try:
                db_name, data = file_manager.open_database(filename)
            except Exception as reason:
                QMessageBox.critical(self, self.tr("Error!"),
                                     reason.__str__())
                return

            self.table_widget.add_data_base(data)

        # Remove Start Page widget
        self.stacked.removeWidget(self.stacked.widget(0))
        self.stacked.addWidget(self.table_widget)
        # Title
        pireal = Pireal.get_service("pireal")
        pireal.change_title(db_name)
        # Enable QAction's
        pireal.enable_disable_db_actions()
        self.__created = True

    def create_new_relation(self):
        dialog = new_relation_dialog.NewRelationDialog(self)
        dialog.show()

    def remove_relation(self):
        lateral = Pireal.get_service("lateral")
        lateral.remove_table()

    def new_query(self, filename=''):
        query_widget = Pireal.get_service("query_widget")
        self.addWidget(query_widget)
        if not query_widget.isVisible():
            query_widget.show()
        pireal = Pireal.get_service("pireal")
        pireal.enable_disable_query_actions()
        query_widget.new_query(filename)

        self.connect(query_widget,
                     SIGNAL("currentEditorSaved(QPlainTextEdit)"),
                     self.save_query)

    def show_start_page(self):
        sp = start_page.StartPage()
        self.stacked.addWidget(sp)

    def close_db(self):
        widget = self.stacked.currentWidget()
        if isinstance(widget, table_widget.TableWidget):
            self.close()

    def save_query(self, weditor=None):
        if weditor is None:
            query_widget = Pireal.get_service("query_widget")
            # Editor instance
            weditor = query_widget.get_active_editor()
        if weditor.rfile.is_new:
            return self.save_query_as(weditor)
        content = weditor.toPlainText()
        weditor.rfile.write(content)
        weditor.document().setModified(False)

        self.emit(SIGNAL("currentFileSaved(QString)"),
                  self.tr("Archivo guardado: {}").format(weditor.filename))

    def open_file(self):

        directory = os.path.expanduser("~")
        filename = QFileDialog.getOpenFileName(self, self.tr("Abrir Archivo"),
                                               directory, settings.DBFILE,
                                               QFileDialog.DontUseNativeDialog)
        if not filename:
            return
        ext = file_manager.get_extension(filename)
        if ext == '.pqf':
            # Query file
            self.new_query(filename)
        elif ext == '.rdb':
            self.load_rdb_database(file_manager.read_rdb_file(filename))
        else:
            self.create_data_base(filename)

    def load_rdb_database(self, content):
        csv_content = ""
        for line in content.splitlines():
            if line.startswith('@'):
                csv_content += '@'
                portion = line.split('(')
                name = portion[0][1:]
                csv_content += name + ':'
                for i in portion[1].split(','):
                    if not i.startswith(' '):
                        field = i.split('/')[0].strip()
                        csv_content += field + ','
            else:
                if not line:
                    continue
                csv_content += line
            csv_content += '\n'

        self.table_widget.add_table_from_rdb_content(csv_content)

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
        from src.core import relation

        if not filenames:
            native_dialog = QFileDialog.DontUseNativeDialog
            directory = os.path.expanduser("~")
            ffilter = settings.RFILES.split(';;')[-1]
            filenames = QFileDialog.getOpenFileNames(self,
                                                     self.tr("Abrir Archivo"),
                                                     directory, ffilter,
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
                        item = Item()
                        item.setText(data)
                        if row == 0:
                            table.setHorizontalHeaderItem(column, item)
                        else:
                            table.setItem(row - 1, column, item)
                    table.insertRow(row)
                table.removeRow(table.rowCount() - 1)
            self.table_widget.stacked.addWidget(table)
        # FIXME: names
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


class Item(QTableWidgetItem):

    def __init__(self, parent=None):
        super(Item, self).__init__(parent)
        self.setFlags(self.flags() ^ Qt.ItemIsEditable)


container = Container()
