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

from PyQt4.QtGui import (
    QWidget,
    QVBoxLayout,
    QStackedWidget,
    QInputDialog,
    QFileDialog
)
from src.gui.main_window import Pireal
from src.gui import (
    start_page,
    table_widget,
    new_relation_dialog
)


class Container(QWidget):

    def __init__(self):
        super(Container, self).__init__()
        self.__filename = ""
        vbox = QVBoxLayout(self)
        vbox.setContentsMargins(0, 0, 0, 0)
        # Stacked
        self.stacked = QStackedWidget()
        vbox.addWidget(self.stacked)

        # Table
        self.table_widget = table_widget.TableWidget()

        Pireal.load_service("container", self)

    def create_data_base(self):
        db_name, ok = QInputDialog.getText(self, self.tr("Nueva DB"),
                                           self.tr("Nombre:"))
        if ok:
            # Remove the start page
            self.stacked.removeWidget(self.stacked.widget(0))
            self.stacked.addWidget(self.table_widget)
            # Enable QAction's
            pireal = Pireal.get_service("pireal")
            pireal.enable_disable_db_actions()
            lateral = Pireal.get_service("lateral")
            lateral.show()
            # Title
            pireal.change_title(db_name)

    def create_new_relation(self):
        dialog = new_relation_dialog.NewRelationDialog(self)
        dialog.show()

    def new_query(self):
        query_widget = Pireal.get_service("query_widget")
        if not query_widget.isVisible():
            query_widget.show()
            pireal = Pireal.get_service("pireal")
            pireal.enable_disable_query_actions()
        query_widget.new_query()

    def show_start_page(self):
        sp = start_page.StartPage()
        self.stacked.addWidget(sp)

    def close_db(self):
        widget = self.stacked.currentWidget()
        if isinstance(widget, table_widget.TableWidget):
            self.close()

    def load_relation(self):
        """ Load relation from file """

        import csv
        import os
        from PyQt4.QtGui import QTableWidgetItem, QTableWidget

        filenames = QFileDialog.getOpenFileNames(self,
                                                 self.tr("Abrir Archivo"))
        lateral = Pireal.get_service("lateral")
        for filename in filenames:
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
        names = [os.path.splitext(os.path.basename(i))[0]
                 for i in filenames]
        lateral.add_item_list(names)

    def execute_queries(self):
        query_widget = Pireal.get_service("query_widget")
        query_widget.execute_queries()

    def closeEvent(self, event):
        print("CLOSE")

container = Container()
