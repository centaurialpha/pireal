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
        self.r1.header = f1

        # Data
        data1 = [['1', 'Gabriel', 'Belén'], ['23', 'Rodrigo', 'Belén']]
        for i in data1:
            self.r1.insert(i)

        # Relation 2
        self.r2 = relation.Relation()
        # Fields
        f2 = ['id', 'skill']
        self.r2.header = f2
        # Data
        data2 = [['3', 'Ruby'], ['1', 'Python']]
        for i in data2:
            self.r2.insert(i)

        # Relation 3
        self.r3 = relation.Relation()
        # Fields
        self.r3.header = ['date']
        data3 = [["2015-12-12"], ["2012-07-09"], ["1998-12-09"]]
        for i in data3:
            self.r3.insert(i)

        # Relation 4
        self.r4 = relation.Relation()
        self.r4.header = ['id', 'skill']
        data4 = [["192", "Ruby"], ["43", "Go"]]
        for i in data4:
            self.r4.insert(i)

    def test_projection(self):
        # Π name (r1)
        expected = [['Gabriel'], ['Rodrigo']]
        rproject = self.r1.project("name")
        project = rproject.content.content
        self.assertEqual(expected, project)

    def test_selection(self):
        # σ id == 23 (r2)
        expected = [['23', 'Rodrigo', 'Belén']]
        rselect = self.r1.select("id == 23")
        select = rselect.content.content
        self.assertEqual(expected, select)

    def test_cardinality(self):
        expected = 3
        self.assertEqual(self.r3.cardinality(), expected)

    def test_degree(self):
        expected = 1
        self.assertEqual(self.r3.degree(), expected)

    def test_update(self):
        # Antes
        # [["192", "Ruby"], ["43", "Go"]]
        # Después
        # [["192", "Ruby"], ["32", "Go!"]]
        expected = [
            ['192', 'Ruby'],
            ['32', 'Go!']
        ]
        self.r4.update(1, 0, '32')
        self.r4.update(1, 1, 'Go!')
        self.assertEqual(self.r4.content.content, expected)

    def test_cartesian_product(self):
        # r2 x r3
        expected = [
            ['3', 'Ruby', '2015-12-12'],
            ['3', 'Ruby', '2012-07-09'],
            ['3', 'Ruby', '1998-12-09'],
            ['1', 'Python', '2015-12-12'],
            ['1', 'Python', '2012-07-09'],
            ['1', 'Python', '1998-12-09']
        ]
        rproduct = self.r2.product(self.r3)
        product = rproduct.content.content
        self.assertEqual(expected, product)

    def test_natural_join(self):
        # r1 ⋈ r2
        expected = [['1', 'Gabriel', 'Belén', 'Python']]
        rjoin = self.r1.njoin(self.r2)
        njoin = rjoin.content.content
        self.assertEqual(expected, njoin)

    def test_louter(self):
        expected = [
            ['1', 'Gabriel', 'Belén', 'Python'],
            ['23', 'Rodrigo', 'Belén', 'null']
        ]
        louter = self.r1.louter(self.r2)
        self.assertEqual(louter.content.content, expected)

    def test_router(self):
        expected = [
            ['3', 'null', 'null', 'Ruby'],
            ['1', 'Gabriel', 'Belén', 'Python']
        ]
        router = self.r1.router(self.r2)
        self.assertEqual(router.content.content, expected)

    def test_fullouter(self):
        expected = [
            ['3', 'null', 'null', 'Ruby'],
            ['1', 'Gabriel', 'Belén', 'Python'],
            ['23', 'Rodrigo', 'Belén', 'null'],
        ]
        full_outer = self.r1.fouter(self.r2)
        self.assertEqual(full_outer.content.content, expected)

    def test_intersection(self):
        project_idr1 = self.r1.project("id")
        project_idr2 = self.r2.project("id")
        expected = [['1']]
        # project_idr1 ∩ project_idr2
        intersection = project_idr1.intersect(project_idr2).content.content
        self.assertEqual(expected, intersection)

    def test_difference(self):
        # r4 - r2
        project_idr4 = self.r4.project("id")
        project_idr2 = self.r2.project("id")
        expected = [['192'], ['43']]
        difference = project_idr4.difference(project_idr2).content.content
        self.assertEqual(expected, difference)

    def test_intersection_alternative(self):
        project_idr1 = self.r1.project("id")
        project_idr2 = self.r2.project("id")
        expected = [['1']]
        # Intersection using difference r1 - (r1 - r2)
        diff = project_idr1.difference(project_idr2)
        union = project_idr1.difference(diff).content.content
        self.assertEqual(expected, union)

    def test_union(self):
        # r2 ∪ r4
        expected = [
            ['3', 'Ruby'],
            ['1', 'Python'],
            ["192", "Ruby"],
            ["43", "Go"]
        ]
        union = self.r2.union(self.r4).content.content
        self.assertEqual(expected, union)

    def test_append_row(self):
        rela = relation.Relation()
        rela.header = ['id', 'name', 'city']
        content = [
            ['1', 'Gabriel', 'Belén'],
            ['23', 'Rodrigo', 'Belén']
        ]
        for t in content:
            rela.insert(t)
        expected_header = ['id', 'name', 'city']
        expected_content = [
            ['1', 'Gabriel', 'Belén'],
            ['23', 'Rodrigo', 'Belén'],
            ['null', 'null', 'null']
        ]
        rela.append_row()
        self.assertEqual(expected_header, rela.header)
        self.assertEqual(expected_content, rela.content.content)

    def test_append_column(self):
        rela = relation.Relation()
        rela.header = ['id', 'name', 'city']
        content = [
            ['1', 'Gabriel', 'Belén'],
            ['23', 'Rodrigo', 'Belén']
        ]
        for t in content:
            rela.insert(t)
        expected_header = ['id', 'name', 'city', 'null']
        expected_content = [
            ['1', 'Gabriel', 'Belén', 'null'],
            ['23', 'Rodrigo', 'Belén', 'null']
        ]
        rela.append_column()
        self.assertEqual(expected_header, rela.header)
        self.assertEqual(expected_content, rela.content.content)

    def test_remove_column(self):
        rela = relation.Relation()
        rela.header = ['id', 'name', 'city']
        content = [
            ['1', 'Gabriel', 'Belén'],
            ['23', 'Rodrigo', 'Belén']
        ]
        for t in content:
            rela.insert(t)
        expected_header = ['id', 'city']
        expected_content = [
            ['1', 'Belén'],
            ['23', 'Belén']
        ]
        rela.remove_column(1)
        self.assertEqual(expected_header, rela.header)
        self.assertEqual(expected_content, rela.content.content)


if __name__ == "__main__":
    unittest.main()
