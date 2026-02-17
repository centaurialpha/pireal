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

from PyQt6.QtCore import QStringListModel, Qt
from PyQt6.QtWidgets import QCompleter, QPlainTextEdit

from pireal.gui.highlighter import Highlighter


class PirealCompleter(QCompleter):
    def __init__(self, parent: QPlainTextEdit):
        super().__init__(Highlighter.KEYWORDS, parent)
        self._editor = parent
        self.setWidget(parent)
        self.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        self.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.activated.connect(self._insert_completion)

    def update_words(self, words: list[str]):
        all_words = Highlighter.KEYWORDS + words
        self.setModel(QStringListModel(all_words, self))

    def _insert_completion(self, completion: str):
        prefix = self.completionPrefix()
        cursor = self._editor.textCursor()
        cursor.insertText(completion[len(prefix) :])
        self._editor.setTextCursor(cursor)
