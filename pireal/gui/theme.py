from PyQt5.QtGui import QColor
from PyQt5.QtGui import QPalette


DARK = {
    'Window': QColor(53, 53, 53),
    'WindowText': QColor(255, 255, 255),
    'WindowTextDisabled': QColor(127, 127, 127),
    'Base': QColor(42, 42, 42),
    'AlternateBase': QColor(66, 66, 66),
    'ToolTipBase': QColor(255, 255, 255),
    'ToolTipText': QColor(255, 255, 255),
    'Text': QColor(255, 255, 255),
    'TextDisabled': QColor(127, 127, 127),
    'Dark': QColor(35, 35, 35),
    'Shadow': QColor(20, 20, 20),
    'Button': QColor(53, 53, 53),
    'ButtonText': QColor(255, 255, 255),
    'ButtonTextDisabled': QColor(127, 127, 127),
    'BrightText': QColor(255, 0, 0),
    'Link': QColor(42, 130, 218),
    'Highlight': QColor(43, 130, 218),
    'HighlightDisabled': QColor(80, 80, 80),
    'HighlightedText': QColor(255, 255, 255),
    'HighlightedTextDisabled': QColor(127, 127, 127)
}


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
