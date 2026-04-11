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

import hashlib
import random

from pireal.core.olakase import (
    _RA,
    _Kind,
    _Momento,
    check_launch,
    check_relation,
    mark_seen,
)


class TestCheckRelation:
    def test_magic_name_triggers(self):
        fake_hash = hashlib.sha256(b"testmagic").hexdigest()
        result = check_relation("testmagic", _hashes=frozenset({fake_hash}))
        assert result == _Momento(kind=_Kind.B)

    def test_case_insensitive(self):
        fake_hash = hashlib.sha256(b"testmagic").hexdigest()
        result = check_relation("TESTMAGIC", _hashes=frozenset({fake_hash}))
        assert result == _Momento(kind=_Kind.B)

    def test_unknown_name_returns_none(self):
        fake_hash = hashlib.sha256(b"testmagic").hexdigest()
        assert check_relation("students", _hashes=frozenset({fake_hash})) is None

    def test_empty_name_returns_none(self):
        assert check_relation("", _hashes=frozenset()) is None

    def test_real_hashes_exist(self):
        assert len(_RA) == 3
        assert all(len(h) == 64 for h in _RA)


class TestCheckLaunch:
    def test_always_triggers_with_prob_1(self, tmp_path, qapp):
        path = tmp_path / "s.ini"
        rng = random.Random(42)
        result = check_launch(rng=rng, prob=1.0, settings_path=path)
        assert result == _Momento(kind=_Kind.A)

    def test_probability_roughly_correct(self, tmp_path, qapp):
        results = []
        for i in range(1000):
            path = tmp_path / f"s{i}.ini"
            rng = random.Random(i)
            results.append(check_launch(rng=rng, prob=0.0314, settings_path=path))
        triggered = [r for r in results if r is not None]
        # 3.14% de 1000 → ~31; margen amplio
        assert 10 < len(triggered) < 80

    def test_mark_seen_persists(self, tmp_path, qapp):
        path = tmp_path / "s.ini"
        mark_seen(settings_path=path)
        # Nueva instancia de QSettings, mismo archivo
        from PyQt6.QtCore import QSettings

        qs = QSettings(str(path), QSettings.Format.IniFormat)
        assert qs.value("state/seen", False, type=bool) is True
