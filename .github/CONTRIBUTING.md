# Guidelines for contributing

## Table of Contents <!-- omit in toc -->

- [Summary](#summary)
  - [Contributors](#contributors)
  - [Maintainers](#maintainers)
- [Git](#git)
- [Python](#python)
  - [Python code style](#python-code-style)
  - [Poetry](#poetry)
- [Docker](#docker)
  - [Docker basics](#docker-basics)
  - [Docker builds](#docker-builds)

## Summary

### Contributors

- **Submit PRs from feature branches on forks.**
- **Ensure PRs pass all CI checks.**
- **Maintain test coverage at 100%.**

### Maintainers

- **The default branch is `develop`.**
- **PRs should be merged into `develop`.** Head branches are deleted automatically after PRs are merged.
- **The only merges to `master` should be fast-forward merges from `develop`.**
- **Branch protection is enabled on `develop` and `master`.**
  - `develop`:
    - Require signed commits
    - Include adminstrators
    - Allow force pushes
  - `master`:
    - Require signed commits
    - Include adminstrators
    - Do not allow force pushes
    - Require status checks to pass before merging (commits must have previously been pushed to `develop` and passed all checks)
- **To create a release:**
  - Bump the version number in `pyproject.toml` with `poetry version`, and manually in `test_version.py`, and commit the changes to `develop`.
  - Push to `develop` and verify all CI checks pass.
  - Fast-forward merge to `master`, push, and verify all CI checks pass.
  - Create an [annotated and signed Git tag](https://www.git-scm.com/book/en/v2/Git-Basics-Tagging)
    - Follow [SemVer](https://semver.org/) guidelines when choosing a version number.
    - List PRs and commits in the tag message:
      ```sh
      git log --pretty=format:"- %s (%h)" "$(git describe --abbrev=0 --tags)"..HEAD
      ```
    - Omit the leading `v` (use `1.0.0` instead of `v1.0.0`)
    - Example: `git tag -a -s 1.0.0`
  - Push the tag. GitHub Actions will build and push the Python package and Docker images.

## Git

- _[Why use Git?](https://www.git-scm.com/about)_ Git enables creation of multiple versions of a code repository called branches, with the ability to track and undo changes in detail.
- Install Git by [downloading](https://www.git-scm.com/downloads) from the website, or with a package manager like [Homebrew](https://brew.sh/).
- [Configure Git to connect to GitHub with SSH](https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/connecting-to-github-with-ssh)
- [Fork](https://docs.github.com/en/free-pro-team@latest/github/getting-started-with-github/fork-a-repo) this repo
- Create a [branch](https://www.git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell) in your fork.
- Commit your changes with a [properly-formatted Git commit message](https://chris.beams.io/posts/git-commit/).
- Create a [pull request (PR)](https://docs.github.com/en/free-pro-team@latest/github/collaborating-with-issues-and-pull-requests/about-pull-requests) to incorporate your changes into the upstream project you forked.

## Python

### Python code style

See _[README.md](../README.md#development)_.

### Poetry

This project uses [Poetry](https://python-poetry.org/) for dependency management.

#### Highlights

- **Automatic dependency management:** rather than having to run `pip freeze > requirements.txt`, Poetry automatically manages the dependency file (called _pyproject.toml_), and enables SemVer-level control over dependencies like [npm](https://semver.npmjs.com/) does.
- **Separation of development and production dependencies**: Poetry can maintain separate lists of dependencies for development and production in the _pyproject.toml_. Production installs can skip development dependencies to speed up Docker builds.
- **Dependency resolution:** Poetry will automatically resolve any dependency version conflicts. As explained in the [pip docs](https://pip.pypa.io/en/latest/user_guide/#requirements-files) and [pypa/pip#988](https://github.com/pypa/pip/issues/988) (open since 2013), pip does not have dependency resolution. PSF has funded an [effort](https://www.pythonpodcast.com/pip-resolver-dependency-management-episode-264/) to improve pip dependency resolution.
- **Lockfile:** similar to _package-lock.json_, Poetry will automatically track specific versions and hashes for every dependency.
- **Builds:** Poetry has features for easily building the application.

#### Installation

The recommended installation method is through the [Poetry custom installer](https://python-poetry.org/docs/#installation), which vendorizes dependencies into an isolated environment, and allows you to update Poetry with `poetry self update`:

```sh
# osx / linux / bashonwindows install instructions
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

# windows powershell install instructions
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python -
```

You can also install Poetry however you prefer to install your user Python packages (`pipx install poetry`, `pip install --user poetry`, etc). Use the standard update methods with these tools (`pipx upgrade poetry`, `pip install --user --upgrade poetry`, etc).

#### Key commands

```sh
# Basic usage: https://python-poetry.org/docs/basic-usage/
# install virtual environment, like python3 -m venv venv or virtualenv virtual
# also installs dependencies, like pip install -r requirements.txt
poetry install

# list installed packages
poetry show --tree

# add a package, like pip install package (add --dev for dev-only install)
poetry add PACKAGE

# update dependencies (not available with standard tools)
poetry update

# activate the virtual environment, like source venv/bin/activate
poetry shell

# run a command within the virtual environment
poetry run COMMAND

# manage environments: https://python-poetry.org/docs/managing-environments/
poetry env info

# configure your Poetry installation to install virtualenvs into .venv
poetry config virtualenvs.in-project true

# export dependencies to requirements.txt
poetry export -f requirements.txt > requirements.txt --dev
```

## Docker

### Docker basics

- **[Docker](https://www.docker.com/)** is a technology for running lightweight virtual machines called **containers**.
  - An **image** is the executable set of files read by Docker.
  - A **container** is a running image.
  - The **[Dockerfile](https://docs.docker.com/engine/reference/builder/)** tells Docker how to build the container.
- To install Docker tools locally:
  - Ubuntu Linux: follow the [instructions for Ubuntu Linux](https://docs.docker.com/install/linux/docker-ce/ubuntu/), making sure to follow the [postinstallation steps](https://docs.docker.com/install/linux/linux-postinstall/) to activate the Docker daemon.
  - macOS and Windows: install [Docker Desktop](https://www.docker.com/products/docker-desktop) (available via [Homebrew](https://brew.sh/) with `brew cask install docker`).
- <details><summary>Expand this details element for more <a href="https://docs.docker.com/engine/reference/commandline/cli/">useful Docker commands</a>.</summary>

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

  </summary>

### Docker builds

See _[README.md](../README.md#development)_.
