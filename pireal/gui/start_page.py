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

from PyQt5.QtQuickWidgets import QQuickWidget

from PyQt5.QtCore import QUrl
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import QAbstractListModel
from PyQt5.QtCore import QModelIndex
from PyQt5.QtCore import Qt

from pireal.core import settings
from pireal.core.file_manager import get_basename


class RecentDBListModel(QAbstractListModel):
    NameRole = Qt.UserRole + 1
    PathRole = NameRole + 1

    def __init__(self):
        super().__init__()
        self._data = []

    def clear(self):
        self.beginResetModel()
        self._data.clear()
        self.endResetModel()

    def remove(self, index):
        self.beginRemoveRows(QModelIndex(), index, index)
        self._data.pop(index)
        self.endRemoveRows()

    def add_item(self, name, path):
        self.beginInsertRows(QModelIndex(), len(self._data), len(self._data))
        self._data.append((name, path))
        self.endInsertRows()

    def rowCount(self, index):
        return len(self._data)

    def data(self, index, role=Qt.DisplayRole):
        try:
            item = self._data[index.row()]
        except IndexError:
            return None
        if role == self.NameRole:
            return item[0]
        elif role == self.PathRole:
            return item[1]
        return None

    def roleNames(self):
        return {
            self.NameRole: b'displayName',
            self.PathRole: b'path'
        }


class StartPage(QWidget):
    """Lógical para la UI QML de la página principal"""

    def __init__(self, parent=None):
        super(StartPage, self).__init__(parent)
        self._central = parent
        self._model = RecentDBListModel()

        vbox = QVBoxLayout(self)
        vbox.setContentsMargins(0, 0, 0, 0)
        self._view = QQuickWidget()
        self._view.rootContext().setContextProperty('listModel', self._model)
        self._set_source()
        self._view.setResizeMode(QQuickWidget.SizeRootObjectToView)
        vbox.addWidget(self._view)

        self._root = self._view.rootObject()
        self._connect_signals()

    def _connect_signals(self):
        self._root.newDatabase.connect(self._central.create_database)
        self._root.openDatabase.connect(self._central.open_database)
        self._root.openExample.connect(self._open_example)
        self._root.openRecentDatabase.connect(lambda path: self._central.open_database(path))
        self._root.removeItem[int].connect(self._model.remove)
        self._central.pireal.themeChanged.connect(self._reload)

    def _set_source(self):
        qml = os.path.join(settings.QML_PATH, "StartPage.qml")
        self._view.setSource(QUrl.fromLocalFile(qml))

    def _reload(self):
        self._view.rootObject().deleteLater()
        self._view.setSource(QUrl())
        self._set_source()
        self._root = self._view.rootObject()
        self._model.clear()
        self.load_items()
        self._connect_signals()

    def _open_example(self):
        db_filename = os.path.abspath(os.path.join(settings.EXAMPLES, 'database.pdb'))
        self._central.open_database(filename=db_filename)
        query_filename = os.path.abspath(os.path.join(settings.EXAMPLES, 'queries.pqf'))
        self._central.open_query(filename=query_filename)
        # Ejecuto las consultas de ejemplo luego de 1.3 segundos
        QTimer.singleShot(1300, self._central.execute_query)

    def _remove_current(self, path):
        self._central.recent_databases.remove(path)

    def load_items(self):
        for path in self._central.recent_databases:
            name = get_basename(path)
            self._model.add_item(name, path)

    def showEvent(self, event):
        """ Load list view every time the start page is displayed """

        super(StartPage, self).showEvent(event)
        self.load_items()
