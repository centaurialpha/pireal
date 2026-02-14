from PyQt6.QtCore import QRegularExpression
from PyQt6.QtGui import QFont, QSyntaxHighlighter, QTextCharFormat

from pireal.gui.theme.manager import get_theme_manager
from pireal.gui.theme.schema import ColorScheme, EditorColorRole


class DBHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)
        theme_manager = get_theme_manager()
        theme_manager.themeChanged.connect(self._on_theme_changed)
        self._setup_formats(theme_manager.current_scheme)

    def _setup_formats(self, scheme: ColorScheme):
        editor = scheme.editor

        self._header_fmt = QTextCharFormat()
        self._header_fmt.setForeground(editor.get(EditorColorRole.KEYWORD))
        self._header_fmt.setFontWeight(QFont.Weight.Bold)

        self._relation_name_fmt = QTextCharFormat()
        self._relation_name_fmt.setForeground(editor.get(EditorColorRole.VARIABLE))
        self._relation_name_fmt.setFontWeight(QFont.Weight.Bold)

        self._attr_fmt = QTextCharFormat()
        self._attr_fmt.setForeground(editor.get(EditorColorRole.STRING))

        self._number_fmt = QTextCharFormat()
        self._number_fmt.setForeground(editor.get(EditorColorRole.NUMBER))

        self._comment_fmt = QTextCharFormat()
        self._comment_fmt.setForeground(editor.get(EditorColorRole.COMMENT))
        self._comment_fmt.setFontItalic(True)

        self.rehighlight()

    def _on_theme_changed(self, scheme: ColorScheme):
        self._setup_formats(scheme)

    def highlightBlock(self, text: str):
        # Comentarios: líneas que empiezan con %
        if text.startswith("%"):
            self.setFormat(0, len(text), self._comment_fmt)
            return

        # Header de relación: @nombre:attr1,attr2,...
        if text.startswith("@"):
            colon = text.find(":")
            if colon != -1:
                # @ + nombre de relación
                self.setFormat(0, colon, self._relation_name_fmt)
                # atributos después del :
                self.setFormat(colon, len(text) - colon, self._attr_fmt)
            else:
                self.setFormat(0, len(text), self._relation_name_fmt)
            return

        # Números en tuplas
        iterator = QRegularExpression(r"\b\d+(\.\d+)?\b").globalMatch(text)
        while iterator.hasNext():
            match = iterator.next()
            self.setFormat(
                match.capturedStart(), match.capturedLength(), self._number_fmt
            )
