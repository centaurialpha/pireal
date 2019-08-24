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
from src.gui.main_window import Pireal
from src.core import settings

from src.core.settings import CONFIG


class StartPage(QWidget):
    """Lógical para la UI QML de la página principal"""

    def __init__(self):
        super(StartPage, self).__init__()
        vbox = QVBoxLayout(self)
        vbox.setContentsMargins(0, 0, 0, 0)
        view = QQuickView()
        qml = os.path.join(settings.QML_PATH, "StartPage.qml")
        view.setSource(QUrl.fromLocalFile(qml))
        view.setResizeMode(QQuickView.SizeRootObjectToView)
        widget = QWidget.createWindowContainer(view)
        vbox.addWidget(widget)

        self.__root = view.rootObject()

        # Connections
        self.__root.openRecentDatabase.connect(self.__open_database)
        self.__root.openPreferences.connect(self.__open_preferences)
        self.__root.openExample.connect(self.__open_example)
        self.__root.openDatabase.connect(self.__open_database)
        self.__root.newDatabase.connect(self.__new_database)
        self.__root.removeCurrent.connect(self.__remove_current)

    def __open_example(self):
        central_widget = Pireal.get_service("central")
        db_filename = os.path.join(settings.EXAMPLES, 'database.pdb')
        central_widget.open_database(filename=db_filename, remember=False)
        query_filename = os.path.join(settings.EXAMPLES, 'queries.pqf')
        central_widget.open_query(filename=query_filename, remember=False)
        # Ejecuto las consultas de ejemplo luego de 1.3 segundos
        QTimer.singleShot(1300, central_widget.execute_queries)

    def __open_preferences(self):
        central_widget = Pireal.get_service("central")
        central_widget.show_settings()

    def __remove_current(self, path):
        central_widget = Pireal.get_service("central")
        central_widget.recent_databases.remove(path)

    def __open_database(self, path=''):
        central_widget = Pireal.get_service("central")
        central_widget.open_database(path)

    def __new_database(self):
        central_widget = Pireal.get_service("central")
        central_widget.create_database()

    def load_items(self):
        self.__root.clear()
        if CONFIG.get("recentFiles"):
            for file_ in CONFIG.get("recentFiles"):
                name = os.path.splitext(os.path.basename(file_))[0]
                self.__root.loadItem(name, file_)

    def showEvent(self, event):
        """ Load list view every time the start page is displayed """

        super(StartPage, self).showEvent(event)
        self.load_items()
