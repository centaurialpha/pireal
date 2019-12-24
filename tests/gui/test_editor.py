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

from PyQt5.QtGui import QTextCursor

from pireal.gui.query_container.editor import Editor


@pytest.fixture
def editor(qtbot):
    widget = Editor(file=None)
    qtbot.addWidget(widget)
    return widget


@pytest.mark.gui
@pytest.mark.parametrize(
    'move, expected_word',
    [
        (6, 'Pireal'),
        (14, 'cómo'),
        (22, 'estas'),
    ]
)
def test_word_under_cursor(editor, move, expected_word):
    text = 'hola Pireal, cómo estas?'
    editor.setPlainText(text)

    cursor: QTextCursor = editor.textCursor()
    editor.moveCursor(QTextCursor.Start)

    cursor.movePosition(
        QTextCursor.Right,
        QTextCursor.MoveAnchor,
        move
    )
    editor.setTextCursor(cursor)

    expected_cursor = editor.word_under_cursor()

    assert isinstance(expected_cursor, QTextCursor)
    assert expected_cursor.selectedText() == expected_word


@pytest.mark.gui
def test_comment_uncomment(editor):
    text = 'hola\ncómo\nestasss?\n??'
    editor.setPlainText(text)

    expected_text = '% hola\ncómo\nestasss?\n??'

    editor.comment()

    assert editor.toPlainText() == expected_text

    editor.uncomment()

    assert editor.toPlainText() == text


@pytest.mark.gui
def test_comment_uncomment_all(editor):
    text = 'hola\ncómo\nestasss?\n??'
    editor.setPlainText(text)

    expected_text = '% hola\n% cómo\n% estasss?\n% ??'

    editor.selectAll()
    editor.comment()

    assert editor.toPlainText() == expected_text

    editor.uncomment()

    assert editor.toPlainText() == text


@pytest.mark.gui
@pytest.mark.parametrize(
    'to_search, case_sensitive, expected_pos',
    [
        ('pireal', True, 13),
        ('PIREAL', True, 6),
        ('gabo', False, 50)
    ]
)
def test_find_text(editor, to_search, case_sensitive, expected_pos):
    text = 'PIREAL pireal es un programa desarrollado por gabo'
    editor.setPlainText(text)

    editor.find_text(to_search, cs=case_sensitive)

    tc = editor.textCursor()
    assert tc.position() == expected_pos
