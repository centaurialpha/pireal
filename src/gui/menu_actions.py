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
This module contains an ordered dictionary, in turn this has a dictionary
with the name and a list of items with properties as an icon , shortcut,
slot for each item in a menu, by default, strings they are in Spanish.

"""

from collections import OrderedDict
from src import translations as tr


MENU = OrderedDict()


# Menu File
MENU['file'] = {
    'name': tr.TR_MENU_FILE,
    'items': [{
        'name': tr.TR_MENU_FILE_NEW_DB,
        'slot': "container:create_data_base"
    }, {
        'name': tr.TR_MENU_FILE_NEW_QUERY,
        'slot': "container:new_query"
    }, "-", {
        'name': tr.TR_MENU_FILE_OPEN,
        'slot': "container:open_file"
    }, {
        'name': tr.TR_MENU_FILE_SAVE_DB,
        'slot': "container:save_data_base"
    }, {
        'name': tr.TR_MENU_FILE_SAVE,
        'slot': "container:save_query"
    }, {
        'name': tr.TR_MENU_FILE_SAVE_AS,
        'slot': "container:save_query_as"
    }, "-", {
        'name': None,
        'slot': "container:open_recent_file"
    }, "-", {
        'name': tr.TR_MENU_FILE_EXIT,
        'slot': "pireal:close"}]}


# Menu Edit
MENU['edit'] = {
    'name': tr.TR_MENU_EDIT,
    'items': [{
        'name': tr.TR_MENU_EDIT_UNDO,
        'slot': "container:undo_action"
    }, {
        'name': tr.TR_MENU_EDIT_REDO,
        'slot': "container:redo_action"
    }, "-", {
        'name': tr.TR_MENU_EDIT_CUT,
        'slot': "container:cut_action"
    }, {
        'name': tr.TR_MENU_EDIT_COPY,
        'slot': "container:copy_action"
    }, {
        'name': tr.TR_MENU_EDIT_PASTE,
        'slot': "container:paste_action"
    }, "-", {
        'name': tr.TR_MENU_EDIT_PREFERENCES,
        'slot': 'pireal:show_preferences'}]}


# Menu Relation
MENU['relation'] = {
    'name': tr.TR_MENU_RELATION,
    'items': [{
        'name': tr.TR_MENU_RELATION_NEW_RELATION,
        'slot': "container:create_new_relation"
    }, {
        'name': tr.TR_MENU_RELATION_DELETE_RELATION,
        'slot': "container:remove_relation"
    }, {
        'name': tr.TR_MENU_RELATION_LOAD_RELATION,
        'slot': "container:load_relation"
    }, "-", {
        'name': tr.TR_MENU_RELATION_ADD_ROW,
        'slot': "container:insert_tuple"
    }, {
        'name': tr.TR_MENU_RELATION_DELETE_ROW,
        'slot': "container:remove_tuple",
    }, "-", {
        'name': tr.TR_MENU_RELATION_EXECUTE,
        'slot': "container:execute_queries"}]}


# Menu Help
MENU['help'] = {
    'name': tr.TR_MENU_HELP,
    'items': [{
        'name': tr.TR_MENU_HELP_ABOUT_PIREAL,
        'slot': "pireal:about_pireal"
    }, {
        'name': tr.TR_MENU_HELP_ABOUT_QT,
        'slot': "pireal:about_qt"}]}
