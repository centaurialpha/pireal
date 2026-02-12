import pytest
from PyQt6.QtWidgets import QApplication

from pireal.gui.theme.manager import ThemeManager


@pytest.fixture
def app():
    """Fixture para QApplication."""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app


def test_manager_initialization(app):
    manager = ThemeManager()

    available = manager.themes()
    theme_ids = [tid for tid, _ in available]

    assert "dark" in theme_ids
    assert "light" in theme_ids
    assert "system" in theme_ids


def test_apply_theme(app):
    manager = ThemeManager()

    manager.apply("dark")
    assert manager.current_id == "dark"
    assert manager.current.name == "Dark"

    manager.apply("light")
    assert manager.current_id == "light"
    assert manager.current.name == "Light"


def test_apply_invalid_theme(app):
    manager = ThemeManager()

    with pytest.raises(ValueError, match="not found"):
        manager.apply("nonexistent-theme")


def test_current_theme_tracking(app):
    manager = ThemeManager()

    assert manager.current_id == "dark"  # Default

    manager.apply("light")
    assert manager.current_id == "light"

    manager.apply("dark")
    assert manager.current_id == "dark"
