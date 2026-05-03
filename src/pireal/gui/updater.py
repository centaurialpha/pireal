# Copyright 2015-2026 - Gabriel Acosta <acostadariogabriel@gmail.com>
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
from urllib.request import Request, urlopen

from packaging.version import Version
from PyQt6.QtCore import (
    QObject,
    pyqtSignal,
)

from pireal import __version__

logger = logging.getLogger("updater")

UPDATE_URL = "https://gabox.dev/pireal_version.json"


class Updater(QObject):
    finished = pyqtSignal()
    updateAvailable = pyqtSignal(str, str)

    def __init__(self, url: str = UPDATE_URL):
        QObject.__init__(self)
        self._url = url

    def check_updates(self):
        logger.info("Checking for updates...")
        try:
            request = Request(self._url, headers={"User-Agent": "pireal-updater"})
            response = urlopen(request, timeout=5)
            data = json.loads(response.read().decode())
            web_version = Version(data["version"])
            current_version = Version(__version__)

            if current_version < web_version:
                logger.info("new version found: %s", web_version)
                self.updateAvailable.emit(str(web_version), data["url"])
            else:
                logger.info("no new version available")
        except (URLError, KeyError, ValueError):
            logger.exception("error checking updates")
        finally:
            self.finished.emit()
