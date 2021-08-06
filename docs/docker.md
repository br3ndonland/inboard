# Docker images

## Pull images

Docker images are stored in [GitHub Container Registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry) (GHCR), which is a Docker registry like Docker Hub. Public Docker images can be pulled anonymously from `ghcr.io`. The inboard images are based on the [official Python Docker images](https://hub.docker.com/_/python).

Simply running `docker pull ghcr.io/br3ndonland/inboard` will pull the latest FastAPI image (Docker uses the `latest` tag by default). If specific versions of inboard or Python are desired, append the version numbers to the specified Docker tags as shown below _(new in inboard version 0.6.0)_. All the available images are also provided with [Alpine Linux](https://alpinelinux.org/) builds, which are available by appending `-alpine` _(new in inboard version 0.11.0)_.

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
