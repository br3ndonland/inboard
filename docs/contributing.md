# Contributing

## Summary

**PRs welcome!**

-   **Consider starting a [discussion](https://github.com/br3ndonland/inboard/discussions) to see if there's interest in what you want to do.**
-   **Submit PRs from feature branches on forks to the `develop` branch.**
-   **Ensure PRs pass all CI checks.**
-   **Maintain test coverage at 100%.**

## Git

-   _[Why use Git?](https://www.git-scm.com/about)_ Git enables creation of multiple versions of a code repository called branches, with the ability to track and undo changes in detail.
-   Install Git by [downloading](https://www.git-scm.com/downloads) from the website, or with a package manager like [Homebrew](https://brew.sh/).
-   [Configure Git to connect to GitHub with SSH](https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/connecting-to-github-with-ssh).
-   [Fork](https://docs.github.com/en/free-pro-team@latest/github/getting-started-with-github/fork-a-repo) this repo.
-   Create a [branch](https://www.git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell) in your fork.
-   Commit your changes with a [properly-formatted Git commit message](https://chris.beams.io/posts/git-commit/).
-   Create a [pull request (PR)](https://docs.github.com/en/free-pro-team@latest/github/collaborating-with-issues-and-pull-requests/about-pull-requests) to incorporate your changes into the upstream project you forked.

## Code style

-   **Python code is formatted with [Black](https://black.readthedocs.io/en/stable/)**. Configuration for Black is stored in _[pyproject.toml](https://github.com/br3ndonland/inboard/blob/develop/pyproject.toml)_.
-   **Python imports are organized automatically with [isort](https://pycqa.github.io/isort/)**.
    -   The isort package organizes imports in three sections:
        1. Standard library
        2. Dependencies
        3. Project
    -   Within each of those groups, `import` statements occur first, then `from` statements, in alphabetical order.
    -   You can run isort from the command line with `poetry run isort .`.
    -   Configuration for isort is stored in _[pyproject.toml](https://github.com/br3ndonland/inboard/blob/develop/pyproject.toml)_.
-   Other web code (JSON, Markdown, YAML) is formatted with [Prettier](https://prettier.io/).
-   Code style is enforced with [pre-commit](https://pre-commit.com/), which runs [Git hooks](https://www.git-scm.com/book/en/v2/Customizing-Git-Git-Hooks).

    -   Configuration is stored in _[.pre-commit-config.yaml](https://github.com/br3ndonland/inboard/blob/develop/.pre-commit-config.yaml)_.
    -   Pre-commit can run locally before each commit (hence "pre-commit"), or on different Git events like `pre-push`.
    -   Pre-commit is installed in the Poetry environment. To use:

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

    -   Pre-commit is also useful as a CI tool. The [hooks](https://github.com/br3ndonland/inboard/blob/develop/.github/workflows/hooks.yml) GitHub Actions workflow runs pre-commit hooks with [GitHub Actions](https://github.com/features/actions).

## Python

### Poetry

This project uses [Poetry](https://python-poetry.org/) for dependency management.

**Install project with all dependencies: `poetry install -E all`**.

#### Highlights

-   **Automatic virtual environment management**: Poetry automatically manages the `virtualenv` for the application.
-   **Automatic dependency management**: rather than having to run `pip freeze > requirements.txt`, Poetry automatically manages the dependency file (called _pyproject.toml_), and enables SemVer-level control over dependencies like [npm](https://semver.npmjs.com/). Poetry also manages a lockfile (called _poetry.lock_), which is similar to _package-lock.json_ for npm. Poetry uses this lockfile to automatically track specific versions and hashes for every dependency.
-   **Dependency resolution**: Poetry will automatically resolve any dependency version conflicts. pip did not have dependency resolution [until the end of 2020](https://pip.pypa.io/en/latest/user_guide/#changes-to-the-pip-dependency-resolver-in-20-3-2020).
-   **Dependency separation**: Poetry can maintain separate lists of dependencies for development and production in the _pyproject.toml_. Production installs can skip development dependencies to speed up Docker builds.
-   **Builds**: Poetry has features for easily building the project into a Python package.

#### Installation

The recommended installation method is through the [Poetry custom installer](https://python-poetry.org/docs/#installation), which vendorizes dependencies into an isolated environment, and allows you to update Poetry with `poetry self update`:

You can also install Poetry however you prefer to install your user Python packages (`pipx install poetry`, `pip install --user poetry`, etc). Use the standard update methods with these tools (`pipx upgrade poetry`, `pip install --user --upgrade poetry`, etc).

#### Key commands

```sh
# Basic usage: https://python-poetry.org/docs/basic-usage/
poetry install  # create virtual environment and install dependencies
poetry show --tree  # list installed packages
poetry add PACKAGE@VERSION # add package production dependencies
poetry add PACKAGE@VERSION --dev # add package to development dependencies
poetry update  # update dependencies (not available with standard tools)
poetry version  # list or update version of this package
poetry shell  # activate the virtual environment, like source venv/bin/activate
poetry run COMMAND  # run a command within the virtual environment
poetry env info  # https://python-poetry.org/docs/managing-environments/
poetry config virtualenvs.in-project true  # install virtualenvs into .venv
poetry export -f requirements.txt > requirements.txt --dev  # export deps
```

### Running the development server

The easiest way to get started is to run the development server locally with the [VSCode debugger](https://code.visualstudio.com/docs/python/debugging). The debugger config is stored in _[launch.json](https://github.com/br3ndonland/inboard/blob/HEAD/.vscode/launch.json)_. After installing the Poetry environment as described above, start the debugger. Uvicorn enables hot-reloading and addition of debug breakpoints while the server is running. The Microsoft VSCode Python extension also offers a FastAPI debugger configuration, [added in version 2020.12.0](https://github.com/microsoft/vscode-python/blob/main/CHANGELOG.md#2020120-14-december-2020), which has been customized and included in _launch.json_. To use it, simply select the FastAPI config and start the debugger.

As explained in the [VSCode docs](https://code.visualstudio.com/docs/containers/python-user-rights), if developing on Linux, note that non-root users may not be able to expose ports less than 1024.

### Testing with pytest

-   Tests are in the _tests/_ directory.
-   Run tests by [invoking `pytest` from the command-line](https://docs.pytest.org/en/latest/how-to/usage.html) within the Poetry environment in the root directory of the repo.
-   [pytest](https://docs.pytest.org/en/latest/) features used include:
    -   [capturing `stdout` with `capfd`](https://docs.pytest.org/en/latest/how-to/capture-stdout-stderr.html)
    -   [fixtures](https://docs.pytest.org/en/latest/how-to/fixtures.html)
    -   [monkeypatch](https://docs.pytest.org/en/latest/how-to/monkeypatch.html)
    -   [parametrize](https://docs.pytest.org/en/latest/how-to/parametrize.html)
    -   [temporary directories and files (`tmp_path` and `tmp_dir`)](https://docs.pytest.org/en/latest/how-to/tmpdir.html)
-   [pytest plugins](https://docs.pytest.org/en/latest/how-to/plugins.html) include:
    -   [pytest-mock](https://github.com/pytest-dev/pytest-mock)
-   [pytest configuration](https://docs.pytest.org/en/latest/reference/customize.html) is in _[pyproject.toml](https://github.com/br3ndonland/inboard/blob/develop/pyproject.toml)_.
-   [FastAPI testing](https://fastapi.tiangolo.com/tutorial/testing/) and [Starlette testing](https://www.starlette.io/testclient/) rely on the [Starlette `TestClient`](https://www.starlette.io/testclient/).
-   Test coverage reports are generated by [coverage.py](https://github.com/nedbat/coveragepy). To generate test coverage reports, first run tests with `coverage run`, then generate a report with `coverage report`. To see interactive HTML coverage reports, run `coverage html` instead of `coverage report`.

## Docker

### Docker basics

-   **[Docker](https://www.docker.com/)** is a technology for running lightweight virtual machines called **containers**.
    -   An **image** is the executable set of files read by Docker.
    -   A **container** is a running image.
    -   The **[Dockerfile](https://docs.docker.com/engine/reference/builder/)** tells Docker how to build the container.
-   To [get started with Docker](https://www.docker.com/get-started):
    -   Ubuntu Linux: follow the [instructions for Ubuntu Linux](https://docs.docker.com/install/linux/docker-ce/ubuntu/), making sure to follow the [postinstallation steps](https://docs.docker.com/install/linux/linux-postinstall/) to activate the Docker daemon.
    -   macOS and Windows: install [Docker Desktop](https://www.docker.com/products/docker-desktop) (available [via Homebrew](https://formulae.brew.sh/cask/docker) with `brew install --cask docker`).

<details><summary>Expand this details element for more <a href="https://docs.docker.com/engine/reference/commandline/cli/">useful Docker commands</a>.</summary>

```sh
# Log in with Docker Hub credentials to pull images
docker login
# List images
docker images
# List running containers: can also use `docker container ls`
docker ps
# View logs for the most recently started container
docker logs -f $(docker ps -q -n 1)
# View logs for all running containers
docker logs -f $(docker ps -aq)
# Inspect a container (web in this example) and return the IP Address
docker inspect web | grep IPAddress
# Stop a container
docker stop # container hash
# Stop all running containers
docker stop $(docker ps -aq)
# Remove a downloaded image
docker image rm # image hash or name
# Remove a container
docker container rm # container hash
# Prune images
docker image prune
# Prune stopped containers (completely wipes them and resets their state)
docker container prune
# Prune everything
docker system prune
# Open a shell in the most recently started container (like SSH)
docker exec -it $(docker ps -q -n 1) /bin/bash
# Or, connect as root:
docker exec -u 0 -it $(docker ps -q -n 1) /bin/bash
# Copy file to/from container:
docker cp [container_name]:/path/to/file destination.file
```

</details>

### Building development images

Note that Docker builds use BuildKit. See the [BuildKit docs](https://github.com/moby/buildkit/blob/HEAD/frontend/dockerfile/docs/syntax.md) and [Docker docs](https://docs.docker.com/develop/develop-images/build_enhancements/).

To build the Docker images for each stage:

```sh
git clone git@github.com:br3ndonland/inboard.git

cd inboard

export DOCKER_BUILDKIT=1

docker build . --rm --target base -t localhost/br3ndonland/inboard:base && \
docker build . --rm --target fastapi -t localhost/br3ndonland/inboard:fastapi && \
docker build . --rm --target starlette -t localhost/br3ndonland/inboard:starlette
```

### Running development containers

```sh
# Run Docker container with Uvicorn and reloading
cd inboard

docker run -d -p 80:80 \
  -e "BASIC_AUTH_USERNAME=test_user" \
  -e "BASIC_AUTH_PASSWORD=r4ndom_bUt_memorable" \
  -e "LOG_LEVEL=debug" \
  -e "PROCESS_MANAGER=uvicorn" \
  -e "WITH_RELOAD=true" \
  -v $(pwd)/inboard:/app/inboard localhost/br3ndonland/inboard:base

docker run -d -p 80:80 \
  -e "BASIC_AUTH_USERNAME=test_user" \
  -e "BASIC_AUTH_PASSWORD=r4ndom_bUt_memorable" \
  -e "LOG_LEVEL=debug" \
  -e "PROCESS_MANAGER=uvicorn" \
  -e "WITH_RELOAD=true" \
  -v $(pwd)/inboard:/app/inboard localhost/br3ndonland/inboard:fastapi

docker run -d -p 80:80 \
  -e "BASIC_AUTH_USERNAME=test_user" \
  -e "BASIC_AUTH_PASSWORD=r4ndom_bUt_memorable" \
  -e "LOG_LEVEL=debug" \
  -e "PROCESS_MANAGER=uvicorn" \
  -e "WITH_RELOAD=true" \
  -v $(pwd)/inboard:/app/inboard localhost/br3ndonland/inboard:starlette

# Run Docker container with Gunicorn and Uvicorn
docker run -d -p 80:80 \
  -e "BASIC_AUTH_USERNAME=test_user" \
  -e "BASIC_AUTH_PASSWORD=r4ndom_bUt_memorable" \
  localhost/br3ndonland/inboard:base
docker run -d -p 80:80 \
  -e "BASIC_AUTH_USERNAME=test_user" \
  -e "BASIC_AUTH_PASSWORD=r4ndom_bUt_memorable" \
  localhost/br3ndonland/inboard:fastapi
docker run -d -p 80:80 \
  -e "BASIC_AUTH_USERNAME=test_user" \
  -e "BASIC_AUTH_PASSWORD=r4ndom_bUt_memorable" \
  localhost/br3ndonland/inboard:starlette

# Test HTTP Basic auth when running the FastAPI or Starlette images:
http :80/status -a test_user:r4ndom_bUt_memorable
```

Change the port numbers to run multiple containers simultaneously (`-p 81:80`).

## GitHub Actions workflows

[GitHub Actions](https://github.com/features/actions) is a continuous integration/continuous deployment (CI/CD) service that runs on GitHub repos. It replaces other services like Travis CI. Actions are grouped into workflows and stored in _.github/workflows_. See [Getting the Gist of GitHub Actions](https://gist.github.com/br3ndonland/f9c753eb27381f97336aa21b8d932be6) for more info.

## Maintainers

-   **The default branch is `develop`.**
-   **PRs should be merged into `develop`.** Head branches are deleted automatically after PRs are merged.
-   **The only merges to `main` should be fast-forward merges from `develop`.**
-   **Branch protection is enabled on `develop` and `main`.**
    -   `develop`:
        -   Require signed commits
        -   Include administrators
        -   Allow force pushes
    -   `main`:
        -   Require signed commits
        -   Include administrators
        -   Do not allow force pushes
        -   Require status checks to pass before merging (commits must have previously been pushed to `develop` and passed all checks)
-   **To create a release:**
    -   Bump the version number in `pyproject.toml` with `poetry version` and commit the changes to `develop`.
    -   Push to `develop` and verify all CI checks pass.
    -   Fast-forward merge to `main`, push, and verify all CI checks pass.
    -   Create an [annotated and signed Git tag](https://www.git-scm.com/book/en/v2/Git-Basics-Tagging)
        -   Follow [SemVer](https://semver.org/) guidelines when choosing a version number.
        -   List PRs and commits in the tag message:
            ```sh
            git log --pretty=format:"- %s (%h)" \
              "$(git describe --abbrev=0 --tags)"..HEAD
            ```
        -   Omit the leading `v` (use `1.0.0` instead of `v1.0.0`)
        -   Example: `git tag -a -s 1.0.0`
    -   Push the tag. GitHub Actions will build and push the Python package and Docker images.
