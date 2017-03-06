# -*- coding: utf-8 -*-
#
# Copyright 2015-2017 - Gabriel Acosta <acostadariogabriel@gmail.com>
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
    QShortcut,
    QFileDialog
)
from PyQt5.QtGui import QKeySequence
from PyQt5.QtQuickWidgets import QQuickWidget
from PyQt5.QtCore import (
    Qt,
    QUrl,
    pyqtSlot,
    pyqtSignal
)
from src.core import settings


class NewDatabaseDialog(QDialog):

    create = pyqtSignal('QString', 'QString', 'QString')

    def __init__(self, parent=None):
        QDialog.__init__(self, parent, Qt.Dialog | Qt.FramelessWindowHint)
        self.setModal(True)
        self.setAttribute(Qt.WA_TranslucentBackground)
        box = QVBoxLayout(self)
        box.setContentsMargins(0, 0, 0, 0)
        view = QQuickWidget()
        view.setResizeMode(QQuickWidget.SizeRootObjectToView)
        qml = os.path.join(settings.QML_PATH, "NewDatabaseDialog.qml")
        view.setSource(QUrl.fromLocalFile(qml))
        box.addWidget(view)

        # Hide dialog with Escape
        short_escape = QShortcut(QKeySequence(Qt.Key_Escape), self)
        short_escape.activated.connect(self.hide)

        self.__root = view.rootObject()
        self.__location_folder = settings.PIREAL_DATABASES
        self.__root.setFolder(self.__location_folder)

        # Conexiones
        self.__root.close.connect(self.close)
        self.__root.databaseNameChanged['QString'].connect(
            self.__update_filename)
        self.__root.locationChanged.connect(
            self.__select_location)
        self.__root.create.connect(
            lambda db_name, location, filename: self.create.emit(
                db_name, location, filename))

    @pyqtSlot()
    def __select_location(self):
        location = QFileDialog.getExistingDirectory(self,
                                                    self.tr("Select Folder"))
        if not location:
            return
        self.__root.setFolder(location)
        self.__location_folder = os.path.join(self.__location_folder,
                                              location)
        self.__root.setFilename(
            os.path.join(location, self.__root.dbName()))

    @pyqtSlot('QString')
    def __update_filename(self, fname):
        new_fname = os.path.join(self.__location_folder, fname)
        self.__root.setFilename(new_fname)
