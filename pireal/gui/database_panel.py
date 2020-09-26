# -*- coding: utf-8 -*-
#
# Copyright 2015-2020 - Gabriel Acosta <acostadariogabriel@gmail.com>
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

import logging

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QPushButton

from PyQt5.QtCore import Qt

from pireal.core.db import DB
from pireal.gui.lateral_widget import LateralWidget, RelationItemType
from pireal.gui.query_container import QueryContainer
from pireal.gui.central_view import CentralView
from pireal.gui.widgets import RememberingSplitter


logger = logging.getLogger('gui.database_panel')


class DBPanel(QWidget):

    def __init__(self, db, parent=None):
        super().__init__(parent=parent)
        layout = QHBoxLayout(self)
        self.db: DB = db
        # Divide UI in 3 areas
        self.lateral_widget = LateralWidget()
        self.central_view = CentralView()
        self.query_widget = QueryContainer()

        self._v_split = RememberingSplitter(orientation=Qt.Vertical)
        self._v_split.addWidget(self.central_view)
        self._v_split.addWidget(self.query_widget)

        self._h_split = RememberingSplitter(orientation=Qt.Horizontal)
        self._h_split.addWidget(self.lateral_widget)
        self._h_split.addWidget(self._v_split)
        layout.addWidget(self._h_split)

        # if not self.db.is_new():
        #     self._load_db()

        # self.lateral_widget.relationClicked.connect(
        #     self.central_view.relation_widget.set_current_index)
        self._create_empty_widget()

    def _create_empty_widget(self):
        widget = QWidget()
        hbox = QHBoxLayout(widget)
        btn_add_relation = QPushButton('Add Relation')
        btn_create_relation = QPushButton('Create Relation')
        hbox.addWidget(btn_add_relation)
        hbox.addWidget(btn_create_relation)

    def _load_db(self):
        for rela in self.db.relations:
            self.central_view.relation_widget.add_view(rela)
            self.add_relation_to_list(rela)

    def add_relation(self, rela):
        self.db.add(rela)
        self.central_view.relation_widget.add_view(rela)

    def add_relation_to_list(self, rela):
        self.lateral_widget.add_item(rela, RelationItemType.Normal)

    def add_relation_to_results_list(self, rela):
        self.lateral_widget.add_item(rela, RelationItemType.Result)

    def clear_relations_list(self):
        self.lateral_widget.clear()

    def clear_relations_result_list(self):
        self.lateral_widget.clear_results()

    def add_query(self, filename: str):
        self.query_widget.load_or_create_new_editor(filename)
