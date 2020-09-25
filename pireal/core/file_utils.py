# -*- coding: utf-8 -*-
#
# Copyright 2015-2020 - Gabriel Acosta <acostadariogabriel@gmail.com>
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
import locale
import logging

logger = logging.getLogger('file_utils')

DEFAULT_ENCODING = 'utf-8'


def read_file(filepath: str) -> str:
    encoding = detect_encoding(filepath)
    if encoding is None:
        encodings = [DEFAULT_ENCODING, locale.getpreferredencoding()]
    else:
        encodings = [encoding]

    with open(filepath, 'rb') as fh:
        data = fh.read()
    for encoding in encodings:
        logging.info('Triying to decode with %s', encoding)
        try:
            content = data.decode(encoding)
            logger.info('Decoded with %s', encoding)
            break
        except UnicodeDecodeError:
            continue
    else:
        raise UnicodeDecodeError('Unable to decode :(')

    return content


def write_file(filepath: str, content: str):
    with open(filepath, 'w') as fh:
        fh.write(content)


def detect_encoding(filepath: str):
    return None


def get_basename(filename):
    return os.path.basename(filename)


def get_path(filename):
    return os.path.dirname(filename)
