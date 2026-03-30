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

from typing import TypeVar

from PyQt6.QtCore import QObject

T = TypeVar("T", bound=QObject)


class Registry:
    _components: dict[str, QObject] = {}

    @classmethod
    def register(cls, name: str, widget: QObject) -> None:
        cls._components[name] = widget

    @classmethod
    def get(cls, name: str, widget_type: type[T]) -> T:
        widget = cls._components[name]
        if not isinstance(widget, widget_type):
            raise TypeError("error")
        return widget


# from functools import wraps
# from typing import ClassVar, Dict, Optional, Type, TypeVar, cast
#
# from PyQt6.QtCore import QObject
#
# T = TypeVar("T", bound=QObject)
#
#
# class Registry:
#     def __init__(self):
#         self._instances: Dict[str, QObject] = {}
#
#     def register(self, name: str, instance: QObject) -> QObject:
#         self._instances[name] = instance
#         return instance
#
#     def get(self, name: str) -> Optional[QObject]:
#         return self._instances.get(name)
#
#     def get_typed(self, name: str, obj_type: Type[T]) -> Optional[T]:
#         obj = self._instances.get(name)
#         if obj is not None and isinstance(obj, obj_type):
#             return cast(obj_type, obj)
#         return None
#
#
# class AutoRegistered:
#     registry_name: ClassVar[Optional[str]] = None
#
#     def __init_subclass__(cls, **kwargs) -> None:
#         super().__init_subclass__(**kwargs)
#
# #        if not issubclass(cls, QObject):
#             return
#         name = cls.registry_name or cls.__name__
#
#         original_init = cls.__init__
#
#         @wraps(original_init)
#         def init_and_register(self, *args, **kwargs):
#             from pireal.gui.main_window import Pireal
#
#             original_init(self, *args, **kwargs)
#             instance_name = kwargs.pop("registry_name", name)
#             pireal_instance = Pireal.instance()
#             if pireal_instance:
#                 if instance_name != name or not pireal_instance.get(name):
#                     pireal_instance.register(instance_name, self)
#
#         cls.__init__ = init_and_register
#
#
# def register_widget(name: str):
#     def decorator(cls):
#         if not issubclass(cls, QObject):
#             raise RuntimeError(f"{cls.__name__} debe heredar de QObject")
#         registry_name = name or cls.__name__
#         Registry.register
