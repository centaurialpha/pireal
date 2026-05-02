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

import argparse
import os
import shutil
import stat
import subprocess
import sys
import sysconfig
import urllib.request
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
SRC_MAIN = ROOT / "src" / "pireal" / "main.py"
ICON_SRC = ROOT / "src" / "pireal" / "resources" / "images" / "pireal_icon.png"
DIST_DIR = ROOT / "dist"
APPDIR = DIST_DIR / "Pireal.AppDir"
APPIMAGETOOL_BIN = Path(__file__).parent / "appimagetool"

APPIMAGETOOL_URL = "https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"

DESKTOP_ENTRY = """\
[Desktop Entry]
Version=1.0
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
SELF=$(readlink -f "$0")
HERE=${SELF%/*}
export LD_LIBRARY_PATH="$HERE/PyQt6/Qt6/lib:$HERE:${LD_LIBRARY_PATH}"
export QT_PLUGIN_PATH="$HERE/PyQt6/Qt6/plugins"
export QT_QPA_PLATFORM_PLUGIN_PATH="$HERE/PyQt6/Qt6/plugins/platforms"
exec "$HERE/pireal.bin" "$@"
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
    nuitka_dist = DIST_DIR / "main.dist"
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
            f"--include-data-dir={ROOT / 'src' / 'pireal' / 'resources'}=pireal/resources",
            "--output-filename=pireal.bin",
            f"--output-dir={DIST_DIR}",
            "--product-name=Pireal",
            f"--product-version={version}",
            "--file-description=Relation Algebra Interpreter",
            "--copyright=Gabriel Acosta",
            f"--linux-icon={ICON_SRC}",
            "--include-qt-plugins=all",
            str(SRC_MAIN),
        ],
        cwd=ROOT,
    )
    return nuitka_dist


def build_appdir(nuitka_dist: Path) -> Path:
    if APPDIR.exists():
        log("cleaning previous AppDir...")
        shutil.rmtree(APPDIR)

    log("assembling AppDir...")

    shutil.copytree(nuitka_dist, APPDIR, dirs_exist_ok=True)

    qt_libs_src = Path(sysconfig.get_path("purelib")) / "PyQt6" / "Qt6" / "lib"
    qt_libs_dst = APPDIR / "PyQt6" / "Qt6" / "lib"
    qt_libs_dst.mkdir(parents=True, exist_ok=True)
    for lib in qt_libs_src.glob("libQt6*.so*"):
        dst = qt_libs_dst / lib.name
        if not dst.exists():
            shutil.copy2(lib, dst)

    apprun = APPDIR / "AppRun"
    apprun.write_text(APPRUN)
    make_executable(apprun)

    shutil.copy(ICON_SRC, APPDIR / "pireal.png")

    (APPDIR / "pireal.desktop").write_text(DESKTOP_ENTRY)

    return APPDIR


def build_appimage(appdir: Path, version: str) -> Path:
    appimagetool = ensure_appimagetool()
    output = DIST_DIR / f"Pireal-{version}-x86_64.AppImage"

    if output.exists():
        output.unlink()

    log("building AppImage...")
    env = os.environ.copy()
    env["ARCH"] = "x86_64"
    run([str(appimagetool), str(appdir), str(output)], env=env)

    make_executable(output)
    log(f"done: {output.relative_to(ROOT)}")
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-nuitka", action="store_true")
    args = parser.parse_args()

    version = get_version()
    log(f"version: {version}")

    nuitka_dist = DIST_DIR / "main.dist"
    if not args.skip_nuitka:
        nuitka_dist = build_nuitka(version)

    appdir = build_appdir(nuitka_dist)
    build_appimage(appdir, version)


if __name__ == "__main__":
    main()
