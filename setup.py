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

# import os
# import shutil
from distutils.core import setup
# from distutils.command.install import install
from setuptools import find_packages

import pireal


# class CustomInstall(install):
#
#     def run(self):
#         super().run()
#         for script in self.distribution.scripts:
#             script_path = os.path.join(self.install_scripts, os.path.basename(script))
#             with open(script_path, 'rb') as fp:
#                 content = fp.read()
#             content = content.replace(b'@ BASE_DIR @', self._custom_data_dir.encode())
#             with open(script_path, 'wb') as fp:
#                 fp.write(content)
#
#         source_desktop_file = self.distribution.get_name() + '.desktop'
#         if not os.path.exists(self._custom_apps_dir):
#             os.makedirs(self._custom_apps_dir)
#         dest_desktop_file = os.path.join(self._custom_apps_dir, source_desktop_file)
#         with open(source_desktop_file, 'rb') as fp:
#             content = fp.read()
#         icon = os.path.join(self._custom_data_dir, 'pireal', 'images', 'pireal_icon.png')
#
#         content = content.replace(b'@ INSTALLED_ICON @', icon.encode())
#         with open(dest_desktop_file, 'wb') as fp:
#             fp.write(content)
#
#         # Man page
#         if not os.path.exists(self._custom_man_dir):
#             os.makedirs(self._custom_man_dir)
#         shutil.copy('man/pireal.1', self._custom_man_dir)
#
#     def finalize_options(self):
#         """Cambio el path de instalación
#         Esto se ejecuta antes de run"""
#         super().finalize_options()
#
#         data_dir = os.path.join(self.prefix, 'share', self.distribution.get_name())
#         apps_dir = os.path.join(self.prefix, 'share', 'applications')
#         man_dir = os.path.join(self.prefix, 'share', 'man', 'man1')
#
#         if self.root is None:
#             build_dir = data_dir
#         else:
#             build_dir = os.path.join(self.root, data_dir[1:])
#             apps_dir = os.path.join(self.root, apps_dir[1:])
#             man_dir = os.path.join(self.root, man_dir[1:])
#
#         self.install_lib = build_dir
#         self._custom_data_dir = data_dir
#         self._custom_apps_dir = apps_dir
#         self._custom_man_dir = man_dir


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
    install_requires=['ordered-set'],
    scripts=['bin/pireal'],
)
