from PyQt5.QtGui import QColor
from PyQt5.QtGui import QPalette

from pireal.core.settings import USER_SETTINGS

DARK = {
    'Window': '#131217',
    'WindowText': QColor(255, 255, 255),
    'WindowTextDisabled': QColor(127, 127, 127),
    'Base': '#212227',
    'AlternateBase': QColor(66, 66, 66),
    'ToolTipBase': QColor(255, 255, 255),
    'ToolTipText': QColor(255, 255, 255),
    'Text': QColor(255, 255, 255),
    'TextDisabled': QColor(80, 80, 80),
    'Dark': QColor(35, 35, 35),
    'Shadow': QColor(20, 20, 20),
    'Button': '#191a1f',
    'ButtonText': QColor(255, 255, 255),
    'ButtonTextDisabled': QColor(127, 127, 127),
    'BrightText': '#ff0000',
    'Link': QColor(42, 130, 218),
    'Highlight': QColor(43, 130, 218),
    'HighlightDisabled': QColor(80, 80, 80),
    'HighlightedText': QColor(255, 255, 255),
    'HighlightedTextDisabled': QColor(127, 127, 127)
}


EDITOR_DARK = {
    # Editor
    'background': '#282a36',
    'foreground': '#f8f8f2',
    'sidebar_background': '#282a36',
    'sidebar_foreground': '#f8f8f2',
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
    'sidebar_foreground': '#000000'
}


# FIXME: se llama repetidas veces
# En lugar de llamar siempre a esta funcion, guardar referencia
def get_editor_color(key):
    if USER_SETTINGS.dark_mode:
        return EDITOR_DARK[key]
    return EDITOR_LIGHT[key]


def apply_dark_mode(app):
    palette = QPalette()
    for role_name, color in DARK.items():
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


def reset_theme(app):
    app.setPalette(app.style().standardPalette())
