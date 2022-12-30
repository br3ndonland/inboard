# 🚢 inboard 🐳

<img src="https://raw.githubusercontent.com/br3ndonland/inboard/develop/docs/assets/images/inboard-logo.svg" alt="inboard logo" width="90%" />

_Docker images and utilities to power your Python APIs and help you ship faster._

[![PyPI](https://img.shields.io/pypi/v/inboard?color=success)](https://pypi.org/project/inboard/)
[![GitHub Container Registry](https://img.shields.io/badge/github%20container%20registry-inboard-success)](https://github.com/br3ndonland/inboard/pkgs/container/inboard)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://black.readthedocs.io/en/stable/)
[![coverage](https://img.shields.io/badge/coverage-100%25-brightgreen?logo=pytest&logoColor=white)](https://coverage.readthedocs.io/en/latest/)
[![builds](https://github.com/br3ndonland/inboard/workflows/builds/badge.svg)](https://github.com/br3ndonland/inboard/actions)

[![Mentioned in Awesome FastAPI](https://awesome.re/mentioned-badge-flat.svg)](https://github.com/mjhea0/awesome-fastapi)

## Description

This repository provides [Docker images](https://github.com/br3ndonland/inboard/pkgs/container/inboard) and a [PyPI package](https://pypi.org/project/inboard/) with useful utilities for Python web servers. It runs [Uvicorn with Gunicorn](https://www.uvicorn.org/), and can be used to build applications with [Starlette](https://www.starlette.io/) and [FastAPI](https://fastapi.tiangolo.com/).

## Justification

_Why use this project?_ You might want to try out inboard because it:

- **Offers a Python package and Docker images that work together**. Python packages and Docker images don't automatically share the same versioning systems, but inboard can help with this. You might install the Python package with a minor version constraint. You can also pull the corresponding Docker image by specifying the minor version in the Docker tag (`FROM ghcr.io/br3ndonland/inboard:<version>`).
- **Tests everything**. inboard performs unit testing of 100% of the Python code, and also runs smoke tests of the Docker images each time they are built.
- **Sets sane defaults, but allows configuration**. Configure a variety of settings with environment variables. Or run it as-is and it just works.
- **Configures logging extensibly**. inboard simplifies logging by handling all its Python log streams with a single logging config. It also offers the ability to filter health check endpoints out of the access logs. Don't like it? No problem. You can easily extend or override the logging behavior.

## Quickstart

[Get started with Docker](https://www.docker.com/get-started), pull and run an image, and try an API endpoint.

```sh
docker pull ghcr.io/br3ndonland/inboard
docker run -d -p 80:80 ghcr.io/br3ndonland/inboard
http :80  # HTTPie: https://httpie.io/
```

## Documentation

Documentation is built with [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/), deployed on [Vercel](https://vercel.com/), and available at [inboard.bws.bio](https://inboard.bws.bio) and [inboard.vercel.app](https://inboard.vercel.app).

[Vercel build configuration](https://vercel.com/docs/build-step):

- Build command: `python3 -m pip install 'mkdocs-material>=8,<9' && mkdocs build --site-dir public`
- Output directory: `public` (default)

[Vercel site configuration](https://vercel.com/docs/configuration) is specified in _vercel.json_.
