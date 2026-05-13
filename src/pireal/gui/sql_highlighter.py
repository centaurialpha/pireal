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

from PyQt6.QtCore import QRegularExpression
from PyQt6.QtGui import QFont, QSyntaxHighlighter, QTextCharFormat

from pireal.gui.theme.manager import get_theme_manager
from pireal.gui.theme.schema import ColorScheme, EditorColorRole


class SQLHighlighter(QSyntaxHighlighter):
    KEYWORDS = [
        "SELECT",
        "FROM",
        "WHERE",
        "AND",
        "OR",
        "NOT",
        "JOIN",
        "INNER",
        "LEFT",
        "RIGHT",
        "FULL",
        "OUTER",
        "NATURAL",
        "CROSS",
        "UNION",
        "INTERSECT",
        "EXCEPT",
        "AS",
        "ON",
        "DISTINCT",
        "ALL",
        "INTO",
        "INSERT",
        "UPDATE",
        "DELETE",
        "CREATE",
        "DROP",
        "TABLE",
        "GROUP",
        "BY",
        "ORDER",
        "HAVING",
        "LIMIT",
        "OFFSET",
        "NULL",
        "IS",
        "IN",
        "BETWEEN",
        "LIKE",
    ]

    def __init__(self, document):
        super().__init__(document)
        theme_manager = get_theme_manager()
        theme_manager.themeChanged.connect(self._on_theme_changed)
        self._setup_formats(theme_manager.current_scheme)

    def _setup_formats(self, scheme: ColorScheme):
        editor = scheme.editor

        self._keyword_fmt = QTextCharFormat()
        self._keyword_fmt.setForeground(editor.get(EditorColorRole.KEYWORD))
        self._keyword_fmt.setFontWeight(QFont.Weight.Bold)

        self._string_fmt = QTextCharFormat()
        self._string_fmt.setForeground(editor.get(EditorColorRole.STRING))

        self._number_fmt = QTextCharFormat()
        self._number_fmt.setForeground(editor.get(EditorColorRole.NUMBER))

        self._comment_fmt = QTextCharFormat()
        self._comment_fmt.setForeground(editor.get(EditorColorRole.COMMENT))
        self._comment_fmt.setFontItalic(True)

        self._compile_rules()

    def _compile_rules(self):
        self._rules = []

        for kw in self.KEYWORDS:
            pattern = QRegularExpression(
                rf"\b{kw}\b",
                QRegularExpression.PatternOption.CaseInsensitiveOption,
            )
            self._rules.append((pattern, self._keyword_fmt))

        self._rules += [
            (QRegularExpression(r"'[^']*'"), self._string_fmt),
            (QRegularExpression(r"\b\d+(\.\d+)?\b"), self._number_fmt),
            (QRegularExpression(r"--[^\n]*"), self._comment_fmt),
        ]

    def _on_theme_changed(self, scheme: ColorScheme):
        self._setup_formats(scheme)
        self.rehighlight()

    def highlightBlock(self, text: str | None):
        for pattern, fmt in self._rules:
            it = pattern.globalMatch(text)
            while it.hasNext():
                match = it.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), fmt)
