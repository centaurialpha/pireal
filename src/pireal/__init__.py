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

# This necesary for sphinx
from typing import cast

from pkg_resources import DistributionNotFound, get_distribution

try:
    __version__ = get_distribution("pireal").version
except DistributionNotFound:
    # package is not installed
    pass

from pireal.gui.main_window import Pireal

instance = None


def get_pireal_instance() -> "Pireal":
    return cast("Pireal", instance)
