# -*- coding: utf-8 -*-
#
# Copyright 2015-2016 - Gabriel Acosta <acostadariogabriel@gmail.com>
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
import logging

from pireal.core import file_manager

logger = logging.getLogger(__name__)


class File:

    def __init__(self, path=None):
        self._path = path

    @property
    def display_name(self) -> str:
        return os.path.basename(self._path)

    @property
    def path(self) -> str:
        return self._path

    def is_new(self):
        return self._path is None

    def read(self):
        try:
            with open(self._path) as fp:
                content = fp.read()
            return content
        except IOError:
            logging.exception('Could not open file: %s', self._path)

    def save(self, content, path=None):
        with open(path, 'w') as fp:
            fp.write(content)
        self._path = path
        return self
