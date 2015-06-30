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

import argparse
import cmd

NAME = "interpreter"
USAGE = "%(prog)s [ files .rpr ]"
DESCRIPTION = ""
EPILOG = """
for more information please visit http://bitbucket.org/centaurialpha/pireal
"""


def arg_parse():
    """ Parse the command line """

    parser = argparse.ArgumentParser(prog=NAME,
                                     usage=USAGE,
                                     description=DESCRIPTION,
                                     epilog=EPILOG)
    parser.add_argument('file', metavar='file', type=str,
                        nargs='+', help="files to load")
    args = parser.parse_args()

    return args.file


class Interpreter(cmd.Cmd):

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = "pireal > "

    def do_select(self, line):
        pass
