#!/bin/sh

# Create dist
make dist

# Make deb
debuild -b -uc -us

# Clean
rm -rf dist
rm -rf debian/debhelper-build-stamp
rm -rf debian/files
rm -rf debian/pireal.substvars
rm -rf debian/pireal/
