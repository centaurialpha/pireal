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

from PyQt5.QtWidgets import QPlainTextEdit
from PyQt5.QtGui import QTextCursor
from PyQt5.QtCore import Qt
from src.utils.console import (
    console,
    highlighter
)


class ConsoleWidget(QPlainTextEdit):

    def __init__(self):
        QPlainTextEdit.__init__(self, 'pireal> ')
        self.setWindowTitle("Python Console for Pireal Developers")
        self.setUndoRedoEnabled(False)
        self.moveCursor(QTextCursor.EndOfLine)

        # Highligher
        self.highlighter = highlighter.PythonHighlighter(self.document())

        self._prompt = 'pireal> '
        self._console = console.Console()

        self._set_stylesheet()

        self._console.push('from src.gui.main_window import Pireal;'
                            'pireal = Pireal.get_service("central")')

    def _set_stylesheet(self):
        self.setStyleSheet("background: black; color: #00ff00;")
        font = self.font()
        font.setPointSize(12)
        self.setFont(font)

    def keyPressEvent(self, event):
        key = event.key()
        if event.modifiers() == Qt.ControlModifier and key == Qt.Key_C:
            self._add_prompt()
            return
        if key in (Qt.Key_Return, Qt.Key_Enter):
            self._write_command()
            return
        if key == Qt.Key_Backspace or key == Qt.Key_Left:
            cursor_pos = self.textCursor().columnNumber() - len(self._prompt)
            if cursor_pos == 0:
                return
        QPlainTextEdit.keyPressEvent(self, event)

    def _write_command(self):
        command = self.document().lastBlock().text()
        command = command[len(self._prompt):]
        if command == 'clear':
            self.setPlainText('')
            self._add_prompt()
            return
        incomplete = self._console.push(command)
        if not incomplete:
            if self._console.output is not None:
                self.appendPlainText(self._console.output)
        self._add_prompt(incomplete)

    def _add_prompt(self, incomplete=False):
        if incomplete:
            prompt = '... '
        else:
            prompt = self._prompt
        self.appendPlainText(prompt)
        self.moveCursor(QTextCursor.End)
