# Copyright 2015-2026 - Gabriel Acosta <acostadariogabriel@gmail.com>
#
# This file is part of Pireal.
#
# Pireal is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# any later version.
#
# Pireal is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Pireal; If not, see <http://www.gnu.org/licenses/>.

from PyQt6.QtGui import QColor


def blend_colors(c1: QColor, c2: QColor, bias: float) -> QColor:
    """Mezcla dos colores con un bias determinado.

    Similar a Rainbow::mix de PrismLauncher.

    Args:
        c1: Color base
        c2: Color a mezclar
        bias: Cantidad de c2 a usar (0.0 = solo c1, 1.0 = solo c2)

    Returns:
        Color resultante de la mezcla

    Example:
        >>> black = QColor(0, 0, 0)
        >>> white = QColor(255, 255, 255)
        >>> gray = blend_colors(black, white, 0.5)
        >>> gray.red()
        127
    """
    if not 0.0 <= bias <= 1.0:
        raise ValueError(f"bias must be between 0.0 and 1.0, got {bias}")

    inverse_bias = 1.0 - bias

    return QColor(
        int(c1.red() * inverse_bias + c2.red() * bias),
        int(c1.green() * inverse_bias + c2.green() * bias),
        int(c1.blue() * inverse_bias + c2.blue() * bias),
        int(c1.alpha() * inverse_bias + c2.alpha() * bias),
    )


def luminance(color: QColor) -> float:
    """Calcula la luminancia relativa de un color.

    Usa la fórmula ITU-R BT.709.

    Args:
        color: Color a analizar

    Returns:
        Luminancia entre 0.0 (negro) y 1.0 (blanco)
    """
    r = color.redF()
    g = color.greenF()
    b = color.blueF()

    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def adjust_luminance(color: QColor, factor: float) -> QColor:
    """Ajusta la luminancia de un color.

    Args:
        color: Color base
        factor: Factor de ajuste (> 1 = más claro, < 1 = más oscuro)

    Returns:
        Color con luminancia ajustada
    """
    h, s, l, a = color.getHslF()
    l = min(1.0, max(0.0, l * factor))

    result = QColor()
    result.setHslF(h, s, l, a)
    return result


def is_dark_color(color: QColor, threshold: float = 0.5) -> bool:
    """Determina si un color es oscuro.

    Args:
        color: Color a evaluar
        threshold: Umbral de luminancia (default 0.5)

    Returns:
        True si el color es oscuro
    """
    return luminance(color) < threshold


def rotate_hue(color: QColor, degrees: int) -> QColor:
    """Rota el hue de un color."""
    h, s, l, a = color.getHslF()
    h = (h + degrees / 360.0) % 1.0

    result = QColor()
    result.setHslF(h, s, l, a)
    return result
