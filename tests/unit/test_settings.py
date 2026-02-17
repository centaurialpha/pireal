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
from unittest.mock import patch
from pireal.settings import Settings


@pytest.fixture
def settings(tmp_path, qapp):
    config_file = tmp_path / "settings.ini"
    with patch("pireal.settings.CONFIG_FILE", config_file):
        s = Settings()
        s.load()
        yield s


@pytest.mark.parametrize(
    "attr, expected",
    [
        ("language", "es"),
        ("font_size", 12),
        ("highlight_current_line", True),
        ("match_parenthesis", True),
        ("theme", "dark"),
    ],
)
def test_defaults(settings, attr, expected):
    assert getattr(settings, attr) == expected


def test_theme_default_light_when_dark_mode_false(tmp_path, qapp):
    config_file = tmp_path / "settings.ini"
    with patch("pireal.settings.CONFIG_FILE", config_file):
        s = Settings()
        s._qs.setValue("dark_mode", False)
        s.load()
        assert s.theme == "light"


def test_load_only_once(settings):
    settings.language = "en"
    settings.load()
    assert settings.language == "en"


def test_values_persisted(tmp_path, qapp):
    config_file = tmp_path / "settings.ini"
    with patch("pireal.settings.CONFIG_FILE", config_file):
        s1 = Settings()
        s1.load()
        s1.language = "en"
        s1.font_size = 16
        s1.theme = "light"

    with patch("pireal.settings.CONFIG_FILE", config_file):
        s2 = Settings()
        s2.load()
        assert s2.language == "en"
        assert s2.font_size == 16
        assert s2.theme == "light"


def test_auto_save_on_setattr(tmp_path, qapp):
    config_file = tmp_path / "settings.ini"
    with patch("pireal.settings.CONFIG_FILE", config_file):
        s1 = Settings()
        s1.load()
        s1.language = "en"  # sin llamar save()

    with patch("pireal.settings.CONFIG_FILE", config_file):
        s2 = Settings()
        s2.load()
        assert s2.language == "en"


def test_no_auto_save_before_load(tmp_path, qapp):
    config_file = tmp_path / "settings.ini"
    with patch("pireal.settings.CONFIG_FILE", config_file):
        s = Settings()
        s.language = "en"  # antes de load(), no debería persistir

    with patch("pireal.settings.CONFIG_FILE", config_file):
        s2 = Settings()
        s2.load()
        assert s2.language == "es"  # default
