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
import codecs
# import locale
import logging

DEFAULT_ENCODING = 'utf-8'


logger = logging.getLogger('core.file_manager')


class DBParserSyntaxError(Exception):
    pass


class FileIOError(Exception):
    pass


# class File:
#     """File representation"""

#     def __init__(self, path=None):
#         self._path = path

#     @property
#     def path(self) -> str:
#         return self._path

#     @property
#     def display_name(self) -> str:
#         if self._path is None:
#             return 'Untitled'
#         return get_basename_with_extension(self._path)

#     @property
#     def filename(self) -> str:
#         return get_basename_with_extension(self._path)

#     @property
#     def is_new(self) -> bool:
#         file_is_new = True
#         if self._exists():
#             file_is_new = False
#         return file_is_new

#     def save(self, content: str, *, path=None):
#         if path is not None:
#             self._path = path
#         with open(self._path, 'w') as fh:
#             fh.write(content)

#     def _exists(self) -> bool:
#         file_exists = False
#         if self._path is not None and os.path.exists(self._path):
#             file_exists = True
#         return file_exists

#     def read(self) -> str:
#         """Read the contents of _path"""
#         if not self._exists():
#        raise FileNotFoundError('You asked me to read the file but the file does not exist gg')
#         # Try to detect encoding
#         encoding = detect_encoding(self._path)
#         if encoding is None:
#             encodings = [DEFAULT_ENCODING, locale.getpreferredencoding()]
#         else:
#             encodings = [encoding]

#         with open(self._path, 'rb') as fh:
#             data = fh.read()

#         for encoding in encodings:
#             logger.info('Triying to decode with %s', encoding)
#             try:
#                 content = data.decode(encoding)
#                 logger.info('Decoded with %s', encoding)
#                 break
#             except UnicodeDecodeError:
#                 continue
#         else:
#             # So sad :/
#             raise UnicodeDecodeError('Unable to decode')
#         return content


# def get_extension(filename):
#     """ This function returns the extension of filename

#     :param filename: Filename path
#     :returns: The extension file
#     """

#     return os.path.splitext(filename)[-1]


# def get_basename(filename):
#     """ This function returns the base name of filename

#     :param filename: Filename, for example: "/home/gabo/file.rpf"
#     :returns: The base name, for example: "file"
#     """

#     return os.path.splitext(get_basename_with_extension(filename))[0]


# def get_basename_with_extension(filename):
#     return os.path.basename(filename)


def get_path(filename):

    return os.path.dirname(filename)


def generate_database(relations) -> str:
    """ This function generates the content of the database

    :param relations: Dictionary with relations (Relation Object)
    :returns: The content of the database
    """
    content = ''
    for relation_name, relation in relations.items():
        header = ','.join(relation.header)
        content += f'@{relation_name}:{header}\n'
        for tuples in relation.content:
            content += ','.join(tuples) + '\n'
        content += '\n'
    content = content[:-1]
    return content


def get_files_from_folder(path):
    return [os.path.splitext(f)[0] for f in os.listdir(path)
            if os.path.isfile(os.path.join(path, f))]


def detect_encoding(filepath):
    with open(filepath, 'rb') as fh:
        line = fh.readline()

    boms = [
        (codecs.BOM_UTF8, 'utf-8-sig'),
        (codecs.BOM_UTF16_BE, 'utf-16'),
        (codecs.BOM_UTF16_LE, 'utf-16'),
    ]

    for bom, encoding in boms:
        if line.startswith(bom):
            return encoding

    return None


def parse_database_content(text) -> list:
    data_list = []

    text_lines = map(str.strip, text.split('@'))
    for text_line in text_lines:
        if not text_line:
            continue
        data = {}
        content = text_line.split('\n')
        db_name, header = content[0].split(':')
        data['name'] = db_name
        data['header'] = list(map(str.rstrip, header.split(',')))

        data['tuples'] = [tuple(map(str.rstrip, t.split(',')[:len(data['header'])]))
                          for t in content[1:]]

        data_list.append(data)

    return data_list
