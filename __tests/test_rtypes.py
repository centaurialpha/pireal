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
        date = rtypes.RelationStr('20/01/1991').cast()
        date2 = datetime.date(1991, 1, 20)
        self.assertTrue(date == date2)
        date = rtypes.RelationStr('06/09/1993').cast()
        self.assertFalse(date < date2)

    def test_hour(self):
        time = rtypes.RelationStr('12:00').cast()
        time2 = datetime.time(12, 00)
        self.assertTrue(time == time2)
        time = rtypes.RelationStr('12:59').cast()
        self.assertTrue(time > time2)


if __name__ == "__main__":
    unittest.main()
