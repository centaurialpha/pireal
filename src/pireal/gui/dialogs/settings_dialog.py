# Copyright 2015-2026 - Gabriel Acosta <acostadariogabriel@gmail.com>
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

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFontDatabase
from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFontComboBox,
    QGridLayout,
    QGroupBox,
    QLabel,
    QVBoxLayout,
)

from pireal import translations as tr
from pireal.settings import settings


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.setWindowTitle(tr.TR_SETTINGS_TITLE)

        vbox = QVBoxLayout(self)
        vbox.addWidget(self._build_general_group())
        vbox.addWidget(self._build_editor_group())
        vbox.addWidget(self._build_font_group())

        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        button_box.rejected.connect(self.reject)
        button_box.accepted.connect(self.accept)
        vbox.addWidget(button_box)

    def _build_general_group(self) -> QGroupBox:
        group = QGroupBox(tr.TR_SETTINGS_GROUP_GENERAL)
        layout = QGridLayout(group)

        self._combo_languages = QComboBox()
        self._languages = {"en": "English", "es": "Spanish"}
        self._combo_languages.addItems(self._languages.values())
        self._combo_languages.setCurrentText(self._languages[settings.language])

        layout.addWidget(QLabel(tr.TR_SETTINGS_LANGUAGE), 0, 0)
        layout.addWidget(self._combo_languages, 0, 1)

        return group

    def _build_editor_group(self) -> QGroupBox:
        group = QGroupBox(tr.TR_SETTINGS_GROUP_EDITOR)
        layout = QGridLayout(group)

        self._check_highlight_line = QCheckBox(tr.TR_SETTINGS_HIGHLIGHT_LINE)
        self._check_highlight_line.setChecked(settings.highlight_current_line)

        self._check_match_parenthesis = QCheckBox(tr.TR_SETTINGS_HIGHLIGHT_BRACES)
        self._check_match_parenthesis.setChecked(settings.match_parenthesis)

        self._check_symbol_mode = QCheckBox(tr.TR_SETTINGS_SYMBOL_MODE)
        self._check_symbol_mode.setChecked(settings.symbol_mode)

        self._check_autocomplete = QCheckBox(tr.TR_SETTINGS_AUTOCOMPLETE)
        self._check_autocomplete.setChecked(settings.autocomplete)

        self._check_query_blocks = QCheckBox(tr.TR_SETTINGS_SHOW_QUERY_BLOCKS)
        self._check_query_blocks.setChecked(settings.show_query_blocks)

        layout.addWidget(self._check_highlight_line, 0, 0)
        layout.addWidget(self._check_match_parenthesis, 0, 1)
        layout.addWidget(self._check_symbol_mode, 1, 0)
        layout.addWidget(self._check_autocomplete, 1, 1)
        layout.addWidget(self._check_query_blocks, 2, 0)

        return group

    def _build_font_group(self) -> QGroupBox:
        group = QGroupBox(tr.TR_SETTINGS_GROUP_FONT)
        layout = QGridLayout(group)

        self._combo_font_family = QFontComboBox()
        self._combo_font_family.setCurrentFont(QFontDatabase.font(settings.font_family, "", settings.font_size))
        self._combo_font_family.currentFontChanged.connect(self._update_font_sizes)

        self._combo_font_size = QComboBox()
        sizes = QFontDatabase.smoothSizes(settings.font_family, "")
        if not sizes:
            sizes = [8, 9, 10, 11, 12, 14, 16, 18, 20, 24, 28, 32, 48, 64]

        self._combo_font_size.addItems([str(s) for s in sizes])
        self._combo_font_size.setCurrentText(str(settings.font_size))

        layout.addWidget(QLabel(tr.TR_SETTINGS_FONT_FAMILY), 0, 0)
        layout.addWidget(self._combo_font_family, 0, 1)
        layout.addWidget(QLabel(tr.TR_SETTINGS_FONT_SIZE), 0, 2)
        layout.addWidget(self._combo_font_size, 0, 3)

        return group

    def accept(self):
        for key, lang in self._languages.items():
            if lang == self._combo_languages.currentText():
                settings.language = key
                break

        settings.highlight_current_line = self._check_highlight_line.isChecked()
        settings.match_parenthesis = self._check_match_parenthesis.isChecked()
        settings.font_family = self._combo_font_family.currentText()
        settings.font_size = int(self._combo_font_size.currentText())
        settings.symbol_mode = self._check_symbol_mode.isChecked()
        settings.autocomplete = self._check_autocomplete.isChecked()
        settings.show_query_blocks = self._check_query_blocks.isChecked()

        super().accept()

    def _update_font_sizes(self, font):
        sizes = QFontDatabase.smoothSizes(font.family(), "")
        if not sizes:
            sizes = [8, 9, 10, 11, 12, 14, 16, 18, 20, 24, 28, 32, 48, 64]
        self._combo_font_size.clear()
        self._combo_font_size.addItems([str(s) for s in sizes])
