# -*- coding: utf-8 -*-
#
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
from PyQt6.QtGui import (
    QFont,
    QSyntaxHighlighter,
    QTextCharFormat,
)

from pireal.gui.theme.manager import get_theme_manager
from pireal.gui.theme.schema import ColorScheme, EditorColorRole


class Highlighter(QSyntaxHighlighter):
    KEYWORDS = [
        "select",
        "project",
        "rename",
        "product",
        "njoin",
        "louter",
        "router",
        "fouter",
        "difference",
        "intersect",
        "union",
        "and",
        "or",
    ]

    def __init__(self, document):
        super().__init__(document)
        theme_manager = get_theme_manager()
        theme_manager.themeChanged.connect(self._on_theme_changed)

        self._setup_formats(theme_manager.current_scheme)

    def _setup_formats(self, scheme: ColorScheme):
        editor = scheme.editor

        # Keywords
        self._keyword_fmt = QTextCharFormat()
        self._keyword_fmt.setForeground(editor.get(EditorColorRole.KEYWORD))
        self._keyword_fmt.setFontWeight(QFont.Weight.Bold)

        # Variables
        self._var_fmt = QTextCharFormat()
        self._var_fmt.setForeground(editor.get(EditorColorRole.VARIABLE))
        self._var_fmt.setFontWeight(QFont.Weight.Bold)

        # Operators
        self._op_fmt = QTextCharFormat()
        self._op_fmt.setForeground(editor.get(EditorColorRole.OPERATOR))
        self._op_fmt.setFontWeight(QFont.Weight.Bold)

        # Numbers
        self._number_fmt = QTextCharFormat()
        self._number_fmt.setForeground(editor.get(EditorColorRole.NUMBER))

        # Strings
        self._string_fmt = QTextCharFormat()
        self._string_fmt.setForeground(editor.get(EditorColorRole.STRING))

        # Comments
        self._comment_fmt = QTextCharFormat()
        self._comment_fmt.setForeground(editor.get(EditorColorRole.COMMENT))
        self._comment_fmt.setFontItalic(True)

        # Compilar reglas
        self._compile_rules()

    def _compile_rules(self):
        self._rules = []

        # Keywords
        for kw in self.KEYWORDS:
            pattern = QRegularExpression(rf"\b{kw}\b")
            self._rules.append((pattern, self._keyword_fmt))

        # Variables
        var_pattern = QRegularExpression(r"\w+\s*:=")
        self._rules.append((var_pattern, self._var_fmt))

        # Operators
        op_pattern = QRegularExpression(r"(:=|\(|\))|=|<|>|<=|>=|!=")
        self._rules.append((op_pattern, self._op_fmt))

        # Numbers
        num_pattern = QRegularExpression(r"\b\d+(\.\d+)?\b")
        self._rules.append((num_pattern, self._number_fmt))

        # Strings
        str_pattern = QRegularExpression(r"'[^']*'|\"[^\"]*\"")
        self._rules.append((str_pattern, self._string_fmt))

        # Comments
        comment_pattern = QRegularExpression(r"%[^\n]*")
        self._rules.append((comment_pattern, self._comment_fmt))

    def _on_theme_changed(self, scheme: ColorScheme):
        self._setup_formats(scheme)
        self.rehighlight()

    def highlightBlock(self, text: str | None):
        for pattern, fmt in self._rules:
            iterator = pattern.globalMatch(text)
            while iterator.hasNext():
                match = iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), fmt)
