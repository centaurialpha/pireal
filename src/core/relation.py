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

import csv


class Relation(object):
    """
    This class represents a relation/table as a set of tuples.
    Fields is a list, where indexes are connected with the
    indexes of the tuples.

    :param filename: *.csv* or *.prf* file
    """

    def __init__(self, filename=''):
        self.content = set()
        if not filename:
            self.fields = list()
        else:
            with open(filename) as f:
                csv_reader = csv.reader(f)
                self.fields = list(next(csv_reader))
                for i in csv_reader:
                    self.insert(i)

    def insert(self, record):
        """ Inserts a register

        :param record: A record (tuple)
        """

        self.content.add(tuple(record))

    def select(self, expression):
        """ The select operator returns a new relation with the tuples that
        satisfy an expression.

        :param expression: A python valid expression
        :returns: A new relation with the tuples that satisfy an *expression*
        """

        new_relation = Relation()
        new_relation.fields = self.fields

        # Filtering
        d = {}
        for register in self.content:
            for e, attr in enumerate(self.fields):
                if register[e].isdigit():
                    d[attr] = int(register[e])
                else:
                    d[attr] = register[e]

            # The expression is evaluated
            if eval(expression, d):
                new_relation.insert(register)

        return new_relation

    def project(self, *args):
        """ The project operator returns a new relation.
        Extract columns (attributes) resulting in a vertical subset of
        attributes of the relation

        :param args: A tuple of field names
        :returns: A new relation with the new fields
        """

        indexes = []
        for arg in args:
            indexes.append(self.fields.index(arg))

        # New fields
        fields = [self.fields[i] for i in indexes]

        # New relation
        new_relation = Relation()
        new_relation.fields = fields

        for rec in self.content:
            new_relation.content.add(tuple(rec[index] for index in indexes))

        return new_relation

    def product(self, other_relation):
        """ The cartesian producto is defined as: R x S, its outline
        corresponds to a combination of all tuples in R with each S
        tuples, and attributes corresponding to those of R followed by S.

        This method throws an exception when you are duplicate field names

        :param other_relation: Relation
        :returns: A new relation
        """

        for i in other_relation.fields:
            if i in self.fields:
                raise Exception("Duplicate attribute \"{}\" in product "
                                "operation.".format(i))
            self.fields.append(i)

        new_relation = Relation()
        new_relation.fields = self.fields

        for i in self.content:
            for e in other_relation.content:
                new_relation.insert(i + e)

        return new_relation

    def __str__(self):
        """ Magic method. Returns a representation of the relation

        |      id      |     name     |    skill     |
        ----------------------------------------------
        |      8       |   Mariela    |     Chef     |
        |      4       |   Rodrigo    |    Gamer     |
        |      2       |   Gabriel    |    Python    |
        """

        fields = ""
        for field in self.fields:
            fields += "|  " + field.center(10) + "  "
        fields += "|\n"
        fields += "-" * (len(fields) - 1) + "\n"

        content = ""
        for rec in self.content:
            for i in rec:
                content += "|  " + i.center(10) + "  "
            content += "|\n"

        return fields + content


if __name__ == "__main__":
    pass
    # Test

    # Fields
    #fields = ["id", "name", "skill"]
    #r = Relation()
    #r.fie-lds = fields

    # Data
    #data = {
        #('1', 'Gabriel', 'Python'),
        #('9', 'Rodrigo', 'Games'),
        #("4", 'Mariela', 'Chef')
    #}
    #r1 = Relation()
    #f1 = ['id', 'name']
    #r1.fields = f1
    #data1 = {('1', 'Gabriel'), ('32', 'Rodrigo')}
    #for reg in data1:
        #r1.insert(reg)

    #r2 = Relation()
    #f2 = ['ids', 'skill']
    #r2.fields = f2
    #data2 = {('1', 'Python'), ('32', 'C++')}
    #for reg in data2:
        #r2.insert(reg)

    #r = r1.product(r2).select("id == 1 and ids == 1").project("name", "skill")
    #print(r)

    # Relation
    #print(r)

    #r2 = r.project("skill", "name")
    # Project skill and name
    #print(r2)

    #r3 = r.select("name == 'Gabriel'")
    #print(r3)

    #rel = r.project("name").select("name == 'Gabriel'")
    #print(rel)