import unittest
import datetime

from src.core import rtypes


class RTypesTestCase(unittest.TestCase):

    def test_positive_integer(self):
        pinteger = rtypes.RelationStr('100').cast()
        self.assertEqual(pinteger, 100)
        self.assertIsInstance(pinteger, int)

    def test_negative_integer(self):
        ninteger = rtypes.RelationStr('-100').cast()
        self.assertEqual(ninteger, -100)
        self.assertIsInstance(ninteger, int)

    def test_positive_float(self):
        pfloat = rtypes.RelationStr('12.32').cast()
        self.assertEqual(pfloat, 12.32)
        self.assertIsInstance(pfloat, float)

    def test_negative_float(self):
        nfloat = rtypes.RelationStr('-12.32').cast()
        self.assertEqual(nfloat, -12.32)
        self.assertIsInstance(nfloat, float)

    def test_date(self):
        date = rtypes.RelationStr('1991/01/20').cast()
        year = 1991
        month = 1
        day = 20
        self.assertEqual(year, date.year)
        self.assertEqual(month, date.month)
        self.assertEqual(day, date.day)
        self.assertIsInstance(date, datetime.datetime)

    def test_hour(self):
        hour = rtypes.RelationStr('15:59').cast()
        h, m = 15, 59
        self.assertEqual(h, hour.hour)
        self.assertEqual(m, hour.minute)
        self.assertIsInstance(hour, datetime.time)

if __name__ == "__main__":
    unittest.main()
