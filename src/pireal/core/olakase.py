# Copyright 2015-2026 - Gabriel Acosta <acostadariogabriel@gmail.com>
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
No leas esto, no tiene sentido, no deberias estar acá, en serio. No lo hagas.

gabo
"""

import hashlib
import random
from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path


class _Kind(Enum):
    A = auto()
    B = auto()


@dataclass(frozen=True)
class _Momento:
    kind: _Kind


_RA = frozenset(
    {
        "70a7dd5beba0ffa58443cc92866df6a1a86bbe4c225b61be27c9ff43bec09350",
        "f73714d9306875e0729204bb966d54848bf85f3fbea54de685cc929a40ad1860",
        "3ea28c6fe216c121158113f91bc92753a6d56eab28c3567852d26d7d1b9bd241",
    }
)

_PROB = 0.0314
_FLAG = "state/seen"


def _qs(path: Path | None):
    from PyQt6.QtCore import QSettings

    from pireal.dirs import DATA_SETTINGS

    path = path or DATA_SETTINGS
    return QSettings(str(path), QSettings.Format.IniFormat)


def _already_seen(path: Path | None) -> bool:
    return _qs(path).value(_FLAG, False, type=bool)


def check_relation(name: str, *, _hashes: frozenset[str] = _RA) -> _Momento | None:
    if hashlib.sha256(name.lower().encode()).hexdigest() in _hashes:
        return _Momento(kind=_Kind.B)


def check_launch(
    *, rng: random.Random | None = None, prob: float = _PROB, settings_path: Path | None = None
) -> _Momento | None:
    if _already_seen(settings_path):
        return None
    r = rng or random.Random()
    if r.random() < prob:
        return _Momento(kind=_Kind.A)
    return None


def _write_flag(path: Path | None, value: bool) -> None:
    qs = _qs(path)
    qs.setValue(_FLAG, value)
    qs.sync()


def mark_seen(settings_path: Path | None = None) -> None:
    _write_flag(settings_path, True)
