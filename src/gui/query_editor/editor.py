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

    def __init__(self, rfile=None):
        super(Editor, self).__init__()
        self.rfile = rfile
        self.modified = False
        # Highlighter
        self._highlighter = highlighter.Highlighter(self.document())
        self.setFont(settings.FONT)
        # Sidebar
        self._sidebar = sidebar.Sidebar(self)

        self.connect(self, SIGNAL("updateRequest(const QRect&, int)"),
                     self._sidebar.update_area)
        self.connect(self, SIGNAL("cursorPositionChanged()"),
                     self._emit_cursor_position)

    @property
    def filename(self):
        """ This function returns the filename of RFile object

        :returns: filename of RFile
        """

        return self.rfile.filename

    def resizeEvent(self, event):
        super(Editor, self).resizeEvent(event)
        # Fixed sidebar height
        self._sidebar.setFixedHeight(self.height())

    def _emit_cursor_position(self):
        line = self.blockCount()
        col = self.textCursor().columnNumber() + 1
        self.emit(SIGNAL("cursorPositionChanged(int, int)"), line, col)
