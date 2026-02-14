from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QGuiApplication
from PyQt6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
)

from pireal.gui.sql_highlighter import SQLHighlighter
from pireal.gui.theme.manager import get_theme_manager
from pireal.settings import settings


class SQLDialog(QDialog):
    def __init__(self, sql: str, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.setWindowTitle("Generated SQL")
        self.resize(800, 400)

        layout = QVBoxLayout(self)

        self._editor = QPlainTextEdit()
        self._editor.setReadOnly(True)
        self._editor.setPlainText(sql)
        self._editor.setFont(QFont(settings.font_family, settings.font_size))
        scheme = get_theme_manager().current_scheme
        pal = self._editor.palette()
        pal.setColor(pal.ColorRole.Base, scheme.editor.background)
        pal.setColor(pal.ColorRole.Text, scheme.editor.foreground)
        self._editor.setPalette(pal)
        self._highlighter = SQLHighlighter(self._editor.document())
        self._editor.setPlainText(sql)
        layout.addWidget(self._editor)

        settings.settingsChanged.connect(self._on_settings_changed)

        button_box = QDialogButtonBox()
        copy_btn = QPushButton("Copy to clipboard")
        copy_btn.clicked.connect(self._copy)
        button_box.addButton(copy_btn, QDialogButtonBox.ButtonRole.ActionRole)
        button_box.addButton(QDialogButtonBox.StandardButton.Close)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def _copy(self):
        QGuiApplication.clipboard().setText(self._editor.toPlainText())

    def _on_settings_changed(self, key: str):
        if key in ("font_family", "font_size"):
            self._editor.setFont(QFont(settings.font_family, settings.font_size))
