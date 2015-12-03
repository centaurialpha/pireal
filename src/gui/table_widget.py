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
    #QTableWidget,
    #QTableWidgetItem,
    #QHeaderView,
    #QAbstractItemView
)
#from PyQt5.QtCore import Qt
    #Qt,
    #SIGNAL
#)

#from src.core import (
    #relation,
    #file_manager
#)
from src.gui import table
from src.gui.main_window import Pireal


class TableWidget(QWidget):

    def __init__(self):
        super(TableWidget, self).__init__()

        vbox = QVBoxLayout(self)
        vbox.setContentsMargins(0, 0, 0, 0)

        self.relations = {}

        # Stack
        self.stacked = QStackedWidget()
        vbox.addWidget(self.stacked)

    def count(self):
        return self.stacked.count()

    def add_relation(self, name, rela):
        if self.relations.get(name, None) is None:
            self.relations[name] = rela
            return True
        return False

    #def add_data_base(self, data):
        ##FIXME: refactoring
        ##lateral = Pireal.get_service("lateral")
        #lateral = Pireal.get_service("main").lateral_widget
        #rel = None
        #for part in data.split('@'):
            #for e, line in enumerate(part.splitlines()):
                ## Remove whitespaces
                #line = ','.join(list(map(str.strip, line.split(','))))
                #if e == 0:
                    ##line = line[:-1]
                    #if line.endswith(','):
                        #line = line[:-1]
                    #name = line.split(':')[0]

                    #rel = relation.Relation()
                    #rel.fields = line.split(':')[-1].split(',')
                #else:
                    #rel.insert(line.split(','))
            #if rel is not None:
                #ptable = table.Table()
                #ptable.setRowCount(1)
                #ptable.setColumnCount(0)
                #self.add_relation(name, rel)

                #for _tuple in rel.content:
                    #row = table.rowCount()
                    #table.setColumnCount(len(rel.fields))
                    #for column, text in enumerate(_tuple):
                        #item = Item()
                        #item.setText(text)
                        #table.setItem(row - 1, column, item)
                    #table.insertRow(row)
                #table.setHorizontalHeaderLabels(rel.fields)
                #self.stacked.addWidget(table)
                #table.removeRow(table.rowCount() - 1)
                #ntuples = ' [' + str(table.rowCount()) + ']'
                #lateral.add_item_list([name + ntuples])

    #def load_relation(self, filenames):
        #lateral = Pireal.get_service("lateral")
        #for filename in filenames:
            #rel = relation.Relation(filename)
            #rel_name = file_manager.get_basename(filename)
            #self.relations[rel_name] = rel
            #table = Table()
            #table.setRowCount(1)
            #table.setColumnCount(0)

            #for _tuple in rel.content:
                #row = table.rowCount()
                #table.setColumnCount(len(rel.fields))
                #for column, text in enumerate(_tuple):
                    #item = Item()
                    #item.setText(text)
                    #table.setItem(row - 1, column, item)
                #table.insertRow(row)
            #table.removeRow(table.rowCount() - 1)
            #table.setHorizontalHeaderLabels(rel.fields)
            #self.stacked.addWidget(table)
            #lateral.add_item_list([rel_name])

    def add_table(self, rows, columns, name, data, fields):
        """ Add new table from New Relation Dialog """

        ptable = table.Table()
        ptable.setRowCount(rows)
        ptable.setColumnCount(columns)
        ptable.setHorizontalHeaderLabels(fields)

        for k, v in list(data.items()):
            item = table.Item()
            item.setText(v)
            ptable.setItem(k[0] - 1, k[1], item)

        self.stacked.addWidget(ptable)
        self.stacked.setCurrentIndex(self.count() - 1)
        central = Pireal.get_service("central")
        active_db = central.get_active_db()
        active_db.modified = True

        #lateral.add_item_list([name])

    #def add_new_table(self, rel, name):
        #import itertools

        #table = Table()
        #table.setRowCount(0)
        #table.setColumnCount(0)

        #data = itertools.chain([rel.fields], rel.content)

        #for row_data in data:
            #row = table.rowCount()
            #table.setColumnCount(len(row_data))
            #for col, text in enumerate(row_data):
                #item = QTableWidgetItem()
                #item.setText(text)
                #if row == 0:
                    #table.setHorizontalHeaderItem(col, item)
                #else:
                    #table.setItem(row - 1, col, item)
            #table.insertRow(row)
        #table.removeRow(table.rowCount() - 1)
        #self.stacked.addWidget(table)
        #self.stacked.setCurrentIndex(self.stacked.count() - 1)
        #lateral = Pireal.get_service("lateral")
        #lateral.add_item_list([name])

    #def remove_table(self, index):
        #table = self.stacked.widget(index)
        #self.stacked.removeWidget(table)

    #def add_table_from_rdb_content(self, content):
        #lateral = Pireal.get_service("lateral")
        #lateral.show()
        #for line in content.splitlines():
            #if line.startswith('@'):
                #table = Table()
                #name = line.split(':')[0][1:]
                #lateral.add_item_list([name])
                #fields = line.split(':')[-1].split(',')[:-1]
                #table.setColumnCount(len(fields))
                #table.setHorizontalHeaderLabels(fields)
                #self.stacked.addWidget(table)
            #else:
                #row = table.rowCount()
                #for e, i in enumerate(line.split(',')):
                    #item = QTableWidgetItem()
                    #item.setText(i)
                    #table.setItem(row - 1, e, item)
                #table.insertRow(row)
