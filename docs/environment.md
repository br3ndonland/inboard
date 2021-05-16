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

    ```py
    # /app/package/custom/module.py
    from fastapi import FastAPI

    api = FastAPI()

    @api.get("/")
    def read_root():
        return {"message": "Hello World!"}
    ```

    <!-- prettier-ignore -->
    !!! note
        The base Docker image sets the environment variable `PYTHONPATH=/app`, so the module name will be relative to `/app` unless you supply a custom [`PYTHONPATH`](https://docs.python.org/3/using/cmdline.html#envvar-PYTHONPATH).

`PRE_START_PATH`

-   Path to a pre-start script.
-   Default: `"/app/inboard/prestart.py"` (provided with inboard)
-   Custom:

    -   `PRE_START_PATH="/app/package/custom_script.sh"`
    -   `PRE_START_PATH= ` (set to an empty value) to disable

    <!-- prettier-ignore -->
    !!! tip
        Add a file `prestart.py` or `prestart.sh` to the application directory, and copy the directory into the Docker image as described (for a project with the Python application in `repo/package`, `COPY package /app/package`). The container will automatically detect and run the prestart script before starting the web server.

[`PYTHONPATH`](https://docs.python.org/3/using/cmdline.html#envvar-PYTHONPATH)

-   Python's search path for module files.
-   Default: `PYTHONPATH="/app"`
-   Custom: `PYTHONPATH="/app/custom"`

## Gunicorn

### Configuration file

`GUNICORN_CONF`

-   Path to a [Gunicorn configuration file](https://docs.gunicorn.org/en/latest/settings.html#config-file). The Gunicorn command-line accepts file paths instead of module paths.
-   Default:
    -   `"/app/inboard/gunicorn_conf.py"` (provided with inboard)
-   Custom:
    -   `GUNICORN_CONF="/app/package/custom_gunicorn_conf.py"`

### Process management

<!-- prettier-ignore -->
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

<!-- prettier-ignore -->
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

    <!-- prettier-ignore -->
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

<!-- prettier-ignore -->
!!! info
    These settings are mostly used for local development.

`WITH_RELOAD`

-   Configure the [Uvicorn auto-reload setting](https://www.uvicorn.org/settings/).
-   Default: `"false"` (don't auto-reload when files change)
-   Custom: `"true"` (watch files with [watchgod](https://github.com/samuelcolvin/watchgod) and auto-reload when files change).

    <!-- prettier-ignore -->
    !!! note
        Auto-reloading is useful for local development. [Watchgod](https://github.com/samuelcolvin/watchgod) was added as an optional dependency in [Uvicorn 0.11.4](https://github.com/encode/uvicorn/releases/tag/0.11.4), and is included with inboard.

`RELOAD_DIRS`

-   Directories and files to watch for changes with [watchgod](https://github.com/samuelcolvin/watchgod), formatted as comma-separated string.
-   Default: watch all directories under project root.
-   Custom:

    -   `"inboard"` (one directory)
    -   `"inboard, tests"` (two directories)
    -   `"inboard, tests, Dockerfile"` (two directories and a file)

    <!-- prettier-ignore -->
    !!! note
        On the command-line, this [Uvicorn setting](https://www.uvicorn.org/settings/) is configured by passing `--reload-dir`, and can be passed multiple times, with one directory each.

        However, when running Uvicorn programmatically, `uvicorn.run` accepts a list of strings (`uvicorn.run(reload_dirs=["dir1", "dir2"])`), so inboard will parse the environment variable, send the list to Uvicorn, and watchgod will watch each directory or file specified.

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

`LOG_FORMAT`

-   [Python logging format](https://docs.python.org/3/library/logging.html#formatter-objects).
-   Default:
    -   `"simple"`: Simply the log level and message.
-   Custom:
    -   `"verbose"`: The most informative format, with the first 80 characters providing metadata, and the remainder supplying the log message.
    -   `"gunicorn"`: Gunicorn's default format.
    -   `"uvicorn"`: Uvicorn's default format, similar to `simple`, with support for `LOG_COLORS`. Note that Uvicorn's `access` formatter is not supported here, because it frequently throws errors related to [ASGI scope](https://asgi.readthedocs.io/en/latest/specs/lifespan.html).
-   Examples:
    ```sh
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
