import unittest
from src.core.interpreter import scanner


class ScannerTestCase(unittest.TestCase):

    def test_next_char(self):
        sc = scanner.Scanner("hola\na todos!")
        self.assertEqual(sc.char, 'h')
        chars = ['o', 'l', 'a', '\n', 'a']
        for char in chars:
            self.assertEqual(sc.next_char(), char)

    def test_position(self):
        sc = scanner.Scanner("hola\n\n\na todos!")
        self.assertEqual(sc.lineno, 1)
        self.assertEqual(sc.index, 0)
        self.assertEqual(sc.colno, 0)
        for i in range(7):
            sc.next()
        self.assertEqual(sc.lineno, 4)
        self.assertEqual(sc.index, 7)
        self.assertEqual(sc.colno, 0)

if __name__ == "__main__":
    unittest.main()
