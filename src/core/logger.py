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

from src.core.settings import LOG_PATH

FORMAT = "[%(asctime)s] [%(levelname)-6s]: %(name)-22s:%(funcName)-5s %(message)s"
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

# class _Logger(object):
#     LEVELS = {
#         'critical': 50,
#         'error': 40,
#         'warning': 30,
#         'info': 20,
#         'debug': 10,
#         'no': 0
#     }

#     def __init__(self):
#         self.__level = 0  # Default not logging
#         logging.basicConfig(format=FORMAT)
#         self.__loggers = {}

#     def __call__(self, name):
#         if name not in self.__loggers:
#             logger = logging.getLogger(name)
#             self.__loggers[name] = logger
#             logger.setLevel(self.__level)
#         return self.__loggers[name]

#     def set_level(self, level):
#         """ Set level for all loggers """

#         if level in self.LEVELS.keys():
#             self.__level = self.LEVELS[level]
#             for log in self.__loggers.keys():
#                 logger = self.__loggers[log]
#                 logger.setLevel(self.__level)


def set_up(verbose: bool):
    root = logging.getLogger()
    handler = logging.FileHandler(LOG_PATH)
    root.addHandler(handler)
    formatter = logging.Formatter(FORMAT, TIME_FORMAT)
    handler.setFormatter(formatter)
    root.setLevel(logging.DEBUG)
    if verbose:
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        root.addHandler(handler)

