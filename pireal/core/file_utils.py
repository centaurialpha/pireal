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
from pathlib import Path

logger = logging.getLogger('file_utils')

DEFAULT_ENCODING = 'utf-8'


def detect_encoding(filepath: str):
    return None


class FileNameError(Exception):
    pass


class File:
    """Represent a file object with extra features"""

    def __init__(self, path: str = None):
        if path is not None:
            self._path = Path(path)
        else:
            self._path = path
        self._created = False
        if not self._exists():
            self._created = True

    @property
    def display_name(self) -> str:
        name = self.filename
        if self._path is not None and not os.access(self._path, os.W_OK):
            name += ' (read-only)'
        return name

    @property
    def filename(self) -> str:
        if self._path is None:
            return 'Untitled'
        return self._path.name

    @property
    def is_new(self) -> bool:
        return self._created

    @property
    def path(self) -> Path:
        return self._path

    def _exists(self) -> bool:
        exists = False
        if self._path is not None and self._path.exists():
            exists = True
        return exists

    def save(self, content: str, path: str = None):
        if path is not None:
            if not isinstance(path, Path):
                path = Path(path)
            self._path = path

        if self._path is None:
            raise FileNameError('No file to save content :/')

        self._path.write_text(content)

    def read(self) -> str:
        if self._path is None:
            raise FileNameError('No file to read :/')
        encoding = detect_encoding(self._path)
        if encoding is None:
            encodings = [DEFAULT_ENCODING, locale.getpreferredencoding]
        else:
            encodings = [encoding]

        data = self._path.read_bytes()

        for encoding in encodings:
            logger.info('Trying to decode %s with %s', self._path, encoding)
            try:
                content = data.decode(encoding)
                break
            except UnicodeDecodeError:
                continue
        else:
            raise UnicodeDecodeError('Unable to decode :(')

        return content
