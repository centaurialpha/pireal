from dataclasses import dataclass

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

from pireal.gui.theme.schema import ColorScheme, EditorColors


@dataclass(frozen=True)
class DarkTheme:
    identifier: str = "dark"
    name: str = "Dark"

    def color_scheme(self) -> ColorScheme:
        editor = EditorColors(
            keyword=QColor("#F92672"),  # Rosa/magenta
            variable=QColor("#A6E22E"),  # Verde
            operator=QColor("#F92672"),  # Rosa
            number=QColor("#AE81FF"),  # Púrpura
            string=QColor("#E6DB74"),  # Amarillo
            comment=QColor("#75715E"),  # Gris oliva
            foreground=QColor("#F8F8F2"),  # Blanco hueso
            background=QColor("#272822"),  # Gris oscuro
            current_line=QColor("#3E3D32"),  # Gris medio
            line_number_fg=QColor("#90908A"),
            line_number_bg=QColor("#272822"),
            selection_bg=QColor("#49483E"),
            selection_fg=QColor("#F8F8F2"),
            bracket_match=QColor("#FFE792"),
            bracket_mismatch=QColor("#F92672"),
            sidebar_background=QColor("#90908A"),
            sidebar_foreground=QColor("#1E1F1C"),
        )

        return ColorScheme.create(
            window=QColor(49, 49, 49),
            window_text=QColor(Qt.GlobalColor.white),
            base=QColor(34, 34, 34),
            alternate_base=QColor(42, 42, 42),
            text=QColor(Qt.GlobalColor.white),
            button=QColor(48, 48, 48),
            button_text=QColor(Qt.GlobalColor.white),
            highlight=QColor(150, 219, 89),
            highlighted_text=QColor(Qt.GlobalColor.black),
            link=QColor(47, 163, 198),
            tooltip_base=QColor(42, 130, 218),
            tooltip_text=QColor(Qt.GlobalColor.white),
            fade_color=QColor(49, 49, 49),
            fade_amount=0.5,
            editor=editor,
        )

    def stylesheet(self) -> str:
        return """
        QToolTip {
            color: #ffffff;
            background-color: #2a82da;
            border: 1px solid white;
            padding: 4px;
            border-radius: 3px;
        }
        QPushButton:hover {
            background-color: #505050;
        }
        QPushButton:pressed {
            background-color: #404040;
        }
        """

    def qt_style(self) -> str:
        return "Fusion"


@dataclass(frozen=True)
class LightTheme:
    identifier: str = "light"
    name: str = "Light"

    def color_scheme(self) -> ColorScheme:
        editor = EditorColors(
            keyword=QColor("#0000FF"),  # Azul
            variable=QColor("#008080"),  # Teal
            operator=QColor("#000080"),  # Navy
            number=QColor("#800080"),  # Púrpura
            string=QColor("#008000"),  # Verde oscuro
            comment=QColor("#808080"),  # Gris
            foreground=QColor("#000000"),
            background=QColor("#FFFFFF"),
            current_line=QColor("#F0F0F0"),
            line_number_fg=QColor("#808080"),
            line_number_bg=QColor("#FFFFFF"),
            selection_bg=QColor("#B4D5FE"),
            selection_fg=QColor("#000000"),
            bracket_match=QColor("#FFD700"),
            bracket_mismatch=QColor("#FF0000"),
            sidebar_background=QColor("#ffffff"),
            sidebar_foreground=QColor("#000000"),
        )

        return ColorScheme.create(
            window=QColor(240, 240, 240),
            window_text=QColor(Qt.GlobalColor.black),
            base=QColor(Qt.GlobalColor.white),
            alternate_base=QColor(245, 245, 245),
            text=QColor(Qt.GlobalColor.black),
            button=QColor(225, 225, 225),
            button_text=QColor(Qt.GlobalColor.black),
            highlight=QColor(0, 120, 215),
            highlighted_text=QColor(Qt.GlobalColor.white),
            link=QColor(0, 102, 204),
            tooltip_base=QColor(255, 255, 220),
            tooltip_text=QColor(Qt.GlobalColor.black),
            fade_color=QColor(200, 200, 200),
            fade_amount=0.4,
            editor=editor,
        )

    def stylesheet(self) -> str:
        return """
        QToolTip {
            color: #000000;
            background-color: #ffffdc;
            border: 1px solid #999999;
            padding: 4px;
            border-radius: 3px;
        }
        QPushButton:hover {
            background-color: #d0d0d0;
        }
        QPushButton:pressed {
            background-color: #c0c0c0;
        }
        """

    def qt_style(self) -> str:
        return "Fusion"
