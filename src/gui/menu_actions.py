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
from PyQt4.QtGui import QApplication

translate = QApplication.translate


MENU = OrderedDict()


# Menu File
MENU['file'] = {
    'name': translate("PIREAL", "&Archivo"),
    'items': [{
        'name': translate("PIREAL", "Nueva Base de Datos"),
        'slot': "actions:create_data_base"
    }, {
        'name': "Nueva Consulta",
        'slot': "actions:new_query"
    }, "-", {
        'name': "Abrir",
        'slot': "actions:open_file"
    }, {
        'name': "Guardar",
        'slot': "actions:save_file"
    }, {
        'name': "Guardar como...",
        'slot': "actions:save_file_as"
    }, "-", {
        'name': "Salir",
        'slot': "pireal:close"}]}


# Menu Edit
MENU['edit'] = {
    'name': "&Editar",
    'items': [{
        'name': "Deshacer",
        'slot': "actions:undo_action"
    }, {
        'name': "Rehacer",
        'slot': "actions:redo_action"
    }, {
        'name': "Cortar",
        'slot': "actions:cut_action"
    }, {
        'name': "Copiar",
        'slot': "actions:copy_action"
    }, {
        'name': "Pegar",
        'slot': "actions:paste_action"}]}


# Menu Relation
MENU['relation'] = {
    'name': "&Relación",
    'items': [{
        'name': "Nueva Relación",
        'slot': "actions:create_new_relation"
    }, {
        'name': "Eliminar Relación",
        'slot': "actions:remove_relation"
    }, "-", {
        'name': "Agregar Registro",
        'slot': "actions:insert_tuple"
    }, {
        'name': "Eliminar Registro",
        'slot': "actions:remove_tuple"}]}


# Menu Help
MENU['help'] = {
    'name': "A&yuda",
    'items': [{
        'name': "Acerca de Pireal",
        'slot': "pireal:about_pireal"
    }, {
        'name': "Acerca de Qt",
        'slot': "pireal:about_qt"}]}
