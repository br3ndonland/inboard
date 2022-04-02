# Logging

## Configuration variables

See [environment variable reference](environment.md).

## Default logging behavior

-   inboard's logging configuration logic is located in [`logging_conf.py`](https://github.com/br3ndonland/inboard/blob/HEAD/inboard/logging_conf.py). By default, inboard will load the `LOGGING_CONFIG` dictionary in this module. The dictionary was named for consistency with [Uvicorn's logging configuration dictionary](https://github.com/encode/uvicorn/blob/HEAD/uvicorn/config.py).
-   When running Uvicorn alone, logging is configured programmatically from within the [`start.py` start script](https://github.com/br3ndonland/inboard/blob/HEAD/inboard/start.py), by passing the `LOGGING_CONFIG` dictionary to `uvicorn.run()`.
-   When running Gunicorn with the Uvicorn worker, the logging configuration dictionary is specified within the [`gunicorn_conf.py`](https://github.com/br3ndonland/inboard/blob/HEAD/inboard/gunicorn_conf.py) configuration file.

## Filtering log messages

[Filters](https://docs.python.org/3/howto/logging-cookbook.html#using-filters-to-impart-contextual-information) identify log messages to filter out, so that the logger does not log messages containing any of the filters. If any matches are present in a log message, the logger will not output the message.

One of the primary use cases for log message filters is health checks. When applications with APIs are deployed, it is common to perform "health checks" on them. Health checks are usually performed by making HTTP requests to a designated API endpoint. These checks are made at frequent intervals, and so they can fill up the access logs with large numbers of unnecessary log records. To avoid logging health checks, add those endpoints to the `LOG_FILTERS` environment variable.

The `LOG_FILTERS` environment variable can be used to specify filters as a comma-separated string, like `LOG_FILTERS="/health, /heartbeat"`. To then add the filters to a class instance, the `LogFilter.set_filters()` method can produce the set of filters from the environment variable value.

```py
# start a REPL session in a venv in which inboard is installed
.venv ❯ python
>>> import os
>>> import inboard
>>> os.environ["LOG_FILTERS"] = "/health, /heartbeat"
>>> inboard.LogFilter.set_filters()
{'/heartbeat', '/health'}
```

inboard will do this automatically by reading the `LOG_FILTERS` environment variable.

Let's see this in action by using the [VSCode debugger](https://code.visualstudio.com/docs/python/debugging), with the configuration in _inboard/.vscode/launch.json_. We'll have one terminal instance open to see the server logs from Uvicorn, and another one open to make client HTTP requests.

Start the server:

```log
/path/to/inboard
❯ export LOG_FILTERS="/health, /heartbeat"

/path/to/inboard
❯  /usr/bin/env /path/to/inboard/.venv/bin/python \
  /path/to/the/python/vscode/extension/pythonFiles/lib/python/debugpy/launcher \
  61527 -- -m inboard.start
DEBUG:    Logging dict config loaded from inboard.logging_conf.
DEBUG:    Checking for pre-start script.
DEBUG:    Running pre-start script with python /path/to/inboard/inboard/app/prestart.py.
[prestart] Hello World, from prestart.py! Add database migrations and other scripts here.
DEBUG:    Ran pre-start script with python /path/to/inboard/inboard/app/prestart.py.
DEBUG:    App module set to inboard.app.main_fastapi:app.
DEBUG:    Running Uvicorn without Gunicorn.
INFO:     Will watch for changes in these directories: ['/path/to/inboard/inboard']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [69531] using watchgod
INFO:     Started server process [69552]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

Make a request to an endpoint that should be logged, using an HTTP client like [HTTPie](https://httpie.io/) or the [HTTPX CLI](https://www.python-httpx.org/):

```sh
❯ http :8000 -b
{
    "Hello": "World"
}

```

The request will be logged through `uvicorn.access`:

```log
INFO:     127.0.0.1:61575 - "GET / HTTP/1.1" 200
```

Next, make a request to an endpoint that should be filtered out of the logs. The username and password you see here are just test values set in the _launch.json_.

```sh
❯ http :8000/health -a test_user:r4ndom_bUt_memorable -b
{
    "application": "inboard",
    "message": null,
    "status": "active"
}
```

The server does not display a log message.

## Extending the logging config

If inboard is installed from PyPI with `poetry add inboard` or `pip install inboard`, the logging configuration can be easily customized as explained in the [Python logging configuration docs](https://docs.python.org/3/library/logging.config.html).

<!-- prettier-ignore -->
!!!example "Example of a custom logging module"

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

    # don't propagate boto logs
    LOGGING_CONFIG["loggers"]["boto3"] = {"propagate": False}
    LOGGING_CONFIG["loggers"]["botocore"] = {"propagate": False}
    LOGGING_CONFIG["loggers"]["s3transfer"] = {"propagate": False}

    ```

## Overriding the logging config

Want to override inboard's entire logging config? No problem. Set up a separate `LOGGING_CONFIG` dictionary, and pass inboard the path to the module containing the dictionary. Try something like this:

!!!example "Example of a complete custom logging config"

    ```py
    # /app/package/custom_logging.py: set with LOGGING_CONF=package.custom_logging
    from uvicorn.config import LOGGING_CONFIG as UVICORN_LOGGING_CONFIG

    LOGGING_CONFIG = {
        "version": 1,
        # Disable other loggers not specified in the configuration
        "disable_existing_loggers": True,
        "formatters": {
            "gunicorn.access": {
                "class": "logging.Formatter",
                "format": "%(asctime)s [%(process)d] [%(levelname)s] %(message)s",
                "datefmt": "[%Y-%m-%d %H:%M:%S %z]",
            },
            # Format Uvicorn loggers with Uvicorn's config directly
            "uvicorn.access": {
                "()": UVICORN_LOGGING_CONFIG["formatters"]["access"]["()"],
                "format": UVICORN_LOGGING_CONFIG["formatters"]["access"]["fmt"],
            },
            "uvicorn.default": {
                "()": UVICORN_LOGGING_CONFIG["formatters"]["default"]["()"],
                "format": UVICORN_LOGGING_CONFIG["formatters"]["default"]["fmt"],
            },
        },
        "handlers": {
            "default": {
                "class": "logging.StreamHandler",
                "formatter": "uvicorn.default",
                "level": "INFO",
                "stream": "ext://sys.stdout",
            },
            # Add a separate handler for stderr
            "error": {
                "class": "logging.StreamHandler",
                "formatter": "uvicorn.default",
                "stream": "ext://sys.stderr",
            },
            # Add a separate handler just for gunicorn.access
            "gunicorn.access": {
                "class": "logging.StreamHandler",
                "formatter": "gunicorn.access",
                "stream": "ext://sys.stdout",
            },
            # Add a separate handler just for uvicorn.access
            "uvicorn.access": {
                "class": "logging.StreamHandler",
                "formatter": "uvicorn.access",
                "stream": "ext://sys.stdout",
            },
        },
        "loggers": {
            "fastapi": {"propagate": True},
            # Use the gunicorn.access handler, and don't propagate to root
            "gunicorn.access": {"handlers": ["gunicorn.access"], "propagate": False},
            # Use the error handler to output to stderr, and don't propagate to root
            "gunicorn.error": {
                "handlers": ["error"],
                "level": "INFO",
                "propagate": False,
            },
            # Use the uvicorn.access handler, and don't propagate to root
            "uvicorn.access": {
                "handlers": ["uvicorn.access"],
                "level": "INFO",
                "propagate": False,
            },
            # Use the error handler to output to stderr, and don't propagate to root
            "uvicorn.error": {
                "handlers": ["error"],
                "level": "INFO",
                "propagate": False,
            },
        },
        # Use the uvicorn.default formatter for root
        "root": {"handlers": ["default"], "level": "INFO"},
    }

    ```

## Design decisions

### Simplify logging

**Logging is complicated in general, but logging a Uvicorn+Gunicorn+Starlette/FastAPI stack is particularly, and unnecessarily, complicated**. Uvicorn and Gunicorn use different logging configurations, and it can be difficult to unify the log streams.

Gunicorn's API for loading [logging configuration dictionaries](https://docs.python.org/3/library/logging.config.html) has some problems:

-   Gunicorn does not have a clearly-documented interface for running programmatically from within a Python module, like `uvicorn.run()`, so `subprocess.run()` can be used instead. There isn't a clear way to pass logging configuration dictionaries to Gunicorn from the command line, unless you `json.dumps()` a logging configuration dictionary.
-   As of Gunicorn version 20, Gunicorn accepted a command-line argument `--log-config-dict`, but it didn't work, and [the maintainers removed it](https://github.com/benoitc/gunicorn/pull/2476).

Uvicorn's API for loading logging configurations is confusing and poorly documented:

-   The [settings documentation as of version 0.11.8](https://github.com/encode/uvicorn/blob/4597b90ffcfb99e44dae6c7d8cc05e1f368e0624/docs/settings.md) (the version available when this project started) said, "`--log-config <path>` - Logging configuration file," but there was no information given on file format.
-   [encode/uvicorn#665](https://github.com/encode/uvicorn/pull/665) and [Uvicorn 0.12.0](https://github.com/encode/uvicorn/releases/tag/0.12.0) added support for loading JSON and YAML configuration files, but not `.py` files.
-   Uvicorn's own logging configuration is a dictionary, `LOGGING_CONFIG`, in [`config.py`](https://github.com/encode/uvicorn/blob/HEAD/uvicorn/config.py), but there's no information provided on how to supply a custom dictionary config. It is possible to pass a dictionary config to Uvicorn when running programmatically, such as `uvicorn.run(log_config=your_dict_config)`, although so far, this capability is only documented in the [changelog](https://github.com/encode/uvicorn/blob/HEAD/CHANGELOG.md) for version 0.10.0.

**The inboard project eliminates this complication and confusion**. Uvicorn, Gunicorn, and FastAPI log streams are propagated to the root logger, and handled by the custom root logging config.

### Require dict configs

The project initially also had support for the old-format `.conf`/`.ini` files, and YAML files, but this was later dropped, because:

-   **Dict configs are the newer, recommended format**, as explained in the [`logging.config` docs](https://docs.python.org/3/library/logging.config.html):

    > The `fileConfig()` API is older than the `dictConfig()` API and does not provide functionality to cover certain aspects of logging. For example, you cannot configure Filter objects, which provide for filtering of messages beyond simple integer levels, using `fileConfig()`. If you need to have instances of Filter in your logging configuration, you will need to use `dictConfig()`. Note that future enhancements to configuration functionality will be added to `dictConfig()`, so it’s worth considering transitioning to this newer API when it’s convenient to do so.

-   **Dict configs allow programmatic control of logging settings** (see how log level is set in [`logging_conf.py`](https://github.com/br3ndonland/inboard/blob/HEAD/inboard/logging_conf.py) for an example).
-   **Gunicorn and Uvicorn both use dict configs in `.py` files for their own logging configurations**.
-   **Gunicorn prefers dict configs** specified with the [`logconfig_dict` option](https://docs.gunicorn.org/en/latest/settings.html#logconfig-dict).
-   **Uvicorn accepts dict configs when running programmatically**, like `uvicorn.run(log_config=your_dict_config)`.
-   **Relying on Python dictionaries reduces testing burden** (only have to write unit tests for `.py` files)
-   **YAML isn't a Python data structure**. YAML is confusingly used for examples in the documentation, but isn't actually a recommended format. There's no built-in YAML data structure in Python, so the YAML must be parsed by PyYAML and converted into a dictionary, then passed to `logging.config.dictConfig()`. **Why not just make the logging config a dictionary in the first place?**

## Further info

For more details on how logging was implemented initially, see [br3ndonland/inboard#3](https://github.com/br3ndonland/inboard/pull/3).

For more information on Python logging configuration, see the [Python `logging` how-to](https://docs.python.org/3/howto/logging.html), [Python `logging` cookbook](https://docs.python.org/3/howto/logging-cookbook.html), [Python `logging` module docs](https://docs.python.org/3/library/logging.html), and [Python `logging.config` module docs](https://docs.python.org/3/library/logging.config.html). Also consider [Loguru](https://loguru.readthedocs.io/en/stable/index.html), an alternative logging module with many improvements over the standard library `logging` module.
