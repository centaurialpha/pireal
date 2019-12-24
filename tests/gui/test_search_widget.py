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
from unittest.mock import patch

from PyQt5.QtCore import Qt

from pireal.gui.query_container import SearchWidget


@pytest.mark.gui
def test_basic(qtbot):
    widget = SearchWidget(parent=None)
    qtbot.addWidget(widget)

    meth_to_mock = SearchWidget.__module__ + '.SearchWidget._execute_search'
    with patch(meth_to_mock) as mock_es:
        qtbot.mouseClick(widget.btn_find_previous, Qt.LeftButton)
        mock_es.assert_called_with(backward=True)

        qtbot.mouseClick(widget.btn_find_next, Qt.LeftButton)
        mock_es.assert_called_with(find_next=True)
