from PyQt6.QtGui import QColor, QPalette

from pireal.settings import SETTINGS
from pireal.core import settings

DARK = {
    "Window": "#171a21",
    "WindowText": "#ffffff",
    "WindowTextDisabled": "#7f7f7f",
    "Base": "#282a36",
    "AlternateBase": "#1c1e26",
    "ToolTipBase": "#2e3139",
    "ToolTipText": "#ffffff",
    "Text": "#dddddd",
    "TextDisabled": "#505050",
    "Dark": "#232323",
    "Shadow": "#323228",
    "Button": "#191a1f",
    "ButtonText": "#ffffff",
    "ButtonTextDisabled": "#7f7f7f",
    "BrightText": "#ec7875",
    "Link": "#2a82da",
    "Highlight": "#42539e",
    "Mid": "#404040",
    "Midlight": "#ff0000",
    "HighlightDisabled": "#505050",
    "HighlightedText": "#f1f1f1",
    "HighlightedTextDisabled": "#7f7f7f",
}


LIGHT = {"Highlight": "#7742539e", "BrightText": "#ec7875", "Dark": "#dddddd"}

EDITOR_LIGHT = {
    "background": "#ffffff",
    "foreground": "#282a36",
    "sidebar_background": "#f0f0f0",
    "sidebar_foreground": "#44475a",
    "current_line": "#eaeaea",
    "keyword": "#9c27b0",
    "number": "#bd93f9",
    "string": "#2a9d8f",
    "comment": "#6272a4",
    "operator": "#ff5555",
    "variable": "#5c6bc0",
}

EDITOR_DARK = {
    "background": "#282a36",
    "foreground": "#f8f8f2",
    "sidebar_background": "#21222c",
    "sidebar_foreground": "#f8f8f2",
    "current_line": "#44475a",
    "keyword": "#c792ea",
    "number": "#bd93f9",
    "string": "#50fa7b",
    "comment": "#6272a4",
    "operator": "#ff5555",
    "variable": "#8be9fd",
}


# FIXME: se llama repetidas veces
# En lugar de llamar siempre a esta funcion, guardar referencia
def get_editor_color(key):
    if settings.DARK_MODE:
        return EDITOR_DARK[key]
    return EDITOR_LIGHT[key]


def apply_theme(app):
    if SETTINGS.dark_mode:
        theme = DARK
    else:
        theme = LIGHT
        app.setPalette(app.style().standardPalette())
    palette = QPalette()
    for role_name, color in theme.items():
        if role_name.endswith("Disabled"):
            role_name = role_name.split("Disabled")[0]
            color_group = QPalette.ColorGroup.Disabled
        else:
            color_group = QPalette.ColorGroup.All
        if not isinstance(color, QColor):
            qcolor = QColor(color)
        else:
            qcolor = color
        color_role = getattr(palette.ColorRole, role_name)
        palette.setBrush(color_group, color_role, qcolor)
    app.setPalette(palette)


def get_color(name: str):
    if SETTINGS.dark_mode:
        colors = DARK
    else:
        colors = LIGHT
    color = colors[name]
    if not isinstance(color, QColor):
        color = QColor(color)
    return color
