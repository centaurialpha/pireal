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
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout
)
from PyQt5.QtQuick import QQuickView
from PyQt5.QtCore import QUrl


class StartPage(QWidget):

    def __init__(self):
        super(StartPage, self).__init__()
        vbox = QVBoxLayout(self)
        vbox.setContentsMargins(0, 0, 0, 0)
        view = QQuickView()
        qml = os.path.join(os.path.dirname(__file__), "StartPage.qml")
        view.setSource(QUrl.fromLocalFile(qml))
        view.setResizeMode(QQuickView.SizeRootObjectToView)
        widget = QWidget.createWindowContainer(view)
        vbox.addWidget(widget)
