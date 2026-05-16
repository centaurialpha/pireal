"""
MkDocs hook: reads version from the installed package or DOCS_VERSION env var
"""

from __future__ import annotations

import importlib.metadata
import os


def on_config(config):
    try:
        version = importlib.metadata.version("pireal")
    except importlib.metadata.PackageNotFoundError:
        version = os.environ.get("DOCS_VERSION", "dev")
    config.extra["version"] = version
    return config
