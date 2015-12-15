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

#import os

from PyQt5.QtWidgets import (
    QSplitter,
    #QFileDialog,
    QMessageBox
)
from PyQt5.QtCore import Qt

#from src.gui.main_window import Pireal
from src.gui import (
    #database_widget
    table_widget,
    list_widget,
    table
)
from src.gui.dialogs import edit_relation_dialog
from src.gui.query_container import query_container
from src import translations as tr
from src.core import (
    relation,
    #pfile,
    #settings,
    file_manager
)
    #table_widget,
    #lateral_widget
#)


class MainContainer(QSplitter):

    def __init__(self, pfile, orientation=Qt.Vertical):
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

        # Connections
        self.lateral_widget.currentRowChanged[int].connect(
            lambda i: self.table_widget.stacked.setCurrentIndex(i))
        #self.lateral_widget.itemRemoved[int].connect(
            #lambda i: self.table_widget.remove_table(i))
        self.lateral_widget.showEditRelation.connect(self.__edit_relation)
        self.lateral_widget.doubleClicked.connect(self.__edit_relation)

        self.setSizes([1, 1])

    #def get_last_open_folder(self):
        #return self.__last_open_folder

    def dbname(self):
        """ Return display name """

        return self.__pfile.name

    def isnew(self):
        return self.__pfile.is_new

    def create_database(self, data):
        rel = None
        for part in data.split('@'):
            for e, line in enumerate(part.splitlines()):
                # Remove whitespaces
                line = ','.join(list(map(str.strip, line.split(','))))
                if e == 0:
                    if line.endswith(','):
                        line = line[:-1]
                    name = line.split(':')[0]
                    rel = relation.Relation()
                    rel.fields = line.split(':')[-1].split(',')
                else:
                    rel.insert(line.split(','))
            if rel is not None:
                #ptable = table.Table()
                #ptable.itemChanged.connect(self.__on_data_table_changed)
                #ptable.setColumnCount(len(rel.fields))
                #ptable.setHorizontalHeaderLabels(rel.fields)
                self.table_widget.add_relation(name, rel)
                self.__add_table(rel, name)

    def load_relation(self, filenames):
        for filename in filenames:
            rel = relation.Relation(filename)
            relation_name = file_manager.get_basename(filename)
            if self.table_widget.add_relation(relation_name, rel):
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
        ptable = table.Table()
        ptable.setColumnCount(len(rela.fields))
        ptable.setHorizontalHeaderLabels(rela.fields)

        for row in rela.content:
            nrow = ptable.rowCount()
            ptable.insertRow(nrow)
            for column, data in enumerate(row):
                item = table.Item()
                item.setText(data)
                ptable.setItem(nrow, column, item)

        self.table_widget.stacked.addWidget(ptable)
        self.lateral_widget.add_item(relation_name, nrow + 1)

        # Connect the signal when data changed
        #ptable.cellChanged.connect(self.__on_data_table_changed)

    def new_query(self):
        self.query_container.add_tab()

    def execute_queries(self):
        self.query_container.execute_queries()

    #def __add_to_recent(self, filename):
        #files = settings.get_setting('recentDB', [])
        #if filename not in files:
            #files.insert(0, filename)
            #del files[settings.PSettings.MAX_RECENT_FILES:]
            #settings.set_setting('recentDB', files)

    #def get_recent_db(self):
        #return settings.PSettings.RECENT_DB

    #def create_new_relation(self):
        #from src.gui.dialogs import new_relation_dialog
        #d = new_relation_dialog.NewRelationDialog()
        #d.show()

    #def _change_state_actions(self, value):
        #qactions = [
            #'undo_action',
            #'redo_action',
            #'copy_action',
            #'cut_action',
            #'paste_action',
        #]
        #for qaction in qactions:
            #Pireal.get_action(qaction).setEnabled(value)

    #def new_query(self, filename=''):
        #self.query_container.add_tab()
        #qcontainer = query_container.QueryContainer()
        #qcontainer.editorFocused.connect(self._change_state_actions)
        #qcontainer.editorModified.connect(self._editor_modified)

        #if not filename:
            #ffile = pfile.PFile()
            #filename = "New_query_{}.qpf".format(self.__nquery)
            #ffile.filename = filename
            #self.__nquery += 1
        #else:
            #ffile = pfile.PFile(filename)
            #qcontainer.add_editor_text(ffile.read())

        #qcontainer.set_pfile(ffile)

        #if not self.query_tab_container.isVisible():
            #self.query_tab_container.show()

        #pireal = Pireal.get_service("pireal")
        #pireal.enable_disable_query_actions()

        #index = self._add_query_tab(qcontainer, ffile.name)
        #self.query_tab_container.setTabToolTip(index, ffile.filename)

        #self.setSizes([(self.height() / 5) * 2, 1])

    #def _add_query_tab(self, widget, title):
        #return self.query_tab_container.add_tab(widget, title)

    #def _editor_modified(self, modified):
        #self.query_tab_container.tab_modified(modified)
        #weditor = self.query_tab_container.currentWidget().editor()
        #weditor.modified = True

    #def execute_queries(self):
        #self.query_container.execute_queries()

    def showEvent(self, event):
        QSplitter.showEvent(self, event)
        self._hsplitter.setSizes([1, self._hsplitter.width() / 3])

#main = MainContainer()
