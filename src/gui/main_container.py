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

from PyQt5.QtWidgets import (
    QSplitter,
    QFileDialog,
    QMessageBox
)
from PyQt5.QtCore import (
    Qt,
    QSettings
)
from PyQt5.QtGui import QStandardItem

from src.gui import (
    table_widget,
    list_widget,
    custom_table
)
from src.gui.dialogs import edit_relation_dialog
from src.gui.query_container import query_container
from src import translations as tr
from src.core import (
    relation,
    pfile,
    file_manager,
    settings
)
from src.core.logger import PirealLogger

# Logger
logger = PirealLogger(__name__)
DEBUG = logger.debug


class MainContainer(QSplitter):

    def __init__(self, pfile='', orientation=Qt.Vertical):
        QSplitter.__init__(self, orientation)
        self.__pfile = pfile
        self._hsplitter = QSplitter(Qt.Horizontal)

        self.lateral_widget = list_widget.LateralWidget()
        self._hsplitter.addWidget(self.lateral_widget)
        self.table_widget = table_widget.TableWidget()
        self._hsplitter.addWidget(self.table_widget)

        self.addWidget(self._hsplitter)

        self.query_container = query_container.QueryContainer()
        self.addWidget(self.query_container)

        self.modified = False

        self.__nquery = 1

        # Connections
        self.lateral_widget.currentRowChanged[int].connect(
            lambda i: self.table_widget.stacked.setCurrentIndex(i))
        #self.lateral_widget.itemRemoved[int].connect(
            #lambda i: self.table_widget.remove_table(i))
        self.lateral_widget.showEditRelation.connect(self.__edit_relation)
        self.lateral_widget.doubleClicked.connect(self.__edit_relation)
        self.query_container.saveEditor['PyQt_PyObject'].connect(
            self.save_query)
        self.setSizes([1, 1])

    def dbname(self):
        """ Return display name """

        return self.__pfile.name

    def isnew(self):
        return self.__pfile.is_new

    @property
    def pfile(self):
        return self.__pfile

    def create_database(self, data):
        for table in data.get('tables'):
            # Table view widget
            table_view = custom_table.Table()
            model = table_view.model()
            # Get data
            table_name = table.get('name')
            fields = table.get('fields')
            tuples = table.get('tuples')
            types = table.get('types')

            model.setHorizontalHeaderLabels(fields)

            # Create relation
            rela = relation.Relation()
            rela.fields = fields
            # Populate table view
            row_count = 0
            for row in tuples:
                for col_count, i in enumerate(row):
                    item = QStandardItem(i)
                    model.setItem(row_count, col_count, item)
                    delegate = table_view.itemDelegate()
                    delegate.data_types[col_count] = types[col_count]
                rela.insert(row)
                row_count += 1
            # Add relation to relations dict
            self.table_widget.add_relation(table_name, rela)
            # Add table to stacked
            self.table_widget.stacked.addWidget(table_view)
            # Add table name to list widget
            self.lateral_widget.add_item(table_name)

    def load_relation(self, filenames):
        for filename in filenames:
            rel = relation.Relation(filename)
            relation_name = file_manager.get_basename(filename)
            if not self.table_widget.add_relation(relation_name, rel):
                QMessageBox.information(self, self.tr("Information"),
                                        self.tr("There is already a "
                                                "relationship with name "
                                                "'{}'".format(relation_name)))
                return
            self.__add_table(rel, relation_name)

    def delete_relation(self):
        selected_items = self.lateral_widget.selectedItems()
        if selected_items:
            if len(selected_items) > 1:
                msg = tr.TR_CENTRAL_CONFIRM_DELETE_RELATIONS
            else:
                msg = tr.TR_CENTRAL_CONFIRM_DELETE_RELATION.format(
                    self.lateral_widget.text_item(
                        self.lateral_widget.currentRow()))

            r = QMessageBox.question(self,
                                     tr.TR_CENTRAL_CONFIRM_DELETE_REL_TITLE,
                                     msg, QMessageBox.No | QMessageBox.Yes)
            if r == QMessageBox.No:
                return
            for item in selected_items:
                index = self.lateral_widget.row(item)
                # Remove from list
                self.lateral_widget.takeItem(index)
                # Remove table
                self.table_widget.remove_table(index)
                # Remove relation
                name = item.text().split()[0].strip()
                self.table_widget.remove_relation(name)

    def __on_data_table_changed(self, table_name):
        current_table = self.table_widget.stacked.currentWidget()
        rel = self.table_widget.relations[table_name]
        # Reset
        rel.clear()
        for nrow in range(current_table.rowCount()):
            reg = []
            for ncol in range(current_table.columnCount()):
                item = current_table.item(nrow, ncol)
                reg.append(item.text())
            # Insert new data
            rel.insert(reg)

    def __edit_relation(self, index):
        index = index.row()
        name = self.lateral_widget.text_item(index)
        item = self.table_widget.stacked.widget(index)
        dialog = edit_relation_dialog.EditRelationDialog(item, name, self)
        dialog.tableChanged.connect(self.__on_data_table_changed)
        dialog.exec_()

    def __add_table(self, rela, relation_name):
        ptable = custom_table.Table()
        model = ptable.model()

        row_count = 0
        for row in rela.content:
            for col_count, data in enumerate(row):
                item = QStandardItem(data)
                model.setItem(row_count, col_count, item)
            row_count += 1

        self.table_widget.stacked.addWidget(ptable)
        self.lateral_widget.add_item(relation_name)

    def new_query(self, filename):
        editor_tab_at = self.query_container.is_open(filename)
        if  editor_tab_at != -1:
            self.query_container.set_focus_editor_tab(editor_tab_at)
        else:
            query_widget = query_container.QueryWidget()
            # Create object file
            ffile = pfile.PFile(filename)
            editor = query_widget.get_editor()
            editor.pfile = ffile
            if not filename:
                ffile.filename = 'untitled_{n}.pqf'.format(n=self.__nquery)
            else:
                content = ffile.read()
                editor.setPlainText(content)
            self.query_container.add_tab(query_widget, ffile.name)
            self.__nquery += 1

    def save_query(self, editor=None):
        if editor is None:
            editor = self.query_container.currentWidget().get_editor()
        if editor.is_new:
            return self.save_query_as(editor)
        # Get content of editor
        content = editor.toPlainText()
        editor.pfile.write(content=content)
        editor.saved()

    def save_query_as(self, editor=None):
        filename = QFileDialog.getSaveFileName(self, tr.TR_CONTAINER_SAVE_FILE,
                                               editor.name,
                                               "Pireal query files(*.pqf)")
        filename = filename[0]
        if not filename:
            return
        # Get the content
        content = editor.toPlainText()
        # Write the file
        editor.pfile.write(content=content, new_fname=filename)
        editor.saved()

    def execute_queries(self):
        self.query_container.execute_queries()

    def showEvent(self, event):
        QSplitter.showEvent(self, event)
        qsettings = QSettings(settings.SETTINGS_PATH, QSettings.IniFormat)
        hsizes = qsettings.value('hsplitter_sizes', None)
        if hsizes is not None:
            self._hsplitter.restoreState(hsizes)
        else:
            self._hsplitter.setSizes([1, self._hsplitter.width() / 3])
        vsizes = qsettings.value('vsplitter_sizes', None)
        if vsizes is not None:
            self.restoreState(vsizes)
        else:
            self.setSizes([(self.height() / 3) * 2, self.height() / 3])

    def save_sizes(self):
        """ Save sizes of Splitters """

        qsettings = QSettings(settings.SETTINGS_PATH, QSettings.IniFormat)
        qsettings.setValue('hsplitter_sizes',
                           self._hsplitter.saveState())
        qsettings.setValue('vsplitter_sizes',
                           self.saveState())
        #FIXME: save sizes of query container