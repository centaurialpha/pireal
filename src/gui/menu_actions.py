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
slot for each item in a menu.

"""

from collections import OrderedDict
from PyQt5.QtWidgets import QApplication

translate = QApplication.translate

MENU = OrderedDict()


# Menu File
MENU['file'] = {
    'name': translate("Pireal", "&File"),
    'items': [{
        'name': translate("Pireal", "New Database"),
        'slot': "central:create_database_wizard"
    }, {
        'name': translate("Pireal", "New Query"),
        'slot': "central:new_query"
    }, "-", {
        'name': translate("Pireal", "Open Database"),
        'slot': "central:open_database"
    }, {
        'name': translate("Pireal", "Save Database"),
        'slot': "central:save_database"
    #}, {
        #'name': translate.TR_MENU_FILE_SAVE,
        #'slot': "central:save_file"
    }, "-", {
        'name': translate("Pireal", "Close Database"),
        'slot': "central:close_database"
    #}, {
        #'name': translate.TR_MENU_FILE_SAVE_AS,
        #'slot': "container:save_query_as"
    #}, "-", {
        #'name': translate.TR_MENU_FILE_CONVERT_TO_PDB,
        #'slot': "container:convert_to_pdb"
    #}, "-", {
        #'name': None,
        #'slot': "main:open_recent_file"
    }, "-", {
        'name': translate("Pireal", "Exit"),
        'slot': "pireal:close"}]}


# Menu Edit
MENU['edit'] = {
    'name': translate("Pireal", "&Edit"),
    'items': [{
        'name': translate("Pireal", "Undo"),
        'slot': "central:undo_action"
    }, {
        'name': translate("Pireal", "Redo"),
        'slot': "central:redo_action"
    }, "-", {
        'name': translate("Pireal", "Cut"),
        'slot': "central:cut_action"
    }, {
        'name': translate("Pireal", "Copy"),
        'slot': "central:copy_action"
    }, {
        'name': translate("Pireal", "Paste"),
        'slot': "central:paste_action"
    }, "-", {
        'name': translate("Pireal", "Preferences"),
        'slot': "central:show_settings"}]}


# Menu Relation
MENU['relation'] = {
    'name': translate("Pireal", "&Relation"),
    'items': [{
        'name': translate("Pireal", "New Relation"),
        'slot': "central:create_new_relation"
    #}, {
        #'name': translate("Pireal", "Edit ",
        #'slot': "central:remove_relation"
    }, {
        'name': translate("Pireal", "Load Relation"),
        'slot': "central:load_relation"
    #}, "-", {
        #'name': translate.TR_MENU_RELATION_ADD_ROW,
        #'slot': "central:insert_tuple"
    #}, {
        #'name': translate.TR_MENU_RELATION_DELETE_ROW,
        #'slot': "central:remove_tuple"
    }, "-", {
        'name': translate("Pireal", "Execute Queries"),
        'slot': "central:execute_queries"}]}


# Menu Help
MENU['help'] = {
    'name': translate("Pireal", "&Help"),
    'items': [{
        'name': translate("Pireal", "About Pireal"),
        'slot': "pireal:about_pireal"
    }, {
        'name': translate("Pireal", "About Qt"),
        'slot': "pireal:about_qt"}]}
