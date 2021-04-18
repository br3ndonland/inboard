"""inboard

Docker images and utilities to power your Python APIs and help you ship faster.

https://github.com/br3ndonland/inboard
"""
try:
    # FastAPI and Starlette are optional dependencies
    from .app.utilities_fastapi import basic_auth as fastapi_basic_auth
    from .app.utilities_starlette import BasicAuth as StarletteBasicAuth
except ImportError:  # pragma: no cover
    # ImportError exceptions will be raised if optional dependencies are not installed
    pass
from .logging_conf import LOGGING_CONFIG, configure_logging

__all__ = (
    "LOGGING_CONFIG",
    "StarletteBasicAuth",
    "configure_logging",
    "fastapi_basic_auth",
)
