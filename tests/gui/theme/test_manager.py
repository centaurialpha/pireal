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

import pytest

from pireal.gui.theme.manager import ThemeManager


def test_manager_initialization(qapp):
    manager = ThemeManager()

    available = manager.themes()
    theme_ids = [tid for tid, _ in available]

    assert "dark" in theme_ids
    assert "light" in theme_ids


def test_apply_theme(qapp):
    manager = ThemeManager()

    manager.apply("dark")
    assert manager.current_id == "dark"
    assert manager.current.name == "Dark"

    manager.apply("light")
    assert manager.current_id == "light"
    assert manager.current.name == "Light"


def test_apply_invalid_theme(qapp):
    manager = ThemeManager()

    with pytest.raises(ValueError, match="not found"):
        manager.apply("nonexistent-theme")


def test_current_theme_tracking(qapp):
    manager = ThemeManager()

    assert manager.current_id == "dark"  # Default

    manager.apply("light")
    assert manager.current_id == "light"

    manager.apply("dark")
    assert manager.current_id == "dark"
