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


def get_basename(filename):

    return os.path.basename(filename)