# Logging

## Configuration variables

See [environment variable reference](environment.md).

## Extending the logging config

If inboard is installed from PyPI with `poetry add inboard` or `pip install inboard`, the logging configuration can be easily extended or overridden. For example:

```py
# /app/package/custom_logging.py: set with LOGGING_CONF=package.custom_logging
import logging
import os

from inboard import LOGGING_CONFIG

# add a custom logging format: set with LOG_FORMAT=mycustomformat
LOGGING_CONFIG["formatters"]["mycustomformat"] = {
    "format": "[%(name)s] %(levelname)s %(message)s"
}


class MyFormatterClass(logging.Formatter):
    """Define a custom logging format class."""

    def __init__(self) -> None:
        super().__init__(fmt="[%(name)s] %(levelname)s %(message)s")


# use a custom logging format class: set with LOG_FORMAT=mycustomclass
LOGGING_CONFIG["formatters"]["mycustomclass"] = {
    "()": "package.custom_logging.MyFormatterClass",
}

# only show access logs when running Uvicorn with LOG_LEVEL=debug
LOGGING_CONFIG["loggers"]["gunicorn.access"] = {"propagate": False}
LOGGING_CONFIG["loggers"]["uvicorn.access"] = {
    "propagate": str(os.getenv("LOG_LEVEL")) == "debug"
}

# don't propagate boto3 logs
LOGGING_CONFIG["loggers"]["boto3"] = {"propagate": False}
LOGGING_CONFIG["loggers"]["botocore"] = {"propagate": False}
LOGGING_CONFIG["loggers"]["s3transfer"] = {"propagate": False}

```

## Design decisions

See [br3ndonland/inboard#3](https://github.com/br3ndonland/inboard/pull/3) for more details on logging setup.

## Further info

For more information on Python logging configuration, see the [Python `logging` how-to](https://docs.python.org/3/howto/logging.html), [Python `logging` cookbook](https://docs.python.org/3/howto/logging-cookbook.html), [Python `logging` module docs](https://docs.python.org/3/library/logging.html), and [Python `logging.config` module docs](https://docs.python.org/3/library/logging.config.html). Also consider [Loguru](https://loguru.readthedocs.io/en/stable/index.html), an alternative logging module with many improvements over the standard library `logging` module.
