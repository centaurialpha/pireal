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

import sys
from code import InteractiveConsole


class Cache(object):
    """Replace stdout and stderr behavior in order to collect outputs."""

    def __init__(self):
        self.reset()

    def reset(self):
        """Clean the cache."""
        self.out = []

    def write(self, line):
        """Collect the output into cache to be accesed later."""
        self.out.append(line)

    def flush(self):
        """Join together all the outputs and return it to be displayed."""
        if len(self.out) > 1:
            output = ''.join(self.out)[:-1]
            self.reset()
            return output


class Console(InteractiveConsole):
    """Work as a Python Console."""

    def __init__(self):
        InteractiveConsole.__init__(self)
        self.stdout = sys.stdout
        self.stderr = sys.stderr
        self._cache = Cache()
        self.output = ''

    def get_output(self):
        """Replace out and error channels with cache."""

        sys.stdout = self._cache
        sys.stderr = self._cache

    def return_output(self):
        """Reassign the proper values to output and error channel."""

        sys.stdout = self.stdout
        sys.stderr = self.stderr

    def push(self, line):
        """Insert a command into the console."""

        self.get_output()
        incomplete = super(Console, self).push(line)
        self.return_output()
        self.output = self._cache.flush()
        return incomplete
