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
# from PyQt5.QtWidgets import QApplication

from src import translations as tr

MENU = OrderedDict()


# Menu File
MENU['database'] = {
    'name': tr.TR_MENU_DB,
    'items': ({
        'name': tr.TR_MENU_FILE_NEW_DB,
        'slot': "central:create_database"
    }, {
        'name': tr.TR_MENU_FILE_OPEN_DB,
        'slot': "central:open_database"
    }, {
        'name': tr.TR_MENU_FILE_SAVE_DB,
        'slot': "central:save_database"
    }, {
        'name': tr.TR_MENU_FILE_SAVE_AS_DB,
        'slot': "central:save_database_as"
    }, {
        'name': tr.TR_MENU_FILE_CLOSE_DB,
        'slot': "central:close_database"
    })
}

MENU['query'] = {
    'name': tr.TR_MENU_QUERY,
    'items': ({
        'name': tr.TR_MENU_QUERY_NEW_QUERY,
        'slot': "central:new_query"
    }, {
        'name': tr.TR_MENU_QUERY_OPEN_QUERY,
        'slot': None,
    }, {
        'name': tr.TR_MENU_QUERY_SAVE_QUERY,
        'slot': None,
    }, {
        'name': tr.TR_MENU_QUERY_SAVE_AS_QUERY,
        'slot': None,
    }, {
        'name': tr.TR_MENU_QUERY_EXECUTE,
        'slot': None
    })
}
# MENU['file'] = {
#     'name': tr.TR_MENU_FILE,
#     'items': [{
#         'name': tr.TR_MENU_FILE_NEW_DB,
#         'slot': "central:create_database"
#     }, {
#         'name': tr.TR_MENU_FILE_OPEN_DB,
#         'slot': "central:open_database"
#     }, {
#         'name': tr.TR_MENU_FILE_SAVE_DB,
#         'slot': "central:save_database"
#     }, {
#         'name': tr.TR_MENU_FILE_SAVE_AS_DB,
#         'slot': "central:save_database_as"
#     }, {
#         'name': tr.TR_MENU_FILE_CLOSE_DB,
#         'slot': "central:close_database"
#     }, "-", {
#         'name': translate("Pireal", "Nueva Consulta"),
#         'slot': "central:new_query"
#     }, {
#         'name': translate("Pireal", "Abrir Consulta"),
#         'slot': "central:open_query"
#     }, {
#         'name': translate("Pireal", "Guardar Consulta"),
#         'slot': "central:save_query"
#     }, "-", {
#         'name': translate("Pireal", "Salir"),
#         'slot': "pireal:close"}]}


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
#         'name': translate("Pireal", "Acercar"),
#         'slot': "central:zoom_in"
#     }, {
#         'name': translate("Pireal", "Alejar"),
#         'slot': "central:zoom_out"
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
