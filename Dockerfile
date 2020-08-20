FROM python:3.8 AS base
LABEL maintainer="Brendon Smith"
COPY poetry.lock pyproject.toml /
ENV APP_MODULE=base.main:app POETRY_VIRTUALENVS_CREATE=false PYTHONPATH=/app
RUN python -m pip install poetry && poetry install --no-dev --no-interaction --no-root -E fastapi
COPY inboard/gunicorn_conf.py inboard/logging_conf.py inboard/start.py inboard/app /
CMD python /start.py

FROM base AS fastapi
ENV APP_MODULE=fastapibase.main:app

FROM base AS starlette
ENV APP_MODULE=starlettebase.main:app
