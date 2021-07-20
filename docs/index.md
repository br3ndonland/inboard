# 🚢 inboard 🐳

<img src="assets/images/inboard-logo.svg" alt="inboard logo" width="90%" />

_Docker images and utilities to power your Python APIs and help you ship faster._

[![PyPI](https://img.shields.io/pypi/v/inboard?color=success)](https://pypi.org/project/inboard/)
[![GitHub Container Registry](https://img.shields.io/badge/github%20container%20registry-inboard-success)](https://github.com/br3ndonland/inboard/pkgs/container/inboard)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://black.readthedocs.io/en/stable/)

[![builds](https://github.com/br3ndonland/inboard/workflows/builds/badge.svg)](https://github.com/br3ndonland/inboard/actions)
[![hooks](https://github.com/br3ndonland/inboard/workflows/hooks/badge.svg)](https://github.com/br3ndonland/inboard/actions)
[![tests](https://github.com/br3ndonland/inboard/workflows/tests/badge.svg)](https://github.com/br3ndonland/inboard/actions)
[![codecov](https://codecov.io/gh/br3ndonland/inboard/branch/develop/graph/badge.svg)](https://codecov.io/gh/br3ndonland/inboard)

[![Mentioned in Awesome FastAPI](https://awesome.re/mentioned-badge-flat.svg)](https://github.com/mjhea0/awesome-fastapi)

## Description

This project provides [Docker images](https://github.com/br3ndonland/inboard/pkgs/container/inboard) and a [PyPI package](https://pypi.org/project/inboard/) with useful utilities for Python web servers. It runs [Uvicorn with Gunicorn](https://www.uvicorn.org/), and can be used to build applications with [Starlette](https://www.starlette.io/) and [FastAPI](https://fastapi.tiangolo.com/).

## Quickstart

[Get started with Docker](https://www.docker.com/get-started), pull and run an image, and try an API endpoint.

```sh
docker pull ghcr.io/br3ndonland/inboard
docker run -d -p 80:80 ghcr.io/br3ndonland/inboard
http :80  # HTTPie: https://httpie.io/
```

## Background

**I built this project to use as a production Python web server layer.** I was working on several different software applications, and wanted a way to centrally manage the web server layer, so I didn't have to configure the server separately for each application. I also found it difficult to keep up with all the changes to the associated Python packages, including Uvicorn, Starlette, and FastAPI. I realized that I needed to abstract the web server layer into a separate project, so that when working on software applications, I could simply focus on building the applications themselves. This project is the result. It's been very helpful to me, and I hope it's helpful to you also.

This project was inspired in part by [tiangolo/uvicorn-gunicorn-docker](https://github.com/tiangolo/uvicorn-gunicorn-docker), but has the following advantages:

-   **One repo**. The tiangolo/uvicorn-gunicorn images are in at least three separate repos ([tiangolo/uvicorn-gunicorn-docker](https://github.com/tiangolo/uvicorn-gunicorn-docker), [tiangolo/uvicorn-gunicorn-fastapi-docker](https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker), and [tiangolo/uvicorn-gunicorn-starlette-docker](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker)), with large amounts of code duplication, making maintenance difficult for an [already-busy maintainer](https://github.com/encode/uvicorn/pull/705#issuecomment-660042305). This repo combines three into one.
-   **One _Dockerfile_.** This repo leverages [multi-stage builds](https://docs.docker.com/develop/develop-images/multistage-build/) to produce multiple Docker images from one _Dockerfile_.
-   **One Python requirements file.** This repo uses [Poetry](https://github.com/python-poetry/poetry) with Poetry Extras for dependency management with a single _pyproject.toml_.
-   **One logging configuration.** Logging a Uvicorn+Gunicorn+Starlette/FastAPI stack is unnecessarily complicated. Uvicorn and Gunicorn use different logging configurations, and it can be difficult to unify the log streams. In this repo, Uvicorn, Gunicorn, and FastAPI log streams are propagated to the root logger, and handled by the custom root logging config. Developers can also supply their own custom logging configurations.
-   **One programming language.** Pure Python with no shell scripts.
-   **One platform.** You're already on GitHub. Why not [pull Docker images from GitHub Container Registry](https://github.blog/2020-09-01-introducing-github-container-registry/)?

The PyPI package is useful if you want to use or extend any of the inboard Python modules, such as the logging configuration.
