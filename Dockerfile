FROM python:3.9 AS base
LABEL org.opencontainers.image.authors="Brendon Smith <br3ndonland@protonmail.com>"
LABEL org.opencontainers.image.description="Docker images to power your Python APIs and help you ship faster."
LABEL org.opencontainers.image.licenses="MIT"
LABEL org.opencontainers.image.source="https://github.com/br3ndonland/inboard"
LABEL org.opencontainers.image.title="inboard"
LABEL org.opencontainers.image.url="https://github.com/users/br3ndonland/packages/container/package/inboard"
ENV APP_MODULE=inboard.app.base.main:app POETRY_HOME=/opt/poetry POETRY_VIRTUALENVS_CREATE=false PYTHONPATH=/app
COPY poetry.lock pyproject.toml /app/
WORKDIR /app/
RUN curl -fsS -o get-poetry.py https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py && \
  python get-poetry.py -y && . $POETRY_HOME/env && \
  poetry install --no-dev --no-interaction --no-root -E fastapi
COPY inboard /app/inboard
CMD python /app/inboard/start.py

FROM base AS fastapi
ENV APP_MODULE=inboard.app.fastapibase.main:app

FROM base AS starlette
ENV APP_MODULE=inboard.app.starlettebase.main:app
