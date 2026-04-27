# Copyright 2026 - Gabriel Acosta <acostadariogabriel@gmail.com>
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

import shutil
import stat
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__name__).parent.parent.parent
SRC_MAIN = ROOT / "src" / "pireal" / "main.py"
ICON_SRC = ROOT / "src" / "pireal" / "resources" / "images" / "pireal_icon.png"
DIST_DIR = ROOT / "dist"
APPDIR = DIST_DIR / "Pireal.AppDir"
APPIMAGETOOL_BIN = Path(__file__).parent / "appimagetool"

APPIMAGETOOL_URL = "https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"

DESKTOP_ENTRY = """\
[Desktop Entry]
Version=4.0.0
Type=Application
Name=Pireal
GenericName=Relational Algebra Interpreter
Comment=Educational tool for working with Relational Algebra
Exec=pireal
Icon=pireal
Terminal=false
Categories=Education;
"""

APPRUN = """\
#!/bin/sh
exec "$APPDIR/pireal" "$@"
"""


def log(msg: str) -> None:
    print(f"[build] {msg}", flush=True)


def run(cmd: list[str | Path], **kwargs) -> None:
    subprocess.run(cmd, check=True, **kwargs)


def get_version() -> str:
    from importlib.metadata import version

    return version("pireal")


def make_executable(path: Path) -> None:
    path.chmod(path.stat().st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)


def ensure_appimagetool() -> Path:
    if APPIMAGETOOL_BIN.exists():
        return APPIMAGETOOL_BIN
    log("Downloading appimagetool...")
    urllib.request.urlretrieve(APPIMAGETOOL_URL, APPIMAGETOOL_BIN)
    make_executable(APPIMAGETOOL_BIN)
    log("appimagetool ready")
    return APPIMAGETOOL_BIN


def build_nuitka(version: str) -> Path:
    nuitka_dist = DIST_DIR / "pirea.dist"
    if nuitka_dist.exists():
        log("cleaning previous nuitka output...")
        shutil.rmtree(nuitka_dist)

    log(f"compiling with nuitka (v{version})...")
    run(
        [
            sys.executable,
            "-m",
            "nuitka",
            "--standalone",
            "--enable-plugin=pyqt6",
            "--include-package-data=pireal",
            "--output-filename=pireal",
            f"--output-dir={DIST_DIR}",
            "--product-name=Pireal",
            f"--product-version={version}",
            "--file-description=Relation Algebra Interpreter",
            "--copyright=Gabriel Acosta",
            f"--linux-icon={ICON_SRC}",
            str(SRC_MAIN),
        ],
        cwd=ROOT,
    )
    return nuitka_dist


def main() -> None:
    version = get_version()
    log(f"version: {version}")

    nuitka_dist = build_nuitka(version)
    print(nuitka_dist)


if __name__ == "__main__":
    main()
