from PySide2.QtGui import QPalette
from PySide2.QtGui import QColor

_DARK = {
    'Window': '#303030',
    'WindowText': '#FFFFFF',
    'Base': '#454545',
    'AlternateBase': 'red',
    'ToolTipBase': 'yellow',
    'ToolTipText': 'red',
    'Text': '#F1F1F1',
    'Button': '#404040',
    'ButtonDisabled': '#606060',
    'ButtonText': '#FFFFFF',
    'ButtonTextDisabled': 'white',
    'BrightText': 'red',
    'Light': 'green',
    'Midlight': 'red',
    'Dark': 'black',
    'Mid': 'cyan',
    'Shadow': 'red'
}

_LIGHT = {
    'MAIN_COLOR': '#FFFFFF'
}

STYLE = {
    'dark': _DARK,
    'light': _LIGHT
}


def load_palette():
    style = STYLE.get('dark')
    palette = QPalette()
    for role, color in style.items():
        qcolor = QColor(color)
        color_group = QPalette.All
        if role.endswith('Disabled'):
            role = role.split('Disabled')[0]
            color_group = QPalette.Disabled
        color_role = getattr(palette, role)
        palette.setBrush(color_group, color_role, qcolor)
    return palette
