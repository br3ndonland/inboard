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
