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

import re
from PyQt5.QtWidgets import (
    QSplitter,
    QFileDialog,
    QMessageBox
)
from PyQt5.QtCore import Qt
from src.gui.main_window import Pireal
from src.gui import database_widget
from src.gui.query_container import query_container
from src import translations as tr
from src.core import (
    parser,
    pfile,
    settings,
    file_manager
)
    #table_widget,
    #lateral_widget
#)


class MainContainer(QSplitter):

    def __init__(self, orientation=Qt.Vertical):
        QSplitter.__init__(self, orientation)

        self.db_widget = database_widget.DBWidget()
        self.addWidget(self.db_widget)

        self.query_tab_container = query_container.QueryTabContainer()
        self.query_tab_container.hide()
        self.addWidget(self.query_tab_container)

        self.__ndatabase, self.__nquery, self.__nrelation = 1, 1, 1

        # Load service
        Pireal.load_service("main", self)

    def open_file(self, filename=''):
        filename = QFileDialog.getOpenFileName(self, tr.TR_CONTAINER_OPEN_FILE,
                                               "~", settings.DBFILE)[0]
        if not filename:
            return
        extension = file_manager.get_extension(filename)
        if extension == '.pqf':
            central = Pireal.get_service("central")
            if not central.created:
                QMessageBox.information(central, "Information",
                                        "First create or open a database")
                return
            # Query file
            self.new_query(filename)
        else:
            # Database file
            self.create_database(filename)

    def create_database(self, filename=''):
        """ This function opens or creates a database """

        central = Pireal.get_service("central")
        if central.created:
            QMessageBox.critical(self, "Error", tr.TR_CONTAINER_ERROR_DB)
            return
        central.add_main_container()
        # Pireal File
        ffile = pfile.PFile(filename)
        if filename:
            try:
                data = ffile.read()
            except Exception as reason:
                QMessageBox.critical(self, "Error", reason.__str__())
                return
            db_name = ffile.name
            self.db_widget.table_widget.add_data_base(data)
        else:
            db_name = "database_{}.pdb".format(self.__ndatabase)
        pireal = Pireal.get_service("pireal")
        # Title
        pireal.change_title(db_name)
        # Enable QAction's
        pireal.enable_disable_db_actions()
        central.created = True
        self.__ndatabase += 1

    def close_database(self):
        pass

    def new_query(self, filename=''):
        qcontainer = query_container.QueryContainer()

        if not filename:
            ffile = pfile.PFile()
            filename = "New_query_{}.qpf".format(self.__nquery)
            ffile.filename = filename
            self.__nquery += 1
        else:
            ffile = pfile.PFile(filename)
            qcontainer.add_editor_text(ffile.read())

        if not self.query_tab_container.isVisible():
            self.query_tab_container.show()

        pireal = Pireal.get_service("pireal")
        pireal.enable_disable_query_actions()

        index = self._add_query_tab(qcontainer, ffile.name)
        self.query_tab_container.setTabToolTip(index, ffile.filename)

        self.setSizes([(self.height() / 5) * 2, 1])

    def _add_query_tab(self, widget, title):
        return self.query_tab_container.add_tab(widget, title)

    def execute_queries(self):
        query_container = self.query_tab_container.currentWidget()
        text = query_container.text()

        #widgets = mdi.subWindowList(1)
        table_widget = self.db_widget.table_widget
        # Ignore comments
        for line in text.splitlines():
            if line.startswith('--'):
                continue
            parts = line.split('=', 1)
            parts[0] = parts[0].strip()
            if re.match(r'^[_a-zA-Z]+[_a-zA-Z0-9]*$', parts[0]):
                relation_name, line = parts
            else:
                relation_name = 'relation_{}'.format(self.__nrelation)
                self.__nrelation += 1
            try:
                expression = parser.convert_to_python(line.strip())
                relation = eval(expression, table_widget.relations)
            except Exception as reason:
                QMessageBox.critical(self, tr.TR_QUERY_ERROR, reason.__str__())
                return

            query_container.add_list_items([relation_name])
            query_container.add_new_table(relation, relation_name)
            table_widget.relations[relation_name] = relation


main = MainContainer()
