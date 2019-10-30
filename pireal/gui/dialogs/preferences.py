# -*- coding: utf-8 -*-
#
# Copyright 2015-2017 - Gabriel Acosta <acostadariogabriel@gmail.com>
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

from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QFontComboBox
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QGroupBox
from PyQt5.QtWidgets import QDialogButtonBox

from PyQt5.QtGui import QFontDatabase

from pireal.core.settings import USER_SETTINGS, USER_SETTINGS_PATH
# from pireal.core.settings import CONFIG
# from pireal.gui.main_window import Pireal


class Preferences(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._central = parent
        self.setWindowTitle('Preferences')
        vbox = QVBoxLayout(self)

        group_language = QGroupBox('Language:')
        grid_language = QGridLayout(group_language)
        self._combo_languages = QComboBox()
        grid_language.addWidget(self._combo_languages, 0, 0)

        group_editor = QGroupBox('Editor:')
        grid_editor = QGridLayout(group_editor)
        self._check_highlight_current_line = QCheckBox('Highlight Current Line')
        self._check_highlight_current_line.setChecked(
            USER_SETTINGS.value('highlightCurrentLine', False, bool))
        grid_editor.addWidget(self._check_highlight_current_line, 0, 0)
        self._check_highlight_braces = QCheckBox('Highlight Braces')
        self._check_highlight_braces.setChecked(
            USER_SETTINGS.value('matchParenthesis', False, bool))
        grid_editor.addWidget(self._check_highlight_braces, 0, 1)

        group_font = QGroupBox('Font:')
        font_db = QFontDatabase()
        grid_font = QGridLayout(group_font)
        self._combo_font_family = QFontComboBox()
        grid_font.addWidget(QLabel('Family:'), 0, 0)
        grid_font.addWidget(self._combo_font_family, 0, 1)
        # self._combo_font_family.setCurrentText(CONFIG.get('fontFamily'))
        # cur_font = CONFIG.get('fontFamily')
        self._combo_font_size = QComboBox()
        # self._combo_font_size.addItems(map(str, font_db.pointSizes(cur_font)))
        # self._combo_font_size.setCurrentText(str(CONFIG.get('fontSize')))
        grid_font.addWidget(QLabel('Size:'), 0, 2)
        grid_font.addWidget(self._combo_font_size, 0, 3)

        btn_box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        btn_box.rejected.connect(self.reject)
        btn_box.accepted.connect(self.accept)

        # Add widgets to layout
        vbox.addWidget(group_language)
        vbox.addWidget(group_editor)
        vbox.addWidget(group_font)
        vbox.addWidget(btn_box)

    def accept(self):
        # font_size = int(self._combo_font_size.currentText())
        # font_family = self._combo_font_family.currentText()

        # CONFIG.set_value('fontSize', font_size)
        # CONFIG.set_value('fontFamily', font_family)
        # CONFIG.set_value('highlightCurrentLine', self._check_highlight_current_line.isChecked())
        # CONFIG.set_value('matchParenthesis', self._check_highlight_braces.isChecked())
        USER_SETTINGS.setValue(
            'highlightCurrentLine', self._check_highlight_current_line.isChecked())
        USER_SETTINGS.setValue('matchParenthesis', self._check_highlight_braces.isChecked())

        # central = Pireal.get_service('central')
        # db = self._central.get_active_db()
        # if db is not None:
        #     qw = db.query_container.currentWidget()
        #     if qw is not None:
        #         editor = qw.get_editor()
        #         editor.set_font(font_family, font_size)
        #         editor.set_highlight_line(self._check_highlight_current_line.isChecked())
        #         editor.set_match_parenthesis(self._check_highlight_braces.isChecked())
        # CONFIG.save_settings()
        super().accept()

# import os
# import webbrowser
# from PyQt5.QtWidgets import (
#     QDialog,
#     QVBoxLayout,
#     QMessageBox,
#     QFontDialog
# )
# from PyQt5.QtGui import QFont
# from PyQt5.QtQuickWidgets import QQuickWidget
# from PyQt5.QtCore import (
#     QUrl,
#     pyqtSlot,
#     QSettings,
#     pyqtSignal,
#     QThread
# )
# from pireal.core import (
#     settings,
#     file_manager
# )
# from pireal.gui import updater
# from pireal.gui.main_window import Pireal
# from pireal.core.settings import CONFIG

# # TODO: verificar el estado de los checkboxes si son distintos al cambiar


# class Preferences(QDialog):
#     settingsClosed = pyqtSignal()

#     def __init__(self, parent=None):
#         QDialog.__init__(self, parent)
#         self.__need_restart = False
#         box = QVBoxLayout(self)
#         box.setContentsMargins(0, 0, 0, 0)
#         view = QQuickWidget()
#         view.setResizeMode(QQuickWidget.SizeRootObjectToView)
#         qml = os.path.join(settings.QML_PATH, "Preferences.qml")
#         view.setSource(QUrl.fromLocalFile(qml))
#         box.addWidget(view)

#         self.__root = view.rootObject()
#         # Lista de idiomas para el Combo qml
#         available_langs = file_manager.get_files_from_folder(
#             settings.LANGUAGE_PATH)
#         langs = ["English"] + available_langs
#         self.__root.addLangsToCombo(langs)

#         self.__root.setCurrentLanguage(CONFIG.get("language"))

#         font = CONFIG.get("fontFamily")
#         size = CONFIG.get("fontSize")
#         if font is None:
#             font, size = CONFIG._get_font()

#         self.__root.setFontFamily(font, size)

#         self.__root.setInitialStates(
#             CONFIG.get("highlightCurrentLine"),
#             CONFIG.get("matchParenthesis"))

#         # Conexiones
#         self.__root.close.connect(lambda: self.settingsClosed.emit())
#         self.__root.resetSettings.connect(self.__reset_settings)
#         self.__root.checkForUpdates.connect(self.__check_for_updates)
#         self.__root.changeLanguage.connect(self.__change_language)
#         self.__root.stateCurrentLineChanged[bool].connect(
#             self.__on_state_current_line_changed)
#         self.__root.stateMatchingParenChanged[bool].connect(
#             self.__on_state_matching_parenthesis_changed)
#         self.__root.needChangeFont.connect(self.__change_font)

#     @pyqtSlot()
#     def __change_font(self):
#         font = CONFIG.get("fontFamily")
#         size = CONFIG.get("fontSize")
#         if font is None:
#             font, size = CONFIG._get_font()
#         font, ok = QFontDialog.getFont(QFont(font, size), self)
#         if ok:
#             CONFIG.set_value("fontFamily", font.family())
#             CONFIG.set_value("fontSize", font.pointSize())
#             central = Pireal.get_service("central")
#             mcontainer = central.get_active_db()
#             if mcontainer is not None:
#                 query_widget = mcontainer.query_container.currentWidget()
#                 if query_widget is not None:
#                     weditor = query_widget.get_editor()
#                     if weditor is not None:
#                         weditor.set_font(font.family(), font.pointSize())
#             # Cambio el texto en la interfáz QML
#             self.__root.setFontFamily(font.family(), font.pointSize())

#     @pyqtSlot(bool)
#     def __on_state_current_line_changed(self, state):
#         CONFIG.set_value("highlightCurrentLine", state)

#     @pyqtSlot(bool)
#     def __on_state_matching_parenthesis_changed(self, state):
#         CONFIG.set_value("matchParenthesis", state)

#     @pyqtSlot('QString')
#     def __change_language(self, lang):
#         qsettings = QSettings(settings.SETTINGS_PATH, QSettings.IniFormat)
#         current_lang = qsettings.value('language', 'English')
#         if current_lang != lang:
#             qsettings.setValue('language', lang)
#             self.__need_restart = True

#     @pyqtSlot()
#     def __check_for_updates(self):
#         # Thread
#         self._thread = QThread()
#         self._updater = updater.Updater()
#         self._updater.moveToThread(self._thread)
#         self._thread.started.connect(self._updater.check_updates)
#         self._updater.finished.connect(self.__on_thread_update_finished)
#         # Start thread
#         self._thread.start()

#     @pyqtSlot()
#     def __on_thread_update_finished(self):
#         self._thread.quit()
#         msg = QMessageBox(self)
#         if not self._updater.error:
#             if self._updater.version:
#                 version = self._updater.version
#                 msg.setWindowTitle(self.tr("New version available!"))
#                 msg.setText(self.tr("Check the web site to "
#                                     "download <b>Pireal {}</b>".format(
#                                         version)))
#                 download_btn = msg.addButton(self.tr("Download!"),
#                                              QMessageBox.YesRole)
#                 msg.addButton(self.tr("Cancel"),
#                               QMessageBox.RejectRole)
#                 msg.exec_()
#                 r = msg.clickedButton()
#                 if r == download_btn:
#                     webbrowser.open_new(
#                         "http://centaurialpha.github.io/pireal")
#             else:
#                 # Cierro BusyIndicator de qml
#                 self.__root.threadFinished()
#                 msg.setWindowTitle(self.tr("Information"))
#                 msg.setText(self.tr("Last version installed"))
#                 msg.addButton(self.tr("Ok"),
#                               QMessageBox.AcceptRole)
#                 msg.exec_()
#         else:
#             msg.critical(self, self.tr("Error"),
#                          self.tr("Connection error"))

#         self._thread.deleteLater()
#         self._updater.deleteLater()
#         self.__root.threadFinished()

#     @pyqtSlot()
#     def __reset_settings(self):
#         """ Remove all settings """

#         msg = QMessageBox(self)
#         msg.setWindowTitle(self.tr("Reset Settings"))
#         msg.setText(self.tr("Are you sure you want to clear all settings?"))
#         msg.setIcon(QMessageBox.Question)
#         msg.addButton(self.tr("No"), QMessageBox.NoRole)
#         yes_btn = msg.addButton(self.tr("Yes"),
#                                 QMessageBox.YesRole)
#         msg.exec_()
#         r = msg.clickedButton()
#         if r == yes_btn:
#             QSettings(settings.SETTINGS_PATH, QSettings.IniFormat).clear()
#             # self.close()
