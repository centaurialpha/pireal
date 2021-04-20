import unittest

from pireal.core.relation import Relation
from pireal.core.ordered_set import OrderedSet
from pireal.interpreter.scanner import Scanner
from pireal.interpreter.lexer import Lexer
from pireal.interpreter.parser import Parser
from pireal.interpreter.parser import Interpreter


class InterpreterIntegrationTestCase(unittest.TestCase):

    def setUp(self):
        self.ra = Relation()
        self.rb = Relation()

        self.ra.header = ['id', 'age', 'birth']
        self.rb.header = ['id', 'skill']

        data_a = OrderedSet()
        data_b = OrderedSet()

        self.ra.insert(('23', '30', '20/01/1991'))
        self.ra.insert(('1', '26', '06/09/1994'))
        self.ra.insert(('3', '20', '19/06/2000'))

        self.rb.insert(('3', 'Web'))
        self.rb.insert(('23', 'Satellites'))
        self.rb.insert(('1', 'Python'))

        self.relations = {'ra': self.ra, 'rb': self.rb}

    def test_age_greater_than_26(self):
        query = 'q := select age > 26 (ra);'

        i = Interpreter(Parser(Lexer(Scanner(query))))
        self.assertFalse(i.SCOPE)
        i.to_python()
        self.assertTrue(i.SCOPE)

        expected_python_code = {'q': 'ra.select("age > 26")'}

        r = eval(expected_python_code['q'], {}, self.relations)

        self.assertEqual(r.header, ['id', 'age', 'birth'])
        self.assertEqual(r.cardinality(), 1)
        self.assertEqual(r.degree(), 3)

        i.clear()

    def test_date(self):
        query = 'q := select birth > "01/01/1993" (ra);'

        i = Interpreter(Parser(Lexer(Scanner(query))))
        self.assertFalse(i.SCOPE)
        i.to_python()
        self.assertTrue(i.SCOPE)

        expected_python_code = {'q': 'ra.select("birth > datetime.date(1993, 1, 1)")'}
        self.assertDictEqual(i.SCOPE, expected_python_code)

        r = eval(expected_python_code['q'], {}, self.relations)
        print(r)

        self.assertEqual(r.header, ['id', 'age', 'birth'])
        self.assertEqual(r.cardinality(), 2)
        self.assertEqual(r.degree(), 3)

        i.clear()
