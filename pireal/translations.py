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

###############################################################################
# START PAGE
###############################################################################
TR_OPEN_DB = QCoreApplication.translate('Pireal', 'Open Database')
TR_NEW_DB = QCoreApplication.translate('Pireal', 'New Database')
TR_EXAMPLE_DB = QCoreApplication.translate('Pireal', 'Example')

###############################################################################
# MENU BAR
###############################################################################
TR_MENU_FILE = QCoreApplication.translate('Pireal', '&File')
TR_MENU_SCHEME = QCoreApplication.translate('Pireal', '&Scheme')
TR_MENU_TOOLS = QCoreApplication.translate('Pireal', '&Tools')
TR_MENU_HELP = QCoreApplication.translate('Pireal', '&Help')

###############################################################################
# MENU ITEMS
###############################################################################
# File
TR_MENU_FILE_NEW_DB = QCoreApplication.translate('Pireal', 'New')
TR_MENU_FILE_OPEN_DB = QCoreApplication.translate('Pireal', 'Open')
TR_MENU_FILE_SAVE_DB = QCoreApplication.translate('Pireal', 'Save')
TR_MENU_FILE_SAVE_AS_DB = QCoreApplication.translate('Pireal', 'Save As...')
TR_MENU_FILE_CLOSE_DB = QCoreApplication.translate('Pireal', 'Close')
TR_MENU_FILE_NEW_QUERY = QCoreApplication.translate('Pireal', 'New')
TR_MENU_FILE_OPEN_QUERY = QCoreApplication.translate('Pireal', 'Open')
TR_MENU_FILE_SAVE_QUERY = QCoreApplication.translate('Pireal', 'Save')
TR_MENU_FILE_SAVE_AS_QUERY = QCoreApplication.translate('Pireal', 'Save As...')
TR_MENU_FILE_CLOSE_QUERY = QCoreApplication.translate('Pireal', 'Close')
TR_MENU_FILE_QUIT = QCoreApplication.translate('Pireal', 'Quit')

# Schema
TR_MENU_SCHEME_CREATE_RELATION = QCoreApplication.translate('Pireal', 'New Relation')
TR_MENU_SCHEME_LOAD_RELATION = QCoreApplication.translate('Pireal', 'Load Relation')
TR_MENU_SCHEME_REMOVE_RELATION = QCoreApplication.translate('Pireal', 'Delete Relation')
TR_MENU_SCHEME_EXECUTE_QUERIES = QCoreApplication.translate('Pireal', 'Execute Query')
# Tools
TR_MENU_TOOLS_SETTINGS = QCoreApplication.translate('Pireal', 'Preferences')
# Help
TR_MENU_HELP_REPORT_ISSUE = QCoreApplication.translate('Pireal', 'Report Issue')
TR_MENU_HELP_ABOUT_PIREAL = QCoreApplication.translate('Pireal', 'About Pireal')
TR_MENU_HELP_ABOUT_QT = QCoreApplication.translate('Pireal', 'About Qt')

###############################################################################
# MESSAGES
###############################################################################
TR_MSG_INFORMATION = QCoreApplication.translate('Pireal', 'Information')
TR_MSG_ONE_DB_AT_TIME = QCoreApplication.translate('Pireal', 'Oops! One database at a time please')
TR_MSG_UPDATES = QCoreApplication.translate('Pireal', 'Pireal Updates')
TR_MSG_UPDATES_BODY = QCoreApplication.translate(
    'Pireal',
    'New version of Pireal available: {}\n\nClick on this message or System Tray icon to download!')
TR_OPEN_DATABASE = QCoreApplication.translate('Pireal', 'Open Database')
TR_MSG_DB_NOT_OPENED = QCoreApplication.translate('Pireal', 'The database file could not be opened')

TR_MSG_OPEN_QUERY = QCoreApplication.translate('Pireal', 'Open Query')
TR_CANCEL = QCoreApplication.translate('Pireal', 'Cancel')
TR_MSG_CONFIRMATION = QCoreApplication.translate('Pireal', 'Confirmation')

TR_MSG_SAVE_CHANGES = QCoreApplication.translate('Pireal', 'Save changes?')
TR_MSG_SAVE_CHANGES_BODY = QCoreApplication.translate(
    'Pireal',
    'The database has been modified. Do you want to save the changes?')

TR_MSG_FILE_MODIFIED = QCoreApplication.translate('Pireal', 'File modified')
TR_MSG_FILE_MODIFIED_BODY = QCoreApplication.translate(
    'Pireal',
    'The file <b>{}</b> has unsaved changes. Do you want to keep them?')

TR_MSG_SAVE_DB_AS = QCoreApplication.translate('Pireal', 'Save Database As...')
TR_MSG_OPEN_RELATION = QCoreApplication.translate('Pireal', 'Open Relation')

TR_MSG_REMOVE_TUPLES = QCoreApplication.translate('Pireal', 'Delete tuple/s?')
TR_MSG_REMOVE_TUPLES_BODY = QCoreApplication.translate(
    'Pireal',
    'Are you sure you want to delete the selected tuples?')

TR_MSG_REMOVE_RELATION = QCoreApplication.translate(
    'Pireal',
    'Are you sure you want to delete the relation <b>{}</b>?')

TR_MSG_FILE_NOT_OPENED = QCoreApplication.translate('Pireal', 'The file could not be opened')

TR_MSG_SAVE_QUERY_FILE = QCoreApplication.translate('Pireal', 'Save Query File')

# Table Widget
TR_TABLE_CLICK_TO_SPLIT = QCoreApplication.translate('Pireal', 'Click to split window')
TR_TABLE_CLICK_TO_JOIN = QCoreApplication.translate('Pireal', 'Click to join window')
TR_TABLE_ADD_TUPLE = QCoreApplication.translate('Pireal', 'Add Tuple')
TR_TABLE_ADD_COL = QCoreApplication.translate('Pireal', 'Add Column')
TR_TABLE_CREATE_RELATION = QCoreApplication.translate('Pireal', 'Create new Relation')

# Query Container
TR_SYNTAX_ERROR = QCoreApplication.translate('Pireal', 'Syntax Error')
TR_NAME_DUPLICATED = QCoreApplication.translate('Pireal', 'Name Duplicated')
TR_RELATION_NAME_ALREADY_EXISTS = QCoreApplication.translate(
    'Pireal',
    'There is already a relationship with name <b>{}</b> :(<br><br>Please choose another.')
TR_QUERY_ERROR = QCoreApplication.translate('Pireal', 'Query Error')
#
TR_RELATIONS = QCoreApplication.translate('Pireal', 'Relations')
TR_RESULTS = QCoreApplication.translate('Pireal', 'Results')

TR_QUERY_NOT_SAVED = QCoreApplication.translate('Pireal', 'Queries not saved')
TR_QUERY_NOT_SAVED_BODY = QCoreApplication.translate(
    'Pireal',
    '{files}\n\nDo you want to save the queries?')
#
# TR_DB_FILE_EMPTY = QCoreApplication.translate('Pireal', 'The file <b>{}</b> is empty :/.')
#
# Search widget
TR_BTN_FIND_PREVIOUS = QCoreApplication.translate('Pireal', 'Find Previous')
TR_BTN_FIND_NEXT = QCoreApplication.translate('Pireal', 'Find Next')
#
###############################################################################
# DIALOGS
###############################################################################
# Preferences
TR_DIALOG_PREF_TITLE = QCoreApplication.translate('Pireal', 'Preferences')
TR_DIALOG_PREF_DARK_MODE = QCoreApplication.translate('Pireal', 'Dark Mode')
TR_DIALOG_PREF_LANG = QCoreApplication.translate('Pireal', 'Language:')
TR_DIALOG_PREF_HIGHLIGHT_CUR_LINE = QCoreApplication.translate('Pireal', 'Highlight Current Line')
TR_DIALOG_PREF_HIGHLIGHT_BRACES = QCoreApplication.translate('Pireal', 'Highlight Braces')
TR_DIALOG_PREF_FONT = QCoreApplication.translate('Pireal', 'Font:')
TR_DIALOG_PREF_FONT_FAMILY = QCoreApplication.translate('Pireal', 'Family:')
TR_DIALOG_PREF_FONT_SIZE = QCoreApplication.translate('Pireal', 'Size:')
# About
TR_DIALOG_ABOUT_PIREAL_TITLE = QCoreApplication.translate('Pireal', 'About Pireal')
TR_DIALOG_ABOUT_PIREAL_BODY = QCoreApplication.translate(
    'Pireal',
    'Relational Algebra Query Evaluator')
TR_DIALOG_ABOUT_PIREAL_COPY = QCoreApplication.translate(
    'Pireal',
    "<br>This Software is distributed under <a href='{}'><span style='color: #3465a4'>"
    "GNU GPL</span></a> 3.<br> The source code is available in"
    " <a href='{}'><span style='color: #3465a4'>GitHub.</span></a>"
)
# New Database
TR_DB_DIALOG_TITLE = QCoreApplication.translate('Pireal', 'Create New Database')
TR_DB_DIALOG_NEW_DB = QCoreApplication.translate('Pireal', 'Pireal New Database')
TR_DB_DIALOG_NEW_DB_SUB = QCoreApplication.translate(
    'Pireal',
    'Choose the name and destination of the database')
TR_DB_DIALOG_DB_NAME = QCoreApplication.translate('Pireal', 'Database Name:')
TR_DB_DIALOG_DB_LOCATION = QCoreApplication.translate('Pireal', 'Location:')
TR_DB_DIALOG_DB_FILENAME = QCoreApplication.translate('Pireal', 'Filename:')
TR_DB_DIALOG_SELECT_FOLDER = QCoreApplication.translate('Pireal', 'Select Folder')
# New Relation
TR_INPUT_DIALOG_HEADER_TITLE = QCoreApplication.translate('Pireal', 'New Header Name:')
TR_INPUT_DIALOG_HEADER_BODY = QCoreApplication.translate('Pireal', 'Header Name:')
#
TR_RELATION_DIALOG_TITLE = QCoreApplication.translate('Pireal', 'Relation Creator')
TR_RELATION_DIALOG_NAME = QCoreApplication.translate('Pireal', 'Relation Name')
# TR_RELATION_DIALOG_ADD_TUPLE = QCoreApplication.translate('Pireal', 'Add Tuple')
# TR_RELATION_DIALOG_DELETE_TUPLE = QCoreApplication.translate('Pireal', 'Delete Tuple')
# TR_RELATION_DIALOG_ADD_COLUMN = QCoreApplication.translate('Pireal', 'Add Column')
# TR_RELATION_DIALOG_DELETE_COLUMN = QCoreApplication.translate('Pireal', 'Delete Column')
# TR_RELATION_DIALOG_FIELD1 = QCoreApplication.translate('Pireal', 'Field 1')
# TR_RELATION_DIALOG_FIELD2 = QCoreApplication.translate('Pireal', 'Field 2')
TR_RELATION_DIALOG_CREATE = QCoreApplication.translate('Pireal', 'Create')
TR_RELATION_DIALOG_CONFIRM_DELETE_TUPLE = QCoreApplication.translate(
    'Pireal', 'Confirm tuple delete')
TR_RELATION_DIALOG_CONFIRM_DELETE_TUPLE_BODY = QCoreApplication.translate(
    'Pireal',
    'Are you sure you want to delete the selected tuple(s)?'
)
TR_RELATION_DIALOG_EMPTY_RELATION_NAME = QCoreApplication.translate(
    'Pireal', 'Relation name not specified')
TR_RELATION_DIALOG_WHITESPACE = QCoreApplication.translate(
    'Pireal',
    'The blanks are so boring :(.<br><br>Please enter data in <b>{}:{}</b>')

###############################################################################
# TOOLTIPS
###############################################################################
TR_TOOLTIP_VERSION_AVAILABLE = QCoreApplication.translate('Pireal', 'New version available!')

TR_REMOVE_TUPLE = QCoreApplication.translate('Pireal', 'Remove Tuple')
TR_REMOVE_COLUMN = QCoreApplication.translate('Pireal', 'Remove Column')
TR_MSG_WRONG = QCoreApplication.translate('Pireal', 'Something has gone wrong')

TR_STATUS_DB_SAVED = QCoreApplication.translate('Pireal', 'Database has been saved: {}')
TR_STATUS_DB_LOADED = QCoreApplication.translate('Pireal', 'Database has been loaded: {}')
TR_STATUS_DB_CONNECTED = QCoreApplication.translate('Pireal', 'Connected to: {}')
TR_STATUS_QUERY_SAVED = QCoreApplication.translate('Pireal', 'Query saved: {}')
