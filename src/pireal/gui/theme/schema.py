from dataclasses import dataclass
from enum import Enum
from typing import Any

from PyQt6.QtGui import QColor, QPalette

from pireal.gui.theme.utils import adjust_luminance, blend_colors, rotate_hue


class EditorColorRole(Enum):
    KEYWORD = "keyword"
    VARIABLE = "variable"
    OPERATOR = "operator"
    NUMBER = "number"
    STRING = "string"
    COMMENT = "comment"
    FOREGROUND = "foreground"
    BACKGROUND = "background"
    CURRENT_LINE = "current_line"
    LINE_NUMBER_FG = "line_number_fg"
    LINE_NUMBER_BG = "line_number_bg"
    SELECTION_BG = "selection_bg"
    SELECTION_FG = "selection_fg"
    BRACKET_MATCH = "bracket_match"
    BRACKET_MISMATCH = "bracket_mismatch"
    SIDEBAR_FOREGROUND = "sidebar_foreground"
    SIDEBAR_BACKGROUND = "sidebar_background"
    ERROR = "error"


@dataclass(frozen=True)
class EditorColors:
    # Syntax highlighting
    keyword: QColor
    variable: QColor
    operator: QColor
    number: QColor
    string: QColor
    comment: QColor

    # Editor UI
    foreground: QColor
    background: QColor
    current_line: QColor
    line_number_fg: QColor
    line_number_bg: QColor
    selection_bg: QColor
    selection_fg: QColor
    bracket_match: QColor
    bracket_mismatch: QColor
    sidebar_background: QColor
    sidebar_foreground: QColor
    error: QColor

    def get(self, role: EditorColorRole) -> QColor:
        """Obtiene un color por role (type-safe).

        Args:
            role: EditorColorRole enum

        Returns:
            QColor correspondiente
        """
        mapping = {
            EditorColorRole.KEYWORD: self.keyword,
            EditorColorRole.VARIABLE: self.variable,
            EditorColorRole.OPERATOR: self.operator,
            EditorColorRole.NUMBER: self.number,
            EditorColorRole.STRING: self.string,
            EditorColorRole.COMMENT: self.comment,
            EditorColorRole.FOREGROUND: self.foreground,
            EditorColorRole.BACKGROUND: self.background,
            EditorColorRole.CURRENT_LINE: self.current_line,
            EditorColorRole.LINE_NUMBER_FG: self.line_number_fg,
            EditorColorRole.LINE_NUMBER_BG: self.line_number_bg,
            EditorColorRole.SELECTION_BG: self.selection_bg,
            EditorColorRole.SELECTION_FG: self.selection_fg,
            EditorColorRole.BRACKET_MATCH: self.bracket_match,
            EditorColorRole.BRACKET_MISMATCH: self.bracket_mismatch,
            EditorColorRole.SIDEBAR_BACKGROUND: self.sidebar_background,
            EditorColorRole.SIDEBAR_FOREGROUND: self.sidebar_foreground,
            EditorColorRole.ERROR: self.error,
        }
        return mapping[role]

    @classmethod
    def derive_from_palette(
        cls,
        base: QColor,
        text: QColor,
        highlight: QColor,
        highlighted_text: QColor,
        alternate_base: QColor,
    ) -> "EditorColors":
        """Deriva colores del editor desde una paleta base.

        Algoritmo inteligente que genera colores harmoniosos.
        """
        # Syntax colors basados en highlight
        keyword = adjust_luminance(highlight, 1.1)
        variable = highlight
        operator = adjust_luminance(highlight, 0.85)

        # Colores distintivos pero harmoniosos
        number = rotate_hue(highlight, 60)  # Naranja/amarillo
        string = rotate_hue(highlight, -60)  # Verde/cyan
        comment = blend_colors(text, base, 0.5)  # Gris medio

        # UI colors
        current_line = blend_colors(base, alternate_base, 0.5)
        line_number_fg = blend_colors(text, base, 0.6)
        line_number_bg = base

        sidebar_bg = blend_colors(base, QColor(0, 0, 0), 0.1)
        sidebar_fg = line_number_fg

        return cls(
            keyword=keyword,
            variable=variable,
            operator=operator,
            number=number,
            string=string,
            comment=comment,
            foreground=text,
            background=base,
            current_line=current_line,
            line_number_fg=line_number_fg,
            line_number_bg=line_number_bg,
            selection_bg=highlight,
            selection_fg=highlighted_text,
            bracket_match=QColor(255, 255, 0),  # Amarillo
            bracket_mismatch=QColor(255, 0, 0),  # Rojo
            sidebar_background=sidebar_bg,
            sidebar_foreground=sidebar_fg,
            error=QColor("#DD4040"),
        )

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "EditorColors":
        """Crea desde diccionario (para JSON)."""

        def parse_color(value: str | dict | Any) -> QColor:
            if isinstance(value, str):
                return QColor(value)
            if isinstance(value, dict):
                return QColor(value["r"], value["g"], value["b"])
            raise ValueError(f"Invalid color format: {value}")

        return cls(
            keyword=parse_color(data["keyword"]),
            variable=parse_color(data["variable"]),
            operator=parse_color(data["operator"]),
            number=parse_color(data["number"]),
            string=parse_color(data["string"]),
            comment=parse_color(data["comment"]),
            foreground=parse_color(data["foreground"]),
            background=parse_color(data["background"]),
            current_line=parse_color(data["current_line"]),
            line_number_fg=parse_color(data["line_number_fg"]),
            line_number_bg=parse_color(data["line_number_bg"]),
            selection_bg=parse_color(data["selection_bg"]),
            selection_fg=parse_color(data["selection_fg"]),
            bracket_match=parse_color(data.get("bracket_match", "#ffff00")),
            bracket_mismatch=parse_color(data.get("bracket_mismatch", "#ff0000")),
            sidebar_background=parse_color(
                data.get("sidebar_background", data.get("background", "#ffffff"))
            ),
            sidebar_foreground=parse_color(
                data.get("sidebar_foreground", data.get("line_number_fg", "#808080"))
            ),
            error=parse_color(data["error"]),
        )


@dataclass(frozen=True)
class ColorScheme:
    window: QColor
    window_text: QColor
    base: QColor
    alternate_base: QColor
    text: QColor
    button: QColor
    button_text: QColor
    highlight: QColor
    highlighted_text: QColor

    link: QColor
    tooltip_base: QColor
    tooltip_text: QColor

    fade_color: QColor
    fade_amount: float

    editor: EditorColors

    @classmethod
    def create(
        cls,
        *,
        window: QColor,
        window_text: QColor,
        base: QColor,
        alternate_base: QColor,
        text: QColor,
        button: QColor,
        button_text: QColor,
        highlight: QColor,
        highlighted_text: QColor,
        link: QColor | None = None,
        tooltip_base: QColor | None = None,
        tooltip_text: QColor | None = None,
        fade_color: QColor | None = None,
        fade_amount: float = 0.5,
        editor: EditorColors | None = None,
    ) -> "ColorScheme":
        """Factory method con defaults inteligentes."""
        # Defaults
        link = link or QColor(47, 163, 198)
        tooltip_base = tooltip_base or QColor(255, 255, 220)
        tooltip_text = tooltip_text or QColor(0, 0, 0)
        fade_color = fade_color or window

        # Generar editor colors si no se proveen
        if editor is None:
            editor = EditorColors.derive_from_palette(
                base=base,
                text=text,
                highlight=highlight,
                highlighted_text=highlighted_text,
                alternate_base=alternate_base,
            )

        return cls(
            window=window,
            window_text=window_text,
            base=base,
            alternate_base=alternate_base,
            text=text,
            button=button,
            button_text=button_text,
            highlight=highlight,
            highlighted_text=highlighted_text,
            link=link,
            tooltip_base=tooltip_base,
            tooltip_text=tooltip_text,
            fade_color=fade_color,
            fade_amount=fade_amount,
            editor=editor,
        )

    def to_palette(self) -> QPalette:
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, self.window)
        palette.setColor(QPalette.ColorRole.WindowText, self.window_text)
        palette.setColor(QPalette.ColorRole.Base, self.base)
        palette.setColor(QPalette.ColorRole.AlternateBase, self.alternate_base)
        palette.setColor(QPalette.ColorRole.Text, self.text)
        palette.setColor(QPalette.ColorRole.Button, self.button)
        palette.setColor(QPalette.ColorRole.ButtonText, self.button_text)
        palette.setColor(QPalette.ColorRole.Highlight, self.highlight)
        palette.setColor(QPalette.ColorRole.HighlightedText, self.highlighted_text)
        palette.setColor(QPalette.ColorRole.Link, self.link)
        palette.setColor(QPalette.ColorRole.ToolTipBase, self.tooltip_base)
        palette.setColor(QPalette.ColorRole.ToolTipText, self.tooltip_text)

        return self._apply_fade(palette)

    def _apply_fade(self, palette: QPalette) -> QPalette:
        roles = [
            QPalette.ColorRole.Window,
            QPalette.ColorRole.WindowText,
            QPalette.ColorRole.Base,
            QPalette.ColorRole.AlternateBase,
            QPalette.ColorRole.Text,
            QPalette.ColorRole.Button,
            QPalette.ColorRole.ButtonText,
            QPalette.ColorRole.Highlight,
            QPalette.ColorRole.HighlightedText,
            QPalette.ColorRole.Link,
        ]

        for role in roles:
            active_color = palette.color(QPalette.ColorGroup.Active, role)
            faded = blend_colors(active_color, self.fade_color, self.fade_amount)
            palette.setColor(QPalette.ColorGroup.Disabled, role, faded)

        return palette

    def to_dict(self) -> dict[str, Any]:
        return {
            "window": self.window.name(),
            "window_text": self.window_text.name(),
            "base": self.base.name(),
            "alternate_base": self.alternate_base.name(),
            "text": self.text.name(),
            "button": self.button.name(),
            "button_text": self.button_text.name(),
            "highlight": self.highlight.name(),
            "highlighted_text": self.highlighted_text.name(),
            "link": self.link.name(),
            "tooltip_base": self.tooltip_base.name(),
            "tooltip_text": self.tooltip_text.name(),
            "fade_color": self.fade_color.name(),
            "fade_amount": self.fade_amount,
        }
