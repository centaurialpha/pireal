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

from collections import defaultdict
import csv
import os


class DBParserSyntaxError(Exception):
    pass


def get_extension(filename):
    """ This function returns the extension of filename

    :param filename: Filename path
    :returns: The extension file
    """

    return os.path.splitext(filename)[-1]


def get_basename(filename):
    """ This function returns the base name of filename

    :param filename: Filename, for example: "/home/gabo/file.rpf"
    :returns: The base name, for example: "file"
     """

    return os.path.splitext(os.path.basename(filename))[0]


def get_path(filename):

    return os.path.dirname(filename)


def generate_database(relations):
    """ This function generates the content of the database

    :param relations: Dictionary with relations (Relation Object)
    :returns: The content of the database
    """

    content = ""
    for relation_name, relation in list(relations.items()):
        content += '@%s:' % relation_name
        header = ','.join(relation.header)
        content += header + '\n'
        for i in relation.content:
            content += ','.join(i) + '\n'
        content += '\n'
    # Remove last line
    content = content[:-1]
    return content


def get_files_from_folder(path):
    return [os.path.splitext(f)[0] for f in os.listdir(path)
            if os.path.isfile(os.path.join(path, f))]


def parse_database_content(text):
    """
    Este método convierte el contenido de la base de datos a un
    diccionario para un mejor manejo despues
    """
    # FIXME: controlar cuando al final de la línea hay una coma
    data_dict = defaultdict(list)
    for line_count, line in enumerate(text.splitlines()):
        # Ignore blank lines
        if not line.strip():
            continue
        if line.startswith("@"):
            # Header de una relación
            tpoint = line.find(":")
            if tpoint == -1:
                raise DBParserSyntaxError("Syntax error, line {}".format(
                    line_count + 1))
            table_name, line = line.split(":")
            table_name = table_name[1:].strip()
            table_dict = {}
            table_dict["name"] = table_name
            table_dict["header"] = list(map(str.strip, line.split(",")))
            table_dict["tuples"] = set()
        else:
            # Tuplas de la relación
            for l in csv.reader([line]):
                tupla = tuple(map(str.strip, l))
                table_dict["tuples"].add(tupla)
        if not table_dict["tuples"]:
            data_dict["tables"].append(table_dict)
    return data_dict
