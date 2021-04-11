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

'''
This module contains an ordered dictionary, in turn this has a dictionary
with the name and a list of items with properties as an icon , shortcut,
slot for each item in a menu.

'''
from collections import namedtuple

from pireal import translations as tr

Action = namedtuple(
    'Action',
    ['name', 'slot', 'is_checkable'],
    defaults=(False,)
)

m_file = {
    'name': tr.TR_MENU_FILE,
    'actions': (
        'Database',
        Action(tr.TR_MENU_FILE_NEW_DB, 'central:create_database'),
        Action(tr.TR_MENU_FILE_OPEN_DB, 'central:open_database'),
        Action(tr.TR_MENU_FILE_SAVE_DB, 'central:save_database'),
        Action(tr.TR_MENU_FILE_SAVE_AS_DB, 'central:save_database_as'),
        Action(tr.TR_MENU_FILE_CLOSE_DB, 'central:close_database'),
        'Query',
        Action(tr.TR_MENU_FILE_NEW_QUERY, 'central:new_query'),
        Action(tr.TR_MENU_FILE_OPEN_QUERY, 'central:open_query'),
        Action(tr.TR_MENU_FILE_SAVE_QUERY, 'central:save_query'),
        Action(tr.TR_MENU_FILE_SAVE_AS_QUERY, 'central:save_query_as'),
        Action(tr.TR_MENU_FILE_CLOSE_QUERY, 'central:close_query'),
        {},  # This is a separator
        Action(tr.TR_MENU_FILE_QUIT, 'pireal:close')
    )
}

m_schema = {
    'name': tr.TR_MENU_SCHEME,
    'actions': (
        Action(tr.TR_MENU_SCHEME_CREATE_RELATION, 'central:create_relation'),
        # Action(tr.TR_MENU_SCHEME_LOAD_RELATION, 'central:load_relation'),
        Action(tr.TR_MENU_SCHEME_REMOVE_RELATION, 'central:remove_relation'),
        {},
        Action(tr.TR_MENU_SCHEME_EXECUTE_QUERIES, 'central:execute_query')
    )
}

m_tools = {
    'name': tr.TR_MENU_TOOLS,
    'actions': (
        Action(tr.TR_MENU_TOOLS_SETTINGS, 'central:show_settings'),
    )
}

m_help = {
    'name': tr.TR_MENU_HELP,
    'actions': (
        Action(tr.TR_MENU_HELP_REPORT_ISSUE, 'pireal:report_issue'),
        {},
        Action(tr.TR_MENU_HELP_ABOUT_PIREAL, 'pireal:about_pireal'),
        Action(tr.TR_MENU_HELP_ABOUT_QT, 'pireal:about_qt')
    )
}

MENU = (
    m_file,
    m_schema,
    m_tools,
    m_help
)
