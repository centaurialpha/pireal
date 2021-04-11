# Copyright 2015-2020 - Gabriel Acosta <acostadariogabriel@gmail.com>
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
OrderedSet implementation.
Based on https://code.activestate.com/recipes/576694/ by Raymond Hettinger
Based on https://github.com/LuminosoInsight/ordered-set
"""

from collections.abc import MutableSet, Sequence


class OrderedSet(MutableSet):
    """Custom set that remembers its order.
    Yes, it may seem anti-mathematical (?, but this is real life
    """

    def __init__(self, iterable=None):
        self._items = []
        self._map = {}
        if iterable is not None:
            self |= iterable

    def add(self, key):
        if key not in self._map:
            self._map[key] = len(self._items)
            self._items.append(key)
        return self._map[key]

    def intersection(self, other):
        common = (item for item in self if item in other)
        return OrderedSet(common)

    def union(self, other):
        return OrderedSet([*self, *other])

    def difference(self, other):
        diff = (item for item in self if item not in other)
        return OrderedSet(diff)

    def __eq__(self, other):
        if isinstance(other, Sequence):
            return list(self) == other
        return set(self) == other

    def __repr__(self):
        return "%s(%r)" % (self.__class__.__name__, list(self))

    def __reversed__(self):
        return reversed(self._items)

    def __len__(self):
        return len(self._items)

    def __iter__(self):
        return iter(self._map)

    def __contains__(self, key):
        return key in self._map

    def __getitem__(self, index):
        if isinstance(index, slice) or hasattr(index, '__index__'):
            return self._items[index]
        else:
            raise TypeError('Mmmm error with %r', index)

    def __setitem__(self, index, data):
        del self._map[self._items[index]]
        self._items[index] = data
        self._map[data] = index

    def discard(self, key):
        if key in self:
            i = self._map[key]
            del self._items[i]
            del self._map[key]
            for k, v in self._map.items():
                if v >= i:
                    self._map[k] = v - 1
