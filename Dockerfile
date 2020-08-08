FROM python:3.8 AS base
LABEL maintainer="Brendon Smith"
COPY poetry.lock pyproject.toml inboard /app/
WORKDIR /app/
RUN python -m pip install poetry && poetry config virtualenvs.create false && poetry install --no-dev --no-interaction --no-root -E fastapi

FROM base as fastapi

FROM base as starlette
