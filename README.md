# :ship: inboard :whale:

_Docker images to power your Python APIs and help you ship faster. With support for Uvicorn, Gunicorn, Starlette, and FastAPI._

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
![hooks](https://github.com/br3ndonland/inboard/workflows/hooks/badge.svg)
![tests](https://github.com/br3ndonland/inboard/workflows/tests/badge.svg)

Brendon Smith ([br3ndonland](https://github.com/br3ndonland/))

## Table of Contents <!-- omit in toc -->

- [Description](#description)
- [Instructions](#instructions)
  - [Configure Docker for GitHub Packages](#configure-docker-for-github-packages)
  - [Pull images](#pull-images)
  - [Use images in a _Dockerfile_](#use-images-in-a-dockerfile)
  - [Run containers](#run-containers)
- [Configuration](#configuration)
  - [General](#general)
  - [Gunicorn and Uvicorn](#gunicorn-and-uvicorn)
  - [Logging](#logging)
- [Development](#development)
  - [Code style](#code-style)
  - [Building development images](#building-development-images)
  - [Running development containers](#running-development-containers)

## Description

This repo is inspired by [tiangolo/uvicorn-gunicorn-docker](https://github.com/tiangolo/uvicorn-gunicorn-docker), with the following advantages:

- **One repo**. The tiangolo/uvicorn-gunicorn images are in at least three separate repos ([tiangolo/uvicorn-gunicorn-docker](https://github.com/tiangolo/uvicorn-gunicorn-docker), [tiangolo/uvicorn-gunicorn-fastapi-docker](https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker), and [tiangolo/uvicorn-gunicorn-starlette-docker](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker)), with large amounts of code duplication, making maintenance difficult for an [already-busy maintainer](https://github.com/encode/uvicorn/pull/705#issuecomment-660042305). This repo combines three into one.
- **One _Dockerfile_.** This repo leverages [multi-stage builds](https://docs.docker.com/develop/develop-images/multistage-build/) to produce multiple Docker images from one _Dockerfile_.
- **One Python requirements file.** This repo uses [Poetry](https://github.com/python-poetry/poetry) with Poetry Extras for dependency management with a single _pyproject.toml_.
- **One logging configuration.** Logging a Uvicorn+Gunicorn+Starlette/FastAPI stack is unnecessarily complicated. Uvicorn and Gunicorn use different logging configurations, and it can be difficult to unify the log streams. In this repo, Uvicorn, Gunicorn, and FastAPI log streams are propagated to the root logger, and handled by the custom root logging config. Developers can also supply their own custom logging configurations.
- **One programming language.** Pure Python with no shell scripts.
- **One platform.** You're already on GitHub. Why not [pull Docker images from GitHub Packages](https://docs.github.com/en/packages/using-github-packages-with-your-projects-ecosystem/configuring-docker-for-use-with-github-packages)?

## Instructions

### Configure Docker for GitHub Packages

[GitHub Packages](https://docs.github.com/en/packages) is a Docker registry. Follow the instructions in the GitHub docs on [configuring Docker for use with GitHub Packages](https://docs.github.com/en/packages/using-github-packages-with-your-projects-ecosystem/configuring-docker-for-use-with-github-packages).

You'll need to [create a personal access token (PAT)](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token). Navigate to [github.com/settings/tokens](https://github.com/settings/tokens), then click "Generate new token." The token should have `read:packages` scope. You can then copy the token and use it with [`docker login`](https://docs.docker.com/engine/reference/commandline/login/):

```sh
# create PAT in GitHub and copy to clipboard

# transfer PAT from clipboard to file
pbpaste > pat-github-packages.txt

# log in with file
cat pat-github-packages.txt | docker login \
  https://docker.pkg.github.com -u YOUR_GITHUB_USERNAME --password-stdin
```

If you don't want to store your PAT in plain text, encrypt it with PGP instead. [GPG](https://www.gnupg.org/) or [Keybase](https://keybase.io) can be used for this. Here's how to do it with Keybase:

```sh
# create PAT in GitHub and copy to clipboard

# transfer PAT from clipboard to PGP encrypted file
pbpaste | keybase pgp encrypt -o pat-github-packages.asc -s

# decrypt and log in
keybase pgp decrypt -i pat-github-packages.asc | docker login \
  https://docker.pkg.github.com -u YOUR_GITHUB_USERNAME --password-stdin
```

### Pull images

After logging in, you can then pull images from `docker.pkg.github.com`. Docker uses the `latest` tag by default.

```sh
docker pull docker.pkg.github.com/br3ndonland/inboard/base
docker pull docker.pkg.github.com/br3ndonland/inboard/fastapi
docker pull docker.pkg.github.com/br3ndonland/inboard/starlette
```

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
FROM docker.pkg.github.com/br3ndonland/inboard/fastapi

# Install Python requirements
COPY poetry.lock pyproject.toml /
RUN poetry install --no-dev --no-interaction --no-root

# Install Python app
COPY package /app/

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
FROM docker.pkg.github.com/br3ndonland/inboard/fastapi

# Install Python requirements
COPY requirements.txt /
RUN python -m pip install -r requirements.txt

# Install Python app
COPY package /app/

# RUN command already included in base image
```

The image could then be built with:

```sh
cd /path/to/repo
docker build . -t imagename:latest
```

### Run containers

Run container:

```sh
docker run -d -p 80:80 imagename
```

Run container with mounted volume and Uvicorn reloading for development:

```sh
cd /path/to/repo
docker run -d -p 80:80 -e "LOG_LEVEL=debug" -e "WITH_RELOAD=true" -v $(pwd)/package:/app imagename
```

- `WITH_RELOAD=true`: `start.py` will run Uvicorn with reloading and without Gunicorn. The Gunicorn configuration won't apply, but these environment variables will still work as [described](#configuration):
  - `MODULE_NAME`
  - `VARIABLE_NAME`
  - `APP_MODULE`
  - `HOST`
  - `PORT`
  - `LOG_COLORS`
  - `LOG_FORMAT`
  - `LOG_LEVEL`
- `-v $(pwd)/package:/app`: the specified directory (`/path/to/repo/package` in this example) will be [mounted as a volume](https://docs.docker.com/engine/reference/run/#volume-shared-filesystems) inside of the container at `/app`. When files in the working directory change, Docker and Uvicorn will sync the files to the running Docker container.
- The final argument is the Docker image name (`imagename` in this example). Replace with your image name.

Hit an API endpoint:

```sh
docker pull docker.pkg.github.com/br3ndonland/inboard/base
docker run -d -p 80:80 docker.pkg.github.com/br3ndonland/inboard/base
http :80  # HTTPie: https://httpie.org/
```

```text
HTTP/1.1 200 OK
content-type: text/plain
date: Sat, 15 Aug 2020 14:43:53 GMT
server: uvicorn
transfer-encoding: chunked

Hello World, from Uvicorn, Gunicorn, and Python 3.8!
```

## Configuration

To set environment variables when starting the Docker image:

```sh
docker run -d -p 80:80 -e APP_MODULE="custom.module:api" -e WORKERS_PER_CORE="2" myimage
```

To set environment variables within a _Dockerfile_:

```dockerfile
FROM docker.pkg.github.com/br3ndonland/inboard/fastapi
ENV APP_MODULE="custom.module:api" WORKERS_PER_CORE="2"
```

### General

- `MODULE_NAME`: Python module (file) with app instance. Note that the base image sets the environment variable `PYTHONPATH=/app`, so the module name will be relative to `/app` unless you supply a custom `PYTHONPATH`.
  - Default:
    - `"main"` if there's a file `/app/main.py`
    - Else `"app.main"` if there's a file `/app/app/main.py`
  - Custom: For a module at `/app/custom/module.py`, `MODULE_NAME="custom.module"`
- `VARIABLE_NAME`: Variable (object) inside of the Python module that contains the ASGI application instance.

  - Default: `"app"`
  - Custom: For an application instance named `api`, `VARIABLE_NAME="api"`

    ```py
    from fastapi import FastAPI

    api = FastAPI()

    @api.get("/")
    def read_root():
        return {"message": "Hello World!"}
    ```

- `APP_MODULE`: Combination of `MODULE_NAME` and `VARIABLE_NAME` pointing to the app instance.
  - Default:
    - `MODULE_NAME:VARIABLE_NAME` (`"main:app"` or `"app.main:app"`)
  - Custom: For a module at `/app/custom/module.py` and variable `api`, `APP_MODULE="custom.module:api"`
- `PRE_START_PATH`: Path to a pre-start script. Add a file `prestart.py` or `prestart.sh` to the application directory, and copy the directory into the Docker image as described (for a project with the Python application in `repo/package`, `COPY package /app/`). The container will automatically detect and run the prestart script before starting the web server.

  - Default: `"/app/prestart.py"`
  - Custom: `PRE_START_PATH="/custom/script.sh"`

- [`PYTHONPATH`](https://docs.python.org/3/using/cmdline.html#envvar-PYTHONPATH): Python's search path for module files.
  - Default: `PYTHONPATH="/app"`
  - Custom: `PYTHONPATH="/app/custom"`

### Gunicorn and Uvicorn

- `GUNICORN_CONF`: Path to a [Gunicorn configuration file](https://docs.gunicorn.org/en/latest/settings.html#config-file).
  - Default:
    - `"/app/gunicorn_conf.py"` if exists
    - Else `"/app/app/gunicorn_conf.py"` if exists
    - Else `"/gunicorn_conf.py"` (the default file provided with the Docker image)
  - Custom:
    - `GUNICORN_CONF="/app/custom_gunicorn_conf.py"`
    - Feel free to use the [`gunicorn_conf.py`](./inboard/gunicorn_conf.py) from this repo as a starting point for your own custom configuration.
- `HOST`: Host IP address (inside of the container) where Gunicorn will listen for requests.
  - Default: `"0.0.0.0"`
  - Custom: _TODO_
- `PORT`: Port the container should listen on.
  - Default: `"80"`
  - Custom: `PORT="8080"`
- [`BIND`](https://docs.gunicorn.org/en/latest/settings.html#server-socket): The actual host and port passed to Gunicorn.
  - Default: `HOST:PORT` (`"0.0.0.0:80"`)
  - Custom: `BIND="0.0.0.0:8080"`
- [`WORKER_CLASS`](https://docs.gunicorn.org/en/latest/settings.html#worker-processes): The class to be used by Gunicorn for the workers.
  - Default: `uvicorn.workers.UvicornWorker`
  - Custom: For the alternate Uvicorn worker, `WORKER_CLASS="uvicorn.workers.UvicornH11Worker"`
- [`WORKERS_PER_CORE`](https://docs.gunicorn.org/en/latest/settings.html#worker-processes): Number of Gunicorn workers per CPU core.
  - Default: `"1"`
  - Custom: `WORKERS_PER_CORE="2"`
  - Notes:
    - This image will check how many CPU cores are available in the current server running your container. It will set the number of workers to the number of CPU cores multiplied by this value.
    - On a server with 2 CPU cores, `WORKERS_PER_CORE="3"` will run 6 worker processes.
    - Floating point values are permitted. If you have a powerful server (let's say, with 8 CPU cores) running several applications, including an ASGI application that won't need high performance, but you don't want to waste server resources, you could set the environment variable to `WORKERS_PER_CORE="0.5"`. A server with 8 CPU cores would start only 4 worker processes.
    - By default, if `WORKERS_PER_CORE="1"` and the server has only 1 CPU core, 2 workers will be started instead of 1, to avoid poor performance and blocking applications. This behavior can be overridden using `WEB_CONCURRENCY`.
- `MAX_WORKERS`: Maximum number of workers to use, independent of number of CPU cores.
  - Default: unlimited (not set)
  - Custom: `MAX_WORKERS="24"`
- [`WEB_CONCURRENCY`](https://docs.gunicorn.org/en/latest/settings.html#worker-processes): Set number of workers independently of number of CPU cores.
  - Default:
    - Number of CPU cores multiplied by the environment variable `WORKERS_PER_CORE`.
    - In a server with 2 cores and default `WORKERS_PER_CORE="1"`, default `"2"`.
  - Custom: To have 4 workers, `WEB_CONCURRENCY="4"`
- [`TIMEOUT`](https://docs.gunicorn.org/en/stable/settings.html#timeout): Workers silent for more than this many seconds are killed and restarted.
  - Default: `"120"`
  - Custom: `TIMEOUT="20"`
- [`GRACEFUL_TIMEOUT`](https://docs.gunicorn.org/en/stable/settings.html#graceful-timeout): Number of seconds to allow workers finish serving requests before restart.
  - Default: `"120"`
  - Custom: `GRACEFUL_TIMEOUT="20"`
- [`KEEP_ALIVE`](https://docs.gunicorn.org/en/stable/settings.html#keepalive): Number of seconds to wait for requests on a Keep-Alive connection.
  - Default: `"2"`
  - Custom: `KEEP_ALIVE="20"`
- `GUNICORN_CMD_ARGS`: Additional [command-line arguments for Gunicorn](https://docs.gunicorn.org/en/stable/settings.html). Gunicorn looks for the `GUNICORN_CMD_ARGS` environment variable automatically, and gives these settings precedence over other environment variables and Gunicorn config files.
  - Custom: To use a custom TLS certificate, copy or mount the certificate and private key into the Docker image, and set [`--keyfile` and `--certfile`](http://docs.gunicorn.org/en/latest/settings.html#ssl) to the location of the files.
    ```sh
    docker run -d -p 443:443 \
      -e GUNICORN_CMD_ARGS="--keyfile=/secrets/key.pem --certfile=/secrets/cert.pem" \
      -e PORT=443 myimage
    ```

### Logging

- `LOGGING_CONF`: Path to a [Python logging configuration file](https://docs.python.org/3/library/logging.config.html). The configuration must be a new-style `.py` file, containing a configuration dictionary object named `LOGGING_CONFIG`. The `LOGGING_CONFIG` dictionary will be passed to [`logging.config.dictConfig()`](https://docs.python.org/3/library/logging.config.html). See [br3ndonland/inboard#3](https://github.com/br3ndonland/inboard/pull/3) for more details on this design choice.
  - Default:
    - `"/app/logging_conf.py"` if exists
    - Else `"/app/app/logging_conf.py"` if exists
    - Else `"/logging_conf.py"` (the default file provided with the Docker image)
  - Custom:
    - `LOGGING_CONF="/app/custom_logging.py"`
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
  2020-08-19 20:50:05 -0400      19012      uvicorn.error   main            INFO       Started server process [19012]
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

### Code style

- Python code is formatted with [Black](https://black.readthedocs.io/en/stable/). Configuration for Black is stored in _[pyproject.toml](pyproject.toml)_.
- Python imports are organized automatically with [isort](https://timothycrosley.github.io/isort/).
  - The isort package organizes imports in three sections:
    1. Standard library
    2. Dependencies
    3. Project
  - Within each of those groups, `import` statements occur first, then `from` statements, in alphabetical order.
  - You can run isort from the command line with `poetry run isort .`.
  - Configuration for isort is stored in _[pyproject.toml](pyproject.toml)_.
- Other web code (JSON, Markdown, YAML) is formatted with [Prettier](https://prettier.io/).

### Building development images

To build the Docker images for each stage:

```sh
git clone git@github.com:br3ndonland/inboard.git

cd inboard

docker build . --rm --target base -t localhost/br3ndonland/inboard/base:latest && \
docker build . --rm --target fastapi -t localhost/br3ndonland/inboard/fastapi:latest && \
docker build . --rm --target starlette -t localhost/br3ndonland/inboard/starlette:latest
```

### Running development containers

```sh
# Uvicorn with reloading
cd inboard

docker run -d -p 80:80 -e "LOG_LEVEL=debug" -e "WITH_RELOAD=true" \
  -v $(pwd)/inboard/gunicorn_conf.py:/gunicorn_conf.py \
  -v $(pwd)/inboard/logging_conf.py:/logging_conf.py \
  -v $(pwd)/inboard/start.py:/start.py \
  -v $(pwd)/inboard/app:/app localhost/br3ndonland/inboard/base

docker run -d -p 80:80 -e "LOG_LEVEL=debug" -e "WITH_RELOAD=true" \
  -v $(pwd)/inboard/gunicorn_conf.py:/gunicorn_conf.py \
  -v $(pwd)/inboard/logging_conf.py:/logging_conf.py \
  -v $(pwd)/inboard/start.py:/start.py \
  -v $(pwd)/inboard/app:/app localhost/br3ndonland/inboard/fastapi

docker run -d -p 80:80 -e "LOG_LEVEL=debug" -e "WITH_RELOAD=true" \
  -v $(pwd)/inboard/gunicorn_conf.py:/gunicorn_conf.py \
  -v $(pwd)/inboard/logging_conf.py:/logging_conf.py \
  -v $(pwd)/inboard/start.py:/start.py \
  -v $(pwd)/inboard/app:/app localhost/br3ndonland/inboard/starlette

# Gunicorn and Uvicorn
docker run -d -p 80:80 localhost/br3ndonland/inboard/base
docker run -d -p 80:80 localhost/br3ndonland/inboard/fastapi
docker run -d -p 80:80 localhost/br3ndonland/inboard/starlette
```

Change the port numbers to run multiple containers simultaneously (`-p 81:80`).
