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
    QDockWidget,
    QTabWidget,
    QWidget
)
from PyQt4.QtCore import SIGNAL
from src.gui.query_editor import editor
from src.gui.main_window import Pireal


class QueryWidget(QDockWidget):

    def __init__(self):
        super(QueryWidget, self).__init__()
        # Remove title bar widget
        title_bar = self.titleBarWidget()
        empty = QWidget()
        self.setTitleBarWidget(empty)
        del title_bar

        self.__nquery = 1
        # Tabs
        self.tab = QTabWidget()
        self.tab.setTabsClosable(True)
        self.setWidget(self.tab)

        Pireal.load_service("query_widget", self)

        # Connections
        self.connect(self.tab, SIGNAL("tabCloseRequested(int)"),
                     self.tab.removeTab)
        self.connect(self.tab, SIGNAL("tabCloseRequested(int)"),
                     self._check_count)

    def _check_count(self):
        """ Hide dock if count = 0 """

        if self.tab.count() == 0:
            pireal = Pireal.get_service("pireal")
            pireal.enable_disable_query_actions(False)
            self.hide()

    def new_query(self):
        """ Add new query editor in QTabWidget """

        qeditor = editor.Editor()
        index = self.tab.addTab(qeditor,
                                self.tr("consulta_{}".format(self.__nquery)))
        self.tab.setCurrentIndex(index)
        self.__nquery += 1

query_widget = QueryWidget()