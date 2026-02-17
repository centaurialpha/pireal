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

import unittest

from pireal.interpreter.utils import is_date, is_time


class UtilsTestCase(unittest.TestCase):
    def test_is_date(self):
        dates = ("20/01/1991", "01/20/1991", "1991/01/20")

        expected_values = (True, False, True)

        for date, expected in zip(dates, expected_values, strict=True):
            with self.subTest(date=date):
                self.assertEqual(is_date(date), expected)

    def test_is_time(self):
        times = (
            "15:15",
            "22:25",
            "32:14",
        )

        expected_values = (True, True, False)

        for t, expected in zip(times, expected_values, strict=True):
            with self.subTest(t=t):
                self.assertEqual(is_time(t), expected)
