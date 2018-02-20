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
    QTextEdit,
)
from PyQt5.QtGui import (
    QTextCharFormat,
    QTextCursor,
    QColor,
    QTextOption,
    QTextDocument
)
from PyQt5.QtCore import Qt

from src.gui.query_container import (
    highlighter,
    sidebar
)
from src.core.settings import PSetting


class Editor(QPlainTextEdit):

    def __init__(self, pfile=None):
        super(Editor, self).__init__()
        self.setMouseTracking(True)
        self.setWordWrapMode(QTextOption.NoWrap)
        self.setCursorWidth(8)
        self.pfile = pfile
        self.modified = False
        # Highlight current line
        self._highlight_line = PSetting.HIGHLIGHT_CURRENT_LINE
        # Highlighter
        self._highlighter = highlighter.Highlighter(self.document())
        # Set document font
        self.set_font(PSetting.FONT)
        # Sidebar
        self._sidebar = sidebar.Sidebar(self)
        self.__message = None
        # Extra selections
        self._selections = {}
        self.__cursor_position_changed()

        # Menu
        self.setContextMenuPolicy(Qt.CustomContextMenu)

        # Connection
        self.updateRequest['const QRect&', int].connect(
            self._sidebar.update_area)
        self.cursorPositionChanged.connect(self.__cursor_position_changed)

    @property
    def filename(self):
        """This function returns the filename of RFile object

        :returns: filename of PFile
        """

        return self.pfile.filename

    @property
    def name(self):
        return self.pfile.display_name

    @property
    def is_new(self):
        return self.pfile.is_new

    def resizeEvent(self, event):
        super(Editor, self).resizeEvent(event)
        # Fixed sidebar height
        self._sidebar.setFixedHeight(self.height())

    def __cursor_position_changed(self):
        # extra_selections = []
        _selection = QTextEdit.ExtraSelection()
        # extra_selections.append(_selection)

        # Highlight current line
        # if PSetting.HIGHLIGHT_CURRENT_LINE:
        if True:
            color = QColor(Qt.lightGray).lighter(125)
            _selection.format.setBackground(color)
            _selection.format.setProperty(
                QTextCharFormat.FullWidthSelection, True)
            _selection.cursor = self.textCursor()
            _selection.cursor.clearSelection()
            # extra_selections.append(_selection)
        self.add_selection('current_line', _selection)

        # Paren matching
        extras = None
        if PSetting.MATCHING_PARENTHESIS:
            extras = self.__check_brackets()
            if extras is not None:
                pass
                # left, right = extras
                # self.add_selection('left_b', left)
                # self.add_selection('right_b', right)

        # self.setExtraSelections(extra_selections)

    def set_font(self, font):
        self.document().setDefaultFont(font)

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

    def zoom_in(self):
        font = self.document().defaultFont()
        point_size = font.pointSize()
        point_size += 1
        font.setPointSize(point_size)
        self.document().setDefaultFont(font)

    def zoom_out(self):
        font = self.document().defaultFont()
        point_size = font.pointSize()
        point_size -= 1
        font.setPointSize(point_size)
        self.document().setDefaultFont(font)

    def saved(self):
        self.modified = False
        self.document().setModified(self.modified)
        self.setFocus()

    def comment(self):
        """Comment one or more lines"""

        tcursor = self.textCursor()
        block_start = self.document().findBlock(tcursor.selectionStart())
        block_end = self.document().findBlock(tcursor.selectionEnd()).next()

        tcursor.beginEditBlock()

        while block_start != block_end:
            if block_start.text():
                tcursor.setPosition(block_start.position())
                if block_start.text()[0] != '%':
                    tcursor.insertText("% ")
            block_start = block_start.next()

        tcursor.endEditBlock()

    def uncomment(self):
        """Uncomment one or more lines"""

        tcursor = self.textCursor()
        block_start = self.document().findBlock(tcursor.selectionStart())
        block_end = self.document().findBlock(tcursor.selectionEnd()).next()

        tcursor.beginEditBlock()

        while block_start != block_end:
            if block_start.text():
                tcursor.setPosition(block_start.position())
                if block_start.text()[0] == '%':
                    tcursor.deleteChar()
            block_start = block_start.next()

        tcursor.endEditBlock()

    def find_text(self, search, cs=False, wo=False,
                  backward=False, find_next=True):
        flags = QTextDocument.FindFlags()
        if cs:
            flags = QTextDocument.FindCaseSensitively
        if wo:
            flags |= QTextDocument.FindWholeWords
        if backward:
            flags |= QTextDocument.FindBackward
        if find_next or backward:
            self.moveCursor(QTextCursor.NoMove)
        else:
            self.moveCursor(QTextCursor.StartOfWord)
        found = self.find(search, flags)
        if not found:
            cursor = self.textCursor()
            if backward:
                self.moveCursor(QTextCursor.End)
            else:
                self.moveCursor(QTextCursor.Start)
            found = self.find(search, flags)
            if not found:
                self.setTextCursor(cursor)

    def highlight_error(self, linenumber):
        if linenumber == -1:
            # Borro la selección
            self.clear_selections('error')
            print('eeee')
            return
        selection = QTextEdit.ExtraSelection()
        selection.cursor = self.textCursor()
        selection.cursor.movePosition(QTextCursor.Start,
                                      QTextCursor.MoveAnchor)
        selection.cursor.movePosition(QTextCursor.Down, QTextCursor.MoveAnchor,
                                      linenumber - 1)
        selection.format.setProperty(QTextCharFormat.FullWidthSelection, True)
        selection.format.setBackground(QColor("#DD4040"))
        selection.format.setForeground(Qt.white)
        self.add_selection('error', selection)

    def add_selection(self, selection_name, selections):
        self._selections[selection_name] = selections
        self.update_selections()

    def update_selections(self):
        selections = []
        for selection_name, selection in self._selections.items():
            selections.append(selection)
        self.setExtraSelections(selections)

    def clear_selections(self, selection_name):
        if selection_name in self._selections:
            self._selections[selection_name] = []
            self.update_selections()
