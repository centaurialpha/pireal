# -*- coding: utf-8 -*-
#
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

import pytest
from unittest import mock

from pireal.core.db import DB
from pireal.gui.database_panel import DBPanel


# @pytest.fixture
# def db_panel(qtbot, mocker):
#     mocker.patch('pireal.gui.database_panel.LateralWidget')
#     mock_db = mock.create_autospec(DB)
#     w = DBPanel(db=mock_db)
#     qtbot.addWidget(w)
#     return w


# def test(db_panel):
#     print(db_panel.lateral_widget)
