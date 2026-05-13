#!/usr/bin/env python3

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

from __future__ import annotations

import argparse
import os
import platform
import re
import shutil
import stat
import subprocess
import sys
import sysconfig
import urllib.request
from importlib.metadata import version
from pathlib import Path
from string import Template

ROOT = Path(__file__).parent.parent
SRC_MAIN = ROOT / "src" / "pireal" / "main.py"
RESOURCES = ROOT / "src" / "pireal" / "resources"
ICON_PNG = RESOURCES / "images" / "pireal_icon.png"
ICON_ICO = RESOURCES / "images" / "pireal_icon.ico"
DIST_DIR = ROOT / "dist"
NUITKA_DIST = DIST_DIR / "main.dist"

# Linux
APPDIR = DIST_DIR / "Pireal.AppDir"
APPIMAGETOOL_BIN = Path(__file__).parent / "linux" / "appimagetool"
APPIMAGETOOL_URL = "https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"

# Windows
INNO_SETUP = Path("C:/Program Files (x86)/Inno Setup 6/ISCC.exe")
ISS_TEMPLATE = Path(__file__).parent / "windows" / "installer.iss.in"
ISS_FILE = Path(__file__).parent / "windows" / "installer.iss"

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


def run(cmd: list[str], **kwargs) -> None:
    subprocess.run(cmd, check=True, **kwargs)


def get_version() -> str:

    return version("pireal")


def nuitka_version(version: str) -> str:
    """
    Extract Nuitka-compatible version (Windows PE format: up to 4 integers).
    e.g. "4.0.0.dev1+gabcdef" -> "4.0.0"
    """
    numbers = re.findall(r"\d+", version.split("+")[0])[:4]
    return ".".join(numbers) if numbers else "0.0.0.0"


def make_executable(path: Path) -> None:
    path.chmod(path.stat().st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)


def build_nuitka(version: str) -> Path:
    if NUITKA_DIST.exists():
        log("cleaning previous nuitka output...")
        shutil.rmtree(NUITKA_DIST)

    log(f"compiling with nuitka (v{version})...")

    cmd = [
        sys.executable,
        "-m",
        "nuitka",
        "--standalone",
        "--enable-plugin=pyqt6",
        f"--include-data-dir={RESOURCES}=pireal/resources",
        f"--output-dir={DIST_DIR}",
        "--product-name=Pireal",
        "--file-description=Relational Algebra Interpreter",
        "--copyright=Gabriel Acosta",
    ]

    match platform.system():
        case "Linux":
            cmd += [
                "--output-filename=pireal.bin",
                f"--linux-icon={ICON_PNG}",
            ]
        case "Windows":
            cmd += [
                "--output-filename=pireal.exe",
                f"--product-version={nuitka_version(version)}",
                f"--windows-icon-from-ico={ICON_ICO}",
                "--windows-console-mode=disable",
            ]

    cmd.append(str(SRC_MAIN))
    run(cmd, cwd=ROOT)
    return NUITKA_DIST


def ensure_appimagetool() -> Path:
    if APPIMAGETOOL_BIN.exists():
        return APPIMAGETOOL_BIN
    log("downloading appimagetool...")
    urllib.request.urlretrieve(APPIMAGETOOL_URL, APPIMAGETOOL_BIN)
    make_executable(APPIMAGETOOL_BIN)
    log("appimagetool ready")
    return APPIMAGETOOL_BIN


def build_appdir(nuitka_dist: Path) -> Path:
    if APPDIR.exists():
        log("cleaning previous AppDir...")
        shutil.rmtree(APPDIR)

    log("assembling AppDir...")
    shutil.copytree(nuitka_dist, APPDIR, dirs_exist_ok=True)

    # Bundle Qt libs to isolate from system Qt
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

    shutil.copy(ICON_PNG, APPDIR / "pireal.png")
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


def build_iss(version: str, nuitka_dist: Path) -> Path:
    iss = Template(ISS_TEMPLATE.read_text(encoding="utf-8")).substitute(
        version=version,
        source_dir=nuitka_dist.resolve(),
        output_dir=DIST_DIR.resolve(),
        icon=ICON_ICO.resolve(),
    )
    ISS_FILE.write_text(iss, encoding="utf-8")
    log(f"generated {ISS_FILE.relative_to(ROOT)}")
    return ISS_FILE


def build_installer(iss_file: Path) -> None:
    if not INNO_SETUP.exists():
        raise FileNotFoundError(f"Inno Setup not found at {INNO_SETUP}\nDownload from https://jrsoftware.org/isdl.php")
    log("building installer...")
    run([str(INNO_SETUP), str(iss_file)])


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Pireal release artifact.")
    parser.add_argument("--skip-nuitka", action="store_true", help="Reuse existing dist/main.dist")
    args = parser.parse_args()

    match platform.system():
        case "Linux" | "Windows":
            pass
        case other:
            print(f"Unsupported platform: {other}")
            sys.exit(1)

    version = get_version()
    log(f"version: {version}, platform: {platform.system()}")

    if not args.skip_nuitka:
        build_nuitka(version)

    match platform.system():
        case "Linux":
            appdir = build_appdir(NUITKA_DIST)
            build_appimage(appdir, version)
        case "Windows":
            iss_file = build_iss(version, NUITKA_DIST)
            build_installer(iss_file)
            log(f"done: dist/Pireal-{version}-windows-x86_64-setup.exe")


if __name__ == "__main__":
    main()
