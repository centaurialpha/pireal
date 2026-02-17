# Copyright 2015-2022 Gabriel Acosta <acostadariogabriel@gmail.com>
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

"""
Pireal - Interactive Relational Algebra Learning Tool

Entry point for the application.
"""

import logging
import logging.handlers
import platform
import sys
from pathlib import Path

from PyQt6.QtCore import QT_VERSION_STR, QDir

from pireal import __version__
from pireal.app import Application
from pireal.core import cliparser
from pireal.dirs import LOGS_DIR, create_app_dirs

logger = logging.getLogger()

ROOT_DIR = Path(__file__).parent
RESOURCES_DIR = ROOT_DIR / "resources"
IMAGES_DIR = RESOURCES_DIR / "images"
LANGUAGES_DIR = RESOURCES_DIR / "lang"


if ROOT_DIR not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


def setup_logger(level: int = logging.INFO) -> None:
    """
    Configure application logging.

    Args:
        level: Logging level (default: INFO)
    """
    console_fmt = "[%(levelname)-6s]: %(name)s:%(funcName)s - %(message)s"
    file_fmt = "[%(asctime)s] [%(levelname)-6s] [%(process)d]: %(name)s:%(funcName)s:%(lineno)d - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(console_fmt))

    log_file = LOGS_DIR / "pireal.log"

    file_handler = logging.handlers.RotatingFileHandler(
        log_file, maxBytes=10 * 1024 * 1024, backupCount=5, encoding="utf-8"
    )
    if log_file.exists() and log_file.stat().st_size > 0:
        file_handler.doRollover()  # Force rotation on startup
    file_handler.setFormatter(logging.Formatter(file_fmt, datefmt=date_format))

    logging.basicConfig(level=level, handlers=[console_handler, file_handler])

    logger.info("Logging initialized at level %s", logging.getLevelName(level))
    logger.info("Log file: %s", log_file)


def run():
    QDir.addSearchPath("icons", str(IMAGES_DIR))
    QDir.addSearchPath("languages", str(LANGUAGES_DIR))

    # Parse CLI
    args = cliparser.get_cli().parse_args()
    if args.version:
        print(__version__)
        sys.exit(0)

    # Creo los dirs antes de leer logs. see #84
    create_app_dirs()

    setup_logger(level=args.log_level)

    logger = logging.getLogger(__name__)
    if platform.system() == "Linux":
        system, os_name = platform.uname()[:2]
    else:
        system = platform.uname()[0]
        os_name = platform.uname()[2]

    python_version = platform.python_version()

    logger.info("Running Pireal %s...", __version__)
    logger.info("Python %s on %s-%s, Qt %s", python_version, os_name, system, QT_VERSION_STR)

    app = Application(args)
    app.run()
