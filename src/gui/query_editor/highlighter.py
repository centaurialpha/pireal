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

from PyQt4.QtGui import (
    QSyntaxHighlighter,
    QTextCharFormat,
    QFont
)
from PyQt4.QtCore import (
    Qt,
    QRegExp
)


class Highlighter(QSyntaxHighlighter):
    """ Syntax Highlighting

    This class defines rules, a rule consists of a QRegExp pattern and a
    QTextCharFormat instance.
    """

    # Keywords
    KEYWORDS = [
        "select",
        "project",
        "njoin",
        "difference",
        "union",
        "and",
        "or"
    ]

    def __init__(self, editor):
        super(Highlighter, self).__init__(editor)
        # Keywords format
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(Qt.darkMagenta)
        keyword_format.setFontWeight(QFont.Bold)

        # Rules
        self._rules = [(QRegExp(pattern), keyword_format)
                       for pattern in Highlighter.KEYWORDS]

    def highlightBlock(self, text):
        """ Reimplementation """

        for pattern, _format in self._rules:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, _format)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)
