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

from PyQt5.QtCore import QRegExp, QSize, Qt, QTimer
from PyQt5.QtCore import pyqtSignal as Signal
from PyQt5.QtGui import (
    QColor,
    QFont,
    QFontMetrics,
    QKeySequence,
    QPainter,
    QPalette,
    QPen,
    QSyntaxHighlighter,
    QTextBlockUserData,
    QTextCharFormat,
    QTextCursor,
    QTextDocument
)

from PyQt5.QtWidgets import (
    QFrame,
    QPlainTextEdit,
    QShortcut,
    QTextEdit,
)

from pireal.core.interpreter import tokens
from pireal.core.settings import USER_SETTINGS
from pireal.gui.theme import get_editor_color


class Highlighter(QSyntaxHighlighter):
    """ Syntax Highlighting

    This class defines rules for syntax highlighting.

    A rule consists of a QRegExp pattern and a QTextCharFormat instance.
    """

    def __init__(self, editor):
        super(Highlighter, self).__init__(editor)
        # Keywords format
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor(get_editor_color('keyword')))
        keyword_format.setFontWeight(QFont.Bold)

        # Rules
        self._rules = [(QRegExp("\\b" + pattern + "\\b"), keyword_format)
                       for pattern in tokens.KEYWORDS.keys()]

        # vars
        var_format = QTextCharFormat()
        var_pattern = QRegExp(r"\w+\s*\:\=")
        var_format.setFontWeight(QFont.Bold)
        var_format.setForeground(QColor(get_editor_color('variable')))

        self._rules.append((var_pattern, var_format))

        op_format = QTextCharFormat()
        op_pattern = QRegExp("(\\:=|\\(|\\))|=|<|>")
        op_format.setForeground(QColor(get_editor_color('operator')))
        op_format.setFontWeight(QFont.Bold)
        self._rules.append((op_pattern, op_format))
        # Number format
        number_format = QTextCharFormat()
        number_pattern = QRegExp(r"\b([A-Z0-9]+)(?:[ _-](\d+))?\b")
        number_pattern.setMinimal(True)
        number_format.setForeground(QColor(get_editor_color('number')))
        self._rules.append((number_pattern, number_format))

        # String format
        string_format = QTextCharFormat()
        string_pattern = QRegExp("\'.*\'")
        string_pattern.setMinimal(True)
        string_format.setForeground(QColor(get_editor_color('string')))
        self._rules.append((string_pattern, string_format))

        # Comment format
        comment_format = QTextCharFormat()
        comment_pattern = QRegExp("%[^\n]*")
        comment_format.setForeground(QColor(get_editor_color('comment')))
        comment_format.setFontItalic(True)
        self._rules.append((comment_pattern, comment_format))

        # Paren
        self.paren = QRegExp(r'\(|\)')

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


class Sidebar(QFrame):
    """ Sidebar widget """

    def __init__(self, editor):
        super(Sidebar, self).__init__(editor)
        self.editor = editor

        self.editor.blockCountChanged.connect(self.update_viewport)
        self.editor.updateRequest.connect(self.update)

    def sizeHint(self):
        return QSize(self.__calculate_width(), 0)

    def redimensionar(self):
        cr = self.editor.contentsRect()
        current_x = cr.left()
        top = cr.top()
        height = cr.height()
        width = self.sizeHint().width()
        self.setGeometry(current_x, top, width, height)

    def update_viewport(self):
        self.editor.setViewportMargins(self.sizeHint().width(), 0, 0, 0)

    def __calculate_width(self):
        digits = len(str(max(1, self.editor.blockCount())))
        fmetrics_width = QFontMetrics(
            self.editor.document().defaultFont()).width("9")
        return 5 + fmetrics_width * digits + 3

    def paintEvent(self, event):
        """This method draws a left sidebar

        :param event: QEvent
        """

        painter = QPainter(self)
        # FIXME: cuando se cambia el tema se cambia esto, en su lugar poner el color en un attr
        # y leer de la config, la próxima vez que se inicie, cambiar
        painter.fillRect(event.rect(), QColor(get_editor_color('sidebar_background')))
        width = self.width() - 8
        height = self.editor.fontMetrics().height()
        font = self.editor.font()
        font_bold = self.editor.font()
        font_bold.setBold(True)
        painter.setFont(font)
        painter.setPen(QPen(QColor(get_editor_color('sidebar_foreground'))))
        current_line = self.editor.textCursor().blockNumber()

        for top, line, block in self.editor.visible_blocks:
            if current_line == line:
                painter.setFont(font_bold)
            else:
                painter.setFont(font)
            painter.drawText(5, top, width, height,
                             Qt.AlignRight, str(line + 1))


class Editor(QPlainTextEdit):

    lineColumnChanged = Signal(int, int)

    def __init__(self, file=None):
        super(Editor, self).__init__()
        self._file = file
        self.setFrameShape(QPlainTextEdit.NoFrame)

        self.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.setCursorWidth(USER_SETTINGS.cursor_width)
        self.__visible_blocks = []
        # Highlight current line
        self._highlight_line = USER_SETTINGS.highlight_current_line
        # Highlight braces
        self._match_parenthesis = USER_SETTINGS.match_parenthesis
        # Highlighter
        self._highlighter = Highlighter(self.document())
        # Set document font
        font_family = USER_SETTINGS.font_family
        font_size = USER_SETTINGS.font_size
        self.set_font(font_family, font_size)
        # Sidebar
        self._sidebar = Sidebar(self)

        self.word_separators = [',', '(', ')', '?']
        # Extra selections
        self._selections = {}
        self.__cursor_position_changed()
        self.apply_scheme()
        # Menu
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.blockCountChanged.connect(self.update)
        # Connection
        self.cursorPositionChanged.connect(self.__cursor_position_changed)

        short_zoom_in = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_Plus), self)
        short_zoom_in.activated.connect(lambda: self.zoom('in'))
        short_zoom_out = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_Minus), self)
        short_zoom_out.activated.connect(lambda: self.zoom('out'))

    @property
    def filename(self):
        return self._file.filename

    @property
    def display_name(self):
        return self._file.display_name

    @property
    def is_modified(self):
        return self.document().isModified()

    def reload_highlighter(self):
        self._highlighter.deleteLater()
        self._highlighter = None
        self._highlighter = Highlighter(self.document())

    def zoom(self, mode):
        if mode == 'out':
            self.zoomOut(1)
        else:
            self.zoomIn(1)
        self._sidebar.update_viewport()

    def set_highlight_line(self, value: bool):
        if self._highlight_line != value:
            self._highlight_line = value
            self.clear_selections('current_line')

    def set_match_parenthesis(self, value: bool):
        if self._match_parenthesis != value:
            self._match_parenthesis = value
            self.clear_selections('parenthesis')

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

    def resizeEvent(self, event):
        super(Editor, self).resizeEvent(event)
        self._sidebar.redimensionar()
        self._sidebar.update_viewport()

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
        lineno = self.textCursor().blockNumber() + 1
        colno = self.textCursor().columnNumber()
        self.lineColumnChanged.emit(lineno, colno)

        self.clear_selections("current_line")

        if self._highlight_line:
            _selection = QTextEdit.ExtraSelection()
            color = QColor(get_editor_color('current_line'))
            _selection.format.setBackground(color)
            _selection.format.setProperty(
                QTextCharFormat.FullWidthSelection, True)
            _selection.cursor = self.textCursor()
            _selection.cursor.clearSelection()
            self.add_selection("current_line", [_selection])

        # Paren matching
        if self._match_parenthesis:
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

    def setFont(self, font):
        super().setFont(font)
        self._sidebar.update_viewport()
        self._sidebar.redimensionar()

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
                    if block_start.text()[0].isspace():
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

    def apply_scheme(self):
        pal = self.palette()
        get = get_editor_color
        pal.setColor(QPalette.Base, QColor(get('background')))
        pal.setColor(QPalette.Text, QColor(get('foreground')))
        self.setPalette(pal)

    def selected_text(self):
        return self.textCursor().selectedText()

    def has_selection(self) -> bool:
        return self.textCursor().hasSelection()
