FROM python:3.8 AS base
LABEL maintainer="Brendon Smith"
COPY poetry.lock pyproject.toml inboard /
ENV APP_MODULE=base.main:app GUNICORN_CONF=/gunicorn_conf.py POETRY_VIRTUALENVS_CREATE=false PYTHONPATH=/app
RUN python -m pip install poetry && poetry install --no-dev --no-interaction --no-root -E fastapi
CMD python /start.py

FROM base AS fastapi
ENV APP_MODULE=fastapi.main:app

FROM base AS starlette
ENV APP_MODULE=starlette.main:app
