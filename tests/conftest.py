import logging
import os
from copy import deepcopy
from pathlib import Path
from typing import Any, Dict, List

import pytest  # type: ignore
from _pytest.monkeypatch import MonkeyPatch  # type: ignore
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture

from inboard import gunicorn_conf as gunicorn_conf_module
from inboard import logging_conf as logging_conf_module
from inboard.app.fastapibase.main import app as fastapi_app
from inboard.app.starlettebase.main import app as starlette_app


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
def clients() -> List[TestClient]:
    """Instantiate test client classes."""
    return [TestClient(fastapi_app), TestClient(starlette_app)]


@pytest.fixture
def gunicorn_conf_path(mocker: MockerFixture, monkeypatch: MonkeyPatch) -> Path:
    """Set path to default Gunicorn configuration file."""
    path = Path(gunicorn_conf_module.__file__)
    monkeypatch.setenv("GUNICORN_CONF", str(path))
    assert os.getenv("GUNICORN_CONF") == str(path)
    return path


@pytest.fixture
def logging_conf_dict() -> Dict[str, Any]:
    """Load logging configuration dictionary from logging configuration module."""
    return deepcopy(logging_conf_module.LOGGING_CONFIG)


@pytest.fixture
def logging_conf_path(mocker: MockerFixture, monkeypatch: MonkeyPatch) -> Path:
    """Set path to default logging configuration file."""
    path = Path(logging_conf_module.__file__)
    monkeypatch.setenv("LOGGING_CONF", str(path))
    assert os.getenv("LOGGING_CONF") == str(path)
    return path


@pytest.fixture
def mock_logger(mocker: MockerFixture) -> logging.Logger:
    """Mock the logger with pytest-mock and a pytest fixture.
    - https://github.com/pytest-dev/pytest-mock
    - https://docs.pytest.org/en/latest/fixture.html
    """
    logger = logging.getLogger()
    mocker.patch.object(logger, "debug")
    mocker.patch.object(logger, "error")
    mocker.patch.object(logger, "info")
    return logger
