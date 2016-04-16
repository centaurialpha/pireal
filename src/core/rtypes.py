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

import re
from datetime import datetime


class RelationStr(str):

    # Positive or negative integers
    IS_INT = re.compile(r'^[\-]?\d+$')
    # Positive or negative floats
    IS_FLOAT = re.compile(r'^[\-]?\d+(\.\d*)$')
    # YYYY/MM/DD
    IS_DATE = re.compile(
        r'^([\d+]{2}|[\d+]{4})[\/][\d+]{2}[\/]([\d+]{2}|[\d+]{4})$')
    # HH:MM
    IS_HOUR = re.compile(r'^[\d+]{2}:[\d+]{2}$')

    def __init__(self, value):
        super(RelationStr, self).__init__()
        self.value = value

    def cast(self):
        if RelationStr.IS_INT.match(self.value):
            return int(self.value)
        elif RelationStr.IS_FLOAT.match(self.value):
            return float(self.value)
        elif RelationStr.IS_DATE.match(self.value):
            return RelationDate(self.value)
        elif RelationStr.IS_HOUR.match(self.value):
            return RelationHour(self.value)
        return self.value


class RelationHour(object):
    """ This class represents a hour """

    def __init__(self, str_hour):
        hour = datetime.strptime(str_hour, "%H:%M").time()
        self.hour = hour.hour
        self.min = hour.minute


class RelationDate(object):
    """ This class represents a date """

    def __init__(self, value):
        try:
            date = datetime.strptime(value, "%d/%m/%Y")
        except ValueError:
            date = datetime.strptime(value, "%Y/%m/%d")
        self.year = date.year
        self.day = date.day
        self.month = date.month
