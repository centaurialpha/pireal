from typing import Protocol

from pireal.gui.theme.schema import ColorScheme


class Theme(Protocol):
    @property
    def identifier(self) -> str: ...

    @property
    def name(self) -> str: ...

    def color_scheme(self) -> ColorScheme: ...

    def stylesheet(self) -> str: ...

    def qt_style(self) -> str: ...
