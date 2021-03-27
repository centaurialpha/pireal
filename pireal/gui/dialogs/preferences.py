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

import os
import webbrowser
from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QMessageBox,
    QFontDialog
)
from PyQt5.QtGui import QFont
from PyQt5.QtQuickWidgets import QQuickWidget
from PyQt5.QtCore import (
    QUrl,
    pyqtSlot,
    QSettings,
    pyqtSignal,
    QThread
)
from pireal.core import file_manager
from pireal.gui import updater
from pireal.gui.main_window import Pireal
from pireal.dirs import (
    QML_RESOURCES,
    LANGUAGES_DIR,
    DATA_SETTINGS,
)
from pireal.core.settings import SETTINGS
# TODO: verificar el estado de los checkboxes si son distintos al cambiar


class Preferences(QDialog):
    settingsClosed = pyqtSignal()

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.__need_restart = False
        box = QVBoxLayout(self)
        box.setContentsMargins(0, 0, 0, 0)
        view = QQuickWidget()
        view.setResizeMode(QQuickWidget.SizeRootObjectToView)
        qml = os.path.join(QML_RESOURCES.stem, "Preferences.qml")
        view.setSource(QUrl.fromLocalFile(qml))
        box.addWidget(view)

        self.__root = view.rootObject()
        # Lista de idiomas para el Combo qml
        available_langs = file_manager.get_files_from_folder(LANGUAGES_DIR)
        langs = ["English"] + available_langs
        self.__root.addLangsToCombo(langs)

        self.__root.setCurrentLanguage(SETTINGS.language)

        font = SETTINGS.font_family
        size = SETTINGS.font_size
        self.__root.setFontFamily(font, size)

        self.__root.setInitialStates(SETTINGS.highlight_current_line, SETTINGS.match_parenthesis)

        # Conexiones
        self.__root.close.connect(lambda: self.settingsClosed.emit())
        self.__root.resetSettings.connect(self.__reset_settings)
        self.__root.checkForUpdates.connect(self.__check_for_updates)
        self.__root.changeLanguage.connect(self.__change_language)
        self.__root.stateCurrentLineChanged[bool].connect(
            self.__on_state_current_line_changed)
        self.__root.stateMatchingParenChanged[bool].connect(
            self.__on_state_matching_parenthesis_changed)
        self.__root.needChangeFont.connect(self.__change_font)

    @pyqtSlot()
    def __change_font(self):
        font = SETTINGS.font_family
        size = SETTINGS.font_size
        font, ok = QFontDialog.getFont(QFont(font, size), self)
        if ok:
            SETTINGS.font_family = font.family()
            SETTINGS.font_size = font.pointSize()
            central = Pireal.get_service("central")
            mcontainer = central.get_active_db()
            if mcontainer is not None:
                query_widget = mcontainer.query_container.currentWidget()
                if query_widget is not None:
                    weditor = query_widget.get_editor()
                    if weditor is not None:
                        weditor.set_font(font.family(), font.pointSize())
            # Cambio el texto en la interfáz QML
            self.__root.setFontFamily(font.family(), font.pointSize())

    @pyqtSlot(bool)
    def __on_state_current_line_changed(self, state):
        SETTINGS.highlight_current_line = state

    @pyqtSlot(bool)
    def __on_state_matching_parenthesis_changed(self, state):
        SETTINGS.match_parenthesis = state

    @pyqtSlot('QString')
    def __change_language(self, lang):
        SETTINGS.language = lang
        self.__need_restart = True

    @pyqtSlot()
    def __check_for_updates(self):
        # Thread
        self._thread = QThread()
        self._updater = updater.Updater()
        self._updater.moveToThread(self._thread)
        self._thread.started.connect(self._updater.check_updates)
        self._updater.finished.connect(self.__on_thread_update_finished)
        # Start thread
        self._thread.start()

    @pyqtSlot()
    def __on_thread_update_finished(self):
        self._thread.quit()
        msg = QMessageBox(self)
        if not self._updater.error:
            if self._updater.version:
                version = self._updater.version
                msg.setWindowTitle(self.tr("New version available!"))
                msg.setText(self.tr("Check the web site to "
                                    "download <b>Pireal {}</b>".format(
                                        version)))
                download_btn = msg.addButton(self.tr("Download!"),
                                             QMessageBox.YesRole)
                msg.addButton(self.tr("Cancel"),
                              QMessageBox.RejectRole)
                msg.exec_()
                r = msg.clickedButton()
                if r == download_btn:
                    webbrowser.open_new(
                        "http://centaurialpha.github.io/pireal")
            else:
                # Cierro BusyIndicator de qml
                self.__root.threadFinished()
                msg.setWindowTitle(self.tr("Information"))
                msg.setText(self.tr("Last version installed"))
                msg.addButton(self.tr("Ok"),
                              QMessageBox.AcceptRole)
                msg.exec_()
        else:
            msg.critical(self, self.tr("Error"),
                         self.tr("Connection error"))

        self._thread.deleteLater()
        self._updater.deleteLater()
        self.__root.threadFinished()

    @pyqtSlot()
    def __reset_settings(self):
        """ Remove all settings """

        msg = QMessageBox(self)
        msg.setWindowTitle(self.tr("Reset Settings"))
        msg.setText(self.tr("Are you sure you want to clear all settings?"))
        msg.setIcon(QMessageBox.Question)
        msg.addButton(self.tr("No"), QMessageBox.NoRole)
        yes_btn = msg.addButton(self.tr("Yes"),
                                QMessageBox.YesRole)
        msg.exec_()
        r = msg.clickedButton()
        if r == yes_btn:
            QSettings(str(DATA_SETTINGS), QSettings.IniFormat).clear()
            # self.close()
