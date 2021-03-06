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

from datetime import datetime

from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QSpacerItem
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QPushButton

from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

import pireal
from pireal import translations as tr


class AboutDialog(QDialog):

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setWindowTitle(tr.TR_DIALOG_ABOUT_PIREAL_TITLE)
        vbox = QVBoxLayout(self)
        # Banner
        banner = QLabel()
        banner.setPixmap(QPixmap(":img/icon"))
        banner.setAlignment(Qt.AlignHCenter)
        vbox.addWidget(banner)

        # Version
        lbl_version = QLabel(f'{pireal.__version__}')
        lbl_version.setAlignment(Qt.AlignHCenter)
        font = lbl_version.font()
        font.setPointSize(10)
        lbl_version.setFont(font)
        vbox.addWidget(lbl_version)

        # Code name
        lbl_code_name = QLabel(f'{pireal.__code_name__}')
        lbl_code_name.setAlignment(Qt.AlignHCenter)
        font = lbl_code_name.font()
        font.setPointSize(9)
        font.setItalic(True)
        lbl_code_name.setFont(font)
        vbox.addWidget(lbl_code_name)

        # Description
        description = QLabel(
            self.tr("Relational Algebra query evaluator"))
        description.setAlignment(Qt.AlignHCenter)
        font = description.font()
        font.setPointSize(13)
        description.setFont(font)
        vbox.addWidget(description)

        # Web
        web_lbl = QLabel("<a href='{0}'><span style='color: #3465a4'>"
                         "www.centaurialpha.github.io/pireal</span></a>")
        web_lbl.setOpenExternalLinks(True)
        web_lbl.setAlignment(Qt.AlignHCenter)
        vbox.addWidget(web_lbl)

        # Copyright
        copy = QLabel(f"<br>Copyright © 2015-{datetime.today().year} - "
                      "Gabriel 'gabo' Acosta")
        copy.setAlignment(Qt.AlignHCenter)
        font = copy.font()
        font.setPointSize(9)
        copy.setFont(font)
        vbox.addWidget(copy)

        # License and source
        lbl_license_source = QLabel(
            tr.TR_DIALOG_ABOUT_PIREAL_COPY.format(pireal.__license__, pireal.__source_code__))
        lbl_license_source.setAlignment(Qt.AlignHCenter)
        lbl_license_source.setOpenExternalLinks(True)
        font = lbl_license_source.font()
        font.setPointSize(13)
        lbl_license_source.setFont(font)
        vbox.addWidget(lbl_license_source)

        # Buttons
        hbox = QHBoxLayout()
        hbox.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Expanding))
        btn_ok = QPushButton(tr.TR_MSG_OK)
        hbox.addWidget(btn_ok)
        vbox.addLayout(hbox)

        btn_ok.clicked.connect(self.close)
