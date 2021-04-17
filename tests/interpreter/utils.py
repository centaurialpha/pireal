import unittest

from pireal.interpreter.utils import (
    is_date,
    is_time,
)


class UtilsTestCase(unittest.TestCase):

    def test_is_date(self):
        dates = (
            '20/01/1991',
            '01/20/1991',
            '1991/01/20'
        )

        expected_values = (True, False, True)

        for date, expected in zip(dates, expected_values):
            with self.subTest(date=date):
                self.assertEqual(is_date(date), expected)

    def test_is_time(self):
        times = (
            '15:15',
            '22:25',
            '32:14',
        )

        expected_values = (True, True, False)

        for t, expected in zip(times, expected_values):
            with self.subTest(t=t):
                self.assertEqual(is_time(t), expected)
