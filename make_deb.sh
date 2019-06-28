#!/bin/sh

debuild -b -uc -us

python setup.py sdist

mv dist/* ../

rm -rf .pybuild
rm -rf debian/debhelper-build-stamp
rm -rf debian/files
rm -rf debian/pireal
rm -rf debian/pireal.postinst.debhelper
rm -rf debian/pireal.prerm.debhelper
rm -rf debian/pireal.substvars
rm -rf pireal.egg-info
rm -rf build
rm -rf dist
