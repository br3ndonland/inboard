# inboard

_Docker images to power your Python APIs and help you ship faster. With support for Uvicorn, Gunicorn, Starlette, and FastAPI._

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
![hooks](https://github.com/br3ndonland/inboard/workflows/hooks/badge.svg)
![tests](https://github.com/br3ndonland/inboard/workflows/tests/badge.svg)

Brendon Smith ([br3ndonland](https://github.com/br3ndonland/))

## Description

This is a refactor of [tiangolo/uvicorn-gunicorn-docker](https://github.com/tiangolo/uvicorn-gunicorn-docker) with the following advantages:

- **One repo**. The tiangolo/uvicorn-gunicorn images are in at least three separate repos, [tiangolo/uvicorn-gunicorn-docker](https://github.com/tiangolo/uvicorn-gunicorn-docker), [tiangolo/uvicorn-gunicorn-starlette-docker](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker), and [tiangolo/uvicorn-gunicorn-starlette-docker](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker), with large amounts of code duplication, making maintenance difficult for an already-busy maintainer. This repo combines three into one.
- **One _Dockerfile_.** This repository leverages [multi-stage builds](https://docs.docker.com/develop/develop-images/multistage-build/) to produce multiple Docker images from one _Dockerfile_.
- **One Python requirements file.** This project leverages Poetry with Poetry Extras for dependency management with the _pyproject.toml_.
- **One platform.** Docker Hub is superfluous. You're already on GitHub. Why not [pull Docker images from GitHub Packages](https://docs.github.com/en/packages/using-github-packages-with-your-projects-ecosystem/configuring-docker-for-use-with-github-packages)?

## Quickstart

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

```dockerfile
FROM docker.pkg.github.com/br3ndonland/inboard/fastapi
```

### Run containers

Run container:

```sh
docker run -d -p 80:80 br3ndonland/inboard/fastapi
```
