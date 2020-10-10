# 🚢 inboard 🐳

_Docker images to power your Python APIs and help you ship faster._

[![PyPI](https://img.shields.io/pypi/v/inboard?color=success)](https://pypi.org/project/inboard/)
[![GitHub Container Registry](https://img.shields.io/badge/github%20container%20registry-inboard-success)](https://github.com/users/br3ndonland/packages/container/package/inboard)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://black.readthedocs.io/en/stable/)

[![builds](https://github.com/br3ndonland/inboard/workflows/builds/badge.svg)](https://github.com/br3ndonland/inboard/actions)
[![hooks](https://github.com/br3ndonland/inboard/workflows/hooks/badge.svg)](https://github.com/br3ndonland/inboard/actions)
[![tests](https://github.com/br3ndonland/inboard/workflows/tests/badge.svg)](https://github.com/br3ndonland/inboard/actions)
[![codecov](https://codecov.io/gh/br3ndonland/inboard/branch/develop/graph/badge.svg)](https://codecov.io/gh/br3ndonland/inboard)

Brendon Smith ([br3ndonland](https://github.com/br3ndonland/))

## Table of Contents <!-- omit in toc -->

- [Description](#description)
- [Instructions](#instructions)
  - [Pull images](#pull-images)
  - [Use images in a _Dockerfile_](#use-images-in-a-dockerfile)
  - [Run containers](#run-containers)
- [Configuration](#configuration)
  - [General](#general)
  - [Gunicorn and Uvicorn](#gunicorn-and-uvicorn)
  - [Logging](#logging)
- [Development](#development)
  - [Installation](#installation)
  - [Code style](#code-style)
  - [Testing with pytest](#testing-with-pytest)
  - [GitHub Actions workflows](#github-actions-workflows)
  - [Building development images](#building-development-images)
  - [Running development containers](#running-development-containers)
  - [Configuring Docker for GitHub Container Registry](#configuring-docker-for-github-container-registry)

## Description

This repo provides [Docker images](https://github.com/users/br3ndonland/packages/container/package/inboard) and a [PyPI package](https://pypi.org/project/inboard/) with useful utilities for Python web servers. It runs [Uvicorn with Gunicorn](https://www.uvicorn.org/), and can be used to build applications with [Starlette](https://www.starlette.io/) and [FastAPI](https://fastapi.tiangolo.com/). It is inspired by [tiangolo/uvicorn-gunicorn-docker](https://github.com/tiangolo/uvicorn-gunicorn-docker), with the following advantages:

- **One repo**. The tiangolo/uvicorn-gunicorn images are in at least three separate repos ([tiangolo/uvicorn-gunicorn-docker](https://github.com/tiangolo/uvicorn-gunicorn-docker), [tiangolo/uvicorn-gunicorn-fastapi-docker](https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker), and [tiangolo/uvicorn-gunicorn-starlette-docker](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker)), with large amounts of code duplication, making maintenance difficult for an [already-busy maintainer](https://github.com/encode/uvicorn/pull/705#issuecomment-660042305). This repo combines three into one.
- **One _Dockerfile_.** This repo leverages [multi-stage builds](https://docs.docker.com/develop/develop-images/multistage-build/) to produce multiple Docker images from one _Dockerfile_.
- **One Python requirements file.** This repo uses [Poetry](https://github.com/python-poetry/poetry) with Poetry Extras for dependency management with a single _pyproject.toml_.
- **One logging configuration.** Logging a Uvicorn+Gunicorn+Starlette/FastAPI stack is unnecessarily complicated. Uvicorn and Gunicorn use different logging configurations, and it can be difficult to unify the log streams. In this repo, Uvicorn, Gunicorn, and FastAPI log streams are propagated to the root logger, and handled by the custom root logging config. Developers can also supply their own custom logging configurations.
- **One programming language.** Pure Python with no shell scripts.
- **One platform.** You're already on GitHub. Why not [pull Docker images from GitHub Container Registry](https://github.blog/2020-09-01-introducing-github-container-registry/)?

## Instructions

### Pull images

Docker images are stored in [GitHub Container Registry](https://docs.github.com/en/free-pro-team@latest/packages/getting-started-with-github-container-registry) (GHCR), which is a Docker registry like Docker Hub. Public Docker images can be pulled anonymously from `ghcr.io`.

```sh
# Pull most recent version of each image
docker pull ghcr.io/br3ndonland/inboard:base
docker pull ghcr.io/br3ndonland/inboard:fastapi
docker pull ghcr.io/br3ndonland/inboard:starlette

# Pull image from specific release
docker pull ghcr.io/br3ndonland/inboard:base-0.2.0
docker pull ghcr.io/br3ndonland/inboard:fastapi-0.2.0
docker pull ghcr.io/br3ndonland/inboard:starlette-0.2.0
```

The FastAPI image is also tagged with `latest`. Docker uses the `latest` tag by default, so simply running `docker pull ghcr.io/br3ndonland/inboard` will pull the FastAPI image.

If authentication to GHCR is needed, follow the instructions [below](#configuring-docker-for-github-container-registry).

### Use images in a _Dockerfile_

For a [Poetry](https://github.com/python-poetry/poetry) project with the following directory structure:

- `repo`
  - `package`
    - `main.py`
    - `prestart.py`
  - `Dockerfile`
  - `poetry.lock`
  - `pyproject.toml`

The _Dockerfile_ could look like this:

```dockerfile
FROM ghcr.io/br3ndonland/inboard:fastapi

# Install Python requirements
COPY poetry.lock pyproject.toml /app/
WORKDIR /app/
RUN . $POETRY_HOME/env && poetry install --no-dev --no-interaction --no-root

# Install Python app
COPY package /app/package
ENV APP_MODULE=package.main:app
# RUN command already included in base image
```

Organizing the _Dockerfile_ this way helps [leverage the Docker build cache](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#leverage-build-cache). Files and commands that change most frequently are added last to the _Dockerfile_. Next time the image is built, Docker will skip any layers that didn't change, speeding up builds.

For a standard `pip` install:

- `repo`
  - `package`
    - `main.py`
    - `prestart.py`
  - `Dockerfile`
  - `requirements.txt`

```dockerfile
FROM ghcr.io/br3ndonland/inboard:fastapi

# Install Python requirements
COPY requirements.txt /app/
WORKDIR /app/
RUN python -m pip install -r requirements.txt

# Install Python app
COPY package /app/package
ENV APP_MODULE=package.main:app
# RUN command already included in base image
```

The image could then be built with:

```sh
cd /path/to/repo
docker build . -t imagename:latest
```

The final argument is the Docker image name (`imagename` in this example). Replace with your image name.

### Run containers

Run container:

```sh
docker run -d -p 80:80 imagename
```

Run container with mounted volume and Uvicorn reloading for development:

```sh
cd /path/to/repo
docker run -d -p 80:80 \
  -e "LOG_LEVEL=debug" -e "PROCESS_MANAGER=uvicorn" -e "WITH_RELOAD=true" \
  -v $(pwd)/package:/app/package imagename
```

Details on the `docker run` command:

- `-e "PROCESS_MANAGER=uvicorn" -e "WITH_RELOAD=true"` will instruct `start.py` to run Uvicorn with reloading and without Gunicorn. The Gunicorn configuration won't apply, but these environment variables will still work as [described](#configuration):
  - `APP_MODULE`
  - `HOST`
  - `PORT`
  - `LOG_COLORS`
  - `LOG_FORMAT`
  - `LOG_LEVEL`
- `-v $(pwd)/package:/app/package`: the specified directory (`/path/to/repo/package` in this example) will be [mounted as a volume](https://docs.docker.com/engine/reference/run/#volume-shared-filesystems) inside of the container at `/app/package`. When files in the working directory change, Docker and Uvicorn will sync the files to the running Docker container.

Hit an API endpoint:

```sh
docker pull ghcr.io/br3ndonland/inboard:fastapi
docker run -d -p 80:80 ghcr.io/br3ndonland/inboard:fastapi
http :80  # HTTPie: https://httpie.org/
```

```text
HTTP/1.1 200 OK
content-length: 17
content-type: application/json
date: Wed, 02 Sep 2020 00:31:01 GMT
server: uvicorn

{
    "Hello": "World"
}
```

## Configuration

To set environment variables when starting the Docker image:

```sh
docker run -d -p 80:80 -e APP_MODULE="package.custom.module:api" -e WORKERS_PER_CORE="2" myimage
```

To set environment variables within a _Dockerfile_:

```dockerfile
FROM ghcr.io/br3ndonland/inboard:fastapi
ENV APP_MODULE="package.custom.module:api" WORKERS_PER_CORE="2"
```

### General

- `APP_MODULE`: Python module with app instance. Note that the base image sets the environment variable `PYTHONPATH=/app`, so the module name will be relative to `/app` unless you supply a custom [`PYTHONPATH`](https://docs.python.org/3/using/cmdline.html#envvar-PYTHONPATH).

  - Default: The appropriate app module from inboard.
  - Custom: For a module at `/app/package/custom/module.py` and app instance object `api`, `APP_MODULE="package.custom.module:api"`

    ```py
    # /app/package/custom/module.py
    from fastapi import FastAPI

    api = FastAPI()

    @api.get("/")
    def read_root():
        return {"message": "Hello World!"}
    ```

- `PRE_START_PATH`: Path to a pre-start script. Add a file `prestart.py` or `prestart.sh` to the application directory, and copy the directory into the Docker image as described (for a project with the Python application in `repo/package`, `COPY package /app/package`). The container will automatically detect and run the prestart script before starting the web server.

  - Default: `"/app/inboard/prestart.py"` (the default file provided with the Docker image)
  - Custom: `PRE_START_PATH="/app/package/custom_script.sh"`

- [`PYTHONPATH`](https://docs.python.org/3/using/cmdline.html#envvar-PYTHONPATH): Python's search path for module files.
  - Default: `PYTHONPATH="/app"`
  - Custom: `PYTHONPATH="/app/custom"`

### Gunicorn and Uvicorn

- `GUNICORN_CONF`: Path to a [Gunicorn configuration file](https://docs.gunicorn.org/en/latest/settings.html#config-file). The Gunicorn command-line accepts file paths instead of module paths.
  - Default:
    - `"/app/inboard/gunicorn_conf.py"` (the default file provided with the Docker image)
  - Custom:
    - `GUNICORN_CONF="/app/package/custom_gunicorn_conf.py"`
- [Gunicorn worker processes](https://docs.gunicorn.org/en/latest/settings.html#worker-processes): The number of Gunicorn worker processes to run is determined based on the `MAX_WORKERS`, `WEB_CONCURRENCY`, and `WORKERS_PER_CORE` environment variables, with a default of 1 worker per CPU core and a default minimum of 2. This is the "performance auto-tuning" feature described in [tiangolo/uvicorn-gunicorn-docker](https://github.com/tiangolo/uvicorn-gunicorn-docker).
  - `MAX_WORKERS`: Maximum number of workers to use, independent of number of CPU cores.
    - Default: not set (unlimited)
    - Custom: `MAX_WORKERS="24"`
  - `WEB_CONCURRENCY`: Set number of workers independently of number of CPU cores.
    - Default: not set
    - Custom: `WEB_CONCURRENCY="4"`
  - `WORKERS_PER_CORE`: Number of Gunicorn workers per CPU core. Overridden if `WEB_CONCURRENCY` is set.
    - Default: 1
    - Custom:
      - `WORKERS_PER_CORE="2"`: Run 2 worker processes per core (8 worker processes on a server with 4 cores).
      - `WORKERS_PER_CORE="0.5"` (floating point values permitted): Run 1 worker process for every 2 cores (2 worker processes on a server with 4 cores).
  - Notes:
    - The default number of workers is the number of CPU cores multiplied by the environment variable `WORKERS_PER_CORE="1"`. On a machine with only 1 CPU core, the default minimum number of workers is 2 to avoid poor performance and blocking, as explained in the release notes for [tiangolo/uvicorn-gunicorn-docker 0.3.0](https://github.com/tiangolo/uvicorn-gunicorn-docker/releases/tag/0.3.0).
    - If both `MAX_WORKERS` and `WEB_CONCURRENCY` are set, the least of the two will be used as the total number of workers.
    - If either `MAX_WORKERS` or `WEB_CONCURRENCY` are set to 1, the total number of workers will be 1, overriding the default minimum of 2.
- `PROCESS_MANAGER`: Manager for Uvicorn worker processes. As described in the [Uvicorn docs](https://www.uvicorn.org), "Uvicorn includes a Gunicorn worker class allowing you to run ASGI applications, with all of Uvicorn's performance benefits, while also giving you Gunicorn's fully-featured process management."
  - Default: `"gunicorn"` (run Uvicorn with Gunicorn as the process manager)
  - Custom: `"uvicorn"` (run Uvicorn alone for local development)
- [`WORKER_CLASS`](https://docs.gunicorn.org/en/latest/settings.html#worker-processes): Uvicorn worker class for Gunicorn to use.
  - Default: `uvicorn.workers.UvicornWorker`
  - Custom: For the [alternate Uvicorn worker](https://www.uvicorn.org/deployment/), `WORKER_CLASS="uvicorn.workers.UvicornH11Worker"` _(TODO: the H11 worker is provided for [PyPy](https://www.pypy.org/) and hasn't yet been tested)_
- [`TIMEOUT`](https://docs.gunicorn.org/en/stable/settings.html#timeout): Workers silent for more than this many seconds are killed and restarted.
  - Default: `"120"`
  - Custom: `TIMEOUT="20"`
- [`GRACEFUL_TIMEOUT`](https://docs.gunicorn.org/en/stable/settings.html#graceful-timeout): Number of seconds to wait for workers to finish serving requests before restart.
  - Default: `"120"`
  - Custom: `GRACEFUL_TIMEOUT="20"`
- [`KEEP_ALIVE`](https://docs.gunicorn.org/en/stable/settings.html#keepalive): Number of seconds to wait for requests on a Keep-Alive connection.
  - Default: `"5"`
  - Custom: `KEEP_ALIVE="20"`
- `HOST`: Host IP address (inside of the container) where Gunicorn will listen for requests.
  - Default: `"0.0.0.0"`
  - Custom: _TODO_
- `PORT`: Port the container should listen on.
  - Default: `"80"`
  - Custom: `PORT="8080"`
- [`BIND`](https://docs.gunicorn.org/en/latest/settings.html#server-socket): The actual host and port passed to Gunicorn.
  - Default: `HOST:PORT` (`"0.0.0.0:80"`)
  - Custom: `BIND="0.0.0.0:8080"` (if custom `BIND` is set, overrides `HOST` and `PORT`)
- `GUNICORN_CMD_ARGS`: Additional [command-line arguments for Gunicorn](https://docs.gunicorn.org/en/stable/settings.html). Gunicorn looks for the `GUNICORN_CMD_ARGS` environment variable automatically, and gives these settings precedence over other environment variables and Gunicorn config files.
  - Custom: To use a custom TLS certificate, copy or mount the certificate and private key into the Docker image, and set [`--keyfile` and `--certfile`](http://docs.gunicorn.org/en/latest/settings.html#ssl) to the location of the files.
    ```sh
    docker run -d -p 443:443 \
      -e GUNICORN_CMD_ARGS="--keyfile=/secrets/key.pem --certfile=/secrets/cert.pem" \
      -e PORT=443 myimage
    ```

### Logging

- `LOGGING_CONF`: Python module containing a logging [configuration dictionary object](https://docs.python.org/3/library/logging.config.html) named `LOGGING_CONFIG`. Can be either a module path (`inboard.logging_conf`) or a file path (`/app/inboard/logging_conf.py`). The `LOGGING_CONFIG` dictionary will be loaded and passed to [`logging.config.dictConfig()`](https://docs.python.org/3/library/logging.config.html). See [br3ndonland/inboard#3](https://github.com/br3ndonland/inboard/pull/3) for more details on logging setup.

  - Default: `"inboard.logging_conf"` (the default module provided with inboard)
  - Custom: For a logging config module at `/app/package/custom_logging.py`, `LOGGING_CONF="package.custom_logging"` or `LOGGING_CONF="/app/package/custom_logging.py"`.
  - If inboard is installed from PyPI with `pip install inboard`, the logging configuration can be easily extended. For example,

    ```py
    # /app/package/custom_logging.py
    from typing import Any, Dict

    from inboard import logging_conf


    LOGGING_CONFIG: Dict[str, Any] = logging_conf.LOGGING_CONFIG
    LOGGING_CONFIG["loggers"]["boto3"] = {"propagate": False}
    LOGGING_CONFIG["loggers"]["botocore"] = {"propagate": False}
    LOGGING_CONFIG["loggers"]["s3transfer"] = {"propagate": False}
    ```

- `LOG_COLORS`: Whether or not to color log messages. Currently only supported for `LOG_FORMAT="uvicorn"`.
  - Default:
    - Auto-detected based on [`sys.stdout.isatty()`](https://docs.python.org/3/library/sys.html#sys.stdout).
  - Custom:
    - `LOG_COLORS="true"`
    - `LOG_COLORS="false"`
- `LOG_FORMAT`: [Python logging format](https://docs.python.org/3/library/logging.html#formatter-objects).
  - Default:
    - `"simple"`: Simply the log level and message.
  - Custom:
    - `"verbose"`: The most informative format, with the first 80 characters providing metadata, and the remainder supplying the log message.
    - `"gunicorn"`: Gunicorn's default format.
    - `"uvicorn"`: Uvicorn's default format, similar to `simple`, with support for `LOG_COLORS`. Note that Uvicorn's `access` formatter is not supported here, because it frequently throws errors related to [ASGI scope](https://asgi.readthedocs.io/en/latest/specs/lifespan.html).
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
- `LOG_LEVEL`: Log level for [Gunicorn](https://docs.gunicorn.org/en/latest/settings.html#logging) or [Uvicorn](https://www.uvicorn.org/settings/#logging).
  - Default: `"info"`
  - Custom (organized from greatest to least amount of logging):
    - `LOG_LEVEL="debug"`
    - `LOG_LEVEL="info"`
    - `LOG_LEVEL="warning"`
    - `LOG_LEVEL="error"`
    - `LOG_LEVEL="critical"`
- `ACCESS_LOG`: Access log file to which to write.
  - Default: `"-"` (`stdout`, print in Docker logs)
  - Custom:
    - `ACCESS_LOG="./path/to/accesslogfile.txt"`
    - `ACCESS_LOG=` (set to an empty value) to disable
- `ERROR_LOG`: Error log file to which to write.
  - Default: `"-"` (`stdout`, print in Docker logs)
  - Custom:
    - `ERROR_LOG="./path/to/errorlogfile.txt"`
    - `ERROR_LOG=` (set to an empty value) to disable

For more information on Python logging configuration, see the [Python `logging` how-to](https://docs.python.org/3/howto/logging.html), [Python `logging` cookbook](https://docs.python.org/3/howto/logging-cookbook.html), [Python `logging` module docs](https://docs.python.org/3/library/logging.html), and [Python `logging.config` module docs](https://docs.python.org/3/library/logging.config.html). Also consider [Loguru](https://loguru.readthedocs.io/en/stable/index.html), an alternative logging module with many improvements over the standard library `logging` module.

## Development

### Installation

- Install Poetry (see the [Poetry docs](https://python-poetry.org/docs/) and _[CONTRIBUTING.md](https://github.com/br3ndonland/inboard/blob/develop/.github/CONTRIBUTING.md#poetry)_ for instructions)
- Install project with all dependencies: `poetry install -E fastapi`

### Code style

- Python code is formatted with [Black](https://black.readthedocs.io/en/stable/). Configuration for Black is stored in _[pyproject.toml](https://github.com/br3ndonland/inboard/blob/develop/pyproject.toml)_.
- Python imports are organized automatically with [isort](https://pycqa.github.io/isort/).
  - The isort package organizes imports in three sections:
    1. Standard library
    2. Dependencies
    3. Project
  - Within each of those groups, `import` statements occur first, then `from` statements, in alphabetical order.
  - You can run isort from the command line with `poetry run isort .`.
  - Configuration for isort is stored in _[pyproject.toml](https://github.com/br3ndonland/inboard/blob/develop/pyproject.toml)_.
- Other web code (JSON, Markdown, YAML) is formatted with [Prettier](https://prettier.io/).
- Code style is enforced with [pre-commit](https://pre-commit.com/), which runs [Git hooks](https://www.git-scm.com/book/en/v2/Customizing-Git-Git-Hooks).

  - Configuration is stored in _[.pre-commit-config.yaml](https://github.com/br3ndonland/inboard/blob/develop/.pre-commit-config.yaml)_.
  - Pre-commit can run locally before each commit (hence "pre-commit"), or on different Git events like `pre-push`.
  - Pre-commit is installed in the Poetry environment. To use:

    ```sh
    # after running `poetry install`
    path/to/inboard
    ❯ poetry shell

    # install hooks that run before each commit
    path/to/inboard
    .venv ❯ pre-commit install

    # and/or install hooks that run before each push
    path/to/inboard
    .venv ❯ pre-commit install --hook-type pre-push
    ```

  - Pre-commit is also useful as a CI tool. The [hooks](https://github.com/br3ndonland/inboard/blob/develop/.github/workflows/hooks.yml) GitHub Actions workflow runs pre-commit hooks with [GitHub Actions](https://github.com/features/actions).

### Testing with pytest

- Tests are in the _tests/_ directory.
- Run tests by [invoking `pytest` from the command-line](https://docs.pytest.org/en/stable/usage.html) within the Poetry environment in the root directory of the repo.
- [pytest](https://docs.pytest.org/en/latest/) features used include:
  - [fixtures](https://docs.pytest.org/en/latest/fixture.html)
  - [monkeypatch](https://docs.pytest.org/en/latest/monkeypatch.html)
  - [parametrize](https://docs.pytest.org/en/latest/parametrize.html)
  - [`tmp_path`](https://docs.pytest.org/en/latest/tmpdir.html)
- [pytest plugins](https://docs.pytest.org/en/stable/plugins.html) include:
  - [pytest-cov](https://github.com/pytest-dev/pytest-cov)
  - [pytest-mock](https://github.com/pytest-dev/pytest-mock)
- [pytest configuration](https://docs.pytest.org/en/stable/customize.html) is in _[pyproject.toml](https://github.com/br3ndonland/inboard/blob/develop/pyproject.toml)_.
- [FastAPI testing](https://fastapi.tiangolo.com/tutorial/testing/) and [Starlette testing](https://www.starlette.io/testclient/) rely on the [Starlette `TestClient`](https://www.starlette.io/testclient/), which uses [Requests](https://requests.readthedocs.io/en/master/) under the hood.
- Test coverage results are reported when invoking `pytest` from the command-line. To see interactive HTML coverage reports, invoke pytest with `pytest --cov-report=html`.
- Test coverage reports are generated within GitHub Actions workflows by [pytest-cov](https://github.com/pytest-dev/pytest-cov) with [coverage.py](https://github.com/nedbat/coveragepy), and uploaded to [Codecov](https://docs.codecov.io/docs) using [codecov/codecov-action](https://github.com/marketplace/actions/codecov). Codecov is then integrated into pull requests with the [Codecov GitHub app](https://github.com/marketplace/codecov).

### GitHub Actions workflows

[GitHub Actions](https://github.com/features/actions) is a continuous integration/continuous deployment (CI/CD) service that runs on GitHub repos. It replaces other services like Travis CI. Actions are grouped into workflows and stored in _.github/workflows_. See [Getting the Gist of GitHub Actions](https://gist.github.com/br3ndonland/f9c753eb27381f97336aa21b8d932be6) for more info.

### Building development images

To build the Docker images for each stage:

```sh
git clone git@github.com:br3ndonland/inboard.git

cd inboard

docker build . --rm --target base -t localhost/br3ndonland/inboard:base && \
docker build . --rm --target fastapi -t localhost/br3ndonland/inboard:fastapi && \
docker build . --rm --target starlette -t localhost/br3ndonland/inboard:starlette
```

### Running development containers

```sh
# Run Docker container with Uvicorn and reloading
cd inboard

docker run -d -p 80:80 \
  -e "LOG_LEVEL=debug" -e "PROCESS_MANAGER=uvicorn" -e "WITH_RELOAD=true" \
  -v $(pwd)/inboard:/app/inboard localhost/br3ndonland/inboard:base

docker run -d -p 80:80 \
  -e "LOG_LEVEL=debug" -e "PROCESS_MANAGER=uvicorn" -e "WITH_RELOAD=true" \
  -v $(pwd)/inboard:/app/inboard localhost/br3ndonland/inboard:fastapi

docker run -d -p 80:80 \
  -e "LOG_LEVEL=debug" -e "PROCESS_MANAGER=uvicorn" -e "WITH_RELOAD=true" \
  -v $(pwd)/inboard:/app/inboard localhost/br3ndonland/inboard:starlette

# Run Docker container with Gunicorn and Uvicorn
docker run -d -p 80:80 localhost/br3ndonland/inboard:base
docker run -d -p 80:80 localhost/br3ndonland/inboard:fastapi
docker run -d -p 80:80 localhost/br3ndonland/inboard:starlette

# Test HTTP Basic Auth when running the FastAPI or Starlette images:
http :80/status --auth-type=basic --auth=test_username:plunge-germane-tribal-pillar
```

Change the port numbers to run multiple containers simultaneously (`-p 81:80`).

### Configuring Docker for GitHub Container Registry

If authentication is needed, follow the instructions in the GitHub docs on [configuring Docker for use with GHCR](https://docs.github.com/en/free-pro-team@latest/packages/getting-started-with-github-container-registry/migrating-to-github-container-registry-for-docker-images). You'll need to [create a personal access token (PAT)](https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/creating-a-personal-access-token). On GitHub, navigate to _Settings -> Developer settings -> Personal access tokens_ ([github.com/settings/tokens](https://github.com/settings/tokens)), then click "Generate new token." The token should have `read:packages` scope. You can then copy the token and use it with [`docker login`](https://docs.docker.com/engine/reference/commandline/login/):

```sh
# create PAT in GitHub and copy to clipboard

# transfer PAT from clipboard to file
pbpaste > pat-ghcr.txt

# log in with file
cat pat-ghcr.txt | docker login ghcr.io -u YOUR_GITHUB_USERNAME --password-stdin
```

If you don't want to store your PAT in plain text, encrypt it with PGP instead. [GPG](https://www.gnupg.org/) or [Keybase](https://keybase.io) can be used for this. Here's how to do it with Keybase:

```sh
# create PAT in GitHub and copy to clipboard

# transfer PAT from clipboard to encrypted file
pbpaste | keybase encrypt -o pat-ghcr.asc $YOUR_USERNAME

# decrypt and log in
keybase decrypt -i pat-ghcr.asc | docker login ghcr.io -u YOUR_GITHUB_USERNAME --password-stdin

# can also use keybase pgp encrypt and keybase pgp decrypt, but must export PGP key
```
