import logging
from typing import List

import pytest  # type: ignore
from fastapi.testclient import TestClient
from pytest_mock import mocker  # type: ignore

# from inboard.app.base.main import App as base_app
from inboard.app.fastapibase.main import app as fastapi_app
from inboard.app.starlettebase.main import app as starlette_app


@pytest.fixture
def clients() -> List[TestClient]:
    return [TestClient(fastapi_app), TestClient(starlette_app)]


@pytest.fixture
def mock_logger(mocker: mocker) -> logging.Logger:
    """Mock the logger with pytest-mock and a pytest fixture
    ---
    - https://github.com/pytest-dev/pytest-mock
    - https://docs.pytest.org/en/latest/fixture.html
    """
    logger = logging.getLogger("pytest")
    mocker.patch.object(logger, "debug")
    mocker.patch.object(logger, "error")
    mocker.patch.object(logger, "info")
    return logger
