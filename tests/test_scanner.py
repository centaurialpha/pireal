import unittest
from src.core.interpreter.lexer import Scanner


class ScannerTestCase(unittest.TestCase):

    def setUp(self):
        text = "hola\na\n a todos."
        self.sc = Scanner(text)

    def test_next_char(self):
        self.assertTrue(self.sc.char, 'h')
        self.sc.next_char()
        self.sc.next_char()
        self.assertTrue(self.sc.char, 'a')

    def test_cursor(self):
        for i in range(9):
            self.sc.next_char()
        cursor = self.sc.cursor()
        self.assertTrue(cursor.lineno, 2)
        self.assertTrue(cursor.colno, 1)
        self.assertTrue(cursor.index, 8)

if __name__ == "__main__":
    unittest.main()
