from __future__ import annotations

import importlib.util
import logging
import logging.config
import os
import sys
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from inboard.types import DictConfig


def find_and_load_logging_conf(logging_conf: str) -> DictConfig:
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
    logging_conf_dict: DictConfig = getattr(logging_conf_module, "LOGGING_CONFIG")
    if not isinstance(logging_conf_dict, dict):
        raise TypeError("LOGGING_CONFIG is not a dictionary instance")
    return logging_conf_dict


def configure_logging(
    logger: logging.Logger = logging.getLogger(),
    logging_conf: str | None = os.getenv("LOGGING_CONF"),
) -> DictConfig:
    """Configure Python logging given the name of a logging module or file."""
    try:
        if not logging_conf:
            logging_conf_path = __name__
            logging_conf_dict: DictConfig = LOGGING_CONFIG
        else:
            logging_conf_path = logging_conf
            logging_conf_dict = find_and_load_logging_conf(logging_conf_path)
        logging.config.dictConfig(logging_conf_dict)
        logger.debug(f"Logging dict config loaded from {logging_conf_path}.")
        return logging_conf_dict
    except Exception as e:
        logger.error(f"Error when setting logging module: {e.__class__.__name__} {e}.")
        raise


class LogFilter(logging.Filter):
    """Subclass of `logging.Filter` used to filter log messages.
    ---

    Filters identify log messages to filter out, so that the logger does not log
    messages containing any of the filters. If any matches are present in a log
    message, the logger will not output the message.

    The environment variable `LOG_FILTERS` can be used to specify filters as a
    comma-separated string, like `LOG_FILTERS="/health, /heartbeat"`. To then
    add the filters to a class instance, the `LogFilter.set_filters()`
    method can produce the set of filters from the environment variable value.
    """

    __slots__ = "name", "nlen", "filters"

    def __init__(
        self,
        name: str = "",
        filters: set[str] | None = None,
    ) -> None:
        """Initialize a filter."""
        self.name = name
        self.nlen = len(name)
        self.filters = filters

    def filter(self, record: logging.LogRecord) -> bool:
        """Determine if the specified record is to be logged.

        Returns True if the record should be logged, or False otherwise.
        """
        if self.filters is None:
            return True
        message = record.getMessage()
        return all(match not in message for match in self.filters)

    @staticmethod
    def set_filters(input_filters: str | None = None) -> set[str] | None:
        """Set log message filters.

        Filters identify log messages to filter out, so that the logger does not
        log messages containing any of the filters. The argument to this method
        should be supplied as a comma-separated string. The string will be split
        on commas and converted to a set of strings.

        This method is provided as a `staticmethod`, instead of as part of `__init__`,
        so that it only runs once when setting the `LOG_FILTERS` module-level constant.
        In contrast, the `__init__` method runs each time a logger is instantiated.
        """
        return (
            {log_filter.strip() for log_filter in str(log_filters).split(sep=",")}
            if (log_filters := input_filters or os.getenv("LOG_FILTERS"))
            else None
        )


LOG_COLORS = (
    True
    if (value := os.getenv("LOG_COLORS")) and value.lower() == "true"
    else False
    if value and value.lower() == "false"
    else sys.stdout.isatty()
)
LOG_FILTERS = LogFilter.set_filters()
LOG_FORMAT = str(os.getenv("LOG_FORMAT", "simple"))
LOG_LEVEL = str(os.getenv("LOG_LEVEL", "info")).upper()
LOGGING_CONFIG: DictConfig = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "filter_log_message": {"()": LogFilter, "filters": LOG_FILTERS},
    },
    "formatters": {
        "simple": {
            "class": "logging.Formatter",
            "format": "%(levelname)-10s %(message)s",
        },
        "verbose": {
            "class": "logging.Formatter",
            "format": (
                "%(asctime)-30s %(process)-10d %(name)-15s "
                "%(module)-15s %(levelname)-10s %(message)s"
            ),
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
            "filters": ["filter_log_message"],
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
