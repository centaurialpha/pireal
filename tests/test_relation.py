# -*- coding: utf-8 -*-
#
# Copyright 2015 - Gabriel Acosta <acostadariogabriel@gmail.com>
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
from src.core import relation


class RelationTestCase(unittest.TestCase):

    def setUp(self):
        # Relation 1
        self.r1 = relation.Relation()
        # Fields
        f1 = ['id', 'name', 'city']
        self.r1.fields = f1
        # Data
        data1 = [('1', 'Gabriel', 'Belén'), ('23', 'Rodrigo', 'Belén')]
        for i in data1:
            self.r1.insert(i)

        # Relation 2
        self.r2 = relation.Relation()
        # Fields
        f2 = ['id', 'skill']
        self.r2.fields = f2
        # Data
        data2 = [('3', 'Ruby'), ('1', 'Python')]
        for i in data2:
            self.r2.insert(i)

        # Relation 3
        self.r3 = relation.Relation()
        # Fields
        self.r3.fields = ['date']
        data3 = [("2015-12-12",), ("2012-07-09",), ("1998-12-09",)]
        for i in data3:
            self.r3.insert(i)

    def test_projection(self):
        # Project name
        # Π name (r1)
        expected = {('Gabriel',), ('Rodrigo',)}
        rproject = self.r1.project("name")
        project = rproject.content
        self.assertEqual(expected, project)

    def test_selection(self):
        # σ id == 23 (r2)
        expected = {('23', 'Rodrigo', 'Belén')}
        rselect = self.r1.select("id == 23")
        select = rselect.content
        self.assertEqual(expected, select)

    def test_cartesian_product_exception(self):
        # r1 x r2
        try:
            self.r1.product(self.r2)
        except relation.DuplicateFieldsError as reason:
            msg = reason.msg
            expected_error = "Duplicate attribute \"id\" in product operation."
        self.assertEqual(expected_error, msg)

    def test_cartesian_product(self):
        # r2 x r3
        expected = {
            ('3', 'Ruby', '2015-12-12'),
            ('1', 'Python', '2015-12-12'),
            ('3', 'Ruby', '2012-07-09'),
            ('1', 'Python', '2012-07-09'),
            ('3', 'Ruby', '1998-12-09'),
            ('1', 'Python', '1998-12-09'),
        }
        rproduct = self.r2.product(self.r3)
        product = rproduct.content
        self.assertEqual(expected, product)

    def test_natural_join(self):
        # r1 ⋈ r2
        expected = {('1', 'Gabriel', 'Belén', 'Python')}
        rjoin = self.r1.njoin(self.r2)
        njoin = rjoin.content
        self.assertEqual(expected, njoin)
