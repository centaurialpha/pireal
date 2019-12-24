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

# from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QTabWidget
# from PyQt5.QtWidgets import QVBoxLayout
# from PyQt5.QtWidgets import QStackedLayout
from PyQt5.QtWidgets import QSplitter

# from pireal.gui.model_view_delegate import create_view
from pireal.gui.relation_widget import RelationWidget


class CentralView(QSplitter):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._tabs = QTabWidget()
        self.addWidget(self._tabs)

        self.relation_widget = RelationWidget(self)
        self._tabs.addTab(self.relation_widget, 'Relations')

        # self.relation_result_widget = RelationResultWidget(self)
        # self._tabs.addTab(self.relation_result_widget, 'Results')
