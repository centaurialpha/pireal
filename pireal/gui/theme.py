from PyQt5.QtGui import QColor
from PyQt5.QtGui import QPalette

from pireal.settings import SETTINGS

DARK = {
    'Window': '#171a21',
    'WindowText': '#ffffff',
    'WindowTextDisabled': '#7f7f7f',
    'Base': '#282a36',
    'AlternateBase': '#1c1e26',
    'ToolTipBase': '#2e3139',
    'ToolTipText': '#ffffff',
    'Text': '#dddddd',
    'TextDisabled': '#505050',
    'Dark': '#232323',
    'Shadow': '#323228',
    'Button': '#191a1f',
    'ButtonText': '#ffffff',
    'ButtonTextDisabled': '#7f7f7f',
    'BrightText': '#ec7875',
    'Link': '#2a82da',
    'Highlight': '#42539e',
    'Mid': '#404040',
    'Midlight': '#ff0000',
    'HighlightDisabled': '#505050',
    'HighlightedText': '#f1f1f1',
    'HighlightedTextDisabled': '#7f7f7f'
}


LIGHT = {
    'Highlight': '#7742539e',
    'BrightText': '#ec7875',
    'Dark': '#dddddd'
}

EDITOR_DARK = {
    # Editor
    'background': '#282a36',
    'foreground': '#f8f8f2',
    'sidebar_background': '#282a36',
    'sidebar_foreground': '#6272a4',
    'current_line': '#383b4c',
    # Hihglighter
    'keyword': '#7ce4fb',
    'number': '#bd93f9',
    'string': '#f1fa8c',
    'comment': '#6272a4',
    'operator': '#ffffff',
    'variable': '#ffb86c',
}

EDITOR_LIGHT = {
    'background': '#ffffff',
    'foreground': '#000000',
    'sidebar_background': '#ffffff',
    'sidebar_foreground': '#000000',
    'current_line': '#eeeeee',
    'keyword': '#808000',
    'number': '#000080',
    'string': '#008000',
    'comment': '#008000',
    'operator': '#000000',
    'variable': '#800000',
}


# FIXME: se llama repetidas veces
# En lugar de llamar siempre a esta funcion, guardar referencia
def get_editor_color(key):
    if SETTINGS.dark_mode:
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
        if role_name.endswith('Disabled'):
            role_name = role_name.split('Disabled')[0]
            color_group = QPalette.Disabled
        else:
            color_group = QPalette.All
        if not isinstance(color, QColor):
            qcolor = QColor(color)
        else:
            qcolor = color
        color_role = getattr(palette, role_name)
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
