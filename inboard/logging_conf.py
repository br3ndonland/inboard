import os
from typing import Dict, Union

LOG_LEVEL = str(os.getenv("LOG_LEVEL", "info")).upper()
PROPAGATE_ACCESS_LOGS = bool(os.getenv("PROPAGATE_ACCESS_LOGS", "true"))
LOGGING_CONFIG: Dict[str, Union[Dict, bool, int, str]] = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "inboard": {
            "format": "%(asctime)s [%(process)d] [%(name)s] [%(levelname)s] %(message)s",  # noqa: E501
            "datefmt": "[%Y-%m-%d %H:%M:%S %z]",
            "class": "logging.Formatter",
        }
    },
    "handlers": {
        "inboard": {
            "class": "logging.StreamHandler",
            "formatter": "inboard",
            "level": LOG_LEVEL,
            "stream": "ext://sys.stdout",
        }
    },
    "root": {"handlers": ["inboard"], "level": LOG_LEVEL},
    "loggers": {
        "fastapi": {"propagate": True},
        "gunicorn": {"propagate": True},
        "gunicorn.access": {"propagate": PROPAGATE_ACCESS_LOGS},
        "gunicorn.error": {"propagate": True},
        "uvicorn": {"propagate": True},
        "uvicorn.access": {"propagate": PROPAGATE_ACCESS_LOGS},
        "uvicorn.asgi": {"propagate": True},
        "uvicorn.error": {"propagate": True},
    },
}
