# -*- coding: utf-8 -*-
import sys
import pytest

from pireal.core.pfile import File
from pireal.core.file_manager import detect_encoding
import tokenize


def test_read(tmpdir):
    fh = tmpdir.join('test.pdb')
    fh.write('holá')
    f = File(path=fh.strpath)
    assert f.read() == 'holá'
