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
    QSettings,
    pyqtSlot
)
from PyQt5.QtGui import (
    QPalette,
    QColor
)

from src.gui import (
    table_widget,
    lateral_widget,
    view,
    model,
    delegate
)

from src.gui.query_container import query_container
from src.core import (
    relation,
    pfile,
    file_manager,
    settings
)
from src.core.logger import Logger

logger = Logger(__name__)


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
        self.query_container.saveEditor['PyQt_PyObject'].connect(
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
            # Para entender más, leer el código de cáda módulo
            # src.gui.model
            # src.gui.view
            # src.gui.delegate
            _view = self.create_table(rela, table_name)
            # Add relation to relations dict
            self.table_widget.add_relation(table_name, rela)
            # Add table to stacked
            self.table_widget.stacked.addWidget(_view)
            # Add table name to list widget
            self.lateral_widget.relation_list.add_item(
                table_name, rela.cardinality(), rela.degree())
        # Select first item
        # self.lateral_widget.relation_list.select_first()

    def create_table(self, relation_obj, relation_name, editable=True):
        """ Se crea la vista, el model y el delegado para @relation_obj """

        _view = view.View()
        header = view.Header()
        _model = model.Model(relation_obj)
        _model.modelModified[bool].connect(self.__on_model_modified)
        _model.cardinalityChanged[int].connect(
                self.__on_cardinality_changed)
        if not editable:
            _model.editable = False
            header.editable = False
        _view.setModel(_model)
        _view.setItemDelegate(delegate.Delegate())
        _view.setHorizontalHeader(header)
        return _view

    @pyqtSlot(bool)
    def __on_model_modified(self, modified):
        self.modified = modified

    @pyqtSlot(int)
    def __on_cardinality_changed(self, value):
        # self.lateral_widget.update_item(value)
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
                    QMessageBox.information(self, self.tr("Información"),
                                            self.tr("Ya existe una relación "
                                                    "con el nombre  "
                                                    "'{}'".format(
                                                        relation_name)))
                    return False

            self.table_widget.add_table(rel, relation_name)
            # self.lateral_widget.add_item(relation_name, rel.cardinality())
            return True

    def delete_relation(self):
        name = self.lateral_widget.relation_list.current_text()
        index = self.lateral_widget.relation_list.current_index()
        if not name:
            return
        msgbox = QMessageBox(self)
        msgbox.setIcon(QMessageBox.Question)
        msgbox.setWindowTitle(self.tr("Confirmación"))
        msgbox.setText(
            self.tr("Está seguro de eliminar la relación <b>{}</b>?".format(
                name)))
        msgbox.addButton(self.tr("No!"), QMessageBox.NoRole)

        si = msgbox.addButton(self.tr("Si, estoy seguro"), QMessageBox.YesRole)
        palette = QPalette()
        palette.setColor(QPalette.Button, QColor("#cc575d"))
        palette.setColor(QPalette.ButtonText, QColor("white"))
        si.setPalette(palette)
        msgbox.exec_()
        if msgbox.clickedButton() == si:
            self.lateral_widget.relation_list.remove_item(index)
            self.table_widget.remove_table(index)
            self.table_widget.remove_relation(name)
            return True
        return False

    def __on_data_table_changed(self, row, col, data):
        # current_relation = self.lateral_widget.current_text()
        # # Relation to be update
        # rela = self.table_widget.relations.get(current_relation)
        # # Clear old content
        # rela.clear()
        # current_table = self.table_widget.stacked.currentWidget()
        # model = current_table.model()
        # for i in range(model.rowCount()):
        #     reg = []
        #     for j in range(model.columnCount()):
        #         if row == i and col == j:
        #             reg.append(data)
        #         else:
        #             reg.append(model.item(i, j).text())
        #     # Insert new content
        #     rela.insert(reg)
        # # Update relation
        # self.table_widget.relations[current_relation] = rela
        pass

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
            editor.pfile.save(data=content)
        except Exception as reason:
            QMessageBox.critical(self, "Error",
                                 self.tr("El archivo no se puede abrir!"
                                         "\n\n{}".format(reason)))
            return False
        editor.saved()
        return editor.pfile.filename

    def save_query_as(self, editor=None):
        filename = QFileDialog.getSaveFileName(self,
                                               self.tr("Guardar Archivo"),
                                               editor.name,
                                               "Pireal query files(*.pqf)")
        filename = filename[0]
        if not filename:
            return
        # Get the content
        content = editor.toPlainText()
        # Write the file
        editor.pfile.save(data=content, path=filename)
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

        qsettings = QSettings(settings.SETTINGS_PATH, QSettings.IniFormat)
        qsettings.setValue('vsplitter_sizes',
                           self._vsplitter.saveState())
        qsettings.setValue('hsplitter_sizes',
                           self.saveState())
        # FIXME: save sizes of query container
