import unittest
import datetime

from pireal.core.rtypes import RType


class RelationTypesTestCase(unittest.TestCase):
    def test_int(self):
        self.assertEqual(RType.cast("1000"), 1000)
        self.assertEqual(RType.cast("0"), 0)
        self.assertEqual(RType.cast("-12"), -12)

    def test_float(self):
        self.assertEqual(RType.cast("12.0"), 12.0)
        self.assertEqual(RType.cast("-12.0"), -12.0)
        self.assertEqual(RType.cast("3.14156"), 3.14156)

    def test_date(self):
        self.assertEqual(
            RType.cast("20/01/1991"), datetime.date(year=1991, month=1, day=20)
        )
        self.assertEqual(
            RType.cast("1991/01/20"), datetime.date(year=1991, month=1, day=20)
        )

    def test_time(self):
        self.assertEqual(RType.cast("15:15"), datetime.time(hour=15, minute=15))

    def test_string(self):
        self.assertEqual(RType.cast("gabox"), "gabox")
