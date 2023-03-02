"""inboard

Docker images and utilities to power your Python APIs and help you ship faster.

https://github.com/br3ndonland/inboard
"""
# FastAPI and Starlette are optional, and will raise ImportErrors if not installed.
try:
    from .app.utilities_fastapi import basic_auth as fastapi_basic_auth
except ImportError:  # pragma: no cover
    pass
try:
    from .app.utilities_starlette import BasicAuth as StarletteBasicAuth
except ImportError:  # pragma: no cover
    pass
from .logging_conf import LOGGING_CONFIG, LogFilter, configure_logging

__all__ = (
    "LOGGING_CONFIG",
    "LogFilter",
    "StarletteBasicAuth",
    "configure_logging",
    "fastapi_basic_auth",
)

__version__ = "0.40.0"
