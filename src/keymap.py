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
KEYMAP is a dictionary, the keys are the names of the
slots of the QAction's, and values are the key sequence.
"""

from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import Qt


KEYMAP = {
    'create_database': QKeySequence(Qt.CTRL + Qt.Key_N),
    'open_database': QKeySequence(Qt.CTRL + Qt.Key_O),
    'save_database': QKeySequence(Qt.CTRL + Qt.Key_S),
    'close_database': QKeySequence(Qt.CTRL + Qt.Key_W),
    'new_query': QKeySequence(Qt.CTRL + Qt.SHIFT + Qt.Key_N),
    'open_query': QKeySequence(Qt.CTRL + Qt.SHIFT + Qt.Key_O),
    'save_query': QKeySequence(Qt.CTRL + Qt.SHIFT + Qt.Key_S),
    'close': QKeySequence(Qt.CTRL + Qt.Key_Q),
    'undo_action': QKeySequence(Qt.CTRL + Qt.Key_Z),
    'redo_action': QKeySequence(Qt.CTRL + Qt.Key_Y),
    'cut_action': QKeySequence(Qt.CTRL + Qt.Key_X),
    'copy_action': QKeySequence(Qt.CTRL + Qt.Key_C),
    'paste_action': QKeySequence(Qt.CTRL + Qt.Key_V),
    'zoom_in': QKeySequence(Qt.CTRL + Qt.Key_Plus),
    'zoom_out': QKeySequence(Qt.CTRL + Qt.Key_Minus),
    'comment': QKeySequence(Qt.CTRL + Qt.Key_D),
    'uncomment': QKeySequence(Qt.CTRL + Qt.SHIFT + Qt.Key_D),
    'show_settings': QKeySequence(Qt.CTRL + Qt.Key_P),
    'search': QKeySequence(Qt.CTRL + Qt.Key_F),
    'create_new_relation': QKeySequence(Qt.CTRL + Qt.ALT + Qt.Key_N),
    'remove_relation': QKeySequence(Qt.CTRL + Qt.ALT + Qt.Key_W),
    'load_relation': QKeySequence(Qt.CTRL + Qt.ALT + Qt.Key_O),
    'execute_queries': QKeySequence(Qt.CTRL + Qt.Key_R),
    'execute_selection': QKeySequence(Qt.CTRL + Qt.Key_F6)
}
