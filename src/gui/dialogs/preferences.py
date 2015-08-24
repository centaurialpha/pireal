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
    QDialog,
    QGroupBox,
    QVBoxLayout,
    QComboBox,
    QSpacerItem,
    QSizePolicy
)
from PyQt4.QtCore import Qt
from src import translations as tr


class Preferences(QDialog):

    def __init__(self, parent=None):
        super(Preferences, self).__init__(parent)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        #self.setWindowTitle(self.tr("Preferencias"))

        container = QVBoxLayout(self)
        container.setContentsMargins(0, 0, 0, 0)

        group_language = QGroupBox(tr.TR_PREFERENCES_GROUP_LANG)
        box = QVBoxLayout(group_language)
        self._combo_lang = QComboBox()
        self._combo_lang.addItems(['English', 'Spanish'])
        box.addWidget(self._combo_lang)

        container.addWidget(group_language)
        container.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding,
                          QSizePolicy.Expanding))
