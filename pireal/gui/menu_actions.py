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
This module contains a dictionary, in turn this has a dictionary
with the name and a list of items with properties as an icon , shortcut,
slot for each item in a menu.

"""

from pireal import translations as tr


MENU = {}


# Menu File
MENU['file'] = {
    'name': tr.TR_MENU_FILE,
    'items': ('Database', {
        'name': tr.TR_MENU_FILE_NEW_DB,
        'slot': 'central:create_database'
    }, {
        'name': tr.TR_MENU_FILE_SAVE_DB,
        'slot': None
    }, {
        'name': tr.TR_MENU_FILE_SAVE_AS_DB,
        'slot': None
    }, {
        'name': tr.TR_MENU_FILE_CLOSE_DB,
        'slot': None
    }, 'Query', {
        'name': tr.TR_MENU_QUERY_NEW_QUERY,
        'slot': 'central:new_query'
    }, {
        'name': tr.TR_MENU_QUERY_SAVE_QUERY,
        'slot': None
    }, {
        'name': tr.TR_MENU_QUERY_SAVE_AS_QUERY,
        'slot': None
    }, {
        'name': tr.TR_MENU_FILE_CLOSE_QUERY,
        'slot': None
    }, '-', {
        'name': tr.TR_MENU_FILE_QUIT,
        'slot': 'pireal:close'
    })
}


# # Menu Edit
# MENU['edit'] = {
#     'name': translate("Pireal", "&Editar"),
#     'items': [{
#         'name': translate("Pireal", "Deshacer"),
#         'slot': "central:undo_action"
#     }, {
#         'name': translate("Pireal", "Rehacer"),
#         'slot': "central:redo_action"
#     }, "-", {
#         'name': translate("Pireal", "Cortar"),
#         'slot': "central:cut_action"
#     }, {
#         'name': translate("Pireal", "Copiar"),
#         'slot': "central:copy_action"
#     }, {
#         'name': translate("Pireal", "Pegar"),
#         'slot': "central:paste_action"
#     }, {
#         'name': translate("Pireal", "Comentar"),
#         'slot': "central:comment"
#     }, {
#         'name': translate("Pireal", "Descomentar"),
#         'slot': "central:uncomment"
#     }, "-", {
#         'name': translate("Pireal", "Buscar..."),
#         'slot': "central:search"
#     }]}
#     # }, "-", {
#     #     'name': translate("Pireal", "Preferencias"),
#     #     'slot': "central:show_settings"}]}


# Menu Relation
MENU['relation'] = {
    'name': tr.TR_MENU_RELATION,
    'items': ({
        'name': tr.TR_MENU_RELATION_NEW,
        'slot': "central:create_new_relation"
    }, {
        'name': tr.TR_MENU_RELATION_DELETE,
        'slot': "central:remove_relation"
    }, {
        'name': tr.TR_MENU_RELATION_LOAD,
        'slot': "central:load_relation"
    })}
# }, "-", {
#     'name': translate("Pireal", "Agregar Tupla"),
#     'slot': "central:add_tuple"
# }, {
#     'name': translate("Pireal", "Eliminar Tupla"),
#     'slot': "central:delete_tuple"

#     'name': translate("Pireal", "Agregar Columna"),
#     'slot': "central:add_column"
# }, {
#     'name': translate("Pireal", "Eliminar Columna"),
#     'slot': "central:delete_column"
# }, "-", {
#     'name': translate("Pireal", "Ejecutar Consultas"),
#     'slot': "central:execute_queries"}]}


MENU['tools'] = {
    'name': tr.TR_MENU_TOOLS,
    'items': [{
        'name': tr.TR_MENU_TOOLS_PREFERENCES,
        'slot': "central:show_settings",
    }, {
        'name': tr.TR_DARK_MODE,
        'checkable': True,
        'slot': 'pireal:switch_theme'
    }]
}

# # Menu Help
MENU['help'] = {
    'name': tr.TR_MENU_HELP,
    'items': [{
        'name': tr.TR_MENU_HELP_REPORT_ISSUE,
        'slot': "pireal:report_issue"
    }, "-", {
        'name': tr.TR_MENU_HELP_ABOUT,
        'slot': "pireal:about_pireal"
    }, {
        'name': tr.TR_MENU_HELP_ABOUT_QT,
        'slot': "pireal:about_qt"}]}
