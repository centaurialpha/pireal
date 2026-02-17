from unittest.mock import patch

import pytest

from pireal.registry import Registry


@pytest.fixture(autouse=True)
def init_settings(tmp_path, qapp):
    config_file = tmp_path / "settings.ini"
    with patch("pireal.settings.CONFIG_FILE", config_file):
        from pireal.settings import settings

        settings._loaded = False  # reset por si acaso
        settings.load()
        yield
        settings._loaded = False  # cleanup


@pytest.fixture(autouse=True)
def clean_registry():
    Registry._components.clear()
    yield
    Registry._components.clear()


@pytest.fixture(autouse=True)
def mock_status_bar(qtbot):
    from PyQt6.QtWidgets import QMainWindow

    from pireal.gui.status_bar import StatusBar

    main_window = QMainWindow()
    qtbot.addWidget(main_window)
    status_bar = StatusBar(main_window)
    qtbot.addWidget(status_bar)
    Registry.register("status-bar", status_bar)
