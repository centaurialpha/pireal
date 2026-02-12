import json
import logging
from dataclasses import dataclass
from pathlib import Path

from pireal.gui.theme.schema import ColorScheme

logger = logging.getLogger(__name__)


@dataclass
class CustomTheme:
    """Tema cargado desde un archivo JSON.

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

    id: str
    name: str
    _color_scheme: ColorScheme
    _stylesheet: str = ""
    _qt_style: str = "Fusion"

    @classmethod
    def from_json(cls, path: Path) -> "CustomTheme":
        """Carga un tema desde un archivo theme.json.

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
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in {path}: {e}") from e

        required_fields = ["id", "name", "colors"]
        missing = [f for f in required_fields if f not in data]
        if missing:
            raise ValueError(f"Missing required fields in {path}: {missing}")

        try:
            color_scheme = ColorScheme.from_dict(data["colors"])
        except (KeyError, ValueError) as e:
            raise ValueError(f"Invalid colors in {path}: {e}") from e

        stylesheet = ""
        qss_file = data.get("qss_file")
        if qss_file:
            qss_path = path.parent / qss_file
            if qss_path.exists():
                stylesheet = qss_path.read_text(encoding="utf-8")
                logger.info(f"Loaded stylesheet from {qss_path}")
            else:
                logger.warning(f"QSS file not found: {qss_path}")

        return cls(
            id=data["id"],
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
