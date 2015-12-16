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

"""
Logging
"""

import logging
import time

from src.core import settings

LOG_FORMAT = "[%(asctime)s]:%(levelname)-7s:%(name)s:%(funcName)s:%(message)s"
TIME_FORMAT = "%H:%M:%S"
_line = '=' * 80 + '\n'
HEADER = _line + "Nueva sesión de Pireal: {date}".format(
    date=time.strftime("%Y-%m-%d")) + '\n'
HEADER += _line


class PLogger(object):
    """ Logger for Pireal """

    def __init__(self):
        self._handler = None
        self._loggers = {}
        logging.basicConfig()

    def __call__(self, name):
        if self._handler is None:
            handler = FileHandlerWithHeader(settings.LOG_FILE_PATH, HEADER)
            formatter = logging.Formatter(fmt=LOG_FORMAT, datefmt=TIME_FORMAT)
            handler.setFormatter(formatter)
            self._handler = handler
        if name not in self._loggers:
            logger = logging.getLogger(name)
            self._loggers[name] = logger
            logger.setLevel(logging.DEBUG)
            logger.addHandler(self._handler)
        return self._loggers[name]


class FileHandlerWithHeader(logging.FileHandler):
    """ Custom Handler with title """

    def __init__(self, filename, header, mode='a', encoding=None, delay=0):
        super(FileHandlerWithHeader, self).__init__(filename, mode,
                                                    encoding, delay)
        # The title is added at each new session
        if not delay and self.stream is not None:
            self.stream.write('{header}\n'.format(header=header))


PirealLogger = PLogger()