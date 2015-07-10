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

import getpass
from PyQt4.QtGui import (
    QInputDialog,
    QFileDialog
)
from PyQt4.QtCore import QObject
from src.gui.main_window import Pireal
from src.core import parser


class Actions(QObject):

    def __init__(self):
        super(Actions, self).__init__()
        Pireal.load_service("actions", self)

    def create_data_base(self):
        mdi = Pireal.get_service("mdi")
        db_name, ok = QInputDialog.getText(mdi, self.tr("New DB"),
                                           self.tr("Name:"),
                                           text=getpass.getuser())
        if ok:
            from src.gui import table_widget
            db_widget = table_widget.MdiDB()
            db_widget.setWindowTitle(db_name + '.pdb')
            db_widget.setMinimumSize(mdi.width(), mdi.height() / 1.7)
            mdi.addSubWindow(db_widget)
            # Enable QAction's
            pireal = Pireal.get_service("pireal")
            pireal.enable_disable_db_actions()
            db_widget.show()

    def create_new_relation(self):
        from src.gui import new_relation_dialog
        pireal = Pireal.get_service("pireal")
        dialog = new_relation_dialog.NewRelationDialog(pireal)
        dialog.show()

    def new_query(self):
        from src.gui.query_editor import query_widget
        widget = query_widget.QueryWidget()
        pireal = Pireal.get_service("pireal")
        # Load the instance
        Pireal.load_service("query-editor", widget)
        # MdiArea
        mdi = Pireal.get_service("mdi")
        widget.setMinimumSize(mdi.width(), mdi.minimumSizeHint().height())
        mdi.addSubWindow(widget)
        # Enable querie's QAction
        pireal.enable_disable_query_actions()
        widget.show()

    def open_file(self):
        pireal = Pireal.get_service("pireal")
        filename = QFileDialog.getOpenFileNames(pireal,
                                                self.tr("Abrir Archivo"))
        print(filename)

    def execute_queries(self):
        # Editor instance
        query_editor = Pireal.get_service("query-editor").editor
        query = query_editor.toPlainText()  # Text
        # Parse query
        expression = parser.convert_to_python(query)
        table_widget = Pireal.get_service("db")
        rel = eval(expression, table_widget.relations)


actions = Actions()
