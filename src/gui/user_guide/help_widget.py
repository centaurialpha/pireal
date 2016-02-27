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

import os

from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QTextBrowser,
    QPushButton
)
from PyQt5.QtCore import (
    QUrl,
    Qt
)

from src.core import settings


class HelpWidget(QDialog):

    def __init__(self, parent=None):
        super(HelpWidget, self).__init__(parent)
        self.setWindowTitle(self.tr("Pireal User Guide"))
        box = QVBoxLayout(self)
        box.setContentsMargins(5, 0, 5, 0)
        self.setAttribute(Qt.WA_DeleteOnClose | Qt.WA_GroupLeader)
        self.text_browser = QTextBrowser()
        box.addWidget(self.text_browser)
        # Buttons
        btns_box = QHBoxLayout()
        btns_box.setContentsMargins(0, 5, 0, 5)
        home_btn = QPushButton(self.tr("Home"))
        btns_box.addWidget(home_btn)
        back_btn = QPushButton(self.tr("Back"))
        btns_box.addWidget(back_btn)
        btns_box.addStretch()
        close_btn = QPushButton(self.tr("Close"))
        btns_box.addWidget(close_btn)
        box.addLayout(btns_box)

        source = os.path.join(settings.USER_GUIDE_PATH, 'index.html')
        self.text_browser.setSource(QUrl(source))
        self.text_browser.setSearchPaths([settings.USER_GUIDE_PATH])
        # Connections
        home_btn.clicked.connect(self.text_browser.home)
        back_btn.clicked.connect(self.text_browser.backward)
        close_btn.clicked.connect(self.close)