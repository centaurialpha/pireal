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

from distutils.core import setup
from setuptools import find_packages
import pireal


CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: X11 Applications',
    'License :: OSI Approved :: GNU General Public License v3 or '
    'later (GPLv3+)',
    'Natural Language :: English',
    'Natural Language :: Spanish',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3 :: Only',
    'Topic :: Education',
    'Topic :: Utilities',
]


setup(
    name='pireal',
    version=pireal.__version__,
    license=pireal.__license__,
    author=pireal.__author__,
    author_email=pireal.__email__,
    description='Relational Algebra query evaluator',
    long_description=open('README.md').read(),
    url=pireal.__url__,
    packages=find_packages(exclude=['tests']),
    package_data={
        'pireal': [
            'gui/qml/*',
            'gui/qml/widgets/*',
            'images/pireal_icon.png',
            'lang/*.qm'
        ]
    },
    classifiers=CLASSIFIERS,
    scripts=['bin/pireal']
)
