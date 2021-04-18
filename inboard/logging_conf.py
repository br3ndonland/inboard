import importlib.util
import logging
import logging.config
import os
import sys
from pathlib import Path
from typing import Optional


def find_and_load_logging_conf(logging_conf: str) -> dict:
    """Find and load a logging configuration module or file."""
    logging_conf_path = Path(logging_conf)
    spec = (
        importlib.util.spec_from_file_location("confspec", logging_conf_path)
        if logging_conf_path.is_file() and logging_conf_path.suffix == ".py"
        else importlib.util.find_spec(logging_conf)
    )
    if not spec:
        raise ImportError(f"Unable to import {logging_conf_path}")
    logging_conf_module = importlib.util.module_from_spec(spec)
    exec_module = getattr(spec.loader, "exec_module")
    exec_module(logging_conf_module)
    if not hasattr(logging_conf_module, "LOGGING_CONFIG"):
        raise AttributeError(f"No LOGGING_CONFIG in {logging_conf_module.__name__}")
    logging_conf_dict = getattr(logging_conf_module, "LOGGING_CONFIG")
    if not isinstance(logging_conf_dict, dict):
        raise TypeError("LOGGING_CONFIG is not a dictionary instance")
    return logging_conf_dict


def configure_logging(
    logger: logging.Logger = logging.getLogger(),
    logging_conf: Optional[str] = os.getenv("LOGGING_CONF"),
) -> dict:
    """Configure Python logging given the name of a logging module or file."""
    try:
        if not logging_conf:
            logging_conf_path = __name__
            logging_conf_dict = LOGGING_CONFIG
        else:
            logging_conf_path = logging_conf
            logging_conf_dict = find_and_load_logging_conf(logging_conf_path)
        logging.config.dictConfig(logging_conf_dict)
        logger.debug(f"Logging dict config loaded from {logging_conf_path}.")
        return logging_conf_dict
    except Exception as e:
        logger.error(f"Error when setting logging module: {e.__class__.__name__} {e}.")
        raise


LOG_COLORS = (
    True
    if (value := os.getenv("LOG_COLORS")) and value.lower() == "true"
    else False
    if value and value.lower() == "false"
    else sys.stdout.isatty()
)
LOG_FORMAT = str(os.getenv("LOG_FORMAT", "simple"))
LOG_LEVEL = str(os.getenv("LOG_LEVEL", "info")).upper()
LOGGING_CONFIG: dict = {
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
