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

import os


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


def generate_database( relations):
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
