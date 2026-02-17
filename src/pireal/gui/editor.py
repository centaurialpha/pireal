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

from PyQt6.QtCore import QEvent, Qt, QTimer, pyqtSignal
from PyQt6.QtGui import (
    QColor,
    QFont,
    QKeyEvent,
    QTextCharFormat,
    QTextCursor,
    QTextDocument,
)
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPlainTextEdit,
    QTextEdit,
    QToolButton,
    QToolTip,
)

from pireal import translations as tr
from pireal.gui import highlighter, sidebar
from pireal.gui.completer import PirealCompleter
from pireal.gui.theme.manager import get_theme_manager
from pireal.gui.theme.schema import ColorScheme, EditorColorRole
from pireal.settings import settings

BRACKETS = "()"
OPOSITE_BRACKET = {
    "(": ")",
    ")": "(",
}


OPERATOR_TOOLTIPS = {
    "select": tr.TR_TOOLTIP_SELECT,
    "project": tr.TR_TOOLTIP_PROJECT,
    "rename": tr.TR_TOOLTIP_RENAME,
    "product": tr.TR_TOOLTIP_PRODUCT,
    "njoin": tr.TR_TOOLTIP_NJOIN,
    "louter": tr.TR_TOOLTIP_LOUTER,
    "router": tr.TR_TOOLTIP_ROUTER,
    "fouter": tr.TR_TOOLTIP_FOUTER,
    "difference": tr.TR_TOOLTIP_DIFFERENCE,
    "intersect": tr.TR_TOOLTIP_INTERSECT,
    "union": tr.TR_TOOLTIP_UNION,
}


class EditorNotification(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        self.setAutoFillBackground(True)
        pal = self.palette()
        pal.setColor(pal.ColorRole.Window, QColor("#ff5555"))
        self.setPalette(pal)
        self._messages_label = QLabel()
        layout.addWidget(self._messages_label)
        close_button = QToolButton()
        close_button.setText("\uf410")
        close_button.setAutoRaise(True)
        close_button.setToolTip("Close")
        layout.addWidget(close_button)

        close_button.clicked.connect(self.hide)

    def show_message(self, text):
        self._messages_label.setText(text)


class BracketHighlighter:
    def _make_selection(self, block, column_index, matched):
        selection = QTextEdit.ExtraSelection()
        if matched:
            color = "#ffff00"
        else:
            color = "#ff0000"
        selection.format.setBackground(QColor(color))
        selection.cursor = QTextCursor(block)
        selection.cursor.setPosition(block.position() + column_index)
        selection.cursor.movePosition(
            QTextCursor.MoveOperation.Right, QTextCursor.MoveMode.KeepAnchor
        )
        return selection

    def _iterate_chars_forward(self, block, start_column_index):
        for col_index, char in list(enumerate(block.text()))[start_column_index:]:
            yield block, col_index, char

        block = block.next()

        while block.isValid():
            for col_index, char in enumerate(block.text()):
                yield block, col_index, char
            block = block.next()

    def _iterate_chars_backward(self, block, start_column_index):
        for col_index, char in reversed(
            list(enumerate(block.text()[:start_column_index]))
        ):
            yield block, col_index, char

        block = block.previous()

        while block.isValid():
            for col_index, char in reversed(list(enumerate(block.text()))):
                yield block, col_index, char
            block = block.previous()

    def _find_matching_bracket(self, bracket, block, column_index):
        if bracket in "([{":
            chars_gen = self._iterate_chars_forward(block, column_index + 1)
        else:
            chars_gen = self._iterate_chars_backward(block, column_index)

        depth = 1
        oposite = OPOSITE_BRACKET[bracket]
        for block, col_index, char in chars_gen:
            if char == oposite:
                depth -= 1
                if depth == 0:
                    return block, col_index
            elif char == bracket:
                depth += 1
        else:
            return None, None

    def _highlight_bracket(self, bracket, block, column_index):
        matched_block, matched_column_index = self._find_matching_bracket(
            bracket, block, column_index
        )
        if matched_block is not None:
            return [
                self._make_selection(block, column_index, True),
                self._make_selection(matched_block, matched_column_index, True),
            ]
        return [self._make_selection(block, column_index, False)]

    def extra_selections(self, block, column_index):
        block_text = block.text()

        if column_index < len(block_text) and block_text[column_index] in BRACKETS:
            return self._highlight_bracket(
                block_text[column_index], block, column_index
            )
        return []


class Editor(QPlainTextEdit):
    errorOccurred = pyqtSignal(int, str)
    errorCleared = pyqtSignal()

    def __init__(self, pfile=None):
        super(Editor, self).__init__()
        # Extra selections
        self._selections = {}

        self._error_line = -1
        self._error_message = ""

        theme_manager = get_theme_manager()
        theme_manager.themeChanged.connect(self._on_theme_changed)

        self._error_color = theme_manager.current_scheme.editor.get(
            EditorColorRole.ERROR
        )

        self._apply_theme(theme_manager.current_scheme)

        self._bracket_highlighter = BracketHighlighter()

        self.setFrameShape(QPlainTextEdit.Shape.NoFrame)
        self.setMouseTracking(True)
        # self.setLineWrapMode(QPlainTextEdit.WrapMode.NoWrap)
        self.setCursorWidth(3)
        self.pfile = pfile
        self.__visible_blocks = []
        self.modified = False
        # Highlighter
        self._highlighter = highlighter.Highlighter(self.document())
        # Set document font
        self.set_font(settings.font_family, settings.font_size)
        # Sidebar
        self._sidebar = sidebar.Sidebar(self)
        self.word_separators = [")", "("]
        # Menu
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.blockCountChanged.connect(self.update)

        # Completer
        self.completer = PirealCompleter(self)
        # Connection
        self.cursorPositionChanged.connect(self._on_cursor_position_changed)

    def _on_cursor_position_changed(self):
        self._highlight_current_line()

        if settings.match_parenthesis:
            cursor_column_index = self.textCursor().positionInBlock()
            bracket_selections = self._bracket_highlighter.extra_selections(
                self.textCursor().block(), cursor_column_index
            )
            self.add_selection("parenthesis", bracket_selections)
        else:
            self.clear_selections("parenthesis")

    def _apply_theme(self, scheme: ColorScheme):
        """Aplica un ColorScheme al editor."""
        editor = scheme.editor

        # Colores del editor
        pal = self.palette()
        pal.setColor(pal.ColorRole.Base, editor.get(EditorColorRole.BACKGROUND))
        pal.setColor(pal.ColorRole.Text, editor.get(EditorColorRole.FOREGROUND))
        self.setPalette(pal)

        self.viewport().setPalette(pal)

        # Color de línea actual
        self._current_line_color = editor.get(EditorColorRole.CURRENT_LINE)
        self._error_color = editor.get(EditorColorRole.ERROR)

        # Re-highlight línea actual
        self._highlight_current_line()

        settings.settingsChanged.connect(self._on_settings_changed)

    def _on_settings_changed(self, key: str):
        if key in ("font_family", "font_size"):
            self.set_font(settings.font_family, settings.font_size)
        elif key == "highlight_current_line":
            self._highlight_current_line()

    def _highlight_current_line(self):
        if not settings.highlight_current_line:
            self.clear_selections("current_line")
            return

        extra_selections = []
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            selection.format.setBackground(self._current_line_color)
            selection.format.setProperty(
                QTextCharFormat.Property.FullWidthSelection, True
            )
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extra_selections.append(selection)

        self.add_selection("current_line", extra_selections)

    def _on_theme_changed(self, scheme: ColorScheme):
        self._apply_theme(scheme)

    @property
    def visible_blocks(self):
        return self.__visible_blocks

    def _update_visible_blocks(self):
        self.__visible_blocks.clear()
        append = self.__visible_blocks.append

        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
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

    def resizeEvent(self, e):
        super(Editor, self).resizeEvent(e)
        self._sidebar.redimensionar()
        self._sidebar.update_viewport()

    def paintEvent(self, e):
        self._update_visible_blocks()
        super().paintEvent(e)

    def word_under_cursor(self, cursor=None):
        """Returns QTextCursor that contains a word under passed cursor
        or actual cursor
        """
        if cursor is None:
            cursor = self.textCursor()
        start_pos = end_pos = cursor.position()
        while not cursor.atStart():
            cursor.movePosition(
                QTextCursor.MoveOperation.Left, QTextCursor.MoveMode.KeepAnchor
            )
            char = cursor.selectedText()[0]
            selected_text = cursor.selectedText()
            if (
                selected_text in self.word_separators
                and (selected_text != "n" and selected_text != "t")
                or char.isspace()
            ):
                break
            start_pos = cursor.position()
            cursor.setPosition(start_pos)
        cursor.setPosition(end_pos)
        while not cursor.atEnd():
            cursor.movePosition(
                QTextCursor.MoveOperation.Right, QTextCursor.MoveMode.KeepAnchor
            )
            char = cursor.selectedText()[0]
            selected_text = cursor.selectedText()
            if (
                selected_text in self.word_separators
                and (selected_text != "n" and selected_text != "t")
                or char.isspace()
            ):
                break
            end_pos = cursor.position()
            cursor.setPosition(end_pos)
        cursor.setPosition(start_pos)
        cursor.setPosition(end_pos, QTextCursor.MoveMode.KeepAnchor)
        return cursor

    def set_font(self, font_family, size):
        font = QFont(font_family, size)
        super().setFont(font)

    def zoom_in(self):
        font = self.font()
        point_size = font.pointSize()
        point_size += 1
        font.setPointSize(point_size)
        self.setFont(font)

    def setFont(self, a0):
        super().setFont(a0)
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
            cursor.movePosition(QTextCursor.MoveOperation.Start)
            start_pos = cursor.position()
            cursor.movePosition(QTextCursor.MoveOperation.End)
            end_pos = cursor.position()
        # Create extra selection
        selection = QTextEdit.ExtraSelection()
        # selection.format.setBackground(self._highlight_line_color)
        selection.cursor = QTextCursor(cursor)
        selection.cursor.setPosition(start_pos)
        selection.cursor.setPosition(end_pos, QTextCursor.MoveMode.KeepAnchor)
        self.add_selection("run_cursor", [selection])
        # Remove extra selection after 0.3 seconds
        QTimer.singleShot(300, lambda: self.clear_selections("run_cursor"))

    def saved(self):
        self.modified = False
        document = self.document()
        if document is not None:
            document.setModified(self.modified)
        self.setFocus()

    def comment(self):
        """Comment one or more lines"""
        tcursor = self.textCursor()
        document = self.document()
        if document is not None:
            block_start = document.findBlock(tcursor.selectionStart())
            block_end = document.findBlock(tcursor.selectionEnd()).next()

            tcursor.beginEditBlock()

            while block_start != block_end:
                if block_start.text():
                    tcursor.setPosition(block_start.position())
                    if block_start.text()[0] != "%":
                        tcursor.insertText("% ")
                block_start = block_start.next()

            tcursor.endEditBlock()

    def uncomment(self):
        """Uncomment one or more lines"""
        tcursor = self.textCursor()
        document = self.document()
        if document is not None:
            block_start = document.findBlock(tcursor.selectionStart())
            block_end = document.findBlock(tcursor.selectionEnd()).next()

            tcursor.beginEditBlock()

            while block_start != block_end:
                if block_start.text():
                    tcursor.setPosition(block_start.position())
                    if block_start.text()[0] == "%":
                        tcursor.deleteChar()
                block_start = block_start.next()

            tcursor.endEditBlock()

    def find_text(
        self, search: str, cs=False, wo=False, backward=False, find_next=True
    ):
        flags = QTextDocument.FindFlag(0)
        if cs:
            flags = QTextDocument.FindFlag.FindCaseSensitively
        if wo:
            flags |= QTextDocument.FindFlag.FindWholeWords
        if backward:
            flags |= QTextDocument.FindFlag.FindBackward
        if find_next or backward:
            self.moveCursor(QTextCursor.MoveOperation.NoMove)
        else:
            self.moveCursor(QTextCursor.MoveOperation.StartOfWord)
        found = self.find(search, flags)
        if not found:
            cursor = self.textCursor()
            if backward:
                self.moveCursor(QTextCursor.MoveOperation.End)
            else:
                self.moveCursor(QTextCursor.MoveOperation.Start)
            found = self.find(search, flags)
            if not found:
                self.setTextCursor(cursor)

    def event(self, e: QEvent | None) -> bool:
        if e.type() == e.Type.ToolTip:
            cursor = self.cursorForPosition(e.pos())
            line = cursor.blockNumber() + 1
            if line == self._error_line:
                QToolTip.showText(e.globalPos(), self._error_message)
                return True
            # tooltip operator
            cursor.select(QTextCursor.SelectionType.WordUnderCursor)
            word = cursor.selectedText().lower()
            if word in OPERATOR_TOOLTIPS:
                QToolTip.showText(e.globalPos(), OPERATOR_TOOLTIPS[word])
                return True
        return super().event(e)

    def highlight_error(self, linenumber, message="Syntax error"):
        if linenumber == -1:
            self.clear_selections("error")
            self._error_line = -1
            self._error_message = ""
            self.errorCleared.emit()
            return

        self._error_line = linenumber
        self._error_message = message

        self.errorOccurred.emit(linenumber, message)

        selection = QTextEdit.ExtraSelection()
        selection.cursor = self.textCursor()
        selection.cursor.movePosition(
            QTextCursor.MoveOperation.Start, QTextCursor.MoveMode.MoveAnchor
        )
        selection.cursor.movePosition(
            QTextCursor.MoveOperation.Down,
            QTextCursor.MoveMode.MoveAnchor,
            linenumber - 1,
        )
        selection.cursor.select(QTextCursor.SelectionType.LineUnderCursor)
        selection.format.setUnderlineStyle(QTextCharFormat.UnderlineStyle.WaveUnderline)
        selection.format.setUnderlineColor(self._error_color)

        self.add_selection("error", [selection])

    def add_selection(self, selection_name, selections):
        self._selections[selection_name] = selections
        self.update_selections()

    def update_selections(self):
        selections = []
        for _, selection in self._selections.items():
            selections.extend(selection)
        self.setExtraSelections(selections)

    def clear_selections(self, selection_name):
        if selection_name in self._selections:
            self._selections[selection_name] = []
            self.update_selections()

    def keyPressEvent(self, e: QKeyEvent | None) -> None:
        if self.completer.popup().isVisible():
            if e.key() in (
                Qt.Key.Key_Enter,
                Qt.Key.Key_Return,
                Qt.Key.Key_Tab,
                Qt.Key.Key_Escape,
            ):
                e.ignore()
                return
        super().keyPressEvent(e)

        if e.modifiers() or not e.text():
            return
        prefix = self._text_under_cursor()
        if len(prefix) < 2:
            self.completer.popup().hide()
            return

        if prefix != self.completer.completionPrefix():
            self.completer.setCompletionPrefix(prefix)
            self.completer.popup().setCurrentIndex(
                self.completer.completionModel().index(0, 0)
            )

        rect = self.cursorRect()
        rect.setWidth(
            self.completer.popup().sizeHintForColumn(0)
            + self.completer.popup().verticalScrollBar().sizeHint().width()
        )
        self.completer.complete(rect)

    def _text_under_cursor(self) -> str:
        cursor = self.textCursor()
        cursor.select(cursor.SelectionType.WordUnderCursor)
        return cursor.selectedText()
