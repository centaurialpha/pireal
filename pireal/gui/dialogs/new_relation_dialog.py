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

import logging

from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QDialogButtonBox
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPlainTextEdit

from PyQt5.QtGui import QFont

from PyQt5.QtCore import Qt

from pireal import translations as tr
from pireal.core.config import AppSettings

from pireal.core.relation import Relation, InvalidFieldNameError, WrongSizeError


logger = logging.getLogger('gui.dialogs.new_relation_dialog')


class RelationCreatorEditor(QPlainTextEdit):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.set_font(AppSettings.font_family, AppSettings.font_size)

    def set_font(self, family: str, size: float):
        font = QFont(family, size)
        super().setFont(font)


class NewRelationDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowTitle(tr.TR_RELATION_DIALOG_TITLE)
        self.setSizeGripEnabled(True)
        self.resize(650, 350)

        self._relation = None

        vbox = QVBoxLayout(self)
        hbox = QHBoxLayout()
        hbox.addWidget(QLabel('Relation name:'))

        self.line_relation_name = QLineEdit()
        hbox.addWidget(self.line_relation_name)
        vbox.addLayout(hbox)

        self.relation_creator = RelationCreatorEditor()
        vbox.addWidget(self.relation_creator)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        vbox.addWidget(self.button_box)

        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

    @property
    def relation_name(self) -> str:
        return self.line_relation_name.text().strip()

    @property
    def relation(self) -> Relation:
        return self._relation

    @property
    def text(self) -> str:
        return self.relation_creator.toPlainText()

    def accept(self):
        if not self.relation_name:
            QMessageBox.warning(
                None, 'Error', tr.TR_RELATION_DIALOG_EMPTY_RELATION_NAME
            )
            self.line_relation_name.setFocus()
            self.line_relation_name.selectAll()
            return
        if not self.text:
            QMessageBox.warning(None, 'Error', "No text")
            return

        text_lines = self.text.splitlines()
        header = [field.strip()
                  for field in text_lines[0].split(',')]

        relation = Relation()
        relation.name = self.relation_name
        try:
            relation.header = header
        except InvalidFieldNameError as exc:
            QMessageBox.warning(None, 'Error', str(exc))
            return

        try:
            for line in text_lines[1:]:
                row = line.split(',')
                relation.insert(tuple(row))
        except WrongSizeError as exc:
            QMessageBox.warning(None, 'Error', str(exc))
            return

        self._relation = relation

        QDialog.accept(self)
