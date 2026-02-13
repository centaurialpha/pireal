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
