# -*- coding: utf-8 -*-
#
# Copyright 2015-2019 - Gabriel Acosta <acostadariogabriel@gmail.com>
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

import argparse


def get_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--database', help='Database file')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose')
    parser.add_argument('--version', action='store_true', help='Version')
    parser.add_argument('--no-check-updates', action='store_true',
                        help='Disable check for updates')
    return parser
