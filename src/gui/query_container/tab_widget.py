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

from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtWidgets import QMessageBox

from PyQt5.QtCore import pyqtSignal as Signal

from src import translations as tr


class TabWidget(QTabWidget):
    saveEditor = Signal()

    def __init__(self):
        super(TabWidget, self).__init__()
        self.setTabPosition(QTabWidget.South)
        self.setTabsClosable(True)
        self.setMovable(True)
        self.setDocumentMode(True)

        self.tabCloseRequested[int].connect(self.remove_tab)

    def remove_tab(self, index):
        editor = self.currentWidget().get_editor()
        if editor.modified:
            msgbox = QMessageBox(self)
            msgbox.setIcon(QMessageBox.Question)
            msgbox.setWindowTitle(tr.TR_MSG_FILE_MODIFIED)
            msgbox.setText(tr.TR_MSG_FILE_MODIFIED_BODY.format(editor.name))
            cancel_btn = msgbox.addButton(tr.TR_MSG_CANCEL, QMessageBox.RejectRole)
            msgbox.addButton(tr.TR_MSG_NO, QMessageBox.NoRole)
            yes_btn = msgbox.addButton(tr.TR_MSG_YES, QMessageBox.YesRole)
            msgbox.exec_()
            r = msgbox.clickedButton()
            if r == cancel_btn:
                return
            if r == yes_btn:
                self.saveEditor.emit(editor)

        super(TabWidget, self).removeTab(index)

    def tab_modified(self, widget, modified):
        editor_widget = widget.get_editor()
        if modified:
            text = "{} \u2022".format(editor_widget.name)
        else:
            text = editor_widget.name
        self.setTabText(self.currentIndex(), text)
        editor_widget.modified = modified

    def add_tab(self, widget, title):
        pass
