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
    QTabWidget
)


class TabWidget(QTabWidget):

    def __init__(self):
        super(TabWidget, self).__init__()
        self.setTabPosition(QTabWidget.South)
        self.setTabsClosable(True)
        self.setMovable(True)

        self.tabCloseRequested[int].connect(self.remove_tab)

    def remove_tab(self, index):
        super(TabWidget, self).removeTab(index)

    def tab_modified(self, modified):
        editor_widget = self.sender().get_editor()
        if modified:
            text = "{} \u2022".format(editor_widget.name)
        else:
            text = editor_widget.name
        self.setTabText(self.currentIndex(), text)

    def add_tab(self, widget, title):
        pass