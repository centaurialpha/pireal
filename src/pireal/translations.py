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

from PyQt6.QtCore import QCoreApplication

TR_MENU_FILE = QCoreApplication.translate("Pireal", "&File")
TR_MENU_SCHEME = QCoreApplication.translate("Pireal", "&Scheme")
TR_MENU_HELP = QCoreApplication.translate("Pireal", "&Help")

TR_OPEN_DB = QCoreApplication.translate("Pireal", "Open Database")
TR_NEW_DB = QCoreApplication.translate("Pireal", "New Database")
TR_EXAMPLE_DB = QCoreApplication.translate("Pireal", "Example")

# File - Database
TR_MENU_FILE_NEW_DB = QCoreApplication.translate("Pireal", "New Database")
TR_MENU_FILE_NEW_DB_FROM_TEXT = QCoreApplication.translate("Pireal", "New from Text")
TR_MENU_FILE_OPEN_DB = QCoreApplication.translate("Pireal", "Open...")
TR_MENU_FILE_SAVE_DB = QCoreApplication.translate("Pireal", "Save")
TR_MENU_FILE_SAVE_AS_DB = QCoreApplication.translate("Pireal", "Save As...")
TR_MENU_FILE_CLOSE_DB = QCoreApplication.translate("Pireal", "Close")

# File - Query
TR_MENU_FILE_NEW_QUERY = QCoreApplication.translate("Pireal", "New Query")
TR_MENU_FILE_OPEN_QUERY = QCoreApplication.translate("Pireal", "Open Query...")
TR_MENU_FILE_SAVE_QUERY = QCoreApplication.translate("Pireal", "Save Query")
TR_MENU_FILE_SAVE_AS_QUERY = QCoreApplication.translate("Pireal", "Save Query As...")
TR_MENU_FILE_CLOSE_QUERY = QCoreApplication.translate("Pireal", "Close Query")

TR_MENU_FILE_QUIT = QCoreApplication.translate("Pireal", "Quit")

# Scheme
TR_MENU_SCHEME_CREATE_RELATION = QCoreApplication.translate("Pireal", "New Relation")
TR_MENU_SCHEME_REMOVE_RELATION = QCoreApplication.translate("Pireal", "Delete Relation")
TR_MENU_SCHEME_EXECUTE_QUERIES = QCoreApplication.translate("Pireal", "Execute")

# Help
TR_MENU_HELP_SHOW_TOUR = QCoreApplication.translate("Pireal", "Show Tour")
TR_MENU_HELP_REPORT_ISSUE = QCoreApplication.translate("Pireal", "Report Issue")
TR_MENU_HELP_ABOUT_PIREAL = QCoreApplication.translate("Pireal", "About Pireal")
TR_MENU_HELP_ABOUT_QT = QCoreApplication.translate("Pireal", "About Qt")

# TR_MSG_INFORMATION = QCoreApplication.translate("Pireal", "Information")
# TR_MSG_ONE_DB_AT_TIME = QCoreApplication.translate(
#     "Pireal", "Oops! One database at a time please"
# )
# TR_MSG_UPDATES = QCoreApplication.translate("Pireal", "Pireal Updates")
# TR_MSG_UPDATES_BODY = QCoreApplication.translate(
#     "Pireal",
#     "New version of Pireal available: {}\n\nClick on this message or System Tray icon to download!",
# )
# TR_OPEN_DATABASE = QCoreApplication.translate("Pireal", "Open Database")
# TR_MSG_DB_NOT_OPENED = QCoreApplication.translate(
#     "Pireal", "The database file could not be opened"
# )
#
# TR_MSG_OPEN_QUERY = QCoreApplication.translate("Pireal", "Open Query")
TR_CANCEL = QCoreApplication.translate("Pireal", "Cancel")
TR_MSG_CONFIRMATION = QCoreApplication.translate("Pireal", "Confirmation")
#
# TR_MSG_SAVE_CHANGES = QCoreApplication.translate("Pireal", "Save changes?")
# TR_MSG_SAVE_CHANGES_BODY = QCoreApplication.translate(
#     "Pireal", "The database has been modified. Do you want to save the changes?"
# )
#
# TR_MSG_FILE_MODIFIED = QCoreApplication.translate("Pireal", "File modified")
# TR_MSG_FILE_MODIFIED_BODY = QCoreApplication.translate(
#     "Pireal", "The file <b>{}</b> has unsaved changes. Do you want to keep them?"
# )
#
TR_MSG_SAVE_DB_AS = QCoreApplication.translate("Pireal", "Save Database As...")
# TR_MSG_OPEN_RELATION = QCoreApplication.translate("Pireal", "Open Relation")
#
# TR_MSG_REMOVE_TUPLES = QCoreApplication.translate("Pireal", "Delete tuple/s?")
# TR_MSG_REMOVE_TUPLES_BODY = QCoreApplication.translate(
#     "Pireal", "Are you sure you want to delete the selected tuples?"
# )
#
TR_MSG_REMOVE_RELATION = QCoreApplication.translate(
    "Pireal", "Are you sure you want to delete the relation <b>{}</b>?"
)
#
# TR_MSG_FILE_NOT_OPENED = QCoreApplication.translate(
#     "Pireal", "The file could not be opened"
# )
#
TR_MSG_SAVE_QUERY_FILE = QCoreApplication.translate("Pireal", "Save Query File")

# Table Widget
# TR_TABLE_CLICK_TO_SPLIT = QCoreApplication.translate("Pireal", "Click to split window")
# TR_TABLE_CLICK_TO_JOIN = QCoreApplication.translate("Pireal", "Click to join window")
TR_TABLE_ADD_TUPLE = QCoreApplication.translate("Pireal", "Add Tuple")
TR_TABLE_ADD_COL = QCoreApplication.translate("Pireal", "Add Column")
# TR_TABLE_CREATE_RELATION = QCoreApplication.translate("Pireal", "Create new Relation")

# Query Container
# TR_SYNTAX_ERROR = QCoreApplication.translate("Pireal", "Syntax Error")
# TR_NAME_DUPLICATED = QCoreApplication.translate("Pireal", "Name Duplicated")
# TR_RELATION_NAME_ALREADY_EXISTS = QCoreApplication.translate(
#     "Pireal",
#     "There is already a relationship with name <b>{}</b> :(<br><br>Please choose another.",
# )
# TR_QUERY_ERROR = QCoreApplication.translate("Pireal", "Query Error")
# #
TR_RELATIONS = QCoreApplication.translate("Pireal", "Relations")
TR_RESULTS = QCoreApplication.translate("Pireal", "Results")
#
# TR_QUERY_NOT_SAVED = QCoreApplication.translate("Pireal", "Queries not saved")
# TR_QUERY_NOT_SAVED_BODY = QCoreApplication.translate(
#     "Pireal", "{files}\n\nDo you want to save the queries?"
# )
#
# TR_DB_FILE_EMPTY = QCoreApplication.translate('Pireal', 'The file <b>{}</b> is empty :/.')
#
# Search widget
TR_BTN_FIND_PREVIOUS = QCoreApplication.translate("Pireal", "Find Previous")
TR_BTN_FIND_NEXT = QCoreApplication.translate("Pireal", "Find Next")
#
###############################################################################
# DIALOGS
###############################################################################
TR_SETTINGS_TITLE = QCoreApplication.translate("Pireal", "Settings")
TR_SETTINGS_GROUP_GENERAL = QCoreApplication.translate("Pireal", "General")
TR_SETTINGS_GROUP_EDITOR = QCoreApplication.translate("Pireal", "Editor")
TR_SETTINGS_GROUP_FONT = QCoreApplication.translate("Pireal", "Font")
TR_SETTINGS_LANGUAGE = QCoreApplication.translate("Pireal", "Language")
TR_SETTINGS_HIGHLIGHT_LINE = QCoreApplication.translate(
    "Pireal", "Highlight Current Line"
)
TR_SETTINGS_HIGHLIGHT_BRACES = QCoreApplication.translate("Pireal", "Highlight Braces")
TR_SETTINGS_FONT_FAMILY = QCoreApplication.translate("Pireal", "Font Family")
TR_SETTINGS_FONT_SIZE = QCoreApplication.translate("Pireal", "Font Size")

# About
TR_DIALOG_ABOUT_PIREAL_TITLE = QCoreApplication.translate("Pireal", "About Pireal")
TR_DIALOG_ABOUT_PIREAL_BODY = QCoreApplication.translate(
    "Pireal", "Relational Algebra Query Evaluator"
)
TR_DIALOG_ABOUT_PIREAL_COPY = QCoreApplication.translate(
    "Pireal",
    "<br>This Software is distributed under <a href='{}'><span style='color: #3465a4'>"
    "GNU GPL</span></a> 3.<br> The source code is available in"
    " <a href='{}'><span style='color: #3465a4'>GitHub.</span></a>",
)
# # New Database
TR_DB_DIALOG_TITLE = QCoreApplication.translate("Pireal", "Create New Database")
# TR_DB_DIALOG_NEW_DB = QCoreApplication.translate("Pireal", "Pireal New Database")
# TR_DB_DIALOG_NEW_DB_SUB = QCoreApplication.translate(
#     "Pireal", "Choose the name and destination of the database"
# )
TR_DB_DIALOG_DB_NAME = QCoreApplication.translate("Pireal", "Database Name:")
TR_DB_DIALOG_DB_LOCATION = QCoreApplication.translate("Pireal", "Location:")
TR_DB_DIALOG_DB_FILENAME = QCoreApplication.translate("Pireal", "Filename:")
# TR_DB_DIALOG_SELECT_FOLDER = QCoreApplication.translate("Pireal", "Select Folder")
# New Relation
TR_INPUT_DIALOG_HEADER_TITLE = QCoreApplication.translate("Pireal", "New Header Name:")
TR_INPUT_DIALOG_HEADER_BODY = QCoreApplication.translate("Pireal", "Header Name:")
TR_RELATION_DIALOG_TITLE = QCoreApplication.translate("Pireal", "Relation Creator")
TR_RELATION_DIALOG_NAME = QCoreApplication.translate("Pireal", "Relation Name")
TR_RELATION_DIALOG_CREATE = QCoreApplication.translate("Pireal", "Create")
TR_RELATION_DIALOG_CONFIRM_DELETE_TUPLE = QCoreApplication.translate(
    "Pireal", "Confirm tuple delete"
)
TR_RELATION_DIALOG_CONFIRM_DELETE_TUPLE_BODY = QCoreApplication.translate(
    "Pireal", "Are you sure you want to delete the selected tuple(s)?"
)
TR_RELATION_DIALOG_EMPTY_RELATION_NAME = QCoreApplication.translate(
    "Pireal", "Relation name not specified"
)
TR_RELATION_DIALOG_WHITESPACE = QCoreApplication.translate(
    "Pireal", "The blanks are so boring :(.<br><br>Please enter data in <b>{}:{}</b>"
)
#
# ###############################################################################
# # TOOLTIPS
# ###############################################################################
# TR_TOOLTIP_VERSION_AVAILABLE = QCoreApplication.translate(
#     "Pireal", "New version available!"
# )
#
TR_REMOVE_TUPLE = QCoreApplication.translate("Pireal", "Remove Tuple")
TR_REMOVE_COLUMN = QCoreApplication.translate("Pireal", "Remove Column")
# TR_MSG_WRONG = QCoreApplication.translate("Pireal", "Something has gone wrong")
#
# TR_STATUS_DB_SAVED = QCoreApplication.translate("Pireal", "Database has been saved: {}")
# TR_STATUS_DB_LOADED = QCoreApplication.translate(
#     "Pireal", "Database has been loaded: {}"
# )
# TR_STATUS_DB_CONNECTED = QCoreApplication.translate("Pireal", "Connected to: {}")
# TR_STATUS_QUERY_SAVED = QCoreApplication.translate("Pireal", "Query saved: {}")
#
# TR_TAB_CLOSE_TITLE = QCoreApplication.translate("Pireal", "Unsaved changes")
# TR_TAB_CLOSE_BODY = QCoreApplication.translate(
#     "Pireal", "The file <b>{name}</b> has unsaved changes. Save before closing?"
# )
#
# Tour
TR_TOUR_GET_STARTED = QCoreApplication.translate("Pireal", "Get started!")
TR_TOUR_NEXT = QCoreApplication.translate("Pireal", "Next →")
TR_TOUR_SLIDE1_TITLE = QCoreApplication.translate("Pireal", "Welcome to Pireal")
TR_TOUR_SLIDE1_BODY = QCoreApplication.translate(
    "Pireal",
    "Pireal is a free and open source <b>Relational Algebra interpreter</b> designed for learning database fundamentals.<br><br>Perfect for students and teachers exploring how databases work under the hood.",
)
TR_TOUR_SLIDE2_TITLE = QCoreApplication.translate("Pireal", "Create or open a Database")
TR_TOUR_SLIDE2_BODY = QCoreApplication.translate(
    "Pireal",
    "You can open an existing <b>.pdb</b> file, create one step by step using the dialog, or go full nerd and <b>code your database directly</b> using the text syntax:",
)
TR_TOUR_SLIDE3_TITLE = QCoreApplication.translate(
    "Pireal", "Write Relational Algebra queries"
)
TR_TOUR_SLIDE3_BODY = QCoreApplication.translate(
    "Pireal",
    "Use the query editor to write <b>Relational Algebra expressions</b>:",
)
TR_TOUR_SLIDE4_TITLE = QCoreApplication.translate("Pireal", "Explore the results")
TR_TOUR_SLIDE4_BODY = QCoreApplication.translate(
    "Pireal",
    "Every query result appears in the <b>Results panel</b> and the <b>sidebar</b>.<br><br>You can inspect each relation, see its cardinality and degree, and compare results side by side.",
)
#
# # Operator Tooltips
TR_TOOLTIP_SELECT = QCoreApplication.translate(
    "Pireal",
    "Filters tuples that satisfy a condition.\nUsage: select condition (relation)",
)
TR_TOOLTIP_PROJECT = QCoreApplication.translate(
    "Pireal",
    "Returns only the specified attributes.\nUsage: project attr1, attr2 (relation)",
)
TR_TOOLTIP_RENAME = QCoreApplication.translate(
    "Pireal", "Renames an attribute.\nUsage: rename old_name new_name (relation)"
)
TR_TOOLTIP_PRODUCT = QCoreApplication.translate(
    "Pireal", "Cartesian product of two relations.\nUsage: relation1 product relation2"
)
TR_TOOLTIP_NJOIN = QCoreApplication.translate(
    "Pireal", "Natural join on common attributes.\nUsage: relation1 njoin relation2"
)
TR_TOOLTIP_LOUTER = QCoreApplication.translate(
    "Pireal", "Left outer join.\nUsage: relation1 louter relation2"
)
TR_TOOLTIP_ROUTER = QCoreApplication.translate(
    "Pireal", "Right outer join.\nUsage: relation1 router relation2"
)
TR_TOOLTIP_FOUTER = QCoreApplication.translate(
    "Pireal", "Full outer join.\nUsage: relation1 fouter relation2"
)
TR_TOOLTIP_DIFFERENCE = QCoreApplication.translate(
    "Pireal",
    "Tuples in first relation but not in second.\nUsage: relation1 difference relation2",
)
TR_TOOLTIP_INTERSECT = QCoreApplication.translate(
    "Pireal", "Tuples present in both relations.\nUsage: relation1 intersect relation2"
)
TR_TOOLTIP_UNION = QCoreApplication.translate(
    "Pireal", "All tuples from both relations.\nUsage: relation1 union relation2"
)

# DB from text dialog
TR_DB_FROM_TEXT_TITLE = QCoreApplication.translate("Pireal", "New Database from Text")
TR_DB_FROM_TEXT_EDITOR_LABEL = QCoreApplication.translate("Pireal", "Database text:")
TR_DB_FROM_TEXT_PREVIEW_LABEL = QCoreApplication.translate("Pireal", "Preview:")
TR_DB_FROM_TEXT_LOAD_BTN = QCoreApplication.translate("Pireal", "Load")
TR_DB_FROM_TEXT_ERROR = QCoreApplication.translate("Pireal", "✗ Error: {}")
TR_DB_FROM_TEXT_NO_RELATIONS = QCoreApplication.translate(
    "Pireal", "✗ No relations found."
)
TR_DB_FROM_TEXT_VALID_ONE = QCoreApplication.translate("Pireal", "✓ 1 valid relation")
TR_DB_FROM_TEXT_VALID_MANY = QCoreApplication.translate(
    "Pireal", "✓ {} valid relations"
)

TR_UNSAVED_QUERIES_TITLE = QCoreApplication.translate("Pireal", "Unsaved queries")
TR_UNSAVED_QUERIES_BODY = QCoreApplication.translate(
    "Pireal",
    "The following queries have unsaved changes:\n{names}\n\nSave before closing?",
)
TR_CLOSE_DB_TITLE = QCoreApplication.translate("Pireal", "Database modified")
TR_CLOSE_DB_BODY = QCoreApplication.translate(
    "Pireal", "The database has unsaved changes. Save before closing?"
)

TR_RECENT_DATABASES = QCoreApplication.translate("Pireal", "Recent Databases")

# Placeholder
TR_PLACEHOLDER_NO_RELATIONS = QCoreApplication.translate(
    "Pireal", "No relations loaded"
)
TR_PLACEHOLDER_HINT = QCoreApplication.translate(
    "Pireal", "Create a relation using the form or write the code directly."
)
TR_PLACEHOLDER_BTN_NEW = QCoreApplication.translate("Pireal", "New relation")
TR_PLACEHOLDER_BTN_FROM_CODE = QCoreApplication.translate("Pireal", "From code")

# Feedback
TR_FEEDBACK_TITLE = QCoreApplication.translate("Pireal", "Send feedback")
TR_FEEDBACK_TYPE_GROUP = QCoreApplication.translate("Pireal", "Type")
TR_FEEDBACK_TYPE_BUG = QCoreApplication.translate("Pireal", "🐛  Bug")
TR_FEEDBACK_TYPE_SUGGESTION = QCoreApplication.translate("Pireal", "💡  Suggestion")
TR_FEEDBACK_TYPE_QUESTION = QCoreApplication.translate("Pireal", "❓  Question")
TR_FEEDBACK_TYPE_OTHER = QCoreApplication.translate("Pireal", "💬  Other")
TR_FEEDBACK_TITLE_LABEL = QCoreApplication.translate("Pireal", "Title:")
TR_FEEDBACK_TITLE_PLACEHOLDER = QCoreApplication.translate(
    "Pireal", "Brief summary of the problem or idea"
)
TR_FEEDBACK_BODY_LABEL = QCoreApplication.translate("Pireal", "Description:")
TR_FEEDBACK_BODY_PLACEHOLDER = QCoreApplication.translate(
    "Pireal", "Describe it in detail. If it's a bug, include the steps to reproduce it."
)
TR_FEEDBACK_ATTACH_BTN = QCoreApplication.translate("Pireal", "Attach image (optional)")
TR_FEEDBACK_ATTACH_DIALOG = QCoreApplication.translate("Pireal", "Select Image")
TR_FEEDBACK_ATTACH_FILTER = QCoreApplication.translate(
    "Pireal", "Images (*.png *.jpg *.jpeg)"
)
TR_FEEDBACK_BTN_SEND = QCoreApplication.translate("Pireal", "Send")
TR_FEEDBACK_BTN_SEND_START_PAGE = QCoreApplication.translate(
    "Pireal", "💬  Send me feedback"
)
TR_FEEDBACK_BTN_SENDING = QCoreApplication.translate("Pireal", "Sending to botcito...")
TR_FEEDBACK_BTN_RETRY = QCoreApplication.translate("Pireal", "Retry")
TR_FEEDBACK_SUCCESS = QCoreApplication.translate(
    "Pireal", "Sent! Thanks for helping to improve Pireal :)."
)
TR_FEEDBACK_ERROR_PREFIX = QCoreApplication.translate(
    "Pireal", "It could not be sent :(: {}"
)
TR_FEEDBACK_ERROR_NO_CONFIG = QCoreApplication.translate(
    "Pireal", "No se encontró la configuración de Telegram."
)
TR_FEEDBACK_ERROR_NO_TOKEN = QCoreApplication.translate(
    "Pireal", "Token o chat ID no configurados."
)
TR_FEEDBACK_HINT_LABEL = QCoreApplication.translate(
    "Pireal",
    (
        "If you prefer, you can also open an issue in"
        '<a href="https://github.com/centaurialpha/pireal/issues">GitHub</a>.'
    ),
)
TR_MENU_HELP_FEEDBACK = QCoreApplication.translate("Pireal", "Enviar feedback")
