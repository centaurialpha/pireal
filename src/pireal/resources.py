# Copyright 2015-2025 - Gabriel Acosta <acostadariogabriel@gmail.com>
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

from importlib.resources import files


def _resources(subpackage: str):
    return files("pireal") / "resources" / subpackage


def font(filename: str) -> str:
    return str(_resources("images") / filename)


def translation(lang: str) -> str:
    return str(_resources("lang") / f"{lang}.qm")


def sample(filename: str) -> str:
    return str(_resources("samples") / filename)


def image(filename: str) -> str:
    return str(_resources("images") / filename)
