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
from PyQt5.QtCore import pyqtSlot as Slot

from pireal.core.db import DB
from pireal.gui.panels.lateral_panel import LateralPanel, RelationItemType
from pireal.gui.panels.query_panel import QueryPanel
from pireal.gui.panels.relation_panel import RelationPanel
from pireal.gui.widgets import RememberingSplitter


logger = logging.getLogger('gui.database_panel')


class DBPanel(QWidget):

    def __init__(self, db=None, parent=None):
        super().__init__(parent=parent)
        layout = QHBoxLayout(self)
        # Divide UI in 3 areas
        self.lateral_panel = LateralPanel()
        self.relation_panel = RelationPanel()
        self.query_panel = QueryPanel(self)

        self.db = db or DB()
        self._load_db()

        self._v_split = RememberingSplitter(orientation=Qt.Vertical)
        self._v_split.addWidget(self.relation_panel)
        self._v_split.addWidget(self.query_panel)

        self._h_split = RememberingSplitter(orientation=Qt.Horizontal)
        self._h_split.addWidget(self.lateral_panel)
        self._h_split.addWidget(self._v_split)
        layout.addWidget(self._h_split)

        self._create_empty_widget()

        # Connections
        self.lateral_panel.relationClicked.connect(self.set_current_index_in_relation_widget)
        self.lateral_panel.resultClicked.connect(self.set_current_index_in_results_widget)

    @Slot(int)
    def set_current_index_in_relation_widget(self, index):
        self.relation_panel.set_current_index(0)
        self.relation_panel.relation_widget.set_current_index(index)

    @Slot(int)
    def set_current_index_in_results_widget(self, index):
        self.relation_panel.set_current_index(1)
        self.relation_panel.relation_result_widget.set_current_index(index)

    def _create_empty_widget(self):
        widget = QWidget()
        hbox = QHBoxLayout(widget)
        btn_add_relation = QPushButton('Add Relation')
        btn_create_relation = QPushButton('Create Relation')
        hbox.addWidget(btn_add_relation)
        hbox.addWidget(btn_create_relation)

    def _load_db(self):
        for rela in self.db.relations:
            self.relation_panel.relation_widget.add_view(rela)
            self.add_relation_to_list(rela)

    def add_relation(self, rela):
        self.db.add(rela)
        self.relation_panel.relation_widget.add_view(rela)

    def add_relation_to_results(self, rela):
        self.relation_panel.relation_result_widget.add_view(rela)

    def add_relation_to_list(self, rela):
        self.lateral_panel.add_item(rela, RelationItemType.Normal)

    def add_relation_to_results_list(self, rela):
        self.lateral_panel.add_item(rela, RelationItemType.Result)

    def clear_relations_list(self):
        logger.debug('clean up list of relations')
        self.lateral_panel.clear()

    def clear_relations_result_list(self):
        logger.debug('clean up list of results')
        self.lateral_panel.clear_results()

    def add_new_editor_query(self, filename: str = None):
        self.query_panel.load_or_create_new_editor(filename)
