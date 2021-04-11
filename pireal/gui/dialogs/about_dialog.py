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

from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QHBoxLayout,
    QSpacerItem,
    QSizePolicy,
    QPushButton
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from pireal import gui
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
        lbl_version = QLabel("{0}".format(gui.__version__))
        lbl_version.setAlignment(Qt.AlignHCenter)
        font = lbl_version.font()
        font.setPointSize(10)
        lbl_version.setFont(font)
        vbox.addWidget(lbl_version)

        # Description
        description = QLabel(tr.TR_DIALOG_ABOUT_PIREAL_BODY)
        description.setAlignment(Qt.AlignHCenter)
        font = description.font()
        font.setPointSize(13)
        description.setFont(font)
        vbox.addWidget(description)

        abuelo_agui_lbl = QLabel(
            'In memory of my grandpa, Agui <span style="color: #EC7875"> </span>')
        font = abuelo_agui_lbl.font()
        font.setPointSize(8)
        abuelo_agui_lbl.setFont(font)
        abuelo_agui_lbl.setAlignment(Qt.AlignHCenter)
        vbox.addWidget(abuelo_agui_lbl)

        # Copyright
        copy = QLabel("<br>Copyright © 2015-{year} - "
                      "Gabriel 'gabo' Acosta".format(
                          year=datetime.today().year))
        copy.setAlignment(Qt.AlignHCenter)
        font = copy.font()
        font.setPointSize(9)
        copy.setFont(font)
        vbox.addWidget(copy)

        # License and source
        lbl_license_source = QLabel(
            tr.TR_DIALOG_ABOUT_PIREAL_COPY.format(gui.__license__, gui.__source_code__)
        )
        lbl_license_source.setAlignment(Qt.AlignHCenter)
        lbl_license_source.setOpenExternalLinks(True)
        font = lbl_license_source.font()
        font.setPointSize(13)
        lbl_license_source.setFont(font)
        vbox.addWidget(lbl_license_source)

        # Buttons
        hbox = QHBoxLayout()
        hbox.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Expanding))
        btn_ok = QPushButton('Ok')
        hbox.addWidget(btn_ok)
        vbox.addLayout(hbox)

        btn_ok.clicked.connect(self.close)
