import logging
import os
from typing import List

import pytest  # type: ignore
from _pytest.monkeypatch import MonkeyPatch  # type: ignore
from fastapi.testclient import TestClient
from pytest_mock import mocker  # type: ignore

# from inboard.app.base.main import App as base_app
from inboard.app.fastapibase.main import app as fastapi_app
from inboard.app.starlettebase.main import app as starlette_app


@pytest.fixture
def clients() -> List[TestClient]:
    """Instantiate test client classes."""
    return [TestClient(fastapi_app), TestClient(starlette_app)]


@pytest.fixture
def basic_auth(
    monkeypatch: MonkeyPatch,
    username: str = "test_username",
    password: str = "test_password",
) -> tuple:
    """Set username and password for HTTP Basic Auth."""
    monkeypatch.setenv("BASIC_AUTH_USERNAME", username)
    monkeypatch.setenv("BASIC_AUTH_PASSWORD", password)
    assert os.getenv("BASIC_AUTH_USERNAME") == username
    assert os.getenv("BASIC_AUTH_PASSWORD") == password
    return username, password


@pytest.fixture
def mock_logger(mocker: mocker) -> logging.Logger:
    """Mock the logger with pytest-mock and a pytest fixture.
    - https://github.com/pytest-dev/pytest-mock
    - https://docs.pytest.org/en/latest/fixture.html
    """
    logger = logging.getLogger("pytest")
    mocker.patch.object(logger, "debug")
    mocker.patch.object(logger, "error")
    mocker.patch.object(logger, "info")
    return logger
