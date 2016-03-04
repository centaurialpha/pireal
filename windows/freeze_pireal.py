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

from cx_Freeze import setup, Executable

opt = {
    'build_exe': {
        'includes': ['PyQt5.QtNetwork'],
        'include_msvcr': True,
        'include_files': []}}

exe = Executable(
    script="pireal",
    base='Win32GUI',
    targetName='Pireal.exe',
    compress=True,
    #icon="windows/pireal.ico"
)

setup(
    name="Pireal",
    version="1.0",
    author="Gabriel Acosta",
    options=opt,
    packages=[
        "src",
        "src.core",
        "src.gui",
        "src.gui.dialogs",
        "src.gui.query_container"
    ],
    package_data={
        "src": ["gui/qml/*"]
    },
    executables=[exe]
)