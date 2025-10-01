# syntax=docker/dockerfile:1
ARG PYTHON_VERSION=3.12 LINUX_VERSION=
FROM python:${PYTHON_VERSION}${LINUX_VERSION:+-$LINUX_VERSION} AS builder
LABEL org.opencontainers.image.authors="Brendon Smith <bws@bws.bio>"
LABEL org.opencontainers.image.description="Docker images and utilities to power your Python APIs and help you ship faster."
LABEL org.opencontainers.image.licenses="MIT"
LABEL org.opencontainers.image.source="https://github.com/br3ndonland/inboard"
LABEL org.opencontainers.image.title="inboard"
LABEL org.opencontainers.image.url="https://github.com/br3ndonland/inboard/pkgs/container/inboard"
ARG \
  HATCH_VERSION=1.14.2 \
  LINUX_VERSION \
  PIPX_VERSION=1.8.0
ENV \
  HATCH_ENV_TYPE_VIRTUAL_PATH=.venv \
  HATCH_VERSION=$HATCH_VERSION \
  LINUX_VERSION=$LINUX_VERSION \
  PATH=/opt/pipx/bin:/app/.venv/bin:$PATH \
  PIPX_BIN_DIR=/opt/pipx/bin \
  PIPX_HOME=/opt/pipx/home \
  PIPX_VERSION=$PIPX_VERSION \
  PYTHONPATH=/app
COPY --link pyproject.toml /app/
COPY --link docs/index.md /app/docs/index.md
WORKDIR /app
RUN <<HEREDOC
set -e
. /etc/os-release
if [ "$ID" = "alpine" ]; then
  apk add --no-cache --virtual .build-deps \
    gcc libc-dev libffi-dev make openssl-dev
elif [ "${LINUX_VERSION%%-*}" = "slim" ]; then
  apt-get update -qy
  apt-get install -qy --no-install-recommends \
    gcc libc-dev make wget
fi
python -m pip install --no-cache-dir --upgrade pip "pipx==$PIPX_VERSION"
pipx install "hatch==$HATCH_VERSION"
HEREDOC
COPY --link inboard /app/inboard
ENTRYPOINT ["python"]
CMD ["-m", "inboard.start"]

FROM builder AS base
ENV APP_MODULE=inboard.app.main_base:app
RUN <<HEREDOC
set -e
hatch env create base
. /etc/os-release
if [ "$ID" = "alpine" ]; then
  apk del .build-deps
elif [ "${LINUX_VERSION%%-*}" = "slim" ]; then
  apt-get purge --auto-remove -qy \
    gcc libc-dev make wget
fi
HEREDOC

FROM builder AS fastapi
ENV APP_MODULE=inboard.app.main_fastapi:app
RUN <<HEREDOC
set -e
hatch env create fastapi
. /etc/os-release
if [ "$ID" = "alpine" ]; then
  apk del .build-deps
elif [ "${LINUX_VERSION%%-*}" = "slim" ]; then
  apt-get purge --auto-remove -qy \
    gcc libc-dev make wget
fi
HEREDOC

FROM builder AS starlette
ENV APP_MODULE=inboard.app.main_starlette:app
RUN <<HEREDOC
set -e
hatch env create starlette
. /etc/os-release
if [ "$ID" = "alpine" ]; then
  apk del .build-deps
elif [ "${LINUX_VERSION%%-*}" = "slim" ]; then
  apt-get purge --auto-remove -qy \
    gcc libc-dev make wget
fi
HEREDOC
