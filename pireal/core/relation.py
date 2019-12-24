# -*- coding: utf-8 -*-
#
# Copyright (C) 2008-2018  Salvo "LtWorf" Tomaselli
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

# This module is based on Relational: <https://github.com/ltworf/relational>

import re
import itertools

from ordered_set import OrderedSet

from pireal.core.rtypes import RelationStr

IS_VALID_FIELD_NAME = re.compile("^[_á-úa-zA-Z][_á-úa-zA-Z0-9]*$")

datetime_dict = {
    'datetime': __import__('datetime')
}

# FIXME: atributo name ?


class RelationError(Exception):
    """Base exception for Relation"""


class InvalidFieldNameError(RelationError):
    """Excepción lanzada cuando un nombre de campo no es válido"""

    def __init__(self, field_name, msg=None):
        if msg is None:
            msg = f'Invalid field name: {field_name}'
        super().__init__(msg)
        self.field_name = field_name


class DuplicateFieldError(RelationError):

    def __init__(self, field_name, msg=None):
        if msg is None:
            msg = f'Duplicated field name: {field_name}'
        super().__init__(msg)
        self.field_name = field_name


class FieldNotInHeaderError(RelationError):
    """Excepción lanzada cuando un campo no existe en la relación"""

    def __init__(self, field_name, relation_name, msg=None):
        if msg is None:
            msg = f'Field name {field_name} doesn\'t exist in {relation_name}'
        super().__init__(msg)


class WrongSizeError(RelationError):
    """Excepción lanzada cuando se trata de insertar un tamaño de
    tuplas diferente a los que acepta la relación"""

    def __init__(self, expected, got, msg=None):
        if msg is None:
            msg = f'Wrong size. Expected {expected}, got {got}'
        super().__init__(msg)
        self.expected = expected
        self.got = got


class SelectionSyntaxError(RelationError):
    pass


class UnionCompatibleError(RelationError):
    pass


def union_compatible(operation):
    """Decorador que comprueba que dos relaciones sean compatibles"""
    def inner(self, *args, **kwargs):
        header_other = args[0].header
        if len(self._header) != len(header_other):
            raise UnionCompatibleError(
                f'Union not compatible for \'{operation.__name__}\'')
        return operation(self, *args, **kwargs)
    return inner


class Relation(object):

    def __init__(self):
        self.content = OrderedSet()
        self.name = None
        self._header = []
        self._null_count = 1

    @property
    def header(self):
        return self._header

    @header.setter
    def header(self, header: list):
        for field in header:
            if not IS_VALID_FIELD_NAME.match(str(field)):
                raise InvalidFieldNameError(field)
        self._header = header

    def insert(self, values):
        if isinstance(values, str):
            values = tuple(values.split())

        if len(values) != len(self._header):
            raise WrongSizeError(
                len(self._header),
                len(values)
            )
        self.content.add(values)

    def update(self, row, column, new_value):
        content = list(self.content)
        self.content.remove(content[row])
        content_row = list(content[row])
        content_row[column] = new_value
        content_row = tuple(content_row)
        self.content.add(content_row)

    def append_row(self):
        """Agrega una fila/tupla al final"""

        nulls = []
        for _ in range(self.degree()):
            nulls.append('null ({})'.format(self._null_count))
            self._null_count += 1
        self.insert(tuple(nulls))

    def cardinality(self):
        """Devuelve la cantidad de filas de la relación"""

        return len(self.content)

    def degree(self):
        """Devuelve el grado de la relación"""

        return len(self._header)

    def project(self, *args):
        """
        The project operator returns a new relation.
        Extract columns (attributes) resulting in a vertical subset of
        attributes of the relation
        """

        indexes = []
        for arg in args:
            try:
                indexes.append(self._header.index(arg))
            except ValueError as reason:
                raise FieldNotInHeaderError(
                    str(reason).split()[0], self.name)
        # New fields
        header = [self._header[i] for i in indexes]
        # New relation
        new_relation = Relation()
        new_relation.header = header

        for data in self.content:
            new_relation.insert(tuple(data[index] for index in indexes))

        return new_relation

    def select(self, expression):
        """
        The select operator returns a new relation with the tuples that
        satisfy an expression.
        """

        new_relation = Relation()
        new_relation.header = self._header

        expr = compile(expression, "select", "eval")

        for tupla in self.content:
            attrs = {
                attr: RelationStr(tupla[e]).cast()
                for e, attr in enumerate(self.header)
            }
            try:
                if eval(expr, datetime_dict, attrs):
                    new_relation.insert(tupla)
            # FIXME: en qué caso pasa esto?
            except SyntaxError:
                raise SelectionSyntaxError
        return new_relation

    def njoin(self, other_relation):
        # Combino los headers
        header = self._header + other_relation.header

        new_relation = Relation()
        new_relation.header = header

        # Campos en común
        sharedf = set(self._header).intersection(set(other_relation.header))
        final_fields = self._header + [i for i in other_relation.header
                                       if i not in sharedf]
        indexes_r = [self._header.index(i) for i in sharedf]
        indexes_or = [other_relation.header.index(i) for i in sharedf]

        for i, j in itertools.product(self.content, other_relation.content):
            for k, l in itertools.product(indexes_r, indexes_or):
                if i[k] == j[l]:
                    new_relation.insert(i + j)
        # Project para eliminar campos repetidos
        return new_relation.project(*final_fields)

    def louter(self, other_relation):
        header = self.header + other_relation.header

        new_relation = Relation()
        new_relation.header = header

        sharedf = set(self._header).intersection(set(other_relation.header))
        final_fields = self._header + [i for i in other_relation.header
                                       if i not in sharedf]

        indexes_r = [self._header.index(i) for i in sharedf]
        indexes_or = [other_relation.header.index(i) for i in sharedf]

        for i in self.content:
            added = False
            for j in other_relation.content:
                for k, l in itertools.product(indexes_r, indexes_or):
                    if i[k] == j[l]:
                        # Esto es un producto cartesiano con la
                        # condición equi-join
                        new_relation.insert(i + j)
                        added = True
            if not added:
                nulls = ["null" for i in range(len(other_relation.header))]
                new_relation.insert(tuple(list(i) + nulls))

        return new_relation.project(*final_fields)

    def router(self, other_relation):
        r = other_relation.louter(self)
        sharedf = [i for i in other_relation.header if i not in self._header]
        return r.project(*self._header + sharedf)

    def fouter(self, other_relation):
        right = self.router(other_relation)
        left = self.louter(other_relation)
        return right.union(left)

    @union_compatible
    def union(self, other_relation):
        """
        The union is defined as: R ∪ S. Returns the set of tuples in R,
        or S, or both. R and S must be compatible unions.
        """

        new_relation = Relation()
        new_relation.header = self._header
        content = self.content.union(other_relation.content)

        for i in content:
            new_relation.insert(i)

        return new_relation

    @union_compatible
    def difference(self, other_relation):
        """
        The difference is defined as: R - S. It is the set of all tuples
        in R, but not in S. R and S must be compatible unions
        """

        new_relation = Relation()
        new_relation.header = self._header
        content = self.content - other_relation.content
        for i in content:
            new_relation.insert(i)
        return new_relation

    @union_compatible
    def intersect(self, other_relation):
        """
        The intersection is defined as: R ∩ S. corresponds to the set of
        all tuples in R and S, R and S compatible unions.
        """

        new_relation = Relation()
        new_relation.header = self._header
        content = self.content.intersection(other_relation.content)

        for i in content:
            new_relation.insert(i)

        return new_relation

    def product(self, other_relation):
        """
        The cartesian product is defined as: R x S, its outline
        corresponds to a combination of all tuples in R with each S
        tuples, and attributes corresponding to those of R followed by S.

        This method throws an exception when you are duplicate field names
        """

        for field in self._header:
            if field in other_relation.header:
                raise DuplicateFieldError(field)

        new_relation = Relation()
        new_relation.header = self._header + other_relation.header

        for i in self.content:
            for e in other_relation.content:
                new_relation.insert(i + e)

        return new_relation

    def __str__(self):
        """Magic method. Returns a representation of the relation"""
        print()

        header = ""
        for field in self._header:
            header += "|  " + field.center(10) + "  "
        header += "|\n"
        header += "-" * (len(header) - 1) + "\n"

        content = ""
        for rec in self.content:
            for i in rec:
                content += "|  " + i.center(10) + "  "
            content += "|\n"

        return header + content

    def __repr__(self):
        return (f'Relation(name={self.name}, '
                f'degree={self.degree()}, '
                f'cardinality={self.cardinality()})')
