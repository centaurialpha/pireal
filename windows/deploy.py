#!/usr/bin/env python3

import os
import sys
import shutil
from subprocess import call

PYINSTALLER_CMD = [
    'pyinstaller',
    'pireal.spec',
    '--log-level',
    'CRITICAL',
    '--noconfirm'
]
QT_INSTALLER_CMD = [
    'C:\\Qt\\QtIFW-4.0.1\\bin\\binarycreator.exe',
    '-c',
    'deploy/config/config.xml',
    '-p',
    'deploy/packages',
    '-f',
    'PirealInstaller',
]

EXCLUDE_FILES = (
    'Qt5Qml.dll',
    'Qt5QmlModels.dll',
    'Qt5Quick.dll',
    'opengl32sw.dll'
)


def main():
    try:
        print('[deploy] running PyInstaller...')
        exit_code = call(PYINSTALLER_CMD)
        if exit_code == 0:
            print('[deploy] build OK')
        else:
            sys.exit(1)

        dist_path = os.path.join('dist', 'pireal')
        dist_files = os.listdir(dist_path)
        final_path_files = os.path.join(
            'deploy', 'packages', 'com.pireal.installer', 'data', 'win64')
        os.makedirs(final_path_files, exist_ok=True)
        for f in dist_files:
            if f in EXCLUDE_FILES:
                continue
            src = os.path.join(dist_path, f)
            dst = os.path.join(final_path_files, os.path.basename(f))
            print(f'[deploy] moving {src} -> {dst}')
            shutil.move(src, dst)
        print('[deploy] OK')

        print('[deploy] creating installer...')
        call(QT_INSTALLER_CMD)
        print('[deploy] installer OK')
    finally:
        print('[cleanup] cleaning up..')
        shutil.rmtree('dist')
        shutil.rmtree('build')
        shutil.rmtree('deploy/packages/com.pireal.installer/data')
        print('[cleanup] OK')


if __name__ == '__main__':
    main()
