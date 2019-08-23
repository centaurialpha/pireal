import pytest

GROUPS = [
    "gui"
]


def pytest_configure(config):
    for marker in GROUPS:
        config.addinivalue_line("markers", marker)
