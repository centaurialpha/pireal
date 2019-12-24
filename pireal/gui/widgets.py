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

"""
Some custom widgets
"""

from PyQt5.QtWidgets import QSplitter

from PyQt5.QtCore import Qt

from pireal.core.settings import DATA_SETTINGS


class RememberingSplitter(QSplitter):
    """
    Splitter that remember state
    """

    def __init__(self, orientation=Qt.Horizontal, parent=None):
        super().__init__(orientation, parent)
        self.name = self.__class__.__name__

    def save_state(self):
        DATA_SETTINGS.setValue(self.name, self.saveState())

    def showEvent(self, event):
        state = DATA_SETTINGS.value(self.name)
        if state is not None:
            self.restoreState(state)
        super().showEvent(event)
