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

import re

IS_VALID_FIELD_NAME = re.compile(r"^[_a-zA-Z][_a-zA-Z0-9]*$")


class Relation(object):
    """
    This class represents a relation/table as a set of tuples.
    Fields is a list, where indexes are connected with the
    indexes of the tuples.
    """

    def __init__(self):
        self.content = set()
        self.__header = list()

    def insert(self, record):
        """ Inserts a register

        :param record: A record (tuple)
        """

        self.content.add(tuple(record))

    def __set_header(self, header):
        """ Set header to the relation """

        for field in header:
            if not IS_VALID_FIELD_NAME.match(field):
                raise Exception("'{f}' is not a valid field name".format(
                    f=field))

        self.__header = header

    def __get_header(self):
        """ Get the header """

        return self.__header

    header = property(__get_header, __set_header)

    def clear(self):
        """ Clear all content of the relation except the header """

        self.content = set()

    def count(self):
        """ Return the number of tuples in the relation """

        return str(len(self.content))

    def select(self, expression):
        """
        The select operator returns a new relation with the tuples that
        satisfy an expression.

        :param expression: A python valid expression
        :returns: A new relation with the tuples that satisfy an *expression*
        """

        new_relation = Relation()
        new_relation.header = self.__header

        value = expression.rsplit(' ', 1)[-1]
        value_i = value.replace('.', '').replace('-', '')
        if value_i.isdigit():
            expression = expression.replace(value, '"' + value + '"')

        # Filtering
        d = {}
        for register in self.content:
            for e, attr in enumerate(self.__header):
                d[attr] = register[e]

            # The expression is evaluated
            try:
                if eval(expression, d):
                    new_relation.insert(register)
            except SyntaxError:
                raise Exception("Couldn't be evaluate the expression: "
                                "'{}'".format(expression))

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
                indexes.append(self.__header.index(arg))
            except ValueError as reason:
                field = reason.__str__().split()[0]
                raise Exception("Invalid field name: {}".format(field))
        # New fields
        header = [self.__header[i] for i in indexes]

        # New relation
        new_relation = Relation()
        new_relation.header = header

        for rec in self.content:
            new_relation.content.add(tuple(rec[index] for index in indexes))

        return new_relation

    def product(self, other_relation):
        """
        The cartesian product is defined as: R x S, its outline
        corresponds to a combination of all tuples in R with each S
        tuples, and attributes corresponding to those of R followed by S.

        This method throws an exception when you are duplicate field names

        :param other_relation: Relation
        :returns: A new relation
        """

        # Check if there are duplicate fields
        for i in self.__header:
            if i in other_relation.header:
                raise Exception("Duplicate field name '{}'"
                                " in product operation".format(i))

        new_relation = Relation()
        new_relation.header = self.__header + other_relation.header

        for i in self.content:
            for e in other_relation.content:
                new_relation.insert(i + e)

        return new_relation

    def njoin(self, other_relation):
        """  """

        # Combination of the headers
        header = self.__header + other_relation.header

        new_relation = Relation()
        new_relation.header = header

        # Shared field names
        sharedf = set(self.__header).intersection(set(other_relation.header))
        ss = self.__header + [i for i in other_relation.header
                              if i not in sharedf]

        # Relation indexes field names
        indexes_rela = [self.__header.index(i) for i in sharedf]
        # Other relation indexes field names
        indexes_other_rela = [other_relation.header.index(i) for i in sharedf]

        for i in self.content:
            for j in other_relation.content:
                for k in indexes_rela:
                    for l in indexes_other_rela:
                        if i[k] == j[l]:
                            new_relation.insert(i + j)

        return new_relation.project(*ss)

    def intersect(self, other_relation):
        """ The intersection is defined as: R ∩ S. corresponds to the set of
        all tuples in R and S, R and S compatible unions.

        :param other_relation: Relation object
        :returns: A new relation
        """

        if self.__header != other_relation.header:
            raise Exception("Not union compatible for intersection")

        new_relation = Relation()
        new_relation.header = self.__header
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

        if self.header != other_relation.header:
            raise Exception("Not union compatible for difference")

        new_relation = Relation()
        new_relation.header = self.header
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

        if self.header != other_relation.header:
            raise Exception("Not union compatible")

        new_relation = Relation()
        new_relation.header = self.header
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

        header = ""
        for field in self.__header:
            header += "|  " + field.center(10) + "  "
        header += "|\n"
        header += "-" * (len(header) - 1) + "\n"

        content = ""
        for rec in self.content:
            for i in rec:
                content += "|  " + i.center(10) + "  "
            content += "|\n"

        return header + content


# Test
if __name__ == "__main__":
    r1 = Relation()
    h1 = ['name', 'id', 'city']
    r1.header = h1
    data1 = {('Gabriel', '1', 'Bel'), ('Rodrigo', '32', 'Bel')}
    for reg in data1:
        r1.insert(reg)

    r2 = Relation()
    h2 = ['id', 'skill']
    r2.header = h2
    data2 = {('1', 'Python'), ('32', 'C++')}
    for reg in data2:
        r2.insert(reg)
    print(r1.select("name == 'Gabriel'"))
