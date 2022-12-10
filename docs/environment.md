# Environment variables

## Usage

To [set environment variables when starting a Docker container](https://docs.docker.com/engine/reference/commandline/run/):

```sh
docker run -d -p 80:80 \
  -e APP_MODULE="package.custom.module:api" \
  -e WORKERS_PER_CORE="2" \
  myimage
```

To [set environment variables within a _Dockerfile_](https://docs.docker.com/engine/reference/builder/#env):

```dockerfile
FROM ghcr.io/br3ndonland/inboard:fastapi
ENV APP_MODULE="package.custom.module:api" WORKERS_PER_CORE="2"
```

## General

`APP_MODULE`

-   Python module with app instance.
-   Default: The appropriate app module from inboard.
-   Custom: For a module at `/app/package/custom/module.py` and app instance object `api`, `APP_MODULE="package.custom.module:api"`

    !!!example "Example of a custom FastAPI app module"

        ```py
        # /app/package/custom/module.py
        from fastapi import FastAPI

        api = FastAPI()

        @api.get("/")
        def read_root():
            return {"message": "Hello World!"}
        ```

    !!! note

        The base Docker image sets the environment variable `PYTHONPATH=/app`, so the module name will be relative to `/app` unless you supply a custom [`PYTHONPATH`](https://docs.python.org/3/using/cmdline.html#envvar-PYTHONPATH).

`PRE_START_PATH`

-   Path to a pre-start script.
    -   inboard optionally runs a pre-start script before starting the server. The path to a pre-start script can be specified with the environment variable `PRE_START_PATH`. If the environment variable is set to a nonzero value, inboard will run the script at the provided path, using the [`subprocess`](https://docs.python.org/3/library/subprocess.html) standard library package.
    -   If the pre-start script exits with an error, inboard will not start the server.
-   Default: `"/app/inboard/prestart.py"` (provided with inboard)
-   Custom:

    -   `PRE_START_PATH="/app/package/custom_script.sh"`
    -   `PRE_START_PATH= ` (set to an empty value) to disable

    !!! tip

        Add a file `prestart.py` or `prestart.sh` to the application directory, and copy the directory into the Docker image as described (for a project with the Python application in `repo/package`, `COPY package /app/package`). The container will automatically detect and run the prestart script before starting the web server.

[`PYTHONPATH`](https://docs.python.org/3/using/cmdline.html#envvar-PYTHONPATH)

-   Python's search path for module files.
-   Default: `PYTHONPATH="/app"`
-   Custom: `PYTHONPATH="/app/custom"`

## Gunicorn

### Configuration file

`GUNICORN_CONF`

-   Path to a [Gunicorn configuration file](https://docs.gunicorn.org/en/latest/settings.html#config-file). Gunicorn accepts either file paths or module paths.
-   Default:
    -   `"python:inboard.gunicorn_conf"` (provided with inboard)
-   Custom:
    -   `GUNICORN_CONF="/app/package/custom_gunicorn_conf.py"` (file path)
    -   `GUNICORN_CONF="python:package.custom_gunicorn_conf"` (module paths accepted with the `python:` prefix)

### Process management

!!! info

    As described in the [Uvicorn docs](https://www.uvicorn.org), "Uvicorn includes a Gunicorn worker class allowing you to run ASGI applications, with all of Uvicorn's performance benefits, while also giving you Gunicorn's fully-featured process management."

`PROCESS_MANAGER`

-   Manager for Uvicorn worker processes.
-   Default: `"gunicorn"` (run Uvicorn with Gunicorn as the process manager)
-   Custom: `"uvicorn"` (run Uvicorn alone for local development)

[`WORKER_CLASS`](https://docs.gunicorn.org/en/latest/settings.html#worker-processes)

-   Uvicorn worker class for Gunicorn to use.
-   Default: `uvicorn.workers.UvicornWorker`
-   Custom: For the [alternate Uvicorn worker](https://www.uvicorn.org/deployment/), `WORKER_CLASS="uvicorn.workers.UvicornH11Worker"` _(the H11 worker is provided for [PyPy](https://www.pypy.org/) and hasn't been tested)_

### Worker process calculation

!!! info

    The number of [Gunicorn worker processes](https://docs.gunicorn.org/en/latest/settings.html#worker-processes) to run is determined based on the `MAX_WORKERS`, `WEB_CONCURRENCY`, and `WORKERS_PER_CORE` environment variables, with a default of 1 worker per CPU core and a default minimum of 2. This is the "performance auto-tuning" feature described in [tiangolo/uvicorn-gunicorn-docker](https://github.com/tiangolo/uvicorn-gunicorn-docker).

`MAX_WORKERS`

-   Maximum number of workers, independent of number of CPU cores.
-   Default: not set (unlimited)
-   Custom: `MAX_WORKERS="24"`

`WEB_CONCURRENCY`

-   Total number of workers, independent of number of CPU cores.
-   Default: not set
-   Custom: `WEB_CONCURRENCY="4"`

`WORKERS_PER_CORE`

-   Number of Gunicorn workers per CPU core. Overridden if `WEB_CONCURRENCY` is set.
-   Default: 1
-   Custom:

    -   `WORKERS_PER_CORE="2"`: Run 2 worker processes per core (8 worker processes on a server with 4 cores).
    -   `WORKERS_PER_CORE="0.5"` (floating point values permitted): Run 1 worker process for every 2 cores (2 worker processes on a server with 4 cores).

    !!! note

        -   The default number of workers is the number of CPU cores multiplied by the value of the environment variable `WORKERS_PER_CORE` (which defaults to 1). On a machine with only 1 CPU core, the default minimum number of workers is 2 to avoid poor performance and blocking, as explained in the release notes for [tiangolo/uvicorn-gunicorn-docker 0.3.0](https://github.com/tiangolo/uvicorn-gunicorn-docker/releases/tag/0.3.0).
        -   If both `MAX_WORKERS` and `WEB_CONCURRENCY` are set, the least of the two will be used as the total number of workers.
        -   If either `MAX_WORKERS` or `WEB_CONCURRENCY` are set to 1, the total number of workers will be 1, overriding the default minimum of 2.

### Worker timeouts

[`GRACEFUL_TIMEOUT`](https://docs.gunicorn.org/en/stable/settings.html#graceful-timeout)

-   Number of seconds to wait for workers to finish serving requests before restart.
-   Default: `"120"`
-   Custom: `GRACEFUL_TIMEOUT="20"`

[`TIMEOUT`](https://docs.gunicorn.org/en/stable/settings.html#timeout)

-   Workers silent for more than this many seconds are killed and restarted.
-   Default: `"120"`
-   Custom: `TIMEOUT="20"`

[`KEEP_ALIVE`](https://docs.gunicorn.org/en/stable/settings.html#keepalive)

-   Number of seconds to wait for workers to finish serving requests on a Keep-Alive connection.
-   Default: `"5"`
-   Custom: `KEEP_ALIVE="20"`

### Host networking

`HOST`

-   Host IP address (inside of the container) where Gunicorn will listen for requests.
-   Default: `"0.0.0.0"`
-   Custom: n/a

`PORT`

-   Port the container should listen on.
-   Default: `"80"`
-   Custom: `PORT="8080"`

[`BIND`](https://docs.gunicorn.org/en/latest/settings.html#server-socket)

-   The actual host and port passed to Gunicorn.
-   Default: `HOST:PORT` (`"0.0.0.0:80"`)
-   Custom: `BIND="0.0.0.0:8080"` (if custom `BIND` is set, overrides `HOST` and `PORT`)

### Runtime configuration

`GUNICORN_CMD_ARGS`

-   Additional [command-line arguments for Gunicorn](https://docs.gunicorn.org/en/stable/settings.html). Gunicorn looks for the `GUNICORN_CMD_ARGS` environment variable automatically, and gives these settings precedence over other environment variables and Gunicorn config files.
-   Custom: To use a custom TLS certificate, copy or mount the certificate and private key into the Docker image, and set [`--keyfile` and `--certfile`](http://docs.gunicorn.org/en/latest/settings.html#ssl) to the location of the files.

    ```sh
    CERTS="--keyfile=/secrets/key.pem --certfile=/secrets/cert.pem"
    docker run -d -p 443:443 \
      -e GUNICORN_CMD_ARGS="$CERTS" \
      -e PORT=443 myimage
    ```

## Uvicorn

!!! info

    These settings are mostly used for local development.

`WITH_RELOAD`

-   Configure the [Uvicorn auto-reload setting](https://www.uvicorn.org/settings/).
-   Default: `"false"` (don't auto-reload when files change)
-   Custom: `"true"` (watch files and auto-reload when files change).

    !!! note

        [Auto-reloading is useful for local development](https://www.uvicorn.org/settings/#development).

`RELOAD_DIRS` _(new in inboard 0.7)_

-   Directories and files to watch for changes, formatted as comma-separated string.
-   Default: watch all directories under project root.
-   Custom:

    -   `"inboard"` (one directory)
    -   `"inboard, tests"` (two directories)
    -   `"inboard, tests, Dockerfile"` (two directories and a file)

    !!! note

        On the command-line, this [Uvicorn setting](https://www.uvicorn.org/settings/) is configured by passing `--reload-dir`, and can be passed multiple times, with one directory each.

        However, when running Uvicorn programmatically, `uvicorn.run` accepts a list of strings (`uvicorn.run(reload_dirs=["dir1", "dir2"])`), so inboard will parse the environment variable, send the list to Uvicorn, and Uvicorn will watch each directory or file specified.

`RELOAD_DELAY` _(new in inboard 0.11)_

-   Floating point value specifying the time, in seconds, to wait before reloading files.
-   Default: not set (the value is set by `uvicorn.config.Config`)
-   Custom: `"0.5"`

    !!! note

        - `uvicorn.run` equivalent: `reload_delay`
        - Uvicorn CLI equivalent: `--reload-delay`

`RELOAD_EXCLUDES` _(new in inboard 0.11)_

-   Glob pattern indicating files to exclude when watching for changes, formatted as comma-separated string.
-   Default: not set (the value is set by `uvicorn.config.Config`)
-   Custom: `"*[Dd]ockerfile"`

    !!! note

        - Parsed into a list of strings in the same manner as for `RELOAD_DIRS`.
        - `uvicorn.run` equivalent: `reload_excludes`
        - Uvicorn CLI equivalent: `--reload-exclude`

`RELOAD_INCLUDES` _(new in inboard 0.11)_

-   Glob pattern indicating files to include when watching for changes, formatted as comma-separated string.
-   Default: not set (the value is set by `uvicorn.config.Config`)
-   Custom: `"*.py, *.md"`

    !!! note

        - Parsed into a list of strings in the same manner as for `RELOAD_DIRS`.
        - `uvicorn.run` equivalent: `reload_includes`
        - Uvicorn CLI equivalent: `--reload-include`

`UVICORN_CONFIG_OPTIONS` _(advanced usage, new in inboard 0.11)_

-   JSON-formatted string containing additional keyword arguments ("kwargs") to pass directly to Uvicorn.
-   Default: not set
-   Custom: `UVICORN_CONFIG_OPTIONS='{"reload": true, "reload_delay": null}'`

The idea here is to allow a catch-all Uvicorn config variable in the spirit of `GUNICORN_CMD_ARGS`, so that advanced users can specify the full range of Uvicorn options even if inboard has not directly implemented them. The `inboard.start` module will run the `UVICORN_CONFIG_OPTIONS` environment variable value through `json.loads()`, and then pass the resultant dictionary through to Uvicorn. If the same option is set with an individual environment variable (such as `WITH_RELOAD`) and with a JSON value in `UVICORN_CONFIG_OPTIONS`, the JSON value will take precedence.

`json.loads()` converts data types from JSON to Python, and returns a Python dictionary. See the guide to [understanding JSON schema](https://json-schema.org/understanding-json-schema/index.html) for many helpful examples of how JSON data types correspond to Python data types. If the Uvicorn options are already available as a Python dictionary, dump them to a JSON-formatted string with `json.dumps()`, and set that as an environment variable.

!!! example "Example of how to format `UVICORN_CONFIG_OPTIONS` as valid JSON"

    ```py
    >>> import json
    >>> import os
    >>> uvicorn_config_dict = dict(host="0.0.0.0", port=80, log_config=None, log_level="info", reload=False)
    >>> json.dumps(uvicorn_config_dict)
    '{"host": "0.0.0.0", "port": 80, "log_config": null, "log_level": "info", "reload": false}'
    >>> os.environ["UVICORN_CONFIG_OPTIONS"] = json.dumps(uvicorn_config_dict)
    >>> json.loads(os.environ["UVICORN_CONFIG_OPTIONS"]) == uvicorn_config_dict
    True
    ```

!!! warning

    The `UVICORN_CONFIG_OPTIONS` environment variable is suggested for advanced usage because it requires some knowledge of `uvicorn.config.Config`. Other than the JSON -> Python dictionary conversion, no additional type conversions or validations are performed on `UVICORN_CONFIG_OPTIONS`. All options should be able to be passed directly to `uvicorn.config.Config`.

    In the example below, `reload` will be passed through with the correct type (because it was formatted with the correct JSON type initially), but `access_log` will have an incorrect type (because it was formatted as a string instead of as a Boolean).

    ```py
    >>> import json
    >>> import os
    >>> os.environ["UVICORN_CONFIG_OPTIONS_INCORRECT"] = '{"access_log": "false", "reload": true}'
    >>> json.loads(os.environ["UVICORN_CONFIG_OPTIONS_INCORRECT"])
    {'access_log': "false", 'reload': True}
    ```

## Logging

`LOGGING_CONF`

-   Python module containing a logging [configuration dictionary object](https://docs.python.org/3/library/logging.config.html) named `LOGGING_CONFIG`. Can be either a module path (`inboard.logging_conf`) or a file path (`/app/inboard/logging_conf.py`). The `LOGGING_CONFIG` dictionary will be loaded and passed to [`logging.config.dictConfig()`](https://docs.python.org/3/library/logging.config.html).
-   Default: `"inboard.logging_conf"` (the default module provided with inboard)
-   Custom: For a logging config module at `/app/package/custom_logging.py`, `LOGGING_CONF="package.custom_logging"` or `LOGGING_CONF="/app/package/custom_logging.py"`.

`LOG_COLORS`

-   Whether or not to color log messages. Currently only supported for `LOG_FORMAT="uvicorn"`.
-   Default:
    -   Auto-detected based on [`sys.stdout.isatty()`](https://docs.python.org/3/library/sys.html#sys.stdout).
-   Custom:
    -   `LOG_COLORS="true"`
    -   `LOG_COLORS="false"`

`LOG_FILTERS`

-   Comma-separated string identifying log records to filter out. The string will be split on commas and converted to a set. Each log message will then be checked for each filter in the set. If any matches are present in the log message, the logger will not log that message.
-   Default: `None` (don't filter out any log records, just log every record)
-   Custom: `LOG_FILTERS="/health, /heartbeat"` (filter out log messages that contain either the string `"/health"` or the string `"/heartbeat"`, to avoid logging health checks)
-   See also:
    -   [AWS Builders' Library: Implementing health checks](https://aws.amazon.com/builders-library/implementing-health-checks/)
    -   [AWS Elastic Load Balancing docs: Target groups - Health checks for your target groups](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/target-group-health-checks.html)
    -   [benoitc/gunicorn#1781](https://github.com/benoitc/gunicorn/issues/1781)
    -   [Python 3 docs: How-To - Logging Cookbook - Using Filters to impart contextual information](https://docs.python.org/3/howto/logging-cookbook.html#using-filters-to-impart-contextual-information)
    -   [Python 3 docs: What's new in Python 3.2 - logging](https://docs.python.org/3/whatsnew/3.2.html#logging)
    -   [Django 4.0 docs: Topics - Logging](https://docs.djangoproject.com/en/4.0/topics/logging/)

`LOG_FORMAT`

-   [Python logging format](https://docs.python.org/3/library/logging.html#formatter-objects).
-   Default:
    -   `"simple"`: Simply the log level and message.
-   Custom:

    -   `"verbose"`: The most informative format, with the first 80 characters providing metadata, and the remainder supplying the log message.
    -   `"gunicorn"`: Gunicorn's default format.
    -   `"uvicorn"`: Uvicorn's default format, similar to `simple`, with support for `LOG_COLORS`. Note that Uvicorn's `access` formatter is not supported here, because it frequently throws errors related to [ASGI scope](https://asgi.readthedocs.io/en/latest/specs/lifespan.html).

    !!!example "Example log message in different formats"

        ```log
        # simple
        INFO       Started server process [19012]

        # verbose
        2020-08-19 21:07:31 -0400      19012      uvicorn.error   main            INFO       Started server process [19012]

        # gunicorn
        [2020-08-19 21:07:31 -0400] [19012] [INFO] Started server process [19012]

        # uvicorn (can also be colored)
        INFO:     Started server process [19012]
        ```

`LOG_LEVEL`

-   Log level for [Gunicorn](https://docs.gunicorn.org/en/latest/settings.html#logging) or [Uvicorn](https://www.uvicorn.org/settings/#logging).
-   Default: `"info"`
-   Custom (organized from greatest to least amount of logging):
    -   `LOG_LEVEL="debug"`
    -   `LOG_LEVEL="info"`
    -   `LOG_LEVEL="warning"`
    -   `LOG_LEVEL="error"`
    -   `LOG_LEVEL="critical"`

`ACCESS_LOG`

-   Access log file to which to write.
-   Default: `"-"` (`stdout`, print in Docker logs)
-   Custom:
    -   `ACCESS_LOG="./path/to/accesslogfile.txt"`
    -   `ACCESS_LOG= ` (set to an empty value) to disable

`ERROR_LOG`

-   Error log file to which to write.
-   Default: `"-"` (`stdout`, print in Docker logs)
-   Custom:
    -   `ERROR_LOG="./path/to/errorlogfile.txt"`
    -   `ERROR_LOG= ` (set to an empty value) to disable

See the [logging reference](logging.md) for further info.

## Authentication

`BASIC_AUTH_USERNAME`

-   Username for HTTP Basic auth.
-   Default: not set
-   Custom: `BASIC_AUTH_USERNAME=test_user`

`BASIC_AUTH_PASSWORD`

-   Password for HTTP Basic auth.
-   Default: not set
-   Custom: `BASIC_AUTH_PASSWORD=r4ndom_bUt_memorable`

See the [authentication reference](authentication.md) for further info.
