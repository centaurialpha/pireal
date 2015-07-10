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


class Relation(object):
    """
    This class represents a relation/table as a set of tuples.
    Fields is a list, where indexes are connected with the
    indexes of the tuples.

    fields = ["id", "name", "skill"]
    content = {
        ('2', 'Gabriel', 'Python'),
        ('8', 'Mariela', 'Chef'),
        ('4', 'Rodrigo', 'Gamer')
    }

    The following output is the result of printing the relation.
    Relation.__str__:

    |      id      |     name     |    skill     |
    ----------------------------------------------
    |      8       |   Mariela    |     Chef     |
    |      4       |   Rodrigo    |    Gamer     |
    |      2       |   Gabriel    |    Python    |

    """

    def __init__(self):
        self.fields = list()
        self.content = set()

    def insert(self, record):
        """ Inserts a register """

        self.content.add(tuple(record))

    def select(self, expression):
        """
        The select operator returns a new relation with the tuples that
        satisfy an expression.
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
        """
        The project operator returns a new relation.
        Extract columns (attributes) resulting in a vertical subset of
        attributes of the relation .
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

    def __str__(self):
        """ Magic method. Returns a representation of the relation """

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

    # Fields
    fields = ["id", "name", "skill"]
    r = Relation()
    r.fields = fields

    # Data
    data = {
        ('1', 'Gabriel', 'Python'),
        ('9', 'Rodrigo', 'Games'),
        ("4", 'Mariela', 'Chef')
    }
    # Insert data
    for reg in data:
        r.insert(reg)

    # Relation
    print(r)

    #r2 = r.project("skill", "name")
    # Project skill and name
    #print(r2)

    #r3 = r.select("name == 'Gabriel'")
    #print(r3)

    #rel = r.project("name").select("name == 'Gabriel'")
    #print(rel)