from unittest import mock
import pytest

from pireal.gui.main_panel import MainPanel

_MODULE_MP = 'pireal.gui.main_panel.MainPanel'


@pytest.fixture
def main_panel(qtbot):
    mp = MainPanel()
    mp._parent = mock.Mock()
    mp._central_view = mock.Mock()
    mp._lateral_widget = mock.Mock()
    mp._query_container = mock.Mock()
    return mp
