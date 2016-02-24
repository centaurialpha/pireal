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
    QWizard,
    QWizardPage,
    QGridLayout,
    QLineEdit,
    QLabel,
    QToolButton,
    QFileDialog
)
from PyQt5.QtCore import pyqtSignal

from src.core import settings


class DatabaseWizard(QWizard):
    wizardFinished = pyqtSignal('PyQt_PyObject')

    def __init__(self, parent=None):
        super(DatabaseWizard, self).__init__(parent)
        self._intro_page = IntroPage()
        self.addPage(self._intro_page)

    def done(self, result):
        data = {}
        if result:
            data = self._intro_page.get_data()
        self.wizardFinished.emit(data)
        QWizard.done(self, result)


class IntroPage(QWizardPage):

    def __init__(self):
        super(IntroPage, self).__init__()
        self.setTitle(self.tr("New Database"))
        self.setSubTitle(self.tr("Name and Location"))
        grid = QGridLayout(self)
        grid.addWidget(QLabel(self.tr("Database Name: ")), 0, 0)
        self._line_dbname = QLineEdit()
        self._line_dbname.textChanged.connect(self.__on_dbname_changed)
        grid.addWidget(self._line_dbname, 0, 1)
        grid.addWidget(QLabel(self.tr("Database Location: ")), 1, 0)
        self._line_dblocation = LineEdit()
        self._line_dblocation.button.clicked.connect(self.__select_location)
        grid.addWidget(self._line_dblocation, 1, 1)
        grid.addWidget(QLabel(self.tr("Database Folder: ")), 2, 0)
        self._dbfolder = settings.PIREAL_PROJECTS
        self._line_dbfolder = QLineEdit()
        self._line_dbfolder.setText(self._dbfolder)
        grid.addWidget(self._line_dbfolder, 2, 1)
        self._line_dbname.setText("pireal_database.pdb")
        self._line_dbname.setSelection(0, 15)

    def __select_location(self):
        location = QFileDialog.getExistingDirectory(self,
                                                    self.tr("Select Folder"))
        if not location:
            return
        self._line_dblocation.setText(location)
        self._dbfolder = os.path.join(self._dbfolder, location)
        self._line_dbfolder.setText(
            os.path.join(location, self._line_dbname.text()))

    def __on_dbname_changed(self, db_name):
        self._line_dbfolder.setText(os.path.join(self._dbfolder, db_name))

    def get_data(self):
        data = {
            'name': self._line_dbname.text(),
            'location': self._line_dblocation.text(),
            'folder': self._line_dbfolder.text(),
            'filename': os.path.join(self._line_dbfolder.text(),
                                     self._line_dbname.text())
        }

        return data


class LineEdit(QLineEdit):

    def __init__(self):
        super(LineEdit, self).__init__()
        self.setReadOnly(True)
        self.setText(settings.PIREAL_PROJECTS)
        self.button = QToolButton(self)
        self.button.setText('...')

    def resizeEvent(self, event):
        QLineEdit.resizeEvent(self, event)
        self.button.setFixedWidth(40)
        self.button.move(self.width() - self.button.width(), 0)
        self.button.setFixedHeight(self.height())