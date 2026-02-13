from dataclasses import dataclass

from PyQt6.QtGui import QColor

from pireal.gui.theme.schema import ColorScheme, EditorColors


@dataclass(frozen=True)
class DarkTheme:
    identifier: str = "dark"
    name: str = "Dark"

    def color_scheme(self) -> ColorScheme:
        editor = EditorColors(
            keyword=QColor("#c678dd"),
            variable=QColor("#e06c75"),
            operator=QColor("#56b6c2"),
            number=QColor("#d19a66"),
            string=QColor("#98c379"),
            comment=QColor("#5c6370"),
            foreground=QColor("#c8cdd4"),
            background=QColor("#282c34"),
            current_line=QColor("#2c313a"),
            line_number_fg=QColor("#4b5263"),
            line_number_bg=QColor("#21252b"),
            selection_bg=QColor("#528bff"),
            selection_fg=QColor("#ffffff"),
            bracket_match=QColor("#528bff"),
            bracket_mismatch=QColor("#e06c75"),
            sidebar_background=QColor("#21252b"),
            sidebar_foreground=QColor("#4b5263"),
            error=QColor("#e06c75"),
        )

        return ColorScheme.create(
            window=QColor("#21252b"),
            window_text=QColor("#c8cdd4"),
            base=QColor("#282c34"),
            alternate_base=QColor("#2c313a"),
            text=QColor("#c8cdd4"),
            button=QColor("#21252b"),
            button_text=QColor("#c8cdd4"),
            highlight=QColor("#528bff"),
            highlighted_text=QColor("#ffffff"),
            link=QColor("#56b6c2"),
            tooltip_base=QColor("#21252b"),
            tooltip_text=QColor("#c8cdd4"),
            fade_color=QColor("#21252b"),
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
            keyword=QColor("#cf222e"),
            variable=QColor("#953800"),
            operator=QColor("#0550ae"),
            number=QColor("#0550ae"),
            string=QColor("#0a3069"),
            comment=QColor("#6e7781"),
            foreground=QColor("#24292f"),
            background=QColor("#ffffff"),
            current_line=QColor("#f0f0f0"),
            line_number_fg=QColor("#8c959f"),
            line_number_bg=QColor("#f6f8fa"),
            selection_bg=QColor("#0969da"),
            selection_fg=QColor("#ffffff"),
            bracket_match=QColor("#0969da"),
            bracket_mismatch=QColor("#cf222e"),
            sidebar_background=QColor("#f6f8fa"),
            sidebar_foreground=QColor("#8c959f"),
            error=QColor("#cf222e"),
        )
        return ColorScheme.create(
            window=QColor("#f6f8fa"),
            window_text=QColor("#24292f"),
            base=QColor("#ffffff"),
            alternate_base=QColor("#f6f8fa"),
            text=QColor("#24292f"),
            button=QColor("#f6f8fa"),
            button_text=QColor("#24292f"),
            highlight=QColor("#0969da"),
            highlighted_text=QColor("#ffffff"),
            link=QColor("#0550ae"),
            tooltip_base=QColor("#f6f8fa"),
            tooltip_text=QColor("#24292f"),
            fade_color=QColor("#f6f8fa"),
            fade_amount=0.3,
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
