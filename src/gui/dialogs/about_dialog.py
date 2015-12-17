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

import webbrowser
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
from src import (
    gui,
    translations as tr
)


class AboutDialog(QDialog):

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setWindowTitle(tr.TR_ABOUT_DIALOG)
        vbox = QVBoxLayout(self)
        # Banner
        banner = QLabel()
        banner.setPixmap(QPixmap(":img/logo").scaled(375, 150))
        banner.setAlignment(Qt.AlignHCenter)
        vbox.addWidget(banner)

        # Version
        label_version = QLabel(tr.TR_ABOUT_DIALOG_VERSION.format(
                               gui.__source_code__, gui.__version__))
        label_version.setAlignment(Qt.AlignHCenter)
        font = label_version.font()
        font.setPointSize(13)
        label_version.setFont(font)
        vbox.addWidget(label_version)

        # Description
        description = QLabel(tr.TR_ABOUT_DIALOG_DESC)
        description.setAlignment(Qt.AlignHCenter)
        font = description.font()
        font.setPointSize(13)
        description.setFont(font)
        vbox.addWidget(description)

        # License and source
        lbl_license_source = QLabel(tr.TR_ABOUT_DIALOG_LICENSE_SOURCE.format(
                                    gui.__license__, gui.__source_code__))
        lbl_license_source.setAlignment(Qt.AlignHCenter)
        font = lbl_license_source.font()
        font.setPointSize(13)
        lbl_license_source.setFont(font)
        vbox.addWidget(lbl_license_source)

        # Buttons
        hbox = QHBoxLayout()
        hbox.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Expanding))
        btn_ok = QPushButton(tr.TR_ABOUT_DIALOG_BTN_OK)
        hbox.addWidget(btn_ok)
        vbox.addLayout(hbox)

        btn_ok.clicked.connect(self.close)
        label_version.linkActivated['QString'].connect(
            lambda link: webbrowser.open_new(link))
        lbl_license_source.linkActivated['QString'].connect(
            lambda link: webbrowser.open_new(link))
