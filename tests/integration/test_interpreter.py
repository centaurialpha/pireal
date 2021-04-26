import unittest
import random
import string
from typing import List

from pireal.utils import eval_expr
from pireal.core.relation import Relation
from pireal.interpreter.parser import interpret
# from pireal.interpreter.scanner import Scanner
# from pireal.interpreter.lexer import Lexer
# from pireal.interpreter.parser import Parser
# from pireal.interpreter.parser import Interpreter


def _random_name():
    str0 = random.sample(string.ascii_lowercase, 3)
    str1 = random.sample(string.digits, 2)
    str2 = random.sample(string.ascii_lowercase, 3)
    return ''.join(str0 + str1 + str2)


def _random_relation(degree=3, cardinality=3):
    r = Relation()
    r.header = [_random_name() for _ in range(degree)]
    for _ in range(cardinality):
        row = []
        for _ in range(degree):
            row.append(_random_name())
        r.insert(tuple(row))
    return r


class _RelationTestCase(unittest.TestCase):

    def _create_relation(self, header: list, content: List[tuple]):
        r = Relation()
        r.header = header
        for row in content:
            r.insert(row)
        return r

    def assertRelationEqual(self, r1, r2):
        self.assertListEqual(r1.header, r2.header)
        self.assertEqual(r1.degree(), r2.degree())
        self.assertEqual(r1.cardinality(), r2.cardinality())
        self.assertEqual(r1.content, r2.content)


class ProjectIntegrationTestCase(_RelationTestCase):

    def setUp(self):
        self.ra = self._create_relation(
            ['id', 'age', 'birth'],
            [
                ('23', '30', '20/01/1991'),
                ('1', '26', '06/09/1994'),
                ('3', '20', '19/06/2000')
            ]
        )
        self.rb = self._create_relation(
            ['id', 'skill'],
            [
                ('3', 'Web'),
                ('23', 'Satellites'),
                ('1', 'Python')
            ]
        )

        self.relations = {'ra': self.ra, 'rb': self.rb}

    def test_basic_query(self):
        query = 'q := rb;'

        interpreter_result = interpret(query)
        expected_memory = {'q': 'rb'}

        self.assertDictEqual(interpreter_result, expected_memory)
        new_relation = eval_expr(interpreter_result['q'], {'rb': self.rb})
        self.assertRelationEqual(self.rb, new_relation)

    def test_basic_project(self):
        query = 'q := project skill (rb);'

        interpreter_result = interpret(query)

        content = [('Web', ), ('Satellites', ), ('Python', )]
        expected_relation = self._create_relation(['skill'], content)

        new_relation = eval_expr(interpreter_result['q'], {'rb': self.rb})

        self.assertRelationEqual(new_relation, expected_relation)

    def test_project_many_attrs(self):
        query = 'q := project id, name, age (r);'

        relation = self._create_relation(
            ['id', 'birth', 'lastname', 'age', 'name'],
            [
                ('1', '20/01/1991', 'Acosta', '30', 'Gabriel'),
                ('3', '06/07/1994', 'Pereyra', '26', 'Mercedes')
            ]
        )

        expected_relation = self._create_relation(
            ['id', 'name', 'age'],
            [
                ('1', 'Gabriel', '30'),
                ('3', 'Mercedes', '26')
            ]
        )

        interpreter_result = interpret(query)

        new_relation = eval_expr(interpreter_result['q'], {'r': relation})

        self.assertRelationEqual(new_relation, expected_relation)

    def test_nested_project(self):
        query = 'q := project id (project id, name, age (r));'

        relation = self._create_relation(
            ['id', 'name', 'age'],
            [
                ('1', 'Gabriel', '30'),
                ('3', 'Mercedes', '26'),
                ('2', 'Rodrigo', '20')
            ]
        )

        expected_relation = self._create_relation(
            ['id'],
            [
                ('1',),
                ('3',),
                ('2',)
            ]
        )

        interpreter_result = interpret(query)

        new_relation = eval_expr(interpreter_result['q'], {'r': relation})

        self.assertRelationEqual(new_relation, expected_relation)


class SelectIntegrationTestCase(_RelationTestCase):

    def test_basic_select(self):
        query = 'q := select id = 4 (r);'

        relation = self._create_relation(
            ['id', 'name'],
            [
                ('1', 'Gabriel'),
                ('2', 'Mercedes'),
                ('3', 'Rodrigo'),
                ('4', 'Hector'),
                ('5', 'Mariela'),
                ('6', 'Ramona')
            ]
        )

        expected_relation = self._create_relation(
            ['id', 'name'],
            [
                ('4', 'Hector'),
            ]
        )

        interpreter_result = interpret(query)

        new_relation = eval_expr(interpreter_result['q'], {'r': relation})

        self.assertRelationEqual(new_relation, expected_relation)

    def test_and_expression(self):
        query = 'q := select age >= 24 and age <= 30 (r);'

        relation = self._create_relation(
            ['name', 'age'],
            [
                ('Gabriel', '30'),
                ('Mercedes', '26'),
                ('Rodrigo', '20'),
                ('Hector', '51'),
            ]
        )

        expected_relation = self._create_relation(
            ['name', 'age'],
            [
                ('Gabriel', '30'),
                ('Mercedes', '26'),
            ]
        )

        interpreter_result = interpret(query)

        new_relation = eval_expr(interpreter_result['q'], {'r': relation})

        self.assertRelationEqual(new_relation, expected_relation)

    def test_nested_and_expression(self):
        query = 'q := select age >= 24 and age <= 30 and name = "gabox" (r);'

        relation = self._create_relation(
            ['name', 'age'],
            [
                ('Gabriel', '30'),
                ('Mercedes', '26'),
                ('Rodrigo', '20'),
                ('Hector', '51'),
                ('gabox', '19'),
                ('gabox', '25'),
                ('gabox', '29'),
                ('gabox', '49'),
            ]
        )

        expected_relation = self._create_relation(
            ['name', 'age'],
            [
                ('gabox', '25'),
                ('gabox', '29')
            ]
        )

        interpreter_result = interpret(query)

        new_relation = eval_expr(interpreter_result['q'], {'r': relation})

        self.assertRelationEqual(new_relation, expected_relation)
