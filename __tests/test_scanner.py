import unittest
from src.core.interpreter import scanner


class ScannerTestCase(unittest.TestCase):

    def test_next_char(self):
        sc = scanner.Scanner("hola\na todos!")
        self.assertEqual(sc.char, 'h')
        chars = ['o', 'l', 'a', '\n', 'a']
        for char in chars:
            self.assertEqual(sc.next_char(), char)

    def test_column_number_position(self):
        sc = scanner.Scanner("hola soy gabo")
        self.assertEqual(sc.colno, 1)
        for i in range(5):
            sc.next()
        self.assertEqual(sc.colno, 6)
        self.assertEqual(sc.char, 's')
        for i in range(4):
            sc.next()
        self.assertEqual(sc.colno, 10)
        self.assertEqual(sc.char, 'g')

    def test_line_number_position(self):
        sc = scanner.Scanner("hola\nsoy\n\nga\nbo")
        self.assertEqual(sc.lineno, 1)
        for i in range(5):
            sc.next()
        self.assertEqual(sc.lineno, 2)
        for i in range(5):
            sc.next()
        self.assertEqual(sc.lineno, 4)

    def test_position(self):
        sc = scanner.Scanner("hola\n\n\na todos!")
        self.assertEqual(sc.lineno, 1)
        self.assertEqual(sc.index, 0)
        self.assertEqual(sc.colno, 1)
        for i in range(7):
            sc.next()
        self.assertEqual(sc.lineno, 4)
        self.assertEqual(sc.index, 7)
        self.assertEqual(sc.colno, 1)


if __name__ == "__main__":
    unittest.main()
