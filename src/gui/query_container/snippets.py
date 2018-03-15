
import re

from PyQt5.QtGui import QTextCursor


SNIPPETS = {
    "select": "select ${1:expression} (${2:relation})",
    "project": "${1:relation} project ${2:relation}",
}

VARIABLE_REG = re.compile(r'\$\{(\d+)\:([^\}]+)\}')


class Snippet(object):

    def __init__(self, prefix, body):
        self.prefix = prefix
        self._body = body

    @property
    def body(self):
        return re.sub(VARIABLE_REG, r"\2", self._body)

    @property
    def variables(self):
        varss = []
        diff = 0

        for match in re.finditer(VARIABLE_REG, self._body):
            start = match.start() - diff
            length = len(match.group(2))
            diff += len(match.group()) - length
            varss.append((start, length))
        return varss


class SnippetManager(object):

    def __init__(self, editor):
        self._editor = editor
        self._cursors = []
        self._current_snippet = None
        self.snippets = {}
        self.active = False
        for prefix, body in SNIPPETS.items():
            snippet = Snippet(prefix, body)
            self.snippets[prefix] = snippet

    def reset(self):
        self._current_snippet = None
        self._cursors.clear()

    def insert_snippet(self):
        cursor = self._editor.word_under_cursor()
        prefix = cursor.selectedText()

        # pos = cursor.position()
        # cursor.movePosition(QTextCursor.StartOfWord)
        # start_pos = cursor.position()
        # cursor.setPosition(pos, QTextCursor.KeepAnchor)
        copy = QTextCursor(cursor)
        copy.movePosition(QTextCursor.StartOfWord)
        start = copy.position()

        self._current_snippet = self.snippets.get(prefix)
        if self._current_snippet is not None:
            self.active = True
            cursor.removeSelectedText()
            cursor.insertText(self._current_snippet.body)
            self._highlight(start)
        else:
            self.active = False

    def _highlight(self, pos):
        variables = self._current_snippet.variables
        if not variables:
            self._current_snippet = None
            self.active = False
            return

        for var in variables:
            cursor = self._editor.textCursor()
            cursor.setPosition(pos)
            cursor.movePosition(QTextCursor.Right, n=var[0])
            cursor.movePosition(QTextCursor.Right,
                                QTextCursor.KeepAnchor, var[1])
            self._cursors.append(cursor)
        self.select_next()

    def select_next(self):
        cursor = self._editor.textCursor()
        try:
            other = self._cursors.pop(0)
        except IndexError:
            self._current_snippet = None
            cursor.clearSelection()
        else:
            cursor = other
        self._editor.setTextCursor(cursor)
