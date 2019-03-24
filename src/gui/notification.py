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

from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QSizePolicy
)
from PyQt5.QtCore import QTimer

from src.gui.main_window import Pireal


class Notification(QWidget):

    def __init__(self, parent=None):
        super(Notification, self).__init__(parent)
        box = QVBoxLayout(self)
        box.setContentsMargins(50, 0, 0, 0)
        self.notificator = QLabel("")
        box.addWidget(self.notificator)

        # Timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.clear)

        # Install service
        Pireal.load_service("notification", self)

    def clear(self):
        self.notificator.clear()

    def show_text(self, text, time_out=3000):
        if time_out != 0:
            self.timer.start(time_out)
        self.notificator.setText(text)


Notification()
