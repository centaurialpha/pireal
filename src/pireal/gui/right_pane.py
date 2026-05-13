# Copyright 2015-2026 - Gabriel Acosta <acostadariogabriel@gmail.com>
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

from PyQt6.QtCore import QSettings, Qt
from PyQt6.QtWidgets import QSplitter, QVBoxLayout, QWidget

from pireal.dirs import DATA_SETTINGS
from pireal.gui.query_widget import QueryWidget
from pireal.gui.status_bar import StatusBar
from pireal.gui.table_widget import TableWidget
from pireal.registry import Registry


class RightPane(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        table_widget = Registry.get("table-widget", TableWidget)
        query_widget = Registry.get("query-widget", QueryWidget)
        status_bar = Registry.get("status-bar", StatusBar)

        self._vsplitter = QSplitter(Qt.Orientation.Vertical)
        self._vsplitter.addWidget(table_widget)
        self._vsplitter.addWidget(query_widget)

        layout.addWidget(self._vsplitter)
        layout.addWidget(status_bar)

    def showEvent(self, a0):
        super().showEvent(a0)
        qsettings = QSettings(str(DATA_SETTINGS), QSettings.Format.IniFormat)
        vsizes = qsettings.value("vsplitter_sizes", None)
        if vsizes is not None:
            self._vsplitter.restoreState(vsizes)
        else:
            h = self.height()
            self._vsplitter.setSizes([round(h * 0.6), round(h * 0.4)])

    def save_state(self) -> None:
        qsettings = QSettings(str(DATA_SETTINGS), QSettings.Format.IniFormat)
        qsettings.setValue("vsplitter_sizes", self._vsplitter.saveState())
