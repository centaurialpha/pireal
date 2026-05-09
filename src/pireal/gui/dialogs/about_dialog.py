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

from datetime import datetime

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPainter, QPalette, QPixmap
from PyQt6.QtWidgets import QDialog, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout, QWidget

from pireal import (
    __version__,
    gui,
    translations as tr,
)


class _VersionPill(QWidget):
    _PADDING_H = 12
    _PADDING_V = 4

    def __init__(self, text: str, parent=None):
        super().__init__(parent)
        self._text = text
        fm = self.fontMetrics()
        self.setFixedSize(
            fm.horizontalAdvance(text) + self._PADDING_H * 2,
            fm.height() + self._PADDING_V * 2,
        )

    def paintEvent(self, a0) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        color = self.palette().color(QPalette.ColorRole.PlaceholderText)
        bg = QColor(color)
        bg.setAlpha(35)
        painter.setBrush(bg)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 3, 3)

        painter.setPen(color)
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, self._text)


class AboutDialog(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setWindowTitle(tr.TR_DIALOG_ABOUT_PIREAL_TITLE)
        vbox = QVBoxLayout(self)
        # Banner
        banner = QLabel()
        banner.setPixmap(QPixmap("icons:pireal_icon.png"))
        banner.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        vbox.addWidget(banner)

        # Version
        version_pill = _VersionPill(f"v{__version__}")
        vbox.addWidget(version_pill, alignment=Qt.AlignmentFlag.AlignHCenter)
        # lbl_version = QLabel(f"{__version__}")
        # lbl_version.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        # font = lbl_version.font()
        # font.setPointSize(10)
        # lbl_version.setFont(font)
        # vbox.addWidget(lbl_version)

        # Description
        description = QLabel(tr.TR_DIALOG_ABOUT_PIREAL_BODY)
        description.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        font = description.font()
        font.setPointSize(13)
        description.setFont(font)
        vbox.addWidget(description)

        abuelo_agui_lbl = QLabel(
            'Dedicated to Marisel, a wonderul woman who inspires me<span style="color: #EC7875"> </span>'
        )
        font = abuelo_agui_lbl.font()
        font.setPointSize(8)
        abuelo_agui_lbl.setFont(font)
        abuelo_agui_lbl.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        vbox.addWidget(abuelo_agui_lbl)

        # Copyright
        copy = QLabel(f"<br>Copyright © 2015-{datetime.today().year} - Gabriel 'gabo' Acosta")
        copy.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        font = copy.font()
        font.setPointSize(9)
        copy.setFont(font)
        vbox.addWidget(copy)

        # License and source
        lbl_license_source = QLabel(tr.TR_DIALOG_ABOUT_PIREAL_COPY.format(gui.__license__, gui.__source_code__))
        lbl_license_source.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        lbl_license_source.setOpenExternalLinks(True)
        font = lbl_license_source.font()
        font.setPointSize(13)
        lbl_license_source.setFont(font)
        vbox.addWidget(lbl_license_source)

        # Buttons
        hbox = QHBoxLayout()
        hbox.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding))
        btn_ok = QPushButton("Ok")
        hbox.addWidget(btn_ok)
        vbox.addLayout(hbox)

        btn_ok.clicked.connect(self.close)
