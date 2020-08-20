import os
import sys
from typing import Dict, Union

LOG_COLORS = bool(os.getenv("LOG_COLORS", sys.stdout.isatty()))
LOG_FORMAT = str(os.getenv("LOG_FORMAT", "simple"))
LOG_LEVEL = str(os.getenv("LOG_LEVEL", "info")).upper()
LOGGING_CONFIG: Dict[str, Union[Dict, bool, int, str]] = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "class": "logging.Formatter",
            "format": "%(levelname)-10s %(message)s",
        },
        "verbose": {
            "class": "logging.Formatter",
            "format": "%(asctime)-30s %(process)-10d %(name)-15s %(module)-15s %(levelname)-10s %(message)s",  # noqa: E501
            "datefmt": "%Y-%m-%d %H:%M:%S %z",
        },
        "gunicorn": {
            "class": "logging.Formatter",
            "format": "%(asctime)s [%(process)d] [%(levelname)s] %(message)s",
            "datefmt": "[%Y-%m-%d %H:%M:%S %z]",
        },
        "uvicorn": {
            "()": "uvicorn.logging.DefaultFormatter",
            "format": "%(levelprefix)s %(message)s",
            "use_colors": LOG_COLORS,
        },
    },
    "handlers": {
        "default": {
            "class": "logging.StreamHandler",
            "formatter": LOG_FORMAT,
            "level": LOG_LEVEL,
            "stream": "ext://sys.stdout",
        }
    },
    "root": {"handlers": ["default"], "level": LOG_LEVEL},
    "loggers": {
        "fastapi": {"propagate": True},
        "gunicorn.access": {"handlers": ["default"], "propagate": True},
        "gunicorn.error": {"propagate": True},
        "uvicorn": {"propagate": True},
        "uvicorn.access": {"propagate": True},
        "uvicorn.asgi": {"propagate": True},
        "uvicorn.error": {"propagate": True},
    },
}
