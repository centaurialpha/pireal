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

import shlex
import pytest

from pireal.core import cliparser


@pytest.fixture
def parser():
    return cliparser.get_cli()


def test_parser_help(parser):
    with pytest.raises(SystemExit):
        parser.parse_args(["--help"])


def test_parser_args_valid(parser):
    cmd = ["-d file.pdb", "--database lalala", "-v", "--verbose", "--version"]
    for line in cmd:
        cmdline = shlex.split(line)
        parser.parse_args(cmdline)


def test_parser_args_invalid(parser):
    cmd = ["algo sdsdsd", "-d"]
    for line in cmd:
        cmdline = shlex.split(line)
        with pytest.raises(SystemExit):
            parser.parse_args(cmdline)
