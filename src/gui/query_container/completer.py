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

from PyQt5.QtWidgets import (
    QCompleter
)
from PyQt5.QtCore import Qt


class Completer(QCompleter):

    def __init__(self, editor):
        super(Completer, self).__init__([], editor)
        self.__editor = editor
        self.setWidget(editor)
        self.setCompletionMode(QCompleter.PopupCompletion)
        self.setCaseSensitivity(Qt.CaseInsensitive)

        self.activated['const QString&'].connect(self._insert_completion)

    def _insert_completion(self, text):
        extra = len(text) - len(self.completionPrefix())
        cursor = self.__editor.textCursor()
        cursor.insertText(text[extra:])

    def complete(self, cursor_rect, list_texts):
        self.model().setStringList(list_texts)
        self.popup().setCurrentIndex(self.model().index(0, 0))
        width = self.popup().sizeHintForColumn(0)
        width += self.popup().verticalScrollBar().sizeHint().width() + 10
        cursor_rect.setWidth(width)
        QCompleter.complete(self, cursor_rect)
