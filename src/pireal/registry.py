from typing import Dict, Type, TypeVar, cast

from PyQt6.QtCore import QObject

T = TypeVar("T", bound=QObject)


class Registry:
    _components: Dict[str, QObject] = {}

    @classmethod
    def register(cls, name: str, widget: QObject) -> None:
        cls._components[name] = widget

    @classmethod
    def get(cls, name: str, widget_type: Type[T]) -> T:
        widget = cls._components[name]
        if not isinstance(widget, widget_type):
            raise TypeError("error")
        return cast(T, widget)


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
