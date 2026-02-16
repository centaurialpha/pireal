# -*- coding: utf-8 -*-
#
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

import io
import mimetypes
import uuid
from pathlib import Path
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from PyQt6.QtCore import Qt, QThread, pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import (
    QButtonGroup,
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPlainTextEdit,
    QPushButton,
    QRadioButton,
    QVBoxLayout,
)

from pireal import translations as tr

FEEDBACK_TYPES = [
    (tr.TR_FEEDBACK_TYPE_BUG, "Bug"),
    (tr.TR_FEEDBACK_TYPE_SUGGESTION, "Sugerencia"),
    (tr.TR_FEEDBACK_TYPE_QUESTION, "Pregunta"),
    (tr.TR_FEEDBACK_TYPE_OTHER, "Otro"),
]

TELEGRAM_TOKEN = ""
TELEGRAM_CHAT_ID = ""


def _build_multipart(fields: dict, file_path: Path) -> tuple[bytes, str]:
    boundary = uuid.uuid4().hex
    body = io.BytesIO()
    for name, value in fields.items():
        body.write(f"--{boundary}\r\n".encode())
        body.write(f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode())
        body.write(f"{value}\r\n".encode())
    mime = mimetypes.guess_type(str(file_path))[0] or "application/octet-stream"
    body.write(f"--{boundary}\r\n".encode())
    body.write(
        f'Content-Disposition: form-data; name="photo"; filename="{file_path.name}"\r\n'.encode()
    )
    body.write(f"Content-Type: {mime}\r\n\r\n".encode())
    body.write(file_path.read_bytes())
    body.write(b"\r\n")
    body.write(f"--{boundary}--\r\n".encode())
    return body.getvalue(), f"multipart/form-data; boundary={boundary}"


class _TelegramSender(QThread):
    success = pyqtSignal()
    failure = pyqtSignal(str)

    def __init__(self, text: str, image_path: Path | None = None, parent=None):
        super().__init__(parent)
        self._text = text
        self._image_path = image_path

    def run(self):
        token = TELEGRAM_TOKEN
        chat_id = TELEGRAM_CHAT_ID

        if not token or not chat_id:
            self.failure.emit("Token o chat ID no configurados.")
            return

        url = f"https://api.telegram.org/bot{token}/sendMessage"
        data = urlencode({"chat_id": chat_id, "text": self._text}).encode()
        if self._image_path:
            url = f"https://api.telegram.org/bot{token}/sendPhoto"
            body, content_type = _build_multipart(
                {"chat_id": chat_id, "caption": self._text}, self._image_path
            )
            req = Request(url, data=body, method="POST")
            req.add_header("Content-Type", content_type)
        else:
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            data = urlencode({"chat_id": chat_id, "text": self._text}).encode()
            req = Request(url, data=data, method="POST")

        try:
            with urlopen(req, timeout=10) as response:
                if response.status == 200:
                    self.success.emit()
                else:
                    self.failure.emit(f"Error del servidor: {response.status}")
        except URLError as e:
            self.failure.emit(f"Error de red: {e.reason}")
        except Exception as e:
            self.failure.emit(str(e))


class FeedbackDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(tr.TR_FEEDBACK_TITLE)
        self.setMinimumWidth(480)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.setWindowFlags(
            self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint
        )

        self._sender: _TelegramSender | None = None
        self._image_path: Path | None = None
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(20, 16, 20, 16)

        # Tipo de feedback
        group_box = QGroupBox(tr.TR_FEEDBACK_TYPE_GROUP)
        group_layout = QHBoxLayout(group_box)
        self._type_group = QButtonGroup(self)

        for i, (label, _) in enumerate(FEEDBACK_TYPES):
            radio = QRadioButton(label)
            if i == 0:
                radio.setChecked(True)
            self._type_group.addButton(radio, i)
            group_layout.addWidget(radio)

        layout.addWidget(group_box)

        hint = QLabel(tr.TR_FEEDBACK_HINT_LABEL)
        hint.setOpenExternalLinks(True)
        hint.setWordWrap(True)
        hint.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = hint.font()
        font.setPointSize(font.pointSize() - 1)
        hint.setFont(font)
        layout.addWidget(hint)

        # Título y descripción
        form = QFormLayout()
        form.setSpacing(8)

        self._title_input = QLineEdit()
        self._title_input.setPlaceholderText(tr.TR_FEEDBACK_TITLE_PLACEHOLDER)
        self._title_input.textChanged.connect(self._update_send_btn)
        form.addRow(tr.TR_FEEDBACK_TITLE_LABEL, self._title_input)

        self._body_input = QPlainTextEdit()
        self._body_input.setPlaceholderText(tr.TR_FEEDBACK_BODY_PLACEHOLDER)
        self._body_input.setMinimumHeight(120)
        self._body_input.textChanged.connect(self._update_send_btn)
        form.addRow(tr.TR_FEEDBACK_BODY_LABEL, self._body_input)

        layout.addLayout(form)

        # Adjuntar imagen
        attach_layout = QHBoxLayout()
        self._attach_btn = QPushButton(tr.TR_FEEDBACK_ATTACH_BTN)
        self._attach_btn.setFlat(True)
        palette = self._attach_btn.palette()
        color = palette.color(palette.ColorRole.Link).name()
        self._attach_btn.setStyleSheet(f"color: {color};")
        self._attach_btn.clicked.connect(self._on_attach)

        self._attach_label = QLabel()
        self._attach_label.hide()

        self._remove_attach_btn = QPushButton("✕")
        self._remove_attach_btn.setFlat(True)
        self._remove_attach_btn.setFixedWidth(24)
        self._remove_attach_btn.hide()
        self._remove_attach_btn.clicked.connect(self._on_remove_attachment)

        attach_layout.addWidget(self._attach_btn)
        attach_layout.addWidget(self._attach_label)
        attach_layout.addWidget(self._remove_attach_btn)
        attach_layout.addStretch()
        layout.addLayout(attach_layout)
        # Status
        self._status_label = QLabel()
        self._status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._status_label.hide()
        layout.addWidget(self._status_label)

        # Botones
        self._button_box = QDialogButtonBox()
        self._send_btn = QPushButton(tr.TR_FEEDBACK_BTN_SEND)
        self._send_btn.setDefault(True)
        self._send_btn.setEnabled(False)
        cancel_btn = QPushButton(tr.TR_CANCEL)
        cancel_btn.setFlat(True)
        self._button_box.addButton(cancel_btn, QDialogButtonBox.ButtonRole.RejectRole)
        self._button_box.addButton(
            self._send_btn, QDialogButtonBox.ButtonRole.AcceptRole
        )
        self._button_box.rejected.connect(self.reject)
        self._button_box.accepted.connect(self._on_send)
        layout.addWidget(self._button_box)

    def _update_send_btn(self):
        has_title = bool(self._title_input.text().strip())
        has_body = bool(self._body_input.toPlainText().strip())
        self._send_btn.setEnabled(has_title and has_body)

    @pyqtSlot()
    def _on_attach(self):
        path, _ = QFileDialog.getOpenFileName(
            self, tr.TR_FEEDBACK_ATTACH_DIALOG, "", tr.TR_FEEDBACK_ATTACH_FILTER
        )
        if not path:
            return
        self._image_path = Path(path)
        self._attach_label.setText(self._image_path.name)
        self._attach_label.show()
        self._remove_attach_btn.show()
        self._attach_btn.hide()

    @pyqtSlot()
    def _on_remove_attachment(self):
        self._image_path = None
        self._attach_label.hide()
        self._remove_attach_btn.hide()
        self._attach_btn.show()

    def _selected_type(self) -> str:
        btn_id = self._type_group.checkedId()
        return FEEDBACK_TYPES[btn_id][1]

    def _build_message(self) -> str:
        tipo = self._selected_type()
        titulo = self._title_input.text().strip()
        cuerpo = self._body_input.toPlainText().strip()
        return f"[Pireal Feedback]\nTipo: {tipo}\nTítulo: {titulo}\n\n{cuerpo}"

    @pyqtSlot()
    def _on_send(self):
        self._send_btn.setEnabled(False)
        self._send_btn.setText(tr.TR_FEEDBACK_BTN_SENDING)
        self._status_label.hide()

        self._sender = _TelegramSender(
            text=self._build_message(),
            image_path=self._image_path,
            parent=self,
        )
        self._sender.success.connect(self._on_success)
        self._sender.failure.connect(self._on_failure)
        self._sender.start()

    @pyqtSlot()
    def _on_success(self):
        self._show_status(tr.TR_FEEDBACK_SUCCESS)
        self._send_btn.hide()

    @pyqtSlot(str)
    def _on_failure(self, error: str):
        self._show_status(tr.TR_FEEDBACK_ERROR_PREFIX.format(error), error=True)
        self._send_btn.setEnabled(True)
        self._send_btn.setText(tr.TR_FEEDBACK_BTN_RETRY)

    def _show_status(self, msg: str, error: bool = False):
        if error:
            from pireal.gui.theme.manager import get_theme_manager
            from pireal.gui.theme.schema import EditorColorRole

            color = (
                get_theme_manager()
                .current_scheme.editor.get(EditorColorRole.ERROR)
                .name()
            )
        else:
            palette = self._status_label.palette()
            color = palette.color(palette.ColorRole.Link).name()
        self._status_label.setText(f'<span style="color:{color}">{msg}</span>')
        self._status_label.show()
