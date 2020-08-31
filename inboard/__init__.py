"""
inboard
---
"""
from importlib.metadata import version


def package_version() -> str:
    """Calculate version number based on pyproject.toml"""
    try:
        return version(__package__)
    except Exception:
        return "Package not found."


__version__ = package_version()
