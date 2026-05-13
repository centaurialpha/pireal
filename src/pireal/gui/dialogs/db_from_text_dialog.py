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

# type: ignore
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QLabel,
    QPlainTextEdit,
    QSplitter,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)

from pireal import translations as tr
from pireal.gui.db_highlighter import DBHighlighter
from pireal.utils import sanitize_data

PLACEHOLDER = """\
@personas:id,nombre,edad
1,Gabriel,34
2,Marisel,32

@cursos:id,nombre
1,Base de Datos
2,Algoritmos
"""


class DBFromTextDialog(QDialog):
    def __init__(self, parent=None, *, title: str | None = None, editor_label: str | None = None):
        super().__init__(parent)
        self.setWindowTitle(title or tr.TR_DB_FROM_TEXT_TITLE)
        self._editor_label = editor_label or tr.TR_DB_FROM_TEXT_EDITOR_LABEL
        self.setMinimumSize(800, 500)
        self.resize(900, 560)

        self._parsed_data: dict | None = None

        self._build_ui()
        self._setup_timer()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 8)
        layout.setSpacing(8)

        splitter = QSplitter(Qt.Orientation.Horizontal)

        left = QWidget()
        left_layout = QVBoxLayout(left)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(4)
        left_layout.addWidget(QLabel(self._editor_label))

        self._editor = QPlainTextEdit()
        self._editor.setPlaceholderText(PLACEHOLDER)
        self._editor.setTabStopDistance(28)
        font = self._editor.font()
        font.setFamily("Monospace")
        font.setPointSize(10)
        self._editor.setFont(font)
        self._highlighter = DBHighlighter(self._editor.document())
        left_layout.addWidget(self._editor)

        right = QWidget()
        right_layout = QVBoxLayout(right)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(4)
        right_layout.addWidget(QLabel(tr.TR_DB_FROM_TEXT_PREVIEW_LABEL))

        self._preview = QTreeWidget()
        self._preview.setHeaderHidden(True)
        self._preview.setAnimated(True)
        right_layout.addWidget(self._preview)

        self._status_label = QLabel("")
        self._status_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        right_layout.addWidget(self._status_label)

        splitter.addWidget(left)
        splitter.addWidget(right)
        splitter.setSizes([480, 320])

        layout.addWidget(splitter)

        self._buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self._buttons.button(QDialogButtonBox.StandardButton.Ok).setText(tr.TR_DB_FROM_TEXT_LOAD_BTN)
        self._buttons.button(QDialogButtonBox.StandardButton.Ok).setEnabled(False)
        self._buttons.accepted.connect(self.accept)
        self._buttons.rejected.connect(self.reject)
        layout.addWidget(self._buttons)

        self._editor.textChanged.connect(self._on_text_changed)

    def _setup_timer(self):
        self._timer = QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.setInterval(300)
        self._timer.timeout.connect(self._update_preview)

    def _on_text_changed(self):
        self._timer.start()

    def _update_preview(self):
        text = self._editor.toPlainText().strip()
        self._preview.clear()

        if not text:
            self._set_status("", ok=True)
            self._buttons.button(QDialogButtonBox.StandardButton.Ok).setEnabled(False)
            self._parsed_data = None
            return

        try:
            data = sanitize_data(text)
        except Exception:
            self._set_status("●", ok=False)
            self._buttons.button(QDialogButtonBox.StandardButton.Ok).setEnabled(False)
            self._parsed_data = None
            return

        tables = data.get("tables", [])
        if not tables:
            self._set_status(tr.TR_DB_FROM_TEXT_NO_RELATIONS, ok=False)
            self._buttons.button(QDialogButtonBox.StandardButton.Ok).setEnabled(False)
            self._parsed_data = None
            return

        for table in tables:
            name = table["name"]
            header = table["header"]
            tuples = table["tuples"]

            cardinality = len(tuples)
            tuple_label = tr.TR_DB_FROM_TEXT_TUPLE_SINGULAR if cardinality == 1 else tr.TR_DB_FROM_TEXT_TUPLE_PLURAL
            root = QTreeWidgetItem(
                self._preview,
                [f"  {name}  ({cardinality} {tuple_label})"],
            )
            root.setExpanded(True)

            # Fila de encabezado
            header_item = QTreeWidgetItem(root, [" | ".join(header)])
            font = header_item.font(0)
            font.setBold(True)
            header_item.setFont(0, font)

            # Tuplas (máximo 5 para no saturar)
            for tupla in list(tuples)[:5]:
                QTreeWidgetItem(root, [" | ".join(tupla)])
            if cardinality > 5:
                QTreeWidgetItem(root, [f"  ... ({cardinality - 5} +)"])

        n = len(tables)
        status = tr.TR_DB_FROM_TEXT_VALID_ONE if n == 1 else tr.TR_DB_FROM_TEXT_VALID_MANY.format(n)
        self._set_status(status, ok=True)
        self._buttons.button(QDialogButtonBox.StandardButton.Ok).setEnabled(True)
        self._parsed_data = data

    def _set_status(self, message: str, *, ok: bool):
        color = "green" if ok else "red"
        self._status_label.setText(f'<span style="color:{color}">{message}</span>')

    def parsed_data(self) -> dict | None:
        return self._parsed_data
