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
import json
import logging
from urllib.error import URLError
from urllib.request import urlopen

from packaging.version import Version
from PyQt6.QtCore import (
    QObject,
    QSettings,
    pyqtSignal,
)

from pireal import __version__
from pireal.dirs import DATA_SETTINGS

logger = logging.getLogger("updater")

URL = "https://api.github.com/repos/centaurialpha/pireal/releases/latest"


class Updater(QObject):
    finished = pyqtSignal()
    updateAvailable = pyqtSignal(str, str)

    def __init__(self):
        QObject.__init__(self)
        self.version = ""

    def check_updates(self):
        logger.info("Checking for updates...")
        try:
            response = urlopen(URL, timeout=5)
            data = json.loads(response.read().decode())
            web_version = Version(data["tag_name"].lstrip("v"))
            current_version = Version(__version__)

            if current_version < web_version:
                self.version = str(web_version)
                self.download_url = data["html_url"]
                logger.info("new version found: %s", self.version)

                qs = QSettings(str(DATA_SETTINGS), QSettings.Format.IniFormat)
                qs.setValue("update_available_version", self.version)
                qs.setValue("update_download_url", self.download_url)
                self.updateAvailable.emit(self.version, self.download_url)
            else:
                logger.info("no new version available")
        except (URLError, KeyError, ValueError):
            logger.exception("error checking updates")
        finally:
            self.finished.emit()
