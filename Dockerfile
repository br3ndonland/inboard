FROM python:3.8 AS base
LABEL maintainer="Brendon Smith"
ENV APP_MODULE=inboard.app.base.main:app POETRY_VIRTUALENVS_CREATE=false PYTHONPATH=/app
COPY poetry.lock pyproject.toml /app/
WORKDIR /app/
RUN python -m pip install poetry && poetry install --no-dev --no-interaction --no-root -E fastapi
COPY inboard /app/inboard
CMD python /app/inboard/start.py

FROM base AS fastapi
ENV APP_MODULE=inboard.app.fastapibase.main:app

FROM base AS starlette
ENV APP_MODULE=inboard.app.starlettebase.main:app
