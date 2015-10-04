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
    QWidget,
    QVBoxLayout,
    QStackedWidget,
    QFileDialog,
    QMessageBox
)
from src.gui.main_window import Pireal
from src.gui import start_page
from src.gui import database_widget
from src import translations as tr
from src.core import settings


class CentralWidget(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        box = QVBoxLayout(self)
        box.setContentsMargins(0, 0, 0, 0)

        # Stacked
        self.stack = QStackedWidget()
        box.addWidget(self.stack)

        # Database widget
        self.db_widget = database_widget.DBWidget()

        self.__db_created = False
        self.__n_database = 1

        # Load service
        Pireal.load_service("central", self)

    def add_start_page(self):
        """  """

        startp = start_page.StartPage()
        index = self.add_widget(startp)
        self.stack.setCurrentIndex(index)

    def add_widget(self, widget):
        """ Add widget to stacked and return the index """

        index = self.stack.addWidget(widget)
        return index

    def new_database(self, name=''):
        if self.__db_created:
            QMessageBox.critical(self, "Error!", tr.TR_CONTAINER_ERROR_DB)
            return
        mdi = Pireal.get_service("mdi")
        index = self.add_widget(mdi)
        self.stack.setCurrentIndex(index)

        # Create mdi child

        sub_window = mdi.addSubWindow(self.db_widget)
        sub_window.resize(self.width(), self.height() / 2)

        window_title = self.db_widget.create_database(name)
        if window_title.startswith('untitled'):
            window_title = window_title.format(self.__n_database)
        sub_window.setWindowTitle(window_title)
        sub_window.show()

        pireal = Pireal.get_service("pireal")
        pireal.enable_disable_db_actions()

        self.__db_created = True
        self.__n_database += 1

    def new_query(self):
        query_widget = Pireal.get_service("query_container")
        pireal = Pireal.get_service("pireal")
        mdi_area = self.stack.currentWidget()
        sub_window = mdi_area.addSubWindow(query_widget)
        sub_window.resize(self.width() / 1.5, self.height() / 2)
        sub_window.show()
        sub_window.add_container()
        pireal.enable_disable_relation_actions()

    def open_file(self, filename=''):
        if not filename:
            filename = QFileDialog.getOpenFileName(self,
                                                   tr.TR_CONTAINER_OPEN_FILE,
                                                   "~", settings.DBFILE)[0]
            if not filename:
                return

        self.new_database(filename)

    def open_recent_file(self):
        pass

    def execute_queries(self):
        query_container = Pireal.get_service("query_container")
        query_container.execute_queries()

central = CentralWidget()
