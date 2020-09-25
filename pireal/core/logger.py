# -*- coding: utf-8 -*-
#
# Copyright 2015-2017 - Gabriel Acosta <acostadariogabriel@gmail.com>
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

import logging
from logging.handlers import RotatingFileHandler

from pireal.dirs import LOGS_DIR
from pireal.core.settings import IS_LINUX

TIME_FORMAT = '%H:%M:%S'
FORMAT = '[{asctime}] [{log_color}{levelname:6}{reset}]: {cyan}{name}.{funcName}{reset}: {message}'

LOG_COLORS = {
    'DEBUG': 'blue',
    'INFO': 'green',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'red'
}
# For color formatter
COLORS = ['black', 'red', 'green', 'yellow', 'blue', 'purple', 'cyan', 'white']
COLORS_DICT = {
    color: '\033[{}m'.format(i)
    for i, color in enumerate(COLORS, start=30)
}
COLOR_RESET = '\033[0m'


class CustomRotatingFileHandler(RotatingFileHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Rotate file at each start of Pireal
        self.doRollover()


class ColoredFormatter(logging.Formatter):
    """Custom formatter with colors.

    NOTE: only works on Linux.
    code based on qutebrowser log.py
    """

    def __init__(self, fmt, datefmt, style, use_colors):
        super().__init__(fmt, datefmt, style)
        self.use_colors = use_colors

    def format(self, record):
        if self.use_colors:
            color_dict = dict(COLORS_DICT)
            color_dict['reset'] = COLOR_RESET
            log_color = LOG_COLORS[record.levelname]
            color_dict['log_color'] = COLORS_DICT[log_color]
        else:
            color_dict = {color: '' for color in COLORS_DICT}
            color_dict['reset'] = ''
            color_dict['log_color'] = ''
        record.__dict__.update(color_dict)
        return super().format(record)


def set_up(debug: bool, verbose: bool):
    log_level = logging.DEBUG if debug else logging.INFO
    root = logging.getLogger()
    log_file = LOGS_DIR / 'the_log.log'
    fhandler = CustomRotatingFileHandler(log_file, maxBytes=1e6, backupCount=10)
    root.addHandler(fhandler)
    # Only use colors in linux
    formatter = ColoredFormatter(FORMAT, TIME_FORMAT, '{', use_colors=IS_LINUX)
    fhandler.setFormatter(formatter)
    root.setLevel(log_level)
    if debug or verbose:
        shandler = logging.StreamHandler()
        shandler.setLevel(log_level)
        shandler.setFormatter(formatter)
        root.addHandler(shandler)
