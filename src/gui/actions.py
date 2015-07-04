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

import getpass
from PyQt4.QtGui import (
    QInputDialog
)
from PyQt4.QtCore import QObject
from src.gui.main_window import Pireal


class Actions(QObject):

    def __init__(self):
        super(Actions, self).__init__()
        Pireal.load_service("actions", self)

    def create_data_base(self):
        mdi = Pireal.get_service("mdi")
        db_name, ok = QInputDialog.getText(mdi, self.tr("New DB"),
                                           self.tr("Name:"),
                                           text=getpass.getuser())
        if ok:
            from src.gui import table_widget
            db_widget = table_widget.MdiDB()
            db_widget.setWindowTitle(db_name + '.pdb')
            db_widget.setMinimumSize(mdi.width(), mdi.height() / 1.7)
            mdi.addSubWindow(db_widget)
            # Enable QAction's
            pireal = Pireal.get_service("pireal")
            pireal.enable_disable_db_actions()
            db_widget.show()


actions = Actions()
