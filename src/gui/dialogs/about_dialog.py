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
from src import gui


class AboutDialog(QDialog):

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setWindowTitle(self.tr("About Pireal"))
        vbox = QVBoxLayout(self)
        # Banner
        banner = QLabel()
        banner.setPixmap(QPixmap(":img/logo").scaled(375, 150))
        banner.setAlignment(Qt.AlignHCenter)
        vbox.addWidget(banner)

        # Version
        label_version = QLabel(self.tr("<a href='{0}'><span style='color: "
                                       "#3465a4'>Version {1}"
                                       "</span></a>".format(
                               gui.__source_code__, gui.__version__)))
        label_version.setAlignment(Qt.AlignHCenter)
        font = label_version.font()
        font.setPointSize(13)
        label_version.setFont(font)
        vbox.addWidget(label_version)

        # Description
        description = QLabel(self.tr("<br><br>an educational tool for "
                                     "working\nwith Relational Algebra."))
        description.setAlignment(Qt.AlignHCenter)
        font = description.font()
        font.setPointSize(13)
        description.setFont(font)
        vbox.addWidget(description)

        # License and source
        lbl_license_source = QLabel(self.tr("<br>This sotfware is licensed "
                                            "under <a href='{0}'><span style"
                                            "='color: #3465a4'>GNU GPL</span>"
                                            "</a> version 3,<br>source code "
                                            "is available on <a href='{1}'>"
                                            "<span style='color: #3465a4'>"
                                            "GitHub.</span></a>".format(
                                    gui.__license__, gui.__source_code__)))
        lbl_license_source.setAlignment(Qt.AlignHCenter)
        font = lbl_license_source.font()
        font.setPointSize(13)
        lbl_license_source.setFont(font)
        vbox.addWidget(lbl_license_source)

        # Buttons
        hbox = QHBoxLayout()
        hbox.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Expanding))
        btn_ok = QPushButton(self.tr("Done"))
        hbox.addWidget(btn_ok)
        vbox.addLayout(hbox)

        btn_ok.clicked.connect(self.close)
        label_version.linkActivated['QString'].connect(
            lambda link: webbrowser.open_new(link))
        lbl_license_source.linkActivated['QString'].connect(
            lambda link: webbrowser.open_new(link))
