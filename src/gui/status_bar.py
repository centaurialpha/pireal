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

from PyQt5.QtWidgets import QStatusBar
from src.gui.main_window import Pireal


class StatusBar(QStatusBar):

    def __init__(self):
        super(StatusBar, self).__init__()

        Pireal.load_service("status", self)

        #self.connect(self, SIGNAL("messageChanged(QString)"),
                     #self.__message_end)
        self.messageChanged['QString'].connect(self.__message_end)

    def show_message(self, msg, timeout=4000):
        """ This function is a implementation of QStatusBar.showMessage

        :param msg: Text message
        :param timeout:
        """

        self.show()
        self.showMessage(msg, timeout)

    def __message_end(self, msg):
        """ This function hide the Status Bar

        :param msg: Text message
        """

        if not msg:
            self.hide()


status = StatusBar()
