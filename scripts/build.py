#!/usr/bin/env python3

"""Build script for Pireal."""

import subprocess
import sys
from pathlib import Path

from pireal import __version__

ROOT = Path(__file__).parent.parent

cmd = [
    sys.executable,
    "-m",
    "nuitka",
    "--standalone",
    "--enable-plugin=pyqt6",
    "--include-package-data=pireal",
    "--output-filename=pireal",
    "--output-dir=dist",
    "--windows-icon-from-ico=src/pireal/resources/images/pireal.ico",
    "--windows-console-mode=disable",
    "--product-name=Pireal",
    f"--product-version={__version__}",
    "--file-description=Relational Algebra Interpreter",
    "--copyright=Gabriel Acosta",
    "src/pireal/main.py",
]

subprocess.run(cmd, check=True)
