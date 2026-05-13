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

import logging
from typing import TypeVar

from PyQt6.QtCore import QObject

T = TypeVar("T", bound=QObject)


logger = logging.getLogger(__name__)


class Registry:
    _components: dict[str, QObject] = {}

    @classmethod
    def register(cls, name: str, widget: QObject) -> None:
        if name in cls._components:
            logger.warning("Overwriting registry component '%s'", name)
        cls._components[name] = widget

    @classmethod
    def get(cls, name: str, widget_type: type[T]) -> T:
        if name not in cls._components:
            raise KeyError(f"Component '{name}' is not registered")
        widget = cls._components[name]
        if not isinstance(widget, widget_type):
            raise TypeError(f"Component '{name}' is {type(widget).__name__}, expected {widget_type.__name__}")
        return widget

    @classmethod
    def clear(cls) -> None:
        cls._components.clear()
