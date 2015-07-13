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

from PyQt4.QtGui import (
    QPlainTextEdit
)
from PyQt4.QtCore import SIGNAL
from src.gui.query_editor import (
    highlighter,
    sidebar
)
from src.core import settings


class Editor(QPlainTextEdit):

    def __init__(self):
        super(Editor, self).__init__()
        # Filename
        self.__filename = ""
        self.modified = False
        # Highlighter
        self._highlighter = highlighter.Highlighter(self.document())
        self.setFont(settings.FONT)
        # Sidebar
        self._sidebar = sidebar.Sidebar(self)

        self.connect(self, SIGNAL("updateRequest(const QRect&, int)"),
                     self._sidebar.update_area)

    def __get_filename(self):
        """ Private method.

        :returns: Return the filename
        """

        return self.__filename

    def __set_filename(self, filename):
        """ Private method

        :param filename: path of filename
        """

        self.__filename = filename

    filename = property(__get_filename, __set_filename)

    def resizeEvent(self, event):
        super(Editor, self).resizeEvent(event)
        # Fixed sidebar height
        self._sidebar.setFixedHeight(self.height())