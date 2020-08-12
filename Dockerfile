FROM python:3.8 AS base
LABEL maintainer="Brendon Smith"
COPY poetry.lock pyproject.toml inboard /app/
WORKDIR /app/
ENV APP_MODULE=inboard.base.main:app GUNICORN_CONF=/app/inboard/gunicorn_conf.py POETRY_VIRTUALENVS_CREATE=false
RUN python -m pip install poetry && poetry install --no-dev --no-interaction -E fastapi

FROM base as fastapi
ENV APP_MODULE=inboard.fastapi.main:app POETRY_VIRTUALENVS_CREATE=false

FROM base as starlette
ENV APP_MODULE=inboard.starlette.main:app POETRY_VIRTUALENVS_CREATE=false
