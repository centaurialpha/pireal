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

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QStackedLayout

from pireal.gui.model_view_delegate import create_view


class RelationWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._stack = QStackedLayout(self)

    def count(self):
        return self._stack.count()

    def current_view(self):
        return self._stack.currentWidget()

    def set_current_index(self, index):
        self._stack.setCurrentIndex(index)

    def add_view(self, relation):
        view = create_view(relation)
        index = self._stack.addWidget(view)
        self._stack.setCurrentIndex(index)
