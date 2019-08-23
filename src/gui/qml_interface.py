# -*- coding: utf-8 -*-
#
# Copyright 2015-2019 - Gabriel Acosta <acostadariogabriel@gmail.com>
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

import abc

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout

from PyQt5.QtQuickWidgets import QQuickWidget

from src.core import file_manager


class QMLInterface(QWidget):
    """Componente que se encarga de cargar una interfáz QML"""

    source = None

    def __init__(self, parent=None):
        super().__init__(parent)
        box = QVBoxLayout(self)
        box.setContentsMargins(0, 0, 0, 0)

        view = QQuickWidget()
        view.setSource(file_manager.get_qml_resource(self.source))
        view.setResizeMode(QQuickWidget.SizeRootObjectToView)

        box.addWidget(view)

        self._root = view.rootObject()

        self.initialize()

    @abc.abstractmethod
    def initialize(self):
        pass

    @property
    def root(self):
        return self._root
