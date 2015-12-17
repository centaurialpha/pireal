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
import logging.handlers
import time

from src.core import settings

LOG_FORMAT = "[%(asctime)s]:%(levelname)-7s:%(name)s:%(funcName)s:%(message)s"
TIME_FORMAT = "%H:%M:%S"
HEADER = "Nueva sesión de Pireal: {date}".format(
    date=time.strftime("%Y-%m-%d"))


class PLogger(object):
    """
    Logger

    Usage:
        from logger import PLogger

        logger = PLogger('example')

        logger.debug("Message debug")
        logger.info("Message info")
        logger.critical("Message error")
    """

    def __init__(self, header=None, separator='='):
        self._handler = None
        self._header = None
        self._loggers = {}
        if header is not None:
            # Default separator is `=` at 80 cols
            # You can change the separator when create PLogger object
            separator *= 80
            # Create header
            self._header = separator + '\n' + header + '\n' + separator

        logging.basicConfig()

    def __call__(self, name):
        if self._handler is None:
            if self._header is not None:
                handler = CustomFileHandler(settings.LOG_FILE_PATH,
                                            self._header)
            else:
                handler = logging.FileHandler(settings.LOG_FILE_PATH)
            formatter = logging.Formatter(fmt=LOG_FORMAT, datefmt=TIME_FORMAT)
            handler.setFormatter(formatter)
            self._handler = handler
        if name not in self._loggers:
            logger = logging.getLogger(name)
            self._loggers[name] = logger
            logger.setLevel(logging.DEBUG)
            logger.addHandler(self._handler)

        return self._loggers[name]


class CustomFileHandler(logging.handlers.RotatingFileHandler):
    """ Custom Rotating File Handler with header """

    def __init__(self, filename, header, mode='a', maxBytes=50000,
                  backupCount=1, encoding=None, delay=0):
        super(CustomFileHandler, self).__init__(filename, mode, maxBytes,
                                                    backupCount, encoding,
                                                    delay)

        # The header is added at each new session
        if not delay and self.stream is not None:
            self.stream.write('{header}\n'.format(header=header))


# Create logger with header
PirealLogger = PLogger(HEADER)
