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

import csv

from PyQt5.QtWidgets import (
    QSplitter,
    QFileDialog,
    QMessageBox
)
from PyQt5.QtCore import (
    Qt,
    QSettings
)
from PyQt5.QtGui import (
    QStandardItem,
    QStandardItemModel
)

from src.gui import (
    table_widget,
    lateral_widget,
    custom_table
)

from src.gui.query_container import query_container
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


class DatabaseContainer(QSplitter):

    def __init__(self, orientation=Qt.Vertical):
        QSplitter.__init__(self, orientation)
        self.pfile = None
        self._hsplitter = QSplitter(Qt.Horizontal)

        self.lateral_widget = lateral_widget.LateralWidget()
        self._hsplitter.addWidget(self.lateral_widget)
        self.table_widget = table_widget.TableWidget()
        self._hsplitter.addWidget(self.table_widget)

        self.addWidget(self._hsplitter)

        self.query_container = query_container.QueryContainer()
        self.addWidget(self.query_container)

        self.modified = False

        self.__nquery = 1

        # Connections
        # FIXME
        self.lateral_widget.itemClicked.connect(
            lambda: self.table_widget.stacked.show_display(
                self.lateral_widget.row()))
        self.query_container.saveEditor['PyQt_PyObject'].connect(
            self.save_query)
        self.setSizes([1, 1])

    def dbname(self):
        """ Return display name """

        return self.pfile.display_name

    def is_new(self):
        return self.pfile.is_new

    def create_database(self, data):
        for table in data.get('tables'):
            # Get data
            table_name = table.get('name')
            header = table.get('header')
            tuples = table.get('tuples')

            # Create relation
            rela = relation.Relation()
            rela.header = header

            # Table view widget
            table_view = custom_table.Table()
            # Model
            model = QStandardItemModel()
            model.setHorizontalHeaderLabels(header)

            # Populate table view
            row_count = 0
            for row in tuples:
                for col_count, i in enumerate(row):
                    item = QStandardItem(i)
                    # Set read only
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    model.setItem(row_count, col_count, item)
                rela.insert(row)
                row_count += 1

            # Set table model
            table_view.setModel(model)
            # Add relation to relations dict
            self.table_widget.add_relation(table_name, rela)
            # Add table to stacked
            self.table_widget.stacked.addWidget(table_view)
            # Add table name to list widget
            self.lateral_widget.add_item(table_name, rela.count())
        # Select first item
        first_item = self.lateral_widget.topLevelItem(0)
        first_item.setSelected(True)

    def load_relation(self, filenames):
        for filename in filenames:
            with open(filename) as f:
                csv_reader = csv.reader(f)
                header = next(csv_reader)
                rel = relation.Relation()
                rel.header = header
                for i in csv_reader:
                    rel.insert(i)
                relation_name = file_manager.get_basename(filename)
                if not self.table_widget.add_relation(relation_name, rel):
                    QMessageBox.information(self, self.tr("Information"),
                                            self.tr("There is already a "
                                                    "relationship with name "
                                                    "'{}'".format(
                                                        relation_name)))
                    return False

            self.table_widget.add_table(rel, relation_name)
            self.lateral_widget.add_item(relation_name, rel.count())
            return True

    def delete_relation(self):
        selected_items = self.lateral_widget.selectedItems()
        if not selected_items:
            return False
        current_row = 0
        if self.lateral_widget.row() != -1:
            current_row = self.lateral_widget.row()
        if len(selected_items) > 1:
            msg = self.tr("Are you sure you want to delete "
                          "the selected relations?")
        else:
            msg = self.tr("Are you sure you want to delete "
                          "the relation <b>{}</b>?".format(
                              self.lateral_widget.item_text(current_row)))
        msgbox = QMessageBox(self)
        msgbox.setIcon(QMessageBox.Question)
        msgbox.setWindowTitle(self.tr("Confirmation"))
        msgbox.setText(msg)
        msgbox.addButton(self.tr("No"), QMessageBox.NoRole)
        yes_btn = msgbox.addButton(self.tr("Yes"), QMessageBox.YesRole)
        msgbox.exec_()
        r = msgbox.clickedButton()
        if r == yes_btn:
            for item in selected_items:
                index = self.lateral_widget.indexOfTopLevelItem(item)
                # Remove from list
                self.lateral_widget.takeTopLevelItem(index)
                # Remove table
                self.table_widget.remove_table(index)
                # Remove relation
                self.table_widget.remove_relation(item.name)
            return True

    def __on_data_table_changed(self, row, col, data):
        current_relation = self.lateral_widget.current_text()
        # Relation to be update
        rela = self.table_widget.relations.get(current_relation)
        # Clear old content
        rela.clear()
        current_table = self.table_widget.stacked.currentWidget()
        model = current_table.model()
        for i in range(model.rowCount()):
            reg = []
            for j in range(model.columnCount()):
                if row == i and col == j:
                    reg.append(data)
                else:
                    reg.append(model.item(i, j).text())
            # Insert new content
            rela.insert(reg)
        # Update relation
        self.table_widget.relations[current_relation] = rela

    def new_query(self, filename):
        editor_tab_at = self.query_container.is_open(filename)
        if editor_tab_at != -1:
            self.query_container.set_focus_editor_tab(editor_tab_at)
        else:
            query_widget = query_container.QueryWidget()
            # Create object file
            ffile = pfile.File(filename)
            editor = query_widget.get_editor()
            editor.pfile = ffile
            if not filename:
                ffile.filename = 'untitled_{n}.pqf'.format(n=self.__nquery)
            else:
                content = ffile.read()
                editor.setPlainText(content)
            self.query_container.add_tab(query_widget, ffile.display_name)
            self.__nquery += 1

    def save_query(self, editor):
        if not editor:
            editor = self.query_container.currentWidget().get_editor()
        if editor.is_new:
            return self.save_query_as(editor)
        # Get content of editor
        content = editor.toPlainText()
        try:
            editor.pfile.save(content=content)
        except Exception as reason:
            QMessageBox.critical(self, "Error",
                                 self.tr("The file couldn't be saved!"
                                         "\n\n{}".format(reason)))
            return False
        editor.saved()
        return editor.pfile.filename

    def save_query_as(self, editor=None):
        filename = QFileDialog.getSaveFileName(self, self.tr("Save File"),
                                               editor.name,
                                               "Pireal query files(*.pqf)")
        filename = filename[0]
        if not filename:
            return
        # Get the content
        content = editor.toPlainText()
        # Write the file
        editor.pfile.save(content=content, new_fname=filename)
        editor.saved()

    def execute_queries(self):
        self.query_container.execute_queries()

    def execute_selection(self):
        editor = self.query_container.currentWidget().get_editor()
        text_cursor = editor.textCursor()
        if text_cursor.hasSelection():
            query = text_cursor.selectedText()
            self.query_container.execute_queries(query)

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
        # FIXME: save sizes of query container
