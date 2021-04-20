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
import datetime
from typing import Union


class RType:

    def __init__(self, value: str):
        self.value = value

    @classmethod
    def cast(cls, value: str) -> Union[int, float, datetime.datetime, datetime.time]:
        return cls(value)._cast()

    def _cast(self):
        try:
            value = int(self.value)
        except ValueError:
            try:
                value = float(self.value)
            except ValueError:
                try:
                    value = datetime.datetime.strptime(self.value, '%d/%m/%Y').date()
                except ValueError:
                    try:
                        value = datetime.datetime.strptime(self.value, '%Y/%m/%d').date()
                    except ValueError:
                        try:
                            hour, minute = self.value.split(':')
                        except ValueError:
                            value = self.value
                        else:
                            value = datetime.time(int(hour), int(minute))
        return value
