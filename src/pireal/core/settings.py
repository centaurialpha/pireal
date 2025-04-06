# Copyright 2015-2025 - Gabriel Acosta <acostadariogabriel@gmail.com>
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


from typing import Any

from PyQt6.QtCore import QSettings


class SettingManager:
    def __init__(self):
        self._settings = QSettings()

    def get(self, key: str, default: Any = None) -> Any:
        if self._settings.contains(key):
            if default is not None:
                return self._settings.value(key, default, type=type(default))
            return self._settings.value(key, default)
        return default

    def set(self, key: str, value: Any) -> None:
        self._settings.setValue(key, value)


_manager = SettingManager()

DARK_MODE = _manager.get("DARK_MODE", False)


def set(name: str, value: Any) -> None:
    _manager.set(name, value)
    if name in globals():
        globals()[name] = value
