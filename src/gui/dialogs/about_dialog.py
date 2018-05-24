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
from src import gui


class AboutDialog(QDialog):

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setWindowTitle(self.tr("Acerca de Pireal"))
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
        copy = QLabel("<br>Copyright © 2015-{year} - "
                      "Gabriel 'gabo' Acosta".format(
                          year=datetime.today().year))
        copy.setAlignment(Qt.AlignHCenter)
        font = copy.font()
        font.setPointSize(9)
        copy.setFont(font)
        vbox.addWidget(copy)

        # License and source
        lbl_license_source = QLabel(self.tr("<br>Este software tiene licencia "
                                            "<a href='{0}'><span style"
                                            "='color: #3465a4'>GNU GPL</span>"
                                            "</a> versión 3,<br>el código "
                                            "fuente "
                                            "está disponible en <a href='{1}'>"
                                            "<span style='color: #3465a4'>"
                                            "GitHub.</span></a>".format(
                                                gui.__license__,
                                                gui.__source_code__)))
        lbl_license_source.setAlignment(Qt.AlignHCenter)
        lbl_license_source.setOpenExternalLinks(True)
        font = lbl_license_source.font()
        font.setPointSize(13)
        lbl_license_source.setFont(font)
        vbox.addWidget(lbl_license_source)

        # Buttons
        hbox = QHBoxLayout()
        hbox.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Expanding))
        btn_ok = QPushButton(self.tr("Aceptar"))
        hbox.addWidget(btn_ok)
        vbox.addLayout(hbox)

        btn_ok.clicked.connect(self.close)
