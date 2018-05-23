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
    'name': translate("Pireal", "&Archivo"),
    'items': [{
        'name': translate("Pireal", "Nueva Base de Datos"),
        'slot': "central:create_database"
    }, {
        'name': translate("Pireal", "Abrir Base de Datos"),
        'slot': "central:open_database"
    }, {
        'name': translate("Pireal", "Guardar Base de Datos"),
        'slot': "central:save_database"
    }, {
        'name': translate("Pireal", "Guardar Base de Datos como..."),
        'slot': "central:save_database_as"
    }, {
        'name': translate("Pireal", "Cerrar Base de Datos"),
        'slot': "central:close_database"
    }, "-", {
        'name': translate("Pireal", "Nueva Consulta"),
        'slot': "central:new_query"
    }, {
        'name': translate("Pireal", "Abrir Consulta"),
        'slot': "central:open_query"
    }, {
        'name': translate("Pireal", "Guardar Consulta"),
        'slot': "central:save_query"
    }, "-", {
        'name': translate("Pireal", "Salir"),
        'slot': "pireal:close"}]}


# Menu Edit
MENU['edit'] = {
    'name': translate("Pireal", "&Editar"),
    'items': [{
        'name': translate("Pireal", "Deshacer"),
        'slot': "central:undo_action"
    }, {
        'name': translate("Pireal", "Rehacer"),
        'slot': "central:redo_action"
    }, "-", {
        'name': translate("Pireal", "Cortar"),
        'slot': "central:cut_action"
    }, {
        'name': translate("Pireal", "Copiar"),
        'slot': "central:copy_action"
    }, {
        'name': translate("Pireal", "Pegar"),
        'slot': "central:paste_action"
    }, {
        'name': translate("Pireal", "Comentar"),
        'slot': "central:comment"
    }, {
        'name': translate("Pireal", "Descomentar"),
        'slot': "central:uncomment"
    }, "-", {
        'name': translate("Pireal", "Acercar"),
        'slot': "central:zoom_in"
    }, {
        'name': translate("Pireal", "Alejar"),
        'slot': "central:zoom_out"
    }, "-", {
        'name': translate("Pireal", "Buscar..."),
        'slot': "central:search"
    }]}
    # }, "-", {
    #     'name': translate("Pireal", "Preferencias"),
    #     'slot': "central:show_settings"}]}


# Menu Relation
MENU['relation'] = {
    'name': translate("Pireal", "&Relación"),
    'items': [{
        'name': translate("Pireal", "Nueva Relación"),
        'slot': "central:create_new_relation"
    }, {
        'name': translate("Pireal", "Eliminar Relación"),
        'slot': "central:remove_relation"
    }, {
        'name': translate("Pireal", "Cargar Relación"),
        'slot': "central:load_relation"
    }, "-", {
        'name': translate("Pireal", "Agregar Tupla"),
        'slot': "central:add_tuple"
    }, {
        'name': translate("Pireal", "Eliminar Tupla"),
        'slot': "central:delete_tuple"

    #     'name': translate("Pireal", "Agregar Columna"),
    #     'slot': "central:add_column"
    # }, {
    #     'name': translate("Pireal", "Eliminar Columna"),
    #     'slot': "central:delete_column"
    }, "-", {
        'name': translate("Pireal", "Ejecutar Consultas"),
        'slot': "central:execute_queries"}]}


# Menu Help
MENU['help'] = {
    'name': translate("Pireal", "A&yuda"),
    'items': [{
        'name': translate("Pireal", "Reportar problema..."),
        'slot': "pireal:report_issue"
    # }, "-", {
        # 'name': translate("Pireal", "RDB a PDB"),
        # 'slot': "central:rdb_to_pdb"
    }, "-", {
        'name': translate("Pireal", "Acerca de Pireal"),
        'slot': "pireal:about_pireal"
    }, {
        'name': translate("Pireal", "Acerca de Qt"),
        'slot': "pireal:about_qt"}]}
