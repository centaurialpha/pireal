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

from src.core.rtypes import RelationStr

IS_VALID_FIELD_NAME = re.compile("^[_á-úa-zA-Z][_á-úa-zA-Z0-9]*$")

# FIXME: test q1 := select id < 6666 (personas);


class Relation(object):
    """
    This class represents a relation/table as a set of tuples.
    Fields is a list, where indexes are connected with the
    indexes of the tuples.
    """

    def __init__(self):
        self.content = Content()
        self.__header = list()

    def insert(self, record):
        """ Inserts a register

        :param record: A record (tuple)
        """

        self.content.add(record)

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

        pass

    def update(self, row, column, value):
        self.content[row][column] = value

    def cardinality(self):
        """ Devuelve la cantidad de filas o tuplas de la relación """

        return len(self.content)

    def degree(self):
        """ Devuelve el grado de la relación """

        return len(self.header)

    def select(self, expression):
        """
        The select operator returns a new relation with the tuples that
        satisfy an expression.

        :param expression: A python valid expression
        :returns: A new relation with the tuples that satisfy an *expression*
        """

        new_relation = Relation()
        new_relation.header = self.__header

        # Filtering
        d = {}
        for register in self.content:
            for e, attr in enumerate(self.__header):
                d[attr] = RelationStr(register[e]).cast()
            # The expression is evaluated
            try:
                if eval(expression, {}, d):
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
            new_relation.insert([rec[index] for index in indexes])

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

    def louther(self, other):
        header = self.__header + other.header

        new_relation = Relation()
        new_relation.header = header

        sharedf = set(self.__header).intersection(set(other.header))
        ss = self.__header + [i for i in other.header if i not in sharedf]

        indexes_rela = [self.__header.index(i) for i in sharedf]
        indexes_other = [other.header.index(i) for i in sharedf]

        for i in self.content:
            added = False
            for j in other.content:
                for k in indexes_rela:
                    for l in indexes_other:
                        if i[k] == j[l]:
                            # Esto es un producto cartesiano con la
                            # condición equi-join
                            new_relation.insert(i + j)
                            added = True
            if not added:
                nulls = ['null' for i in range(len(other.header))]
                new_relation.insert(i + nulls)

        return new_relation.project(*ss)

    def routher(self, other):
        r = other.louther(self)
        sharedf = [i for i in other.header if i not in self.header]
        return r.project(*self.header + sharedf)

    def fouther(self, other):
        right = self.routher(other)
        left = self.louther(other)
        return right.union(left)

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

        # if self.header != other_relation.header:
        #    raise Exception("Not union compatible")

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


class Content(object):
    """ Esta clase representa un objeto list pero que se comporta como un
    set (conjunto).
    - Por qué no usas set Gabo?
    Por que necesito un objeto que pueda acceder mediante índices (un set
    no permite eso), además el órden me importa (el órden es un concepto sin
    sentido para los conjuntos y las matemáticas) pero esto es un problema
    del mundo real ;)
    """

    def __init__(self):
        self.content = []
        self.__index = 0

    def add(self, item):
        if item not in self.content:
            self.content.append(item)

    def difference(self, other):
        return list(filter(lambda x: x not in other, self))

    def intersection(self, other):
        return list(filter(lambda x: x in self, other))

    def union(self, other):
        return list(self) + list(filter(lambda x: x not in self, other))

    def __iter__(self):
        return self

    def __next__(self):
        try:
            item = self.content[self.__index]
            self.__index += 1
            return item
        except IndexError:
            self.__index = 0
            raise StopIteration

    def __str__(self):
        return str([x for x in self])

    def __len__(self):
        return len(self.content)

    def __getitem__(self, index):
        return self.content[index]

    def __setitem__(self, index, value):
        self.content[index] = value


if __name__ == "__main__":
    r1 = Relation()
    h1 = ['name', 'id', 'city']
    r1.header = h1
    data1 = [['Gabriel', '1', 'Bel'], ['Rodrigo', '32', 'Bel']]
    for reg in data1:
        r1.insert(reg)

    r2 = Relation()
    h2 = ['id', 'skill']
    r2.header = h2
    data2 = [['1', 'Python'], ['32', 'C++']]
    for reg in data2:
        r2.insert(reg)
    print(r1.select("name == 'Gabriel'"))
