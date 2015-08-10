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
from PyQt4.QtGui import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QPixmap,
    QHBoxLayout,
    QSpacerItem,
    QSizePolicy,
    QPushButton
)
from PyQt4.QtCore import (
    Qt,
    SIGNAL
)
from src import gui


class AboutDialog(QDialog):

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setWindowTitle(self.tr("Acerca de Pireal"))
        vbox = QVBoxLayout(self)
        # Banner
        banner = QLabel()
        banner.setPixmap(QPixmap(":img/banner").scaled(300, 120))
        banner.setAlignment(Qt.AlignHCenter)
        vbox.addWidget(banner)

        # Description
        description = QLabel(self.tr("<b>Pireal</b> es una herramienta "
                                     "educativa para trabajar con Álgebra "
                                     "Relacional.<br>"))
        vbox.addWidget(description)

        # Links, author, source
        vbox.addWidget(QLabel(self.tr("<b>Versión:</b> {}").format(
            gui.__version__)))
        source = QLabel(self.tr("<b>Código fuente:</b> <a href="
                                "'{0}'>{1}</a>").format(gui.__source_code__,
                                                        gui.__source_code__))
        vbox.addWidget(source)
        lname, llink = gui.__license__.split()
        _license = QLabel(self.tr("<b>Licencia:</b> <a href="
                                  "'{0}'>{1}</a>").format(llink, lname))
        vbox.addWidget(_license)
        vbox.addWidget(QLabel(self.tr("<b>Autor:</b> {}").format(
            gui.__author__)))
        vbox.addWidget(QLabel(self.tr("<b>e-mail:</b> {}").format(
            gui.__email__)))

        # Button ok
        hbox = QHBoxLayout()
        hbox.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Expanding))
        btn_ok = QPushButton("Ok")
        hbox.addWidget(btn_ok)
        vbox.addLayout(hbox)

        self.connect(btn_ok, SIGNAL("clicked()"), self.close)
        self.connect(source, SIGNAL("linkActivated(QString)"),
                     lambda link: webbrowser.open_new(link))
        self.connect(_license, SIGNAL("linkActivated(QString)"),
                     lambda link: webbrowser.open_new(link))
