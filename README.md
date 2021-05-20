# 🚢 inboard 🐳

<img src="https://raw.githubusercontent.com/br3ndonland/inboard/develop/docs/assets/images/inboard-logo.svg" alt="inboard logo" width="90%" />

_Docker images and utilities to power your Python APIs and help you ship faster._

[![PyPI](https://img.shields.io/pypi/v/inboard?color=success)](https://pypi.org/project/inboard/)
[![GitHub Container Registry](https://img.shields.io/badge/github%20container%20registry-inboard-success)](https://github.com/users/br3ndonland/packages/container/package/inboard)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://black.readthedocs.io/en/stable/)

[![builds](https://github.com/br3ndonland/inboard/workflows/builds/badge.svg)](https://github.com/br3ndonland/inboard/actions)
[![hooks](https://github.com/br3ndonland/inboard/workflows/hooks/badge.svg)](https://github.com/br3ndonland/inboard/actions)
[![tests](https://github.com/br3ndonland/inboard/workflows/tests/badge.svg)](https://github.com/br3ndonland/inboard/actions)
[![codecov](https://codecov.io/gh/br3ndonland/inboard/branch/develop/graph/badge.svg)](https://codecov.io/gh/br3ndonland/inboard)

[![Mentioned in Awesome FastAPI](https://awesome.re/mentioned-badge-flat.svg)](https://github.com/mjhea0/awesome-fastapi)

## Description

This repository provides [Docker images](https://github.com/users/br3ndonland/packages/container/package/inboard) and a [PyPI package](https://pypi.org/project/inboard/) with useful utilities for Python web servers. It runs [Uvicorn with Gunicorn](https://www.uvicorn.org/), and can be used to build applications with [Starlette](https://www.starlette.io/) and [FastAPI](https://fastapi.tiangolo.com/).

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

- Build command: `python3 -m pip install 'mkdocs-material>=7.0.0,<=8.0.0' && mkdocs build --site-dir public`
- Output directory: `public` (default)

[Vercel site configuration](https://vercel.com/docs/configuration) is specified in _[vercel.json](vercel.json)_.
