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

from pireal.dirs import LOGS_DIR

FORMAT = "[%(asctime)s] [%(levelname)-6s]: %(name)s:%(funcName)-5s %(message)s"
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'


def set_up(verbose: bool):
    root = logging.getLogger()
    handler = logging.FileHandler(LOGS_DIR / 'the_log.log')
    root.addHandler(handler)
    formatter = logging.Formatter(FORMAT, TIME_FORMAT)
    handler.setFormatter(formatter)
    root.setLevel(logging.DEBUG)
    if verbose:
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        root.addHandler(handler)
