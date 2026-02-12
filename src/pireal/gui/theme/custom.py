import json
import logging
from dataclasses import dataclass
from pathlib import Path

from pireal.gui.theme.schema import ColorScheme, EditorColors

logger = logging.getLogger(__name__)


@dataclass
class CustomTheme:
    """
    Tema cargado desde un archivo JSON.

    Formato esperado del JSON:
    {
        "id": "my-theme",
        "name": "My Amazing Theme",
        "qt_style": "Fusion",
        "qss_file": "style.qss",  // opcional
        "colors": {
            "window": "#313131",
            "window_text": "#ffffff",
            // ... resto de colores
        }
    }
    """

    identifier: str
    name: str
    _color_scheme: ColorScheme
    _stylesheet: str = ""
    _qt_style: str = "Fusion"

    @classmethod
    def from_json(cls, path: Path) -> "CustomTheme":
        """
        Carga un tema desde un archivo theme.json.

        Args:
            path: Ruta al archivo theme.json

        Returns:
            CustomTheme configurado

        Raises:
            FileNotFoundError: Si el archivo no existe
            ValueError: Si el JSON es inválido
        """

        if not path.exists():
            raise FileNotFoundError(f"Theme file not found: {path}")

        try:
            data = json.loads(path.read_text())
        except json.JSONDecodeError as err:
            raise ValueError(f"Invalid JSON in {path}: {err}") from err

        required = ["identifier", "name", "colors"]
        missing = [field for field in required if field not in data]
        if missing:
            raise ValueError(f"Missing required fields in {path}: {missing}")

        colors = data["colors"]

        def parse_color(value):
            from PyQt6.QtGui import QColor

            if isinstance(value, str):
                return QColor(value)
            if isinstance(value, dict):
                return QColor(value["r"], value["g"], value["b"])
            raise ValueError(f"Invalid color format: {value}")

        editor = None
        if "editor" in colors:
            try:
                editor = EditorColors.from_dict(colors["editor"])
            except (KeyError, ValueError) as e:
                logger.warning(
                    f"Invalid editor colors in {path}: {e}, deriving automatically"
                )

        try:

            color_scheme = ColorScheme.create(
                window=parse_color(colors["window"]),
                window_text=parse_color(colors["window_text"]),
                base=parse_color(colors["base"]),
                alternate_base=parse_color(colors["alternate_base"]),
                text=parse_color(colors["text"]),
                button=parse_color(colors["button"]),
                button_text=parse_color(colors["button_text"]),
                highlight=parse_color(colors["highlight"]),
                highlighted_text=parse_color(colors["highlighted_text"]),
                link=parse_color(colors["link"]) if "link" in colors else None,
                tooltip_base=parse_color(colors["tooltip_base"])
                if "tooltip_base" in colors
                else None,
                tooltip_text=parse_color(colors["tooltip_text"])
                if "tooltip_text" in colors
                else None,
                fade_color=parse_color(colors["fade_color"])
                if "fade_color" in colors
                else None,
                fade_amount=float(colors.get("fade_amount", 0.5)),
                editor=editor,  # None = se deriva automáticamente
            )
        except KeyError as err:
            raise ValueError(f"Missing color field in {path}: {err}") from err

        # Cargar QSS si existe
        stylesheet = ""
        qss_file = data.get("qss_file")
        if qss_file:
            qss_path = path.parent / qss_file
            if qss_path.exists():
                stylesheet = qss_path.read_text(encoding="utf-8")
                logger.debug(f"Loaded stylesheet from {qss_path}")
            else:
                logger.warning(f"QSS file not found: {qss_path}")

        return cls(
            identifier=data["identifier"],
            name=data["name"],
            _color_scheme=color_scheme,
            _stylesheet=stylesheet,
            _qt_style=data.get("qt_style", "Fusion"),
        )

    def color_scheme(self) -> ColorScheme:
        return self._color_scheme

    def stylesheet(self) -> str:
        return self._stylesheet

    def qt_style(self) -> str:
        return self._qt_style


def discover_themes(themes_dir: Path) -> list[CustomTheme]:
    """
    Args:
        themes_dir: Directorio raíz de temas

    Returns:
        Lista de CustomTheme cargados

    Example:
        >>> themes_dir = Path("~/.pireal/themes").expanduser()
        >>> custom_themes = discover_themes(themes_dir)
        >>> for theme in custom_themes:
        ...     print(theme.name)
    """
    if not themes_dir.exists():
        logger.info(f"Themes directory does not exist: {themes_dir}")
        return []

    themes = []
    for theme_file in themes_dir.rglob("theme.json"):
        try:
            theme = CustomTheme.from_json(theme_file)
            themes.append(theme)
            logger.info(f"Loaded custom theme: {theme.name} from {theme_file}")
        except (FileNotFoundError, ValueError) as e:
            logger.error(f"Failed to load theme from {theme_file}: {e}")

    return themes
