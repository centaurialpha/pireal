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
import sys
from src.core import settings

LOG_FORMAT = "[%(asctime)s]:%(levelname)-7s:%(name)s:%(message)s"
TIME_FORMAT = "%H:%M:%S"


class CustomFormatter(logging.Formatter):
    """ Custom Formatter with colors """

    RESET = '\x1b[0m'
    YELLOW = '\x1b[33m'
    RED = '\x1b[31m'
    GREEN = '\x1b[32m'
    BLUE = '\x1b[34m'

    def format(self, record, colour=False):
        msg = super().format(record)

        if not colour:
            return msg

        level = record.levelno
        if level >= logging.CRITICAL:
            colour = self.RED
        elif level >= logging.ERROR:
            colour = self.RED
        elif level >= logging.WARNING:
            colour = self.YELLOW
        elif level >= logging.INFO:
            colour = self.BLUE
        elif level >= logging.DEBUG:
            colour = self.GREEN
        else:
            colour = self.RESET

        return colour + msg + self.RESET


class CustomHandler(logging.StreamHandler):

    def __init__(self, stream=sys.stdout):
        super(CustomHandler, self).__init__(stream)

    def format(self, record, colour=False):
        if not isinstance(self.formatter, CustomFormatter):
            self.formatter = CustomFormatter()

        return self.formatter.format(record, colour)

    def emit(self, record):
        stream = self.stream
        try:
            msg = self.format(record, stream.isatty())
            stream.write(msg)
            stream.write(self.terminator)
            self.flush()
        except Exception:
            self.handlerError(record)


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    if settings.LINUX:
        # Handler
        handler = CustomHandler()
        # Formatter
        formatter = CustomFormatter(LOG_FORMAT, TIME_FORMAT)
    else:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(LOG_FORMAT, TIME_FORMAT)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
