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

import datetime

import pytest

from pireal.interpreter.utils import is_date, is_time


@pytest.mark.parametrize(
    "date, expected",
    [
        ("20/01/1991", True),
        ("01/20/1991", False),
        ("1991/01/20", True),
        ("2024-01-15", True),  # ISO 8601
        ("not-a-date", False),
    ],
)
def test_is_date(date, expected):
    ok, _ = is_date(date)
    assert ok == expected


def test_is_date_returns_correct_value():
    ok, date = is_date("15/01/2024")
    assert ok
    assert date == datetime.date(2024, 1, 15)


def test_is_date_invalid_returns_none():
    ok, date = is_date("not-a-date")
    assert not ok
    assert date is None


@pytest.mark.parametrize(
    "time, expected",
    [
        ("15:15", True),
        ("22:25", True),
        ("32:14", False),
    ],
)
def test_is_time(time, expected):
    ok, _ = is_time(time)
    assert ok == expected
