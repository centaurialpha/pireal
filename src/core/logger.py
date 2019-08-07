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

from src.core.settings import LOG_FILE

FORMAT = "[%(asctime)s] [%(levelname)-6s]: %(name)s:%(funcName)-5s %(message)s"
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'


class CustomRotatingFileHandler(RotatingFileHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Rotate file at each start of Pireal
        self.doRollover()


def set_up(verbose: bool):
    root = logging.getLogger()
    fhandler = CustomRotatingFileHandler(LOG_FILE, maxBytes=1e6, backupCount=10)
    root.addHandler(fhandler)
    formatter = logging.Formatter(FORMAT, TIME_FORMAT)
    fhandler.setFormatter(formatter)
    root.setLevel(logging.DEBUG)
    if verbose:
        shandler = logging.StreamHandler()
        shandler.setFormatter(formatter)
        root.addHandler(shandler)
