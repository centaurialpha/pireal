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

from src.core.rtypes import RelationStr

IS_VALID_FIELD_NAME = re.compile("^[_á-úa-zA-Z][_á-úa-zA-Z0-9]*$")

datetime_dict = {
    'datetime': __import__('datetime')
}


class Error(Exception):
    """Base exception"""


class FieldError(Error):
    def __init__(self, campo, msg=None):
        if msg is None:
            msg = "Error con el campo '{}'".format(campo)
        super().__init__(msg)
        self.campo = campo


class InvalidFieldNameError(FieldError):
    """Excepción lanzada cuando un nombre de campo no es válido"""

    def __init__(self, campo, msg=None):
        super().__init__(
            campo, msg="El nombre de campo '{}' no es válido".format(campo))


class DuplicateFieldError(FieldError):

    def __init__(self, campo, msg=None):
        super().__init__(
            campo, msg="Campo duplicado '{}' en la operación producto".format(
                campo))


class FieldNotInHeaderError(FieldError):
    """Excepción lanzada cuando un campo no existe en la relación"""

    def __init__(self, campo, relacion, msg=None):
        super().__init__(campo, msg="El campo '{}' no existe en '{}'".format(
            campo, relacion))
        self.nombre_relacion = relacion


class WrongSizeError(Error):
    """Excepción lanzada cuando se trata de insertar un tamaño de
    tuplas diferente a los que acepta la relación"""

    def __init__(self, expected, got, msg=None):
        if msg is None:
            msg = "Wrong size. Expected {}, got {}".format(expected, got)
        super().__init__(msg)
        self.expected = expected
        self.got = got


class UnionCompatibleError(Error):
    pass


def union_compatible(operation):
    """Decorador que comprueba que dos relaciones sean compatibles"""
    def inner(self, *args, **kwargs):
        header_other = args[0].header
        if len(self._header) != len(header_other):
            raise UnionCompatibleError(
                "Union not compatible for '{}'".format(operation.__name__))
        return operation(self, *args, **kwargs)
    return inner


class Relation(object):

    def __init__(self):
        self.content = set()
        self._header = []
        self.name = ""
        self._null_count = 1

    @property
    def header(self):
        return self._header

    @header.setter
    def header(self, header: list):
        for field in header:
            if not IS_VALID_FIELD_NAME.match(field):
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

        null_row = ["null ({})".format(self._null_count)
                    for i in range(self.degree())]
        self.insert(tuple(null_row))
        self._null_count += 1

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
            attrs = {attr: RelationStr(tupla[e]).cast()
                     for e, attr in enumerate(self.header)}
            try:
                if eval(expr, datetime_dict, attrs):
                    new_relation.insert(tupla)
            except SyntaxError:
                raise Exception("Error")
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


# class Relation(object):
#     """
#     Esta clase representa un objeto Relation.
#     Un objeto Relation tiene dos atributos (content y header), el content o
#     contenido es una lista de listas, estas listas representan las tuplas o
#     filas de la relación (uso listas para poder modificar la relación), la
#     cantidad de filas o listas dentro de la lista content es la cardinalidad
#     de la relación (ver el método Relation.cardinality()).

#     El header es una lista con los nombres de campos, el tamaño del header
#     es el grado de la relación (ver el método Relation.degree()).

#     Un objeto de ésta clase tiene las operaciones básicas y derivadas
#     del Álgebra Relacional como: Selección, Proyección, Producto, Unión,
#     Intersección, Diferencia, Join Natural y Outher Joins (Left, Right y Full).

#     Ejemplo del uso de la clase:

#     - Creo el objeto y le agrego los campos o header
#     personas = Relation()
#     personas.header = ["id_persona", "nombre", "ciudad"]

#     - Creo una lista con los datos para cada campo
#     tuplas = [
#         ["1", "Gabriel", "Belén"],
#         ["32", "Mercedes", "SFV de Catamarca"],
#         ["23", "Rodrigo", "Belén"]
#     ]

#     - Agrego las tuplas a la relación
#     for t in tuplas:
#         personas.insert(t)

#     - Puedo ver la representación de la relación haciendo:
#     print(personas)

#     |  id_persona  |    nombre    |    ciudad    |
#     ----------------------------------------------
#     |      1       |   Gabriel    |    Belén     |
#     |      32      |   Mercedes   |  SFV de Catamarca  |
#     |      23      |   Rodrigo    |    Belén     |


#     - Ejemplo de Seleción:
#     personas.select("nombre == 'Gabriel'")
#     """

#     def __init__(self):
#         self.content = Content()
#         self.__header = list()

#     def insert(self, record):
#         """ Inserts a register

#         :param record: A record (tuple)
#         """

#         self.content.add(record)

#     def append_row(self):
#         """ Agrega una fila/tupla al final """

#         null_row = ['null' for i in range(self.degree())]
#         self.insert(null_row)

#     def append_column(self):
#         """ Agrega una columna al final de la tabla con valores 'null' """

#         self.__header.append('null')
#         for t in self.content:
#             t.append('null')

#     def remove_column(self, column):
#         """ Elimina la columna @column """

#         # Primero elimino el campo
#         del self.__header[column]
#         # Ahora elimino las tuplas en ese campo
#         for t in self.content:
#             del t[column]

#     def __set_header(self, header):
#         """ Set header to the relation """

#         for field in header:
#             if not IS_VALID_FIELD_NAME.match(field):
#                 raise Exception("'{f}' is not a valid field name".format(
#                     f=field))

#         self.__header = header

#     def __get_header(self):
#         """ Get the header """

#         return self.__header

#     header = property(__get_header, __set_header)

#     def clear(self):
#         """ Clear all content of the relation except the header """

#         pass

#     def update(self, row, column, value):
#         self.content[row][column] = value

#     def cardinality(self):
#         """ Devuelve la cantidad de filas o tuplas de la relación """

#         return len(self.content)

#     def degree(self):
#         """ Devuelve el grado de la relación """

#         return len(self.header)

#     def select(self, expression):
#         """
#         The select operator returns a new relation with the tuples that
#         satisfy an expression.

#         :param expression: A python valid expression
#         :returns: A new relation with the tuples that satisfy an *expression*
#         """

#         new_relation = Relation()
#         new_relation.header = self.__header

#         # Filtering
#         d = {}
#         for register in self.content:
#             for e, attr in enumerate(self.__header):
#                 d[attr] = RelationStr(register[e]).cast()
#             # The expression is evaluated
#             try:
#                 if eval(expression, datetime_dict, d):
#                     new_relation.insert(register)
#             except SyntaxError:
#                 raise Exception("Couldn't be evaluate the expression: "
#                                 "'{}'".format(expression))

#         return new_relation

#     def project(self, *args):
#         """ The project operator returns a new relation.
#         Extract columns (attributes) resulting in a vertical subset of
#         attributes of the relation

#         :param args: A tuple of field names
#         :returns: A new relation with the new fields
#         """

#         indexes = []
#         for arg in args:
#             try:
#                 indexes.append(self.__header.index(arg))
#             except ValueError as reason:
#                 field = reason.__str__().split()[0]
#                 raise Exception("Invalid field name: {}".format(field))
#         # New fields
#         header = [self.__header[i] for i in indexes]

#         # New relation
#         new_relation = Relation()
#         new_relation.header = header

#         for rec in self.content:
#             new_relation.insert([rec[index] for index in indexes])

#         return new_relation

#     def product(self, other_relation):
#         """
#         The cartesian product is defined as: R x S, its outline
#         corresponds to a combination of all tuples in R with each S
#         tuples, and attributes corresponding to those of R followed by S.

#         This method throws an exception when you are duplicate field names

#         :param other_relation: Relation
#         :returns: A new relation
#         """

#         # Check if there are duplicate fields
#         for i in self.__header:
#             if i in other_relation.header:
#                 raise Exception("Duplicate field name '{}'"
#                                 " in product operation".format(i))

#         new_relation = Relation()
#         new_relation.header = self.__header + other_relation.header

#         for i in self.content:
#             for e in other_relation.content:
#                 new_relation.insert(i + e)

#         return new_relation

#     def njoin(self, other_relation):
#         """  """

#         # Combination of the headers
#         header = self.__header + other_relation.header

#         new_relation = Relation()
#         new_relation.header = header

#         # Shared field names
#         sharedf = set(self.__header).intersection(set(other_relation.header))
#         ss = self.__header + [i for i in other_relation.header
#                               if i not in sharedf]

#         # Relation indexes field names
#         indexes_rela = [self.__header.index(i) for i in sharedf]
#         # Other relation indexes field names
#         indexes_other_rela = [other_relation.header.index(i) for i in sharedf]

#         for i in self.content:
#             for j in other_relation.content:
#                 for k in indexes_rela:
#                     for l in indexes_other_rela:
#                         if i[k] == j[l]:
#                             new_relation.insert(i + j)

#         return new_relation.project(*ss)

#     def louter(self, other):
#         header = self.__header + other.header

#         new_relation = Relation()
#         new_relation.header = header

#         sharedf = set(self.__header).intersection(set(other.header))
#         ss = self.__header + [i for i in other.header if i not in sharedf]

#         indexes_rela = [self.__header.index(i) for i in sharedf]
#         indexes_other = [other.header.index(i) for i in sharedf]

#         for i in self.content:
#             added = False
#             for j in other.content:
#                 for k in indexes_rela:
#                     for l in indexes_other:
#                         if i[k] == j[l]:
#                             # Esto es un producto cartesiano con la
#                             # condición equi-join
#                             new_relation.insert(i + j)
#                             added = True
#             if not added:
#                 nulls = ['null' for i in range(len(other.header))]
#                 new_relation.insert(i + nulls)

#         return new_relation.project(*ss)

#     def router(self, other):
#         r = other.louter(self)
#         sharedf = [i for i in other.header if i not in self.header]
#         return r.project(*self.header + sharedf)

#     def fouter(self, other):
#         right = self.router(other)
#         left = self.louter(other)
#         return right.union(left)

#     def intersect(self, other_relation):
#         """ The intersection is defined as: R ∩ S. corresponds to the set of
#         all tuples in R and S, R and S compatible unions.

#         :param other_relation: Relation object
#         :returns: A new relation
#         """

#         if self.__header != other_relation.header:
#             raise Exception("Not union compatible for intersection")

#         new_relation = Relation()
#         new_relation.header = self.__header
#         content = self.content.intersection(other_relation.content)

#         if not content:
#             return new_relation

#         for i in content:
#             new_relation.insert(i)

#         return new_relation

#     def difference(self, other_relation):
#         """ The difference is defined as: R - S. It is the set of all tuples
#         in R, but not in S. R and S must be compatible unions

#         :param other_relation: Relation object
#         :returns: A new relation
#         """

#         if self.header != other_relation.header:
#             raise Exception("Not union compatible for difference")

#         new_relation = Relation()
#         new_relation.header = self.header
#         content = self.content.difference(other_relation.content)

#         for i in content:
#             new_relation.insert(i)

#         return new_relation

#     def union(self, other_relation):
#         """ The union is defined as: R ∪ S. Returns the set of tuples in R,
#         or S, or both. R and S must be compatible unions.

#         :param other_relation: Relation object
#         :returns: A new relation
#         """

#         # if self.header != other_relation.header:
#         #    raise Exception("Not union compatible")

#         new_relation = Relation()
#         new_relation.header = self.header
#         content = self.content.union(other_relation.content)

#         for i in content:
#             new_relation.insert(i)

#         return new_relation

#     def __str__(self):
#         """ Magic method. Returns a representation of the relation

#         |      id      |     name     |    skill     |
#         ----------------------------------------------
#         |      8       |   Mariela    |     Chef     |
#         |      4       |   Rodrigo    |    Gamer     |
#         |      2       |   Gabriel    |    Python    |
#         """

#         header = ""
#         for field in self.__header:
#             header += "|  " + field.center(10) + "  "
#         header += "|\n"
#         header += "-" * (len(header) - 1) + "\n"

#         content = ""
#         for rec in self.content:
#             for i in rec:
#                 content += "|  " + i.center(10) + "  "
#             content += "|\n"

#         return header + content
