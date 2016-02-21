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


class DuplicateFieldsError(Exception):

    def __init__(self, msg):
        super(DuplicateFieldsError, self).__init__()
        self.msg = msg


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

    def clear(self):
        self.content = set()

    def select(self, expression):
        """
        The select operator returns a new relation with the tuples that
        satisfy an expression.

        :param expression: A python valid expression
        :returns: A new relation with the tuples that satisfy an *expression*
        """

        new_relation = Relation()
        new_relation.fields = self.fields

        value = expression.rsplit(' ', 1)[-1]
        if value.isdigit():
            expression = expression.replace(value, '"' + value + '"')

        # Filtering
        d = {}
        for register in self.content:
            for e, attr in enumerate(self.fields):
                d[attr] = register[e]

            # The expression is evaluated
            try:
                if eval(expression, d):
                    new_relation.insert(register)
            except SyntaxError:
                raise Exception("Error de Sintáxis\nNo se pudo evaluar la "
                                "expresión \"{}\"".format(expression))

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
            try:
                indexes.append(self.fields.index(arg))
            except ValueError as reason:
                field = reason.__str__().split()[0]
                raise Exception("Campo inválido: {}".format(field))
        # New fields
        fields = [self.fields[i] for i in indexes]

        # New relation
        new_relation = Relation()
        new_relation.fields = fields

        for rec in self.content:
            new_relation.content.add(tuple(rec[index] for index in indexes))

        return new_relation

    def product(self, other_relation):
        """ The cartesian product is defined as: R x S, its outline
        corresponds to a combination of all tuples in R with each S
        tuples, and attributes corresponding to those of R followed by S.

        This method throws an exception when you are duplicate field names

        :param other_relation: Relation
        :returns: A new relation
        """

        for i in other_relation.fields:
            if i in self.fields:
                raise DuplicateFieldsError("Duplicate attribute \"{}\" in "
                                           "product operation.".format(i))
            self.fields.append(i)

        new_relation = Relation()
        new_relation.fields = self.fields

        for i in self.content:
            for e in other_relation.content:
                new_relation.insert(i + e)

        return new_relation

    def njoin(self, other_relation):

        sharedf = set(self.fields).intersection(set(other_relation.fields))
        new_relation = Relation()

        fields = [i for i in other_relation.fields if i not in self.fields]
        new_relation.fields = self.fields + fields

        sid = []
        for i in sharedf:
            sid.append(self.fields.index(i))

        oid = []
        for i in sharedf:
            oid.append(other_relation.fields.index(i))

        noid = [i for i in range(len(other_relation.fields)) if i not in oid]

        for i in self.content:
            for j in other_relation.content:
                for k in range(len(sid)):
                    if i[sid[k]] == j[oid[k]]:
                        new_relation.insert(list(i) + list(j[l] for l in noid))

        return new_relation

    def intersect(self, other_relation):
        """ The intersection is defined as: R ∩ S. corresponds to the set of
        all tuples in R and S, R and S compatible unions.

        :param other_relation: Relation object
        :returns: A new relation
        """

        if self.fields != other_relation.fields:
            raise Exception("Not union compatible")

        new_relation = Relation()
        new_relation.fields = self.fields
        content = self.content.intersection(other_relation.content)

        if not content:
            return new_relation

        for i in content:
            new_relation.insert(i)

        return new_relation

    def difference(self, other_relation):
        """ The difference is defined as: R - S. It is the set of all tuples
        in R, but not in S. R and S must be compatible unions

        :param other_relation: Relation object
        :returns: A new relation
        """

        if self.fields != other_relation.fields:
            raise Exception("Not union compatible")

        new_relation = Relation()
        new_relation.fields = self.fields
        content = self.content.difference(other_relation.content)

        for i in content:
            new_relation.insert(i)

        return new_relation

    def union(self, other_relation):
        """ The union is defined as: R ∪ S. Returns the set of tuples in R,
        or S, or both. R and S must be compatible unions.

        :param other_relation: Relation object
        :returns: A new relation
        """

        if self.fields != other_relation.fields:
            raise Exception("Not union compatible")

        new_relation = Relation()
        new_relation.fields = self.fields
        content = self.content.union(other_relation.content)

        for i in content:
            new_relation.insert(i)

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
    # Test

    r1 = Relation()
    f1 = ['id', 'name']
    r1.fields = f1
    data1 = {('1', 'Gabriel'), ('32', 'Rodrigo')}
    for reg in data1:
        r1.insert(reg)

    r2 = Relation()
    f2 = ['id', 'skill']
    r2.fields = f2
    data2 = {('1', 'Python'), ('32', 'C++')}
    for reg in data2:
        r2.insert(reg)
