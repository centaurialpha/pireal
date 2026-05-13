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

from PyQt6.QtCore import (
    QStringListModel,
    Qt,
)
from PyQt6.QtGui import QBrush, QPalette
from PyQt6.QtWidgets import (
    QCompleter,
    QPlainTextEdit,
)

from pireal.gui.highlighter import Highlighter
from pireal.gui.theme.manager import get_theme_manager
from pireal.gui.theme.schema import (
    ColorScheme,
    EditorColorRole,
)


class _CompleterModel(QStringListModel):
    def __init__(self, keywords: list[str], parent=None):
        super().__init__(keywords, parent)
        self._keyword_set = set(keywords)

    def set_words(self, words: list[str]) -> None:
        self.setStringList(words)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.ForegroundRole:
            text = super().data(index, Qt.ItemDataRole.DisplayRole)
            if text is None:
                return None
            scheme = get_theme_manager().current_scheme
            if text in self._keyword_set:
                return QBrush(scheme.editor.get(EditorColorRole.KEYWORD))
            return QBrush(scheme.editor.get(EditorColorRole.VARIABLE))
        return super().data(index, role)


class PirealCompleter(QCompleter):
    def __init__(self, parent: QPlainTextEdit):
        super().__init__(parent)
        self.setMaxVisibleItems(10)
        self._editor = parent
        self._keywords = Highlighter.KEYWORDS

        self._model = _CompleterModel(self._keywords, self)
        self.setModel(self._model)
        self.setWidget(parent)
        self.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        self.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.activated.connect(self._insert_completion)

        self._apply_popup_style(get_theme_manager().current_scheme)
        get_theme_manager().themeChanged.connect(self._apply_popup_style)

    def _apply_popup_style(self, scheme: ColorScheme) -> None:
        popup = self.popup()
        if popup is None:
            return

        bg = scheme.editor.get(EditorColorRole.BACKGROUND).name()
        fg = scheme.editor.get(EditorColorRole.FOREGROUND).name()
        border = scheme.highlight.name()
        h = scheme.highlight
        selected_bg = f"rgba({h.red()}, {h.green()}, {h.blue()}, 50)"

        palette = popup.palette()
        palette.setColor(QPalette.ColorRole.Text, scheme.editor.get(EditorColorRole.FOREGROUND))
        palette.setColor(QPalette.ColorRole.Base, scheme.editor.get(EditorColorRole.BACKGROUND))
        popup.setPalette(palette)

        popup.setMinimumWidth(220)
        popup.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        popup.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        popup.setStyleSheet(f"""
            QListView {{
                background-color: {bg};
                color: {fg};
                border: 1px solid {border};
                border-radius: 6px;
                padding: 4px;
                outline: 0;
            }}
            QListView::item {{
                color: {fg};
                padding: 4px 12px;
                border-radius: 3px;
            }}
            QListView::item:selected {{
                background-color: {selected_bg};
            }}
            QScrollBar:vertical {{
                width: 0px;
            }}
        """)

    def update_words(self, words: list[str]) -> None:
        self._model.set_words(self._keywords + words)

    def _insert_completion(self, completion: str) -> None:
        prefix = self.completionPrefix()
        cursor = self._editor.textCursor()
        cursor.insertText(completion[len(prefix) :])
        self._editor.setTextCursor(cursor)


# from PyQt6.QtCore import QStringListModel, Qt
# from PyQt6.QtWidgets import QCompleter, QPlainTextEdit
#
# from pireal.gui.highlighter import Highlighter
#
#
# class PirealCompleter(QCompleter):
#     def __init__(self, parent: QPlainTextEdit):
#         super().__init__(Highlighter.KEYWORDS, parent)
#         self._editor = parent
#         self.setWidget(parent)
#         self.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
#         self.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
#         self.activated.connect(self._insert_completion)
#
#     def update_words(self, words: list[str]):
#         all_words = Highlighter.KEYWORDS + words
#         self.setModel(QStringListModel(all_words, self))
#
#     def _insert_completion(self, completion: str):
#         prefix = self.completionPrefix()
#         cursor = self._editor.textCursor()
#         cursor.insertText(completion[len(prefix) :])
#         self._editor.setTextCursor(cursor)
