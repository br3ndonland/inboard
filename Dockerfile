ARG PYTHON_VERSION=3.9 LINUX_VERSION=
FROM python:${PYTHON_VERSION}${LINUX_VERSION:+-$LINUX_VERSION} AS base
LABEL org.opencontainers.image.authors="Brendon Smith <bws@bws.bio>"
LABEL org.opencontainers.image.description="Docker images and utilities to power your Python APIs and help you ship faster."
LABEL org.opencontainers.image.licenses="MIT"
LABEL org.opencontainers.image.source="https://github.com/br3ndonland/inboard"
LABEL org.opencontainers.image.title="inboard"
LABEL org.opencontainers.image.url="https://github.com/br3ndonland/inboard/pkgs/container/inboard"
ARG LINUX_VERSION PIPX_VERSION=0.16.4 POETRY_VERSION=1.1.11
ENV APP_MODULE=inboard.app.main_base:app LINUX_VERSION=$LINUX_VERSION PATH=/opt/pipx/bin:/app/.venv/bin:$PATH PIPX_BIN_DIR=/opt/pipx/bin PIPX_HOME=/opt/pipx/home PIPX_VERSION=$PIPX_VERSION POETRY_VERSION=$POETRY_VERSION PYTHONPATH=/app
COPY poetry.lock poetry.toml pyproject.toml /app/
WORKDIR /app
RUN sh -c 'if [ "$LINUX_VERSION" = "slim" ]; then apt-get update -qy && apt-get install -qy --no-install-recommends gcc libc-dev make wget; fi' && \
  sh -c '. /etc/os-release; if [ "$ID" = "alpine" ]; then apk add --no-cache --virtual .build-deps gcc libc-dev libffi-dev make openssl-dev; fi' && \
  python -m pip install --no-cache-dir --upgrade pip "pipx==$PIPX_VERSION" && pipx install "poetry==$POETRY_VERSION" && poetry install --no-dev --no-interaction --no-root && \
  sh -c 'if [ "$LINUX_VERSION" = "slim" ]; then apt-get purge --auto-remove -qy gcc libc-dev make wget; fi' && \
  sh -c '. /etc/os-release; if [ "$ID" = "alpine" ]; then apk del .build-deps; fi'
COPY inboard /app/inboard
ENTRYPOINT ["python"]
CMD ["-m", "inboard.start"]

FROM base AS fastapi
ENV APP_MODULE=inboard.app.main_fastapi:app
RUN poetry install --no-dev --no-interaction --no-root -E fastapi

FROM base AS starlette
ENV APP_MODULE=inboard.app.main_starlette:app
RUN poetry install --no-dev --no-interaction --no-root -E starlette
