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
from distutils.command.install import install
from distutils.core import setup


class CustomInstall(install):
    """
    Custom installation class on package files.

    It copies all the files into the "PREFIX/share/pireal" dir.
    """

    def run(self):
        install.run(self)

        for script in self.distribution.scripts:
            script_path = os.path.join(self.install_scripts,
                                       os.path.basename(script))
            with open(script_path, 'r') as f:
                content = f.read()
            content = content.replace('@ INSTALLED_BASE_DIR @',
                                      self._custom_data_dir)
            with open(script_path, 'w') as f:
                f.write(content)

            src_desktop = self.distribution.get_name() + '.desktop'
            src_desktop = src_desktop.lower()

            if not os.path.exists(self._custom_apps_dir):
                os.makedirs(self._custom_apps_dir)
            dst_desktop = os.path.join(self._custom_apps_dir, src_desktop)
            with open(src_desktop, 'r') as f:
                content = f.read()
            icon = os.path.join(self._custom_data_dir, 'src', 'images',
                                'pireal_icon.png')
            content = content.replace('@ INSTALLED_ICON @', icon)
            with open(dst_desktop, 'w') as f:
                f.write(content)

    def finalize_options(self):
        """ Alter the installation path """

        install.finalize_options(self)
        data_dir = os.path.join(self.prefix, "share",
                                self.distribution.get_name())
        apps_dir = os.path.join(self.prefix, "share", "applications")

        if self.root is None:
            build_dir = data_dir
        else:

            build_dir = os.path.join(self.root, data_dir[1:])
            apps_dir = os.path.join(self.root, apps_dir[1:])

        self.install_lib = build_dir
        self._custom_data_dir = data_dir
        self._custom_apps_dir = apps_dir


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

DESCRIPTION = ""

setup(
    name="pireal",
    version="3.0",
    description="",
    author="Gabriel Acosta",
    author_email="acostadariogabriel@gmail.com",
    url="http://centaurialpha.github.io/pireal",
    license='GPLv3+',
    long_description=open('README.rst').read(),
    package_data={
        "src": [
            "gui/qml/*",
            "images/pireal_icon.png",
            "lang/*.qm"]
    },
    packages=[
        "src",
        "src.core",
        "src.gui",
        "src.gui.dialogs",
        "src.gui.query_container"
    ],
    scripts=['pireal'],
    classifiers=classifiers,
    cmdclass={'install': CustomInstall},
)
