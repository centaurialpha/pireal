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
import shutil
<<<<<<< HEAD
from setuptools.command.install import install
from setuptools import setup, find_packages


class CustomInstall(install):

    def run(self):
        install.run(self)

=======
from setuptools import setup, find_packages

>>>>>>> 3305dee (deploy: add install script to create shortcuts after installation)

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: X11 Applications',
    'License :: OSI Approved :: GNU General Public License v3 or '
    'later (GPLv3+)',
    'Natural Language :: English',
    'Natural Language :: Spanish',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3 :: Only',
    'Topic :: Education',
    'Topic :: Utilities'
]


setup(
<<<<<<< HEAD
    name="pireal",
    version="3.0",
    description="Relational Algebra Interpreter",
    author="Gabriel Acosta",
    author_email="acostadariogabriel@gmail.com",
    url="http://centaurialpha.github.io/pireal",
    license='GPLv3+',
    long_description=open('README.md').read(),
    packages=find_packages(exclude=['tests']),
    scripts=['bin/pireal'],
    classifiers=classifiers,
    cmdclass={'install': CustomInstall},
=======
    name='pireal',
    version=open('version.txt').read().strip(),
    description='Relational Algebra Interpreter',
    author='Gabriel Acosta',
    author_email='acostadariogabriel@gmail.com',
    url='http://centaurialpha.github.io/pireal',
    license='GPLv3+',
    long_description=open('README.md').read(),
    packages=find_packages(exclude=['tests']),
    package_data={
        'pireal': ['resources/samples/*', 'resources/images/pireal_icon.png'],
    },
    scripts=['bin/pireal'],
    classifiers=classifiers,
    install_requires=['pyqt5'],
    extras_require={
        'test': ['flake8', 'pycodestyle', 'pytest', 'pytest-cov'],
        'dev': ['ipython'],
    }
>>>>>>> 3305dee (deploy: add install script to create shortcuts after installation)
)
