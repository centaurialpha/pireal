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

"""
QML interface
"""

import os

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout

from PyQt5.QtQuick import QQuickView
from PyQt5.QtCore import QUrl
from PyQt5.QtCore import QTimer
# from pireal.gui.main_window import Pireal
from pireal.core import settings

# from pireal.core.settings import CONFIG


class StartPage(QWidget):
    """Lógical para la UI QML de la página principal"""

    def __init__(self, parent=None):
        super(StartPage, self).__init__(parent)
        self._central = parent
        vbox = QVBoxLayout(self)
        vbox.setContentsMargins(0, 0, 0, 0)
        view = QQuickView()
        qml = os.path.join(settings.QML_PATH, "StartPage.qml")
        view.setSource(QUrl.fromLocalFile(qml))
        view.setResizeMode(QQuickView.SizeRootObjectToView)
        widget = QWidget.createWindowContainer(view)
        vbox.addWidget(widget)

        self._root = view.rootObject()

        # Connections
        self._root.openRecentDatabase.connect(lambda: self._central.open_database(path))
        # self._root.openPreferences.connect(self._open_preferences)
        self._root.openExample.connect(self._open_example)
        # self._root.openDatabase.connect(lambda path: self._central.open_database(path))
        self._root.newDatabase.connect(self._central.create_database)
        # self._root.removeCurrent.connect(self._remove_current)

    def _open_example(self):
        db_filename = os.path.join(settings.EXAMPLES, 'database.pdb')
        self._central.open_database(filename=db_filename)
        query_filename = os.path.join(settings.EXAMPLES, 'queries.pqf')
        self._central.open_query(filename=query_filename)
        # Ejecuto las consultas de ejemplo luego de 1.3 segundos
        QTimer.singleShot(1300, self._central.execute_queries)

    def _open_preferences(self):
        self._central.show_settings()

    def _remove_current(self, path):
        self._central.recent_databases.remove(path)

    def _open_database(self, path=''):
        self._central.open_database(path)

    def load_items(self):
        self._root.clear()
        # if CONFIG.get("recentFiles"):
        #     for file_ in CONFIG.get("recentFiles"):
        #         name = os.path.splitext(os.path.basename(file_))[0]
        #         self._root.loadItem(name, file_)

    def showEvent(self, event):
        """ Load list view every time the start page is displayed """

        super(StartPage, self).showEvent(event)
        self.load_items()