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
import json
import codecs


def get_extension(filename):
    """ This function returns the extension of filename

    :param filename: Filename path
    :returns: The extension file
    """

    return os.path.splitext(filename)[-1]


def write_database(filename, data):
    try:
        with open(filename, mode='w') as f:
            json.dump(data, f)
    except Exception:
        raise Exception("Directory not found: {}".format(filename))


def open_database(filename):
    try:
        with open(filename, mode='r') as f:
            return get_basename(filename), f.read()
    except Exception:
        raise


def read_rdb_file(filename):
    content = codecs.open(filename, 'r', 'iso-8859-1').read()
    return content


def convert_to_pdb(rdb_content):
    content = ""
    for line in rdb_content.splitlines():
        if line.startswith('@'):
            content += "@"
            portion = line.split('(')
            name = portion[0][1:]
            content += name + ':'
            for i in portion[1].split(','):
                if not i.startswith(' '):
                    field = i.split('/')[0].strip()
                    content += field + ','
        else:
            if not line:
                continue

            for lline in line.splitlines():
                lline = lline.replace('\'', '')
                line = lline
            content += line
        content += '\n'
    return content


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

    :param relations: Dictionary with relations
    :returns: The content of the database
    """

    content = ""
    for relation_name, relation in list(relations.items()):
        content += '@' + relation_name
        content += ':' + ','.join(relation.fields) + '\n'
        for i in relation.content:
            content += ','.join(i) + '\n'
    return content


def get_files_from_folder(path):
    return [os.path.splitext(f)[0] for f in os.listdir(path)
            if os.path.isfile(os.path.join(path, f))]
