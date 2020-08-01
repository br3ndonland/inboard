"""
inboard
---
"""
from importlib.metadata import version


def package_version() -> str:
    """Calculate version number based on pyproject.toml"""
    return version(__package__)


__version__ = package_version()
