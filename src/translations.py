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

from PyQt4.QtGui import QApplication

translate = QApplication.translate


TR_SETTINGS_MENUBAR = translate("Pireal", "Settings")

# Menu File
TR_MENU_FILE = translate("Pireal", "&File")
TR_MENU_FILE_NEW_DB = translate("Pireal", "New Database")
TR_MENU_FILE_NEW_QUERY = translate("Pireal", "New Query")
TR_MENU_FILE_OPEN = translate("Pireal", "Open")
TR_MENU_FILE_SAVE_DB = translate("Pireal", "Save Database")
TR_MENU_FILE_SAVE = translate("Pireal", "Save")
TR_MENU_FILE_SAVE_AS = translate("Pireal", "Save As...")
TR_MENU_FILE_EXIT = translate("Pireal", "Exit")

# Menu Edit
TR_MENU_EDIT = translate("Pireal", "&Edit")
TR_MENU_EDIT_UNDO = translate("Pireal", "Undo")
TR_MENU_EDIT_REDO = translate("Pireal", "Redo")
TR_MENU_EDIT_CUT = translate("Pireal", "Cut")
TR_MENU_EDIT_COPY = translate("Pireal", "Copy")
TR_MENU_EDIT_PASTE = translate("Pireal", "Paste")

# Menu Relation
TR_MENU_RELATION = translate("Pireal", "&Relation")
TR_MENU_RELATION_NEW_RELATION = translate("Pireal", "New Relation")
TR_MENU_RELATION_DELETE_RELATION = translate("Pireal", "Delete Relation")
TR_MENU_RELATION_LOAD_RELATION = translate("Pireal", "Load Relation")
TR_MENU_RELATION_ADD_ROW = translate("Pireal", "Add Row")
TR_MENU_RELATION_DELETE_ROW = translate("Pireal", "Delete Row")
TR_MENU_RELATION_EXECUTE = translate("Pireal", "Execute Queries")

# Menu Help
TR_MENU_HELP = translate("Pireal", "&Help")
TR_MENU_HELP_ABOUT_PIREAL = translate("Pireal", "About Pireal")
TR_MENU_HELP_ABOUT_QT = translate("Pireal", "About Qt")

# About dialog
TR_ABOUT_DIALOG = translate("Pireal", "About Pireal")
TR_ABOUT_DIALOG_DESC = translate("Pireal", ("<br><br>an educational "
                                 "tool for working\nwith Relational Algebra."))
TR_ABOUT_DIALOG_VERSION = translate("Pireal", ("<a href='{0}'>Version {1}</a>"))
TR_ABOUT_DIALOG_LICENSE_SOURCE = translate("Pireal", ("<br>This software is "
                                           "licensed under <a href='{0}'>GNU "
                                           "GPL</a> version 3,<br>source code"
                                           " is available on "
                                           "<a href='{1}'>GitHub.</a>"))
TR_ABOUT_DIALOG_BTN_OK = translate("Pireal", "Done")

# New relation dialog
TR_RELATION_DIALOG_TITLE = translate("Pireal", "New Relation")
TR_RELATION_DIALOG_FIELDS = translate("Pireal", ("The first row corresponds"
                                      " to the fields."))
TR_RELATION_DIALOG_NAME = translate("Pireal", "Relationship name")
TR_RELATION_DIALOG_ADD_COL = translate("Pireal", "Add Column")
TR_RELATION_DIALOG_ADD_ROW = translate("Pireal", "Add Row")
TR_RELATION_DIALOG_DELETE_ROW = translate("Pireal", "Delete Row")
TR_RELATION_DIALOG_DELETE_COL = translate("Pireal", "Delete Column")
TR_RELATION_DIALOG_BTN_OK = translate("Pireal", "Ok")
TR_RELATION_DIALOG_BTN_CANCEL = translate("Pireal", "Cancel")
TR_RELATION_DIALOG_ERROR_NAME = translate("Pireal",
                                          "Relation name not specified.")
TR_RELATION_DIALOG_ERROR_FIELD = translate("Pireal", "Invalid field name.")
TR_RELATION_DIALOG_FIELD_EMPTY = translate("Pireal", "Field {0}:{1} is empty!")
TR_RELATION_DIALOG_F1 = translate("Pireal", "Field 1")
TR_RELATION_DIALOG_F2 = translate("Pireal", "Field 2")

# Container
TR_CONTAINER_ERROR_DB = translate("Pireal", ("You can only have a database"
                                  "open at a time"))
TR_CONTAINER_UNSELECTED_RELATIONSHIP = translate("Pireal",
                                                 "None selected relationship")
TR_CONTAINER_CONFIRM_DELETE_REL_TITLE = translate("Pireal", "Confirmation")
TR_CONTAINER_CONFIRM_DELETE_REL = translate("Pireal", ("Are you sure you want"
                                            "to delete the"
                                            "relationship <b>{}</b>?"))
TR_CONTAINER_FILE_SAVED = translate("Pireal", "File Saved: {}")
TR_CONTAINER_SAVE_FILE = translate("Pireal", "Save File")
TR_CONTAINER_SAVE_DB = translate("Pireal", "Save Database")
TR_CONTAINER_OPEN_FILE = translate("Pireal", "Open File")

# Query widget
TR_QUERY_ERROR = translate("Pireal", "Query error")
TR_QUERY_FILE_MODIFIED = translate("Pireal", "File modified")
TR_QUERY_FILE_MODIFIED_MSG = translate("Pireal", ("The file <b>{}</b> has "
                                       "unsaved changes. You want "
                                       "to keep them?"))

# Preferences
TR_PREFERENCES_GROUP_LANG = translate("Pireal", "Language")
TR_PREFERENCES_GROUP_GRAL = translate("Pireal", "General")
TR_PREFERENCES_CHECK_START_PAGE = translate("Pireal", "Show Start Page")
TR_PREFERENCES_CHECK_UPDATES = translate("Pireal", "Notify me of new updates")
TR_PREFERENCES_BTN_CHECK_FOR_UPDATES = translate("Pireal", "Check for updates")
TR_PREFERENCES_BTN_RESET = translate("Pireal", "Reset preferences")
TR_PREFERENCES_RESET_MSG = translate("Pireal", ("Are you sure you want"
                                                " to clear all settings?"))
TR_PREFERENCES_RESET_TITLE = translate("Pireal", "Reset settings?")
