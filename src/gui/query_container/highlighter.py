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

from PyQt5.QtGui import (
    QSyntaxHighlighter,
    QTextCharFormat,
    QFont,
    QTextBlockUserData,
    QColor
)
from PyQt5.QtCore import (
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
        "or"
    ]

    def __init__(self, editor):
        super(Highlighter, self).__init__(editor)
        # Keywords format
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#222"))
        keyword_format.setFontWeight(QFont.Bold)

        # Rules
        self._rules = [(QRegExp("\\b" + pattern + "\\b"), keyword_format)
                       for pattern in Highlighter.KEYWORDS]

        # vars
        var_format = QTextCharFormat()
        var_pattern = QRegExp("\w+\s*\:\=")
        var_format.setFontWeight(QFont.Bold)
        var_format.setForeground(QColor("#dd1144"))

        self._rules.append((var_pattern, var_format))

        op_format = QTextCharFormat()
        op_pattern = QRegExp("(\\:=|\\(|\\))|=|<|>")
        op_format.setForeground(QColor("#222"))
        op_format.setFontWeight(QFont.Bold)
        self._rules.append((op_pattern, op_format))
        # Number format
        number_format = QTextCharFormat()
        number_pattern = QRegExp(r"\b([A-Z0-9]+)(?:[ _-](\d+))?\b")
        number_pattern.setMinimal(True)
        number_format.setForeground(QColor("orange"))
        self._rules.append((number_pattern, number_format))

        # String format
        string_format = QTextCharFormat()
        string_pattern = QRegExp("\'.*\'")
        string_pattern.setMinimal(True)
        string_format.setForeground(Qt.darkGreen)
        self._rules.append((string_pattern, string_format))

        # Comment format
        comment_format = QTextCharFormat()
        comment_pattern = QRegExp("%[^\n]*")
        comment_format.setForeground(QColor("#999988"))
        comment_format.setFontItalic(True)
        self._rules.append((comment_pattern, comment_format))

        # Paren
        self.paren = QRegExp('\(|\)')

    def highlightBlock(self, text):
        """ Reimplementation """

        block_data = TextBlockData()
        # Paren
        index = self.paren.indexIn(text, 0)
        while index >= 0:
            matched_paren = str(self.paren.capturedTexts()[0])
            info = ParenInfo(matched_paren, index)
            block_data.insert_paren_info(info)
            index = self.paren.indexIn(text, index + 1)

        self.setCurrentBlockUserData(block_data)

        for pattern, _format in self._rules:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, _format)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)


class TextBlockData(QTextBlockUserData):

    def __init__(self):
        super(TextBlockData, self).__init__()
        self.paren = []
        self.__valid = False

    def insert_paren_info(self, info):
        self.__valid = True
        self.paren.append(info)

    @property
    def isValid(self):
        return self.__valid


class ParenInfo(object):

    def __init__(self, char, pos):
        self.character = char
        self.position = pos
