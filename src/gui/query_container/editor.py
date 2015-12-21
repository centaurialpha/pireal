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
    QPlainTextEdit,
    QTextEdit
)
from PyQt5.QtGui import (
    QTextCharFormat,
    QTextCursor,
    QColor
)
from PyQt5.QtCore import (
    Qt,
    pyqtSignal
)
#from src.gui.main_window import Pireal
from src.gui.query_container import (
    highlighter,
    sidebar,
    #completer
)
from src.core import settings


class Editor(QPlainTextEdit):
    _cursorPositionChanged = pyqtSignal(int, int)

    def __init__(self, pfile=None):
        super(Editor, self).__init__()
        self.pfile = pfile
        self.modified = False
        # Highlighter
        self._highlighter = highlighter.Highlighter(self.document())
        self.setFont(settings.PSettings.FONT)
        # Sidebar
        self._sidebar = sidebar.Sidebar(self)
        # Completer
        #self._completer = completer.Completer(self)

        self.__cursor_position_changed()

        # Connection
        self.updateRequest['const QRect&', int].connect(
            self._sidebar.update_area)
        self.cursorPositionChanged.connect(self.__cursor_position_changed)

    @property
    def filename(self):
        """ This function returns the filename of RFile object

        :returns: filename of PFile
        """

        return self.pfile.filename

    @property
    def name(self):
        return self.pfile.name

    @property
    def is_new(self):
        return self.pfile.is_new

    def resizeEvent(self, event):
        super(Editor, self).resizeEvent(event)
        # Fixed sidebar height
        self._sidebar.setFixedHeight(self.height())

    #def keyPressEvent(self, event):
        #key = event.key()
        #if self._completer.popup().isVisible():
            #if key in (Qt.Key_Enter, Qt.Key_Return, Qt.Key_Tab):
                #event.ignore()
                #self._completer.popup().hide()
                #return
            #elif key in (Qt.Key_Space, Qt.Key_Escape, Qt.Key_Backspace):
                #self._completer.popup().hide()

        #QPlainTextEdit.keyPressEvent(self, event)

        #if key == Qt.Key_Period:
            #cursor = self.textCursor()
            #cursor.movePosition(QTextCursor.WordLeft,
                                #QTextCursor.KeepAnchor, 2)

            #text = cursor.selectedText()
            #text = text[:text.rfind('.')]
            #cursor_rect = self.cursorRect()

            #completions = self.__get_completions(text)

            #self._completer.complete(cursor_rect, completions)

    #def __get_completions(self, text):
        #table_widget = Pireal.get_service("main").db_widget.table_widget
        #relation = table_widget.relations.get(text)
        #return relation.fields

    def setHighlightCurrentLine(self, value):
        settings.PSettings.HIGHLIGHT_CURRENT_LINE = value
        self.__cursor_position_changed()

    def __cursor_position_changed(self):
        _selection = QTextEdit.ExtraSelection()
        extra_selections = []
        extra_selections.append(_selection)

        # Highlight current line
        if settings.PSettings.HIGHLIGHT_CURRENT_LINE:
            color = QColor(Qt.lightGray).lighter(125)
            _selection.format.setBackground(color)
            _selection.format.setProperty(QTextCharFormat.FullWidthSelection,
                                          True)
            _selection.cursor = self.textCursor()
            _selection.cursor.clearSelection()
            extra_selections.append(_selection)

        # Paren matching
        extras = self.__check_brackets()
        if extras:
            extra_selections.extend(extras)
        self.setExtraSelections(extra_selections)

        # Emit line and column signal
        #line = self.blockCount()
        #col = self.textCursor().columnNumber() + 1
        #self._cursorPositionChanged.emit(line, col)

    def __check_brackets(self):
        left, right = QTextEdit.ExtraSelection(), QTextEdit.ExtraSelection()
        cursor = self.textCursor()
        block = cursor.block()
        data = block.userData()
        previous, _next = None, None

        if data is not None:
            position = cursor.position()
            block_pos = cursor.block().position()
            paren = data.paren
            n = len(paren)

            for k in range(0, n):
                if paren[k].position == position - block_pos or \
                paren[k].position == position - block_pos - 1:
                    previous = paren[k].position + block_pos
                    if paren[k].character == '(':
                        _next = self.__match_left(block,
                                                  paren[k].character,
                                                  k + 1, 0)
                    elif paren[k].character == ')':
                        _next = self.__match_right(block,
                                                   paren[k].character,
                                                   k, 0)

        if _next is not None and _next > 0:
            if previous is not None and previous > 0:
                _format = QTextCharFormat()

                cursor.setPosition(previous)
                cursor.movePosition(QTextCursor.NextCharacter,
                                    QTextCursor.KeepAnchor)

                _format.setForeground(Qt.blue)
                _format.setBackground(Qt.white)
                left.format = _format
                left.cursor = cursor

                cursor.setPosition(_next)
                cursor.movePosition(QTextCursor.NextCharacter,
                                    QTextCursor.KeepAnchor)

                _format.setForeground(Qt.white)
                _format.setBackground(Qt.blue)
                right.format = _format
                right.cursor = cursor

                return left, right

        elif previous is not None:
            _format = QTextCharFormat()

            cursor.setPosition(previous)
            cursor.movePosition(QTextCursor.NextCharacter,
                                QTextCursor.KeepAnchor)

            _format.setForeground(Qt.white)
            _format.setBackground(Qt.red)
            left.format = _format
            left.cursor = cursor
            return (left,)

    def __match_left(self, block, char, start, found):
        while block.isValid():
            data = block.userData()
            if data is not None:
                paren = data.paren
                n = len(paren)
                for i in range(start, n):
                    if paren[i].character == char:
                        found += 1

                    if paren[i].character == ')':
                        if not found:
                            return paren[i].position + block.position()
                        else:
                            found -= 1

                block = block.next()
                start = 0

    def __match_right(self, block, char, start, found):
        while block.isValid():
            data = block.userData()

            if data is not None:
                paren = data.paren

                if start is None:
                    start = len(paren)
                for i in range(start - 1, -1, -1):
                    if paren[i].character == char:
                        found += 1
                    if paren[i].character == '(':
                        if found == 0:
                            return paren[i].position + block.position()
                        else:
                            found -= 1
            block = block.previous()
            start = None

    def setFont(self, font=settings.PSettings.FONT):
        self.document().setDefaultFont(font)

    def saved(self):
        self.modified = False
        self.document().setModified(self.modified)
        self.setFocus()
