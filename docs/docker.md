# Docker images

## Pull images

Docker images are stored in [GitHub Container Registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry) (GHCR), which is a Docker registry like Docker Hub. Public Docker images can be pulled anonymously from `ghcr.io`. The inboard images are based on the [official Python Docker images](https://hub.docker.com/_/python).

Simply running `docker pull ghcr.io/br3ndonland/inboard` will pull the latest FastAPI image (Docker uses the `latest` tag by default). If specific versions of inboard or Python are desired, specify the version number at the beginning of the Docker tag as shown below _(new in inboard version 0.6.0)_. All the available images are also provided with [Alpine Linux](https://alpinelinux.org/) builds, which are available by appending `-alpine`, and Debian "slim" builds, which are available by appending `-slim` _(new in inboard version 0.11.0)_. Alpine and Debian slim users should be aware of their [limitations](#linux-distributions).

Please see [inboard Git tags](https://github.com/br3ndonland/inboard/tags), [inboard PyPI release history](https://pypi.org/project/inboard/#history), and [inboard Docker images on GHCR](https://github.com/br3ndonland/inboard/pkgs/container/inboard) for the latest version numbers and available Docker tags.

!!! example "Example Docker tags"

    ```{ .sh .no-copy }
    # Pull latest FastAPI image (Docker automatically appends the `latest` tag)
    docker pull ghcr.io/br3ndonland/inboard

    # Pull latest version of each image
    docker pull ghcr.io/br3ndonland/inboard:base
    docker pull ghcr.io/br3ndonland/inboard:fastapi
    docker pull ghcr.io/br3ndonland/inboard:starlette

    # Pull image from specific release
    docker pull ghcr.io/br3ndonland/inboard:0.38.0-fastapi

    # Pull image from latest minor version release (new in inboard 0.22.0)
    docker pull ghcr.io/br3ndonland/inboard:0.38-fastapi

    # Pull image with specific Python version
    docker pull ghcr.io/br3ndonland/inboard:fastapi-python3.11

    # Pull image from latest minor release and with specific Python version
    docker pull ghcr.io/br3ndonland/inboard:0.38-fastapi-python3.11

    # Append `-alpine` to image tags for Alpine Linux (new in inboard 0.11.0)
    docker pull ghcr.io/br3ndonland/inboard:latest-alpine
    docker pull ghcr.io/br3ndonland/inboard:0.38-fastapi-alpine

    # Append `-slim` to any of the above for Debian slim (new in inboard 0.11.0)
    docker pull ghcr.io/br3ndonland/inboard:latest-slim
    docker pull ghcr.io/br3ndonland/inboard:0.38-fastapi-slim
    ```

## Use images in a _Dockerfile_

For a [Hatch](https://hatch.pypa.io/latest/) project with the following directory structure:

-   `repo/`
    -   `package_name/`
        -   `__init__.py`
        -   `main.py`
        -   `prestart.py`
    -   `tests/`
    -   `Dockerfile`
    -   `pyproject.toml`
    -   `README.md`

The _pyproject.toml_ could look like this:

!!! example "Example _pyproject.toml_ for Hatch project"

    ```toml
    [build-system]
    build-backend = "hatchling.build"
    requires = ["hatchling"]

    [project]
    authors = [{email = "you@example.com", name = "Your Name"}]
    dependencies = [
      "inboard[fastapi]",
    ]
    description = "Your project description here."
    dynamic = ["version"]
    license = "MIT"
    name = "package-name"
    readme = "README.md"
    requires-python = ">=3.8.1,<4"

    [project.optional-dependencies]
    checks = [
      "black",
      "flake8",
      "isort",
      "mypy",
    ]
    docs = [
      "mkdocs-material",
    ]
    tests = [
      "coverage[toml]",
      "httpx",
      "pytest",
      "pytest-mock",
      "pytest-timeout",
    ]

    [tool.coverage.report]
    exclude_lines = ["if TYPE_CHECKING:", "pragma: no cover"]
    fail_under = 100
    show_missing = true

    [tool.coverage.run]
    command_line = "-m pytest"
    source = ["package_name", "tests"]

    [tool.hatch.build.targets.sdist]
    include = ["/package_name"]

    [tool.hatch.build.targets.wheel]
    packages = ["package_name"]

    [tool.hatch.envs.ci]
    dev-mode = false
    features = [
      "checks",
      "tests",
    ]
    path = ".venv"

    [tool.hatch.envs.default]
    dev-mode = true
    features = [
      "checks",
      "docs",
      "tests",
    ]
    path = ".venv"

    [tool.hatch.envs.production]
    dev-mode = false
    features = []
    path = ".venv"

    [tool.hatch.version]
    path = "package_name/__init__.py"

    [tool.isort]
    profile = "black"
    src_paths = ["package_name", "tests"]

    [tool.mypy]
    files = ["**/*.py"]
    plugins = "pydantic.mypy"
    show_error_codes = true
    strict = true

    [tool.pytest.ini_options]
    addopts = "-q"
    minversion = "6.0"
    testpaths = ["tests"]

    ```

The _Dockerfile_ could look like this:

!!! example "Example _Dockerfile_ for Hatch project"

    ```dockerfile
    FROM ghcr.io/br3ndonland/inboard:fastapi

    # Set environment variables
    ENV APP_MODULE=package_name.main:app

    # Install Python requirements
    COPY pyproject.toml README.md /app/
    WORKDIR /app
    RUN hatch env prune && hatch env create production

    # Install Python app
    COPY package_name /app/package_name

    # RUN command already included in base image
    ```

!!! tip "Syncing dependencies with Hatch"

    Hatch does not have a direct command for syncing dependencies, and `hatch env create` won't always sync dependencies if they're being installed into the same virtual environment directory (as they would be in a Docker image). Running `hatch env prune && hatch env create <env_name>` should do the trick.

For a standard `pip` install:

-   `repo/`
    -   `package_name/`
        -   `__init__.py`
        -   `main.py`
        -   `prestart.py`
    -   `tests/`
    -   `Dockerfile`
    -   `requirements.txt`
    -   `README.md`

Packaging would be set up separately as described in the [Python packaging user guide](https://packaging.python.org/en/latest/).

The _requirements.txt_ could look like this:

!!! example "Example _requirements.txt_ for `pip` project"

    ```text
    inboard[fastapi]
    ```

The _Dockerfile_ could look like this:

!!! example "Example _Dockerfile_ for `pip` project"

    ```dockerfile
    FROM ghcr.io/br3ndonland/inboard:fastapi

    # Set environment variables
    ENV APP_MODULE=package_name.main:app

    # Install Python requirements
    COPY requirements.txt /app/
    WORKDIR /app
    RUN python -m pip install -r requirements.txt

    # Install Python app
    COPY package_name /app/package_name

    # RUN command already included in base image
    ```

Organizing the _Dockerfile_ this way helps [leverage the Docker build cache](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#leverage-build-cache). Files and commands that change most frequently are added last to the _Dockerfile_. Next time the image is built, Docker will skip any layers that didn't change, speeding up builds.

The image could then be built with:

```sh
cd /path/to/repo
docker build . -t imagename:latest
```

The final argument is the Docker image name (`imagename` in this example). Replace with your image name.

## Run containers

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

-   `-e "PROCESS_MANAGER=uvicorn" -e "WITH_RELOAD=true"` will instruct `start.py` to run Uvicorn with reloading and without Gunicorn. The Gunicorn configuration won't apply, but these environment variables will still work as [described](environment.md):
    -   `APP_MODULE`
    -   `HOST`
    -   `PORT`
    -   `LOG_COLORS`
    -   `LOG_FORMAT`
    -   `LOG_LEVEL`
    -   `RELOAD_DIRS`
    -   `WITH_RELOAD`
-   `-v $(pwd)/package:/app/package`: the specified directory (`/path/to/repo/package` in this example) will be [mounted as a volume](https://docs.docker.com/engine/reference/run/#volume-shared-filesystems) inside of the container at `/app/package`. When files in the working directory change, Docker and Uvicorn will sync the files to the running Docker container.

## Docker and Hatch

This project uses [Hatch](https://hatch.pypa.io/latest/) for Python dependency management and packaging, and uses [`pipx`](https://pypa.github.io/pipx/) to install Hatch in Docker:

-   `ENV PATH=/opt/pipx/bin:/app/.venv/bin:$PATH` is set first to prepare the `$PATH`.
-   `pip` is used to install `pipx`.
-   `pipx` is used to install Hatch, with `PIPX_BIN_DIR=/opt/pipx/bin` used to specify the location where `pipx` installs the Hatch command-line application, and `PIPX_HOME=/opt/pipx/home` used to specify the location for `pipx` itself.
-   `hatch env create` is used with `HATCH_ENV_TYPE_VIRTUAL_PATH=.venv` and `WORKDIR=/app` to create the virtualenv at `/app/.venv` and install the project's packages into the virtualenv.

With this approach:

-   Subsequent `python` commands use the executable at `app/.venv/bin/python`.
-   As long as `HATCH_ENV_TYPE_VIRTUAL_PATH=.venv` and `WORKDIR /app` are retained, subsequent Hatch commands use the same virtual environment at `/app/.venv`.

## Docker and Poetry

This project now uses Hatch for Python dependency management and packaging. Poetry 1.1 was used before Hatch. If you have a downstream project using the inboard Docker images with Poetry, you can add `RUN pipx install poetry` to your Dockerfile to install Poetry for your project.

As explained in [python-poetry/poetry#1879](https://github.com/python-poetry/poetry/discussions/1879#discussioncomment-346113), there were two conflicting conventions to consider when working with Poetry in Docker:

1. Docker's convention is to not use virtualenvs, because containers themselves provide sufficient isolation.
2. Poetry's convention is to always use virtualenvs, because of the reasons given in [python-poetry/poetry#3209](https://github.com/python-poetry/poetry/pull/3209#issuecomment-710678083).

This project used [`pipx`](https://pypa.github.io/pipx/) to install Poetry in Docker:

-   `ENV PATH=/opt/pipx/bin:/app/.venv/bin:$PATH` was set first to prepare the `$PATH`.
-   `pip` was used to install `pipx`.
-   `pipx` was used to install Poetry.
-   `poetry install` was used with `POETRY_VIRTUALENVS_CREATE=true`, `POETRY_VIRTUALENVS_IN_PROJECT=true` and `WORKDIR /app` to install the project's packages into the virtualenv at `/app/.venv`.

With this approach:

-   Subsequent `python` commands used the executable at `app/.venv/bin/python`.
-   As long as `POETRY_VIRTUALENVS_IN_PROJECT=true` and `WORKDIR /app` were retained, subsequent Poetry commands used the same virtual environment at `/app/.venv`.

## Linux distributions

### Alpine

The [official Python Docker image](https://hub.docker.com/_/python) is built on [Debian Linux](https://www.debian.org/) by default, with [Alpine Linux](https://alpinelinux.org/) builds also provided. Alpine is known for its security and small Docker image sizes.

!!! info "Runtime determination of the Linux distribution"

    To determine the Linux distribution at runtime, it can be helpful to source `/etc/os-release`, which contains an `ID` variable specifying the distribution (`alpine`, `debian`, etc).

Alpine differs from Debian in some important ways, including:

-   Shell (Alpine does not use Bash by default)
-   Packages (Alpine uses [`apk`](https://docs.alpinelinux.org/user-handbook/0.1a/Working/apk.html) as its package manager, and does not include some common packages like `curl` by default)
-   C standard library (Alpine uses [`musl`](https://musl.libc.org/) instead of [`gcc`](https://gcc.gnu.org/))

The different C standard library is of particular note for Python packages, because [binary package distributions](https://packaging.python.org/guides/packaging-binary-extensions/) may not be available for Alpine Linux. To work with these packages, their build dependencies must be installed, then the packages must be built from source. Users will typically then delete the build dependencies to keep the final Docker image size small.

The basic build dependencies used by inboard include `gcc`, `libc-dev`, and `make`. These may not be adequate to build all packages. For example, to [install `psycopg`](https://www.psycopg.org/docs/install.html), it may be necessary to add more build dependencies, build the package, (optionally delete the build dependencies) and then include its `libpq` runtime dependency in the final image. A set of build dependencies for this scenario might look like the following:

!!! example "Example Alpine Linux _Dockerfile_ for PostgreSQL project"

    ```dockerfile
    # syntax=docker/dockerfile:1
    ARG INBOARD_DOCKER_TAG=fastapi-alpine
    FROM ghcr.io/br3ndonland/inboard:${INBOARD_DOCKER_TAG}
    ENV APP_MODULE=mypackage.main:app
    COPY pyproject.toml README.md /app/
    WORKDIR /app
    RUN <<HEREDOC

    . /etc/os-release

    if [ "$ID" = "alpine" ]; then
      apk add --no-cache --virtual .build-project \
        build-base freetype-dev gcc libc-dev libpng-dev make openblas-dev postgresql-dev
    fi

    hatch env create production

    if [ "$ID" = "alpine" ]; then
      apk del .build-project
      apk add --no-cache libpq
    fi

    HEREDOC
    COPY mypackage /app/mypackage
    ```

!!! info "Alpine Linux virtual packages"

    Adding `--virtual .build-project` creates a "virtual package" named `.build-project` that groups the rest of the dependencies listed. All of the dependencies can then be deleted as a set by simply referencing the name of the virtual package, like `apk del .build-project`.

!!! warning "Python packages with Rust extensions on Alpine Linux"

    As described above, Python packages can have C extensions. In addition, an increasing number of packages also feature [Rust](https://www.rust-lang.org/) extensions. Building Python packages with Rust extensions will typically require installation of Rust and [Cargo](https://doc.rust-lang.org/cargo/) (`apk add --no-cache rust cargo`), as well as installation of a Python plugin like [`maturin`](https://github.com/PyO3/maturin) or [`setuptools-rust`](https://github.com/PyO3/setuptools-rust) (`python3 -m pip install --no-cache-dir setuptools-rust`). Remember to uninstall after (`python3 -m pip uninstall -y setuptools-rust`). The installed `rust` package should be retained.

    In addition to build dependencies, Rust also has runtime dependencies, which are satisfied by the `rust` package installed with `apk`. The addition of the Rust runtime dependencies bloats Docker image sizes, and may make it impractical to work with Python packages that have Rust extensions on Alpine Linux. For related discussion, see [rust-lang/rust#88221](https://github.com/rust-lang/rust/issues/88221) and [rust-lang/rustup#2213](https://github.com/rust-lang/rustup/issues/2213).

The good news - Python now supports binary package distributions built for `musl`-based Linux distributions like Alpine Linux. See [PEP 656](https://www.python.org/dev/peps/pep-0656/) and [`cibuildwheel`](https://cibuildwheel.readthedocs.io/en/stable/) for details.

### Debian slim

The [official Python Docker image](https://hub.docker.com/_/python) provides "slim" variants of the Debian base images. These images are built on Debian, but then have the build dependencies removed after Python is installed. As with Alpine Linux, there are some caveats:

-   Commonly-used packages are removed, requiring reinstallation in downstream images.
-   The overall number of security vulnerabilities will be reduced as compared to the Debian base images, but vulnerabilities inherent to Debian will still remain.
-   If `/etc/os-release` is sourced, the `$ID` will still be `debian`, so custom environment variables or other methods must be used to identify images as "slim" variants.

A _Dockerfile_ equivalent to the Alpine Linux example might look like the following:

!!! example "Example Debian Linux slim _Dockerfile_ for PostgreSQL project"

    ```dockerfile
    # syntax=docker/dockerfile:1
    ARG INBOARD_DOCKER_TAG=fastapi-slim
    FROM ghcr.io/br3ndonland/inboard:${INBOARD_DOCKER_TAG}
    ENV APP_MODULE=mypackage.main:app
    COPY pyproject.toml README.md /app/
    WORKDIR /app
    ARG INBOARD_DOCKER_TAG
    RUN <<HEREDOC

    . /etc/os-release

    if [ "$ID" = "debian" ] && echo "$INBOARD_DOCKER_TAG" | grep -q "slim"; then
      apt-get update -qy
      apt-get install -qy --no-install-recommends \
        gcc libc-dev make wget
    fi

    hatch env create production

    if [ "$ID" = "debian" ] && echo "$INBOARD_DOCKER_TAG" | grep -q "slim"; then
      apt-get purge --auto-remove -qy \
        gcc libc-dev make wget
    fi

    HEREDOC
    COPY mypackage /app/mypackage
    ```

!!! info "Redeclaring Docker build arguments"

    Why is `ARG INBOARD_DOCKER_TAG` repeated in the example above? To understand this, it is necessary to [understand how `ARG` and `FROM` interact](https://docs.docker.com/engine/reference/builder/#understand-how-arg-and-from-interact). Any `ARG`s before `FROM` are outside the Docker build context. In order to use them again inside the build context, they must be redeclared.

!!! tip "Here-documents in Dockerfiles"

    The `RUN` commands in the Dockerfiles above use a special syntax called a [here-document](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/V3_chap02.html#tag_18_07), or "heredoc". This syntax allows multiple lines of text to be passed into a shell command, enabling Dockerfile `RUN` commands to be written like shell scripts, instead of having to jam commands into long run-on lines. Heredoc support was added to Dockerfiles in the [1.4.0 release](https://github.com/moby/buildkit/releases/tag/dockerfile%2F1.4.0).

    For more info, see:

    -   [br3ndonland/inboard#54](https://github.com/br3ndonland/inboard/pull/54)
    -   [BuildKit docs: Dockerfile frontend syntaxes](https://github.com/moby/buildkit/blob/HEAD/frontend/dockerfile/docs/syntax.md)
    -   [BuildKit releases: dockerfile/1.4.0](https://github.com/moby/buildkit/releases/tag/dockerfile%2F1.4.0)
    -   [Docker blog 2021-07-30: Introduction to heredocs in Dockerfiles](https://www.docker.com/blog/introduction-to-heredocs-in-dockerfiles/)
    -   [Docker docs: Develop with Docker - Build images with BuildKit](https://docs.docker.com/develop/develop-images/build_enhancements/)
    -   [Docker docs: Dockerfile reference - BuildKit](https://docs.docker.com/engine/reference/builder/#buildkit)
