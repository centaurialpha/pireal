# -*- coding: utf-8 -*-
#
# Copyright 2015-2021 - Gabriel Acosta <acostadariogabriel@gmail.com>
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

from PyQt5.QtCore import Qt

from pireal.settings import SETTINGS


class SettingsDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowTitle('Settings')

        vbox = QVBoxLayout(self)

        group_general = QGroupBox(self.tr('General'))
        group_editor = QGroupBox(self.tr('Editor'))
        group_font = QGroupBox(self.tr('Font'))

        layout_general = QGridLayout(group_general)
        layout_editor = QGridLayout(group_editor)
        layout_font = QGridLayout(group_font)

        self._check_dark_mode = QCheckBox(self.tr('Dark Mode'))
        self._check_dark_mode.setChecked(SETTINGS.dark_mode)

        self._combo_languages = QComboBox()

        self._check_highlight_line = QCheckBox(self.tr('Highlight Current Line'))
        self._check_highlight_line.setChecked(SETTINGS.highlight_current_line)
        self._check_highlight_braces = QCheckBox(self.tr('Highlight Braces'))
        self._check_highlight_braces.setChecked(SETTINGS.match_parenthesis)

        self._combo_font_family = QFontComboBox()
        font_db = QFontDatabase()
        font_family = font_db.font(SETTINGS.font_family, '', SETTINGS.font_size)
        self._combo_font_family.setCurrentFont(font_family)
        self._combo_font_size = QComboBox()
        sizes_list_str = [str(size) for size in font_db.smoothSizes(SETTINGS.font_family, '')]
        self._combo_font_size.addItems(sizes_list_str)
        self._combo_font_size.setCurrentText(str(SETTINGS.font_size))

        layout_general.addWidget(self._check_dark_mode, 0, 0)
        layout_general.addWidget(QLabel(self.tr('Language:')), 0, 1, Qt.AlignRight)
        layout_general.addWidget(self._combo_languages, 0, 2)
        layout_editor.addWidget(self._check_highlight_line, 0, 0)
        layout_editor.addWidget(self._check_highlight_braces, 0, 1)
        layout_font.addWidget(QLabel(self.tr('Font Family:')), 0, 0)
        layout_font.addWidget(self._combo_font_family, 0, 1)
        layout_font.addWidget(QLabel(self.tr('Font Size:')), 0, 2, Qt.AlignRight)
        layout_font.addWidget(self._combo_font_size, 0, 3)

        button_box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        button_box.rejected.connect(self.reject)
        button_box.accepted.connect(self.accept)

        vbox.addWidget(group_general)
        vbox.addWidget(group_editor)
        vbox.addWidget(group_font)
        vbox.addWidget(button_box)

    def accept(self):
        # TODO: refresh editor font
        SETTINGS.dark_mode = self._check_dark_mode.isChecked()
        SETTINGS.highlight_current_line = self._check_highlight_line.isChecked()
        SETTINGS.match_parenthesis = self._check_highlight_braces.isChecked()
        SETTINGS.font_family = self._combo_font_family.currentText()
        SETTINGS.font_size = int(self._combo_font_size.currentText())
        super().accept()
