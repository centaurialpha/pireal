# -*- coding: utf-8 -*-
#
# Copyright 2015-2019 - Gabriel Acosta <acostadariogabriel@gmail.com>
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

from PyQt5.QtCore import QCoreApplication

tr = QCoreApplication.translate

# Menu
TR_MENU_DB = tr('Pireal', '&Database')
TR_MENU_QUERY = tr('Preail', '&Query')
# TR_MENU_EDIT = tr('Pireal', '&Edit')
TR_MENU_RELATION = tr('Pireal', '&Relation')
TR_MENU_TOOLS = tr('Pireal', '&Tools')
TR_MENU_HELP = tr('Pireal', '&Help')
# Menu Database
TR_MENU_FILE_NEW_DB = tr('Pireal', 'New...')
TR_MENU_FILE_OPEN_DB = tr('Pireal', 'Open...')
TR_MENU_FILE_SAVE_DB = tr('Pireal', 'Save...')
TR_MENU_FILE_SAVE_AS_DB = tr('Pireal', 'Save As...')
TR_MENU_FILE_CLOSE_DB = tr('Pireal', 'Close')
# Menu Query
TR_MENU_QUERY_NEW_QUERY = tr('Pireal', 'New...')
TR_MENU_QUERY_OPEN_QUERY = tr('Pireal', 'Open...')
TR_MENU_QUERY_SAVE_QUERY = tr('Pireal', 'Save...')
TR_MENU_QUERY_SAVE_AS_QUERY = tr('Pireal', 'Save As...')
TR_MENU_QUERY_EXECUTE = tr('Pireal', 'Execute')
# Menu Relation
TR_MENU_RELATION_NEW = tr('Pireal', 'New...')
TR_MENU_RELATION_DELETE = tr('Pireal', 'Delete')
TR_MENU_RELATION_LOAD = tr('Pireal', 'Load')
# Menu Tools
TR_MENU_TOOLS_PREFERENCES = tr('Pireal', 'Preferences')
# Menu Help
TR_MENU_HELP_HELP = tr('Pireal', 'Help')
TR_MENU_HELP_REPORT_ISSUE = tr('Pireal', 'Report Issue')
TR_MENU_HELP_ABOUT = tr('Pireal', 'About Pireal')
TR_MENU_HELP_ABOUT_QT = tr('Pireal', 'About Qt')

TR_MSG_INFORMATION = tr('Pireal', 'Information')
TR_MSG_ONE_DB_AT_TIME = tr('Pireal', 'Oops! One database at a time please')

TR_OPEN_DATABASE = tr('Pireal', 'Open Database')
TR_MSG_DB_NOT_OPENED = tr('Pireal', 'The database file could not be opened')

TR_MSG_ERROR = tr('Pireal', 'Error')
TR_MSG_CANCEL = tr('Pireal', 'Cancel')
TR_MSG_NO = tr('Pireal', 'No')
TR_MSG_YES = tr('Pireal', 'Yes')
TR_MSG_CONFIRMATION = tr('Pireal', 'Confirmation')
TR_MSG_OK = tr('Pireal', 'Ok')

TR_OPEN_QUERY = tr('Pireal', 'Open Query')

TR_MSG_SAVE_CHANGES = tr('Pireal', 'Save changes?')
TR_MSG_SAVE_CHANGES_BODY = tr(
    'Pireal',
    'The database has been modified. Do you want to save the changes?')

TR_MSG_FILE_MODIFIED = tr('Pireal', 'File modified')
TR_MSG_FILE_MODIFIED_BODY = tr(
    'Pireal',
    'The file <b>{}</b> has unsaved changes. Do you want to keep them?')

TR_NOTIFICATION_DB_SAVED = tr('Pireal', 'The database has been saved: {}')
TR_NOTIFICATION_DB_CONNECTED = tr('Pireal', 'Connected to: {}')

TR_MSG_SAVE_DB_AS = tr('Pireal', 'Save Database As...')

TR_MSG_REMOVE_TUPLES = tr('Pireal', 'Delete tuple/s?')
TR_MSG_REMOVE_TUPLES_BODY = tr('Pireal', 'Are you sure you want to delete the selected tuples?')

TR_MSG_REMOVE_RELATION = tr('Pireal', 'Are you sure you want to delete the relation <b>{}</b>?')

TR_MSG_FILE_NOT_OPENED = tr('Pireal', 'The file could not be opened')

TR_MSG_SAVE_QUERY_FILE = tr('Pieal', 'Save Query File')

# DIALOGS
TR_DIALOG_ABOUT_PIREAL_TITLE = tr('Pireal', 'About Pireal')
TR_DIALOG_ABOUT_PIREAL_BODY = tr('Pireal', 'Relational Algebra Query Evaluator')
TR_DIALOG_ABOUT_PIREAL_COPY = tr(
    'Pireal',
    "<br>This Software is distributed under <a href='{}'><span style='color: #3465a4'>"
    "GNU GPL</span></a> 3.<br> The source code is available in"
    " <a href='{}'><span style='color: #3465a4'>GitHub.</span></a>"
)

TR_HEADER_NOT_EMPTY = tr('Pireal', 'The field must not be empty')

# Table Widget
TR_TABLE_WORKSPACE = tr('Pireal', 'Workspace')
TR_TABLE_RESULTS = tr('Pireal', 'Results')
TR_TABLE_CLICK_TO_SPLIT = tr('Pireal', 'Click to split window')
TR_TABLE_CLICK_TO_JOIN = tr('Pireal', 'Click to join window')
TR_TABLE_ADD_TUPLE = tr('Pireal', 'Add Tuple')
TR_TABLE_ADD_COL = tr('Pireal', 'Add Column')
TR_TABLE_CREATE_RELATION = tr('Pireal', 'Create new Relation')

# Query Container
TR_UNDOCK = tr('Pireal', 'Undock')
TR_SYNTAX_ERROR = tr('Pireal', 'Syntax Error')
TR_NAME_DUPLICATED = tr('Pireal', 'Name Duplicated')
TR_RELATION_NAME_ALREADY_EXISTS = tr(
    'Pireal',
    'There is already a relationship with name <b>{}</b> :(<br><br>Please choose another.')
TR_QUERY_ERROR = tr('Pireal', 'Query Error')

TR_RELATIONS = tr('Pireal', 'Relations')

# New Relation Dialog
TR_RELATION_DIALOG_TITLE = tr('Pireal', 'Relation Creator')
TR_RELATION_DIALOG_NAME = tr('Pireal', 'Relation Name')
TR_RELATION_DIALOG_ADD_TUPLE = tr('Pireal', 'Add Tuple')
TR_RELATION_DIALOG_DELETE_TUPLE = tr('Pireal', 'Delete Tuple')
TR_RELATION_DIALOG_ADD_COLUMN = tr('Pireal', 'Add Column')
TR_RELATION_DIALOG_DELETE_COLUMN = tr('Pireal', 'Delete Column')
TR_RELATION_DIALOG_FIELD1 = tr('Pireal', 'Field 1')
TR_RELATION_DIALOG_FIELD2 = tr('Pireal', 'Field 2')
TR_RELATION_DIALOG_CREATE = tr('Pireal', 'Create')
TR_RELATION_DIALOG_CONFIRM_DELETE_TUPLE = tr('Pireal', 'Confirm tuple delete')
TR_RELATION_DIALOG_CONFIRM_DELETE_TUPLE_BODY = tr(
    'pireal',
    'Are you sure you want to delete the selected tuple(s)?'
)
TR_RELATION_DIALOG_EMPTY_RELATION_NAME = tr('Pireal', 'Relation name not specified')
TR_RELATION_DIALOG_WHITESPACE = tr(
    'Pireal',
    'The blanks are so boring :(.<br><br>Please enter data in <b>{}:{}</b>')

TR_QUERY_NOT_SAVED = tr('Pireal', 'Queries not saved')
TR_QUERY_NOT_SAVED_BODY = tr('Pireal', '{files}<br><br>Do you want to save the queries?')

# New Database
TR_DB_DIALOG_TITLE = tr('Pireal', 'New Database Wizard')
TR_DB_DIALOG_NEW_DB = tr('Pireal', 'Pireal New Database')
TR_DB_DIALOG_NEW_DB_SUB = tr('Pireal', 'Choose the name and destination of the database')
TR_DB_DIALOG_DB_NAME = tr('Pireal', 'Database Name:')
TR_DB_DIALOG_DB_LOCATION = tr('Pireal', 'Location:')
TR_DB_DIALOG_DB_FILENAME = tr('Pireal', 'Filename:')
TR_DB_DIALOG_SELECT_FOLDER = tr('Pireal', 'Select Folder')
