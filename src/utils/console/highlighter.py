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
)
from PyQt5.QtCore import (
    QRegExp,
    Qt
)


KEYWORDS = ["and", "assert", "break", "class", "continue", "def", "del",
            "elif", "else", "except", "exec", "finally", "for", "from",
            "global", "if", "import", "in", "is", "as", "lambda", "not",
            "or", "pass", "print", "raise", "return", "super", "try", "while",
            "with", "yield", "None", "True", "False"
]
EXTRAS = ["abs", "all", "any", "basestring", "bin", "bool", "bytearray",
          "callable", "chr", "classmethod", "cmp", "compile", "complex",
          "delattr", "dict", "dir", "divmod", "enumerate", "eval", "execfile",
          "file", "filter", "float", "format", "frozenset", "getattr",
          "globals", "hasattr", "hash", "help", "hex", "id", "input", "int",
          "isinstance", "issubclass", "iter", "len", "list", "locals", "long",
          "map", "max", "memoryview", "min", "next", "object", "oct", "open",
          "ord", "pow", "property", "range", "raw_input", "reduce", "reload",
          "repr", "reversed", "round", "set", "setattr", "slice", "sorted",
          "staticmethod", "str", "sum", "tuple", "type", "unichr", "unicode",
          "vars", "xrange", "zip", "apply", "buffer", "coerce", "intern"
]


class PythonHighlighter(QSyntaxHighlighter):

    def __init__(self, console):
        super(PythonHighlighter, self).__init__(console)
        self._rules = []

        # Keywords format
        fkeyword = QTextCharFormat()
        fkeyword.setForeground(Qt.cyan)

        # Prompt format
        fprompt = QTextCharFormat()
        fprompt.setForeground(Qt.red)
        pprompt = QRegExp('pireal> ')
        self._rules.append((pprompt, fprompt))

        # Extras format
        fextra = QTextCharFormat()
        fextra.setForeground(Qt.darkCyan)

        for pattern in EXTRAS:
            self._rules.append((QRegExp("\\b" + pattern + "\\b"), fextra))

        for pattern in KEYWORDS:
            self._rules.append((QRegExp("\\b" + pattern + "\\b"), fkeyword))

    def highlightBlock(self, text):
        for pattern, _format in self._rules:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, _format)
                index = expression.indexIn(text, index + length)
        self.setCurrentBlockState(0)