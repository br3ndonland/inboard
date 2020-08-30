import logging
import os
import shutil
from pathlib import Path
from typing import Any, Dict, List

import pytest  # type: ignore
from _pytest.monkeypatch import MonkeyPatch  # type: ignore
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture

from inboard import gunicorn_conf as gunicorn_conf_module
from inboard import logging_conf as logging_conf_module
from inboard.app import prestart as pre_start_module
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
def gunicorn_conf_path(monkeypatch: MonkeyPatch) -> Path:
    """Set path to default Gunicorn configuration file."""
    path = Path(gunicorn_conf_module.__file__)
    monkeypatch.setenv("GUNICORN_CONF", str(path))
    assert os.getenv("GUNICORN_CONF") == str(path)
    return path


@pytest.fixture
def gunicorn_conf_path_tmp(tmp_path: Path) -> Path:
    """Copy gunicorn configuration file to custom temporary file."""
    tmp_file = shutil.copy(Path(gunicorn_conf_module.__file__), tmp_path)
    return Path(tmp_file)


@pytest.fixture
def logging_conf_dict(mocker: MockerFixture) -> Dict[str, Any]:
    """Load logging configuration dictionary from logging configuration module."""
    return mocker.patch.dict(logging_conf_module.LOGGING_CONFIG)


@pytest.fixture
def logging_conf_path(monkeypatch: MonkeyPatch) -> Path:
    """Set path to default logging configuration file."""
    path = Path(logging_conf_module.__file__)
    monkeypatch.setenv("LOGGING_CONF", str(path))
    assert os.getenv("LOGGING_CONF") == str(path)
    return path


@pytest.fixture
def logging_conf_path_tmp(tmp_path: Path) -> Path:
    """Copy logging configuration file to custom temporary file."""
    tmp_file = shutil.copy(Path(logging_conf_module.__file__), tmp_path)
    return Path(tmp_file)


@pytest.fixture
def logging_conf_path_tmp_txt(tmp_path: Path) -> Path:
    """Create custom temporary logging config file with incorrect extension."""
    tmp_file = tmp_path / "tmp_logging_conf.txt"
    return Path(tmp_file)


@pytest.fixture
def logging_conf_path_tmp_no_dict(tmp_path: Path) -> Path:
    """Create custom temporary logging config file.
    - Correct extension
    - No `LOGGING_CONFIG` object
    """
    tmp_file = tmp_path / "tmp_logging_conf.py"
    with open(Path(tmp_file), "x") as f:
        f.write("print('Hello, World!')\n")
    return Path(tmp_file)


@pytest.fixture
def logging_conf_path_tmp_incorrect_type(tmp_path: Path) -> Path:
    """Create custom temporary logging config file.
    - Correct extension
    - Incorrect data type for `LOGGING_CONFIG` object
    """
    tmp_file = tmp_path / "tmp_logging_conf_incorrect_type.py"
    with open(Path(tmp_file), "x") as f:
        f.write("LOGGING_CONFIG: list = ['Hello', 'World']\n")
    return Path(tmp_file)


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


@pytest.fixture
def pre_start_script_tmp_py(tmp_path: Path) -> Path:
    """Copy pre-start script to custom temporary file."""
    tmp_file = shutil.copy(Path(pre_start_module.__file__), tmp_path)
    return Path(tmp_file)


@pytest.fixture
def pre_start_script_tmp_sh(tmp_path: Path) -> Path:
    """Create custom temporary pre-start shell script."""
    tmp_file = tmp_path / "prestart.sh"
    with open(Path(tmp_file), "x") as f:
        f.write('echo "Hello World, from a temporary pre-start shell script"\n')
    return Path(tmp_file)
