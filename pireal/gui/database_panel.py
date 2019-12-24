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

from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QSplitter

from PyQt5.QtCore import Qt

from pireal.core.db import DB
from pireal.core.relation import Relation
from pireal.gui.panels.lateral_panel import LateralPanel, RelationItemType
from pireal.gui.panels.query_panel import QueryPanel
from pireal.gui.panels.relation_panel import RelationPanel

logger = logging.getLogger('gui.database_panel')


class DBPanel(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        layout = QHBoxLayout(self)

        self._db: DB = None

        self.lateral_panel = LateralPanel(self)
        self.relation_panel = RelationPanel(self)
        self.query_panel = QueryPanel(self)

        # Divide UI in 3 areas
        self._v_split = QSplitter(orientation=Qt.Vertical)
        self._v_split.addWidget(self.relation_panel)
        self._v_split.addWidget(self.query_panel)

        self._h_split = QSplitter(orientation=Qt.Horizontal)
        self._h_split.addWidget(self.lateral_panel)
        self._h_split.addWidget(self._v_split)
        layout.addWidget(self._h_split)

        self.lateral_panel.relationClicked.connect(
            self.relation_panel.set_current_relation_index)

    @property
    def is_dirty(self) -> bool:
        return self._db.dirty

    def is_new(self) -> bool:
        return self._db.is_new

    def add_database(self, db: DB):
        if self._db is not None:
            logger.debug('DB already set')
            return
        for relation_name, relation_obj in db:
            self.lateral_panel.add_item(
                relation_obj,
                rtype=RelationItemType.Normal)
            self.relation_panel.add_relation(relation_obj)

        self._db = db

    def add_relation(self, relation: Relation):
        self._db.add(relation)
        self.lateral_panel.add_item(
            relation,
            rtype=RelationItemType.Normal)
        self.relation_panel.add_relation(relation)
