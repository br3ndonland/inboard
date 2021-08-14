# Docker images

## Pull images

Docker images are stored in [GitHub Container Registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry) (GHCR), which is a Docker registry like Docker Hub. Public Docker images can be pulled anonymously from `ghcr.io`. The inboard images are based on the [official Python Docker images](https://hub.docker.com/_/python).

Simply running `docker pull ghcr.io/br3ndonland/inboard` will pull the latest FastAPI image (Docker uses the `latest` tag by default). If specific versions of inboard or Python are desired, append the version numbers to the specified Docker tags as shown below _(new in inboard version 0.6.0)_. All the available images are also provided with [Alpine Linux](https://alpinelinux.org/) builds, which are available by appending `-alpine`, and Debian "slim" builds, which are available by appending `-slim` _(new in inboard version 0.11.0)_. Alpine and Debian slim users should be aware of their [limitations](#linux-distributions).

!!! info "Available Docker tags"

    ```sh
    # Pull latest FastAPI image (Docker automatically appends the `latest` tag)
    docker pull ghcr.io/br3ndonland/inboard

    # Pull latest version of each image
    docker pull ghcr.io/br3ndonland/inboard:base
    docker pull ghcr.io/br3ndonland/inboard:fastapi
    docker pull ghcr.io/br3ndonland/inboard:starlette

    # Pull image from specific release (new in inboard 0.6.0)
    docker pull ghcr.io/br3ndonland/inboard:base-0.6.0
    docker pull ghcr.io/br3ndonland/inboard:fastapi-0.6.0
    docker pull ghcr.io/br3ndonland/inboard:starlette-0.6.0

    # Pull image with specific Python version
    docker pull ghcr.io/br3ndonland/inboard:base-python3.8
    docker pull ghcr.io/br3ndonland/inboard:fastapi-python3.8
    docker pull ghcr.io/br3ndonland/inboard:starlette-python3.8

    # Pull image from specific release and with specific Python version
    docker pull ghcr.io/br3ndonland/inboard:base-0.6.0-python3.8
    docker pull ghcr.io/br3ndonland/inboard:fastapi-0.6.0-python3.8
    docker pull ghcr.io/br3ndonland/inboard:starlette-0.6.0-python3.8

    # Append `-alpine` to any of the above for Alpine Linux (new in inboard 0.11.0)
    docker pull ghcr.io/br3ndonland/inboard:latest-alpine
    docker pull ghcr.io/br3ndonland/inboard:fastapi-alpine
    docker pull ghcr.io/br3ndonland/inboard:fastapi-0.11.0-alpine
    docker pull ghcr.io/br3ndonland/inboard:fastapi-python3.8-alpine
    docker pull ghcr.io/br3ndonland/inboard:fastapi-0.11.0-python3.8-alpine

    # Append `-slim` to any of the above for Debian slim (new in inboard 0.11.0)
    docker pull ghcr.io/br3ndonland/inboard:latest-slim
    docker pull ghcr.io/br3ndonland/inboard:fastapi-slim
    docker pull ghcr.io/br3ndonland/inboard:fastapi-0.11.0-slim
    docker pull ghcr.io/br3ndonland/inboard:fastapi-python3.8-slim
    docker pull ghcr.io/br3ndonland/inboard:fastapi-0.11.0-python3.8-slim
    ```

## Use images in a _Dockerfile_

For a [Poetry](https://github.com/python-poetry/poetry) project with the following directory structure:

-   `repo/`
    -   `package/`
        -   `main.py`
        -   `prestart.py`
    -   `Dockerfile`
    -   `poetry.lock`
    -   `pyproject.toml`

The _Dockerfile_ could look like this:

<!-- prettier-ignore -->
!!!example "Example Dockerfile for Poetry project"

    ```dockerfile
    FROM ghcr.io/br3ndonland/inboard:fastapi

    # Install Python requirements
    COPY poetry.lock pyproject.toml /app/
    WORKDIR /app/
    RUN poetry install --no-dev --no-interaction --no-root

    # Install Python app
    COPY package /app/package
    ENV APP_MODULE=package.main:app
    # RUN command already included in base image
    ```

Organizing the _Dockerfile_ this way helps [leverage the Docker build cache](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#leverage-build-cache). Files and commands that change most frequently are added last to the _Dockerfile_. Next time the image is built, Docker will skip any layers that didn't change, speeding up builds.

For a standard `pip` install:

-   `repo/`
    -   `package/`
        -   `main.py`
        -   `prestart.py`
    -   `Dockerfile`
    -   `requirements.txt`

<!-- prettier-ignore -->
!!!example "Example Dockerfile for project with pip and requirements.txt"

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
    ARG INBOARD_DOCKER_TAG=fastapi-alpine
    FROM ghcr.io/br3ndonland/inboard:${INBOARD_DOCKER_TAG}
    ENV APP_MODULE=mypackage.main:app
    COPY poetry.lock pyproject.toml /app/
    WORKDIR /app/
    RUN sh -c '. /etc/os-release; if [ "$ID" = "alpine" ]; then apk add --no-cache --virtual .build-project build-base freetype-dev gcc libc-dev libpng-dev make openblas-dev postgresql-dev; fi' && \
      poetry install --no-dev --no-interaction --no-root && \
      sh -c '. /etc/os-release; if [ "$ID" = "alpine" ]; then apk del .build-project && apk add --no-cache libpq; fi'
    COPY mypackage /app/mypackage
    ```

!!! info "Alpine Linux virtual packages"

    Adding `--virtual .build-project` creates a "virtual package" named `.build-project` that groups the rest of the dependencies listed. All of the dependencies can then be deleted as a set by simply referencing the name of the virtual package, like `apk del .build-project`.

The good news - Python is planning to support binary package distributions built for Alpine Linux. See [PEP 656](https://www.python.org/dev/peps/pep-0656/) for details.

### Debian slim

The [official Python Docker image](https://hub.docker.com/_/python) provides "slim" variants of the Debian base images. These images are built on Debian, but then have the build dependencies removed after Python is installed. As with Alpine Linux, there are some caveats:

-   Commonly-used packages are removed, requiring reinstallation in downstream images.
-   The overall number of security vulnerabilities will be reduced as compared to the Debian base images, but vulnerabilities inherent to Debian will still remain.
-   If `/etc/os-release` is sourced, the `$ID` will still be `debian`, so custom environment variables or other methods must be used to identify images as "slim" variants.

A _Dockerfile_ equivalent to the Alpine Linux example might look like the following:

!!! example "Example Debian Linux slim _Dockerfile_ for PostgreSQL project"

    ```dockerfile
    ARG INBOARD_DOCKER_TAG=fastapi-slim
    FROM ghcr.io/br3ndonland/inboard:${INBOARD_DOCKER_TAG}
    ENV APP_MODULE=mypackage.main:app INBOARD_DOCKER_TAG=${INBOARD_DOCKER_TAG}
    COPY poetry.lock pyproject.toml /app/
    WORKDIR /app/
    RUN sh -c 'if [[ $INBOARD_DOCKER_TAG == *slim* ]]; then apt-get update -qy && apt-get install -qy --no-install-recommends gcc libc-dev libpq-dev make wget; fi' && \
      poetry install --no-dev --no-interaction --no-root && \
      sh -c 'if [[ $INBOARD_DOCKER_TAG == *slim* ]]; then apt-get purge --auto-remove -qy gcc libc-dev make wget; fi'
    COPY mypackage /app/mypackage
    ```
