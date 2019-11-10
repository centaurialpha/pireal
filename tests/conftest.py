import pytest

GROUPS = [
    "gui",
    "integration"
]


def pytest_configure(config):
    for marker in GROUPS:
        config.addinivalue_line("markers", marker)
