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
    QFont,
    QColor,
    QTextOption,
    QTextDocument
)
from PyQt5.QtCore import Qt, QTimer

from src.gui.query_container import (
    highlighter,
    sidebar
)
from src.core.settings import CONFIG
# from src.gui.query_container import snippets


class Editor(QPlainTextEdit):

    def __init__(self, pfile=None):
        super(Editor, self).__init__()
        pal = self.palette()
        pal.setColor(pal.Text, QColor("#555"))
        self.setPalette(pal)

        self.setFrameShape(QPlainTextEdit.NoFrame)
        self.setMouseTracking(True)
        self.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.setCursorWidth(3)
        self.pfile = pfile
        self.__visible_blocks = []
        self.modified = False
        # Highlight current line
        self._highlight_line = CONFIG.get("highlightCurrentLine")
        # Highlighter
        self._highlighter = highlighter.Highlighter(self.document())
        # Set document font
        font_family = CONFIG.get("fontFamily")
        size = CONFIG.get("fontSize")
        if font_family is None:
            font_family, size = CONFIG._get_font()

        self.set_font(font_family, size)
        # Sidebar
        self._sidebar = sidebar.Sidebar(self)
        self.__message = None
        self.word_separators = [")", "("]
        # Extra selections
        self._selections = {}
        self.__cursor_position_changed()
        # self.snippets = snippets.SnippetManager(self)
        # Menu
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.blockCountChanged.connect(self.update)
        # Connection
        self.cursorPositionChanged.connect(self.__cursor_position_changed)

    @property
    def visible_blocks(self):
        return self.__visible_blocks

    def _update_visible_blocks(self):
        self.__visible_blocks.clear()
        append = self.__visible_blocks.append

        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(
            self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()
        editor_height = self.height()
        while block.isValid():
            visible = bottom <= editor_height
            if not visible:
                break
            if block.isVisible():
                append((top, block_number, block))
            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            block_number += 1

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
        self._sidebar.redimensionar()
        self._sidebar.update_viewport()

    def keyPressEvent(self, event):
        # key = event.key()
        # if key == Qt.Key_Tab:
        #     if self.snippets._current_snippet is not None:
        #         self.snippets.select_next()
        #     else:
        #         self.snippets.insert_snippet()
        # else:
        super().keyPressEvent(event)

    def paintEvent(self, event):
        self._update_visible_blocks()
        super().paintEvent(event)

    def word_under_cursor(self, cursor=None):
        """Returns QTextCursor that contains a word under passed cursor
        or actual cursor"""
        if cursor is None:
            cursor = self.textCursor()
        start_pos = end_pos = cursor.position()
        while not cursor.atStart():
            cursor.movePosition(QTextCursor.Left, QTextCursor.KeepAnchor)
            char = cursor.selectedText()[0]
            selected_text = cursor.selectedText()
            if (selected_text in self.word_separators and (
                    selected_text != "n" and selected_text != "t") or
                    char.isspace()):
                break
            start_pos = cursor.position()
            cursor.setPosition(start_pos)
        cursor.setPosition(end_pos)
        while not cursor.atEnd():
            cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor)
            char = cursor.selectedText()[0]
            selected_text = cursor.selectedText()
            if (selected_text in self.word_separators and (
                    selected_text != "n" and selected_text != "t") or
                    char.isspace()):
                break
            end_pos = cursor.position()
            cursor.setPosition(end_pos)
        cursor.setPosition(start_pos)
        cursor.setPosition(end_pos, QTextCursor.KeepAnchor)
        return cursor

    def __cursor_position_changed(self):
        self.clear_selections("current_line")

        if self._highlight_line:
            _selection = QTextEdit.ExtraSelection()
            color = QColor("#fffde1")
            _selection.format.setBackground(color)
            _selection.format.setProperty(
                QTextCharFormat.FullWidthSelection, True)
            _selection.cursor = self.textCursor()
            _selection.cursor.clearSelection()
            self.add_selection("current_line", [_selection])

        # Paren matching
        if CONFIG.get("matchParenthesis"):
            self.clear_selections("parenthesis")
            extras = self.__check_brackets()
            if extras is not None:
                left, right = extras
                self.add_selection("parenthesis", [left, right])

    def set_font(self, font_family, size):
        font = QFont(font_family, size)
        # self.setFont(font)
        super().setFont(font)

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
            return (left, right)

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
        font = self.font()
        point_size = font.pointSize()
        point_size += 1
        font.setPointSize(point_size)
        self.setFont(font)

    def setFont(self, font):
        super().setFont(font)
        self._sidebar.update_viewport()
        self._sidebar.redimensionar()

    def zoom_out(self):
        font = self.font()
        point_size = font.pointSize()
        point_size -= 1
        font.setPointSize(point_size)
        self.setFont(font)

    def show_run_cursor(self):
        """Highlight momentarily a piece of code. Tomado de Ninja-IDE"""

        cursor = self.textCursor()
        if cursor.hasSelection():
            # Get selection range
            start_pos, end_pos = cursor.selectionStart(), cursor.selectionEnd()
            cursor.clearSelection()
            self.setTextCursor(cursor)
        else:
            # If no selected text, highlight current line
            cursor.movePosition(QTextCursor.Start)
            start_pos = cursor.position()
            cursor.movePosition(QTextCursor.End)
            end_pos = cursor.position()
        # Create extra selection
        selection = QTextEdit.ExtraSelection()
        selection.format.setBackground(Qt.lightGray)
        selection.cursor = QTextCursor(cursor)
        selection.cursor.setPosition(start_pos)
        selection.cursor.setPosition(end_pos, QTextCursor.KeepAnchor)
        self.add_selection("run_cursor", [selection])
        # Remove extra selection after 0.3 seconds
        QTimer.singleShot(
            300, lambda: self.clear_selections("run_cursor"))

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
        self.add_selection('error', [selection])

    def add_selection(self, selection_name, selections):
        self._selections[selection_name] = selections
        self.update_selections()

    def update_selections(self):
        selections = []
        for selection_name, selection in self._selections.items():
            selections.extend(selection)
        self.setExtraSelections(selections)

    def clear_selections(self, selection_name):
        if selection_name in self._selections:
            self._selections[selection_name] = []
            self.update_selections()
