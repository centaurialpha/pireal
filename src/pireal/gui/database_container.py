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
import logging

from PyQt5.QtWidgets import QSplitter
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox

from PyQt5.QtCore import Qt
from PyQt5.QtCore import QSettings
from PyQt5.QtCore import pyqtSlot as Slot

from pireal.gui import (
    table_widget,
    lateral_widget,
)
from pireal.gui.model_view_delegate import create_view
from pireal.gui.lateral_widget import RelationItemType

from pireal.gui.query_container import query_container
from pireal.core import (
    relation,
    pfile,
    file_manager
)
from pireal.dirs import DATA_SETTINGS
from pireal import translations as tr
from pireal.gui.main_window import Pireal
from pireal import settings

logger = logging.getLogger(__name__)


class DatabaseContainer(QSplitter):

    def __init__(self, orientation=Qt.Horizontal):
        QSplitter.__init__(self, orientation)
        self.pfile = None

        self.lateral_widget = lateral_widget.LateralWidget()
        self.table_widget = table_widget.TableWidget()
        self.query_container = query_container.QueryContainer(self)

        self._vsplitter = QSplitter(Qt.Vertical)
        self._vsplitter.addWidget(self.table_widget)
        self._vsplitter.addWidget(self.query_container)
        self.addWidget(self.lateral_widget)
        self.addWidget(self._vsplitter)

        self.modified = False

        self.__nquery = 1

        # Connections
        # FIXME
        self.lateral_widget.relationClicked.connect(self._on_relation_clicked)

        # lambda i: self.table_widget.stacked.setCurrentIndex(i))
        # For change table widget item when up/down
        # see issue #39
        self.lateral_widget.relationSelectionChanged.connect(
            lambda i: self.table_widget.stacked.setCurrentIndex(i))
        self.query_container.saveEditor.connect(
            self.save_query)
        self.setSizes([1, 1])

    def _on_relation_clicked(self, index):
        if not self.table_widget._other_tab.isVisible():
            self.table_widget._tabs.setCurrentIndex(0)
        self.table_widget.stacked.setCurrentIndex(index)

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

            # Creo el objeto Relation
            rela = relation.Relation()
            rela.header = header
            # Relleno el objeto con las tuplas
            for _tuple in tuples:
                rela.insert(_tuple)
            # Se usa el patrón Modelo/Vista/Delegado
            _view = self.create_table(rela, table_name)
            # Add relation to relations dict
            self.table_widget.add_relation(table_name, rela)
            # Add table to stacked
            self.table_widget.stacked.addWidget(_view)
            # Add table name to list widget
            # FIXME: feooo
            rela.name = table_name
            self.lateral_widget.add_item(rela, RelationItemType.Normal)

    def create_table(self, relation_obj, relation_name, editable=True):
        """ Se crea la vista, el model y el delegado para @relation_obj """

        return create_view(relation_obj, editable=editable)

    @Slot(bool)
    def __on_model_modified(self, modified):
        self.modified = modified

    @Slot(int)
    def __on_cardinality_changed(self, value):
        self.lateral_widget.relation_list.update_cardinality(value)

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
                    QMessageBox.information(
                        self,
                        tr.TR_MSG_INFORMATION,
                        tr.TR_RELATION_NAME_ALREADY_EXISTS.format(relation_name)
                    )
                    return False

            self.table_widget.add_table(rel, relation_name)
            return True

    def delete_relation(self):
        index = self.lateral_widget.current_index()
        name = self.lateral_widget.current_text()
        if not name:
            return
        ret = QMessageBox.question(
            self,
            tr.TR_MSG_CONFIRMATION,
            tr.TR_MSG_REMOVE_RELATION.format(name),
            QMessageBox.Yes | QMessageBox.No
        )
        if ret == QMessageBox.Yes:
            self.lateral_widget.remove_relation(index)
            self.table_widget.remove_table(index)
            self.table_widget.remove_relation(name)
            return True
        return False

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
        if not editor.modified:
            return
        if editor.is_new:
            return self.save_query_as(editor)
        # Get content of editor
        content = editor.toPlainText()
        try:
            editor.pfile.save(data=content)
        except Exception:
            QMessageBox.critical(
                self,
                'Error',
                tr.TR_MSG_FILE_NOT_OPENED
            )
            return False
        editor.saved()
        return editor.pfile.filename

    def save_query_as(self, editor=None):
        if not editor:
            if self.query_container.currentWidget() is None:
                return
            editor = self.query_container.currentWidget().get_editor()
        filename = QFileDialog.getSaveFileName(
            self,
            tr.TR_MSG_SAVE_QUERY_FILE,
            editor.name,
            settings.get_extension_filter('.pqf')
        )
        filename = filename[0]
        if not filename:
            return
        # Get the content
        content = editor.toPlainText()
        # Write the file
        editor.pfile.save(data=content, path=filename)
        editor.saved()
        pireal = Pireal.get_service('pireal')
        pireal.status_bar.show_message(tr.TR_STATUS_QUERY_SAVED.format(filename))

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
        qsettings = QSettings(str(DATA_SETTINGS), QSettings.IniFormat)
        vsizes = qsettings.value('vsplitter_sizes', None)
        if vsizes is not None:
            self._vsplitter.restoreState(vsizes)
        else:
            self._vsplitter.setSizes([self.height() / 3, self.height() / 6])
        hsizes = qsettings.value('hsplitter_sizes', None)
        if hsizes is not None:
            self.restoreState(hsizes)
        else:
            self.setSizes([self.width() / 10, self.width() / 3])

    def save_sizes(self):
        """ Save sizes of Splitters """

        qsettings = QSettings(str(DATA_SETTINGS), QSettings.IniFormat)
        qsettings.setValue('vsplitter_sizes',
                           self._vsplitter.saveState())
        qsettings.setValue('hsplitter_sizes',
                           self.saveState())
        # FIXME: save sizes of query container
