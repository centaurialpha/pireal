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

from PyQt6.QtGui import QKeySequence

KEYMAP = {
    "create_database": QKeySequence("Ctrl + n"),
    "open_database": QKeySequence("Ctrl + o"),
    "save_database": QKeySequence("Ctrl + s"),
    "close_database": QKeySequence("Ctrl + w"),
    "new_query": QKeySequence("Ctrl + Shift + n"),
    "open_query": QKeySequence(""),
    "save_query": QKeySequence(""),
    "close": QKeySequence(""),
    "undo_action": QKeySequence(""),
    "redo_action": QKeySequence(""),
    "cut_action": QKeySequence(""),
    "copy_action": QKeySequence(""),
    "paste_action": QKeySequence(""),
    "zoom_in": QKeySequence(""),
    "zoom_out": QKeySequence(""),
    "comment": QKeySequence(""),
    "uncomment": QKeySequence(""),
    "show_settings": QKeySequence(""),
    "search": QKeySequence(""),
    "create_new_relation": QKeySequence(""),
    "remove_relation": QKeySequence(""),
    "load_relation": QKeySequence(""),
    "execute_queries": QKeySequence(""),
    "execute_selection": QKeySequence(""),
}
