# -*- coding: utf-8 -*-
#
# Copyright 2015-2017 - Gabriel Acosta <acostadariogabriel@gmail.com>
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

from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QFontComboBox
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QGroupBox
from PyQt5.QtWidgets import QDialogButtonBox

from PyQt5.QtGui import QFontDatabase

from pireal.core.settings import USER_SETTINGS


class Preferences(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._central = parent
        self.setWindowTitle('Preferences')
        vbox = QVBoxLayout(self)

        group_language = QGroupBox('Language:')
        grid_language = QGridLayout(group_language)
        self._combo_languages = QComboBox()
        grid_language.addWidget(self._combo_languages, 0, 0)

        group_editor = QGroupBox('Editor:')
        grid_editor = QGridLayout(group_editor)
        self._check_highlight_current_line = QCheckBox('Highlight Current Line')
        self._check_highlight_current_line.setChecked(USER_SETTINGS.highlight_current_line)
        grid_editor.addWidget(self._check_highlight_current_line, 0, 0)
        self._check_highlight_braces = QCheckBox('Highlight Braces')
        self._check_highlight_braces.setChecked(USER_SETTINGS.match_parenthesis)
        grid_editor.addWidget(self._check_highlight_braces, 0, 1)

        group_font = QGroupBox('Font:')
        font_db = QFontDatabase()
        grid_font = QGridLayout(group_font)
        self._combo_font_family = QFontComboBox()
        grid_font.addWidget(QLabel('Family:'), 0, 0)
        grid_font.addWidget(self._combo_font_family, 0, 1)
        self._combo_font_family.setCurrentText(USER_SETTINGS.font_family)
        self._combo_font_size = QComboBox()
        self._combo_font_size.addItems(map(str, font_db.pointSizes(USER_SETTINGS.font_family)))
        self._combo_font_size.setCurrentText(str(USER_SETTINGS.font_size))

        grid_font.addWidget(QLabel('Size:'), 0, 2)
        grid_font.addWidget(self._combo_font_size, 0, 3)

        btn_box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        btn_box.rejected.connect(self.reject)
        btn_box.accepted.connect(self.accept)

        # Add widgets to layout
        vbox.addWidget(group_language)
        vbox.addWidget(group_editor)
        vbox.addWidget(group_font)
        vbox.addWidget(btn_box)

    def accept(self):
        USER_SETTINGS.font_family = self._combo_font_family.currentText()
        USER_SETTINGS.font_size = int(self._combo_font_size.currentText())
        USER_SETTINGS.match_parenthesis = self._check_highlight_braces.isChecked()
        USER_SETTINGS.highlight_current_line = self._check_highlight_current_line.isChecked()
        USER_SETTINGS.save()

        super().accept()
