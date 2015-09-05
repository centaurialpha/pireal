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

import os
from cx_Freeze import (
    setup,
    Executable
)
from src import gui


def get_packages():
    packages = []
    for dir_path, dir_names, filenames in os.walk("src"):
        if '__pycache__' not in dir_path.split('/')[-1]:
            if '__init__.py' in filenames:
                packages.append(dir_path)


opt = {
    'build_exe': {
        'includes': ['PyQt4.QtNetwork'],
        'include_msvcr': True,
        'include_files': []}}


exe = Executable(
    script="pireal.py",
    base="Win32GUI",
    targetName="Pireal.exe",
    compress=True
)


setup(
    name="Pireal",
    version=gui.__version__,
    author=gui.__author__,
    options=opt,
    packages=get_packages(),
    package_data={},
    executables=[exe]
)
