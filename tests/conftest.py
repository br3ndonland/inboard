import os
import shutil
from pathlib import Path
from typing import List

import pytest
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture

from inboard import gunicorn_conf as gunicorn_conf_module
from inboard import logging_conf as logging_conf_module
from inboard.app import prestart as pre_start_module
from inboard.app.main_base import app as base_app
from inboard.app.main_fastapi import app as fastapi_app
from inboard.app.main_starlette import app as starlette_app


@pytest.fixture(scope="session")
def app_module_tmp_path(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """Copy app modules to temporary directory to test custom app module paths."""
    tmp_dir = tmp_path_factory.mktemp("app")
    shutil.copytree(Path(pre_start_module.__file__).parent, Path(f"{tmp_dir}/tmp_app"))
    return tmp_dir


@pytest.fixture
def basic_auth(
    monkeypatch: pytest.MonkeyPatch,
    username: str = "test_user",
    password: str = "r4ndom_bUt_memorable",
) -> tuple:
    """Set username and password for HTTP Basic auth."""
    monkeypatch.setenv("BASIC_AUTH_USERNAME", username)
    monkeypatch.setenv("BASIC_AUTH_PASSWORD", password)
    assert os.getenv("BASIC_AUTH_USERNAME") == username
    assert os.getenv("BASIC_AUTH_PASSWORD") == password
    return username, password


@pytest.fixture(scope="session")
def client_asgi() -> TestClient:
    """Instantiate test client classes."""
    return TestClient(base_app)


@pytest.fixture(scope="session")
def clients() -> List[TestClient]:
    """Instantiate test client classes."""
    return [TestClient(fastapi_app), TestClient(starlette_app)]


@pytest.fixture
def gunicorn_conf_path(monkeypatch: pytest.MonkeyPatch) -> Path:
    """Set path to default Gunicorn configuration file."""
    path = Path(gunicorn_conf_module.__file__)
    monkeypatch.setenv("GUNICORN_CONF", str(path))
    assert os.getenv("GUNICORN_CONF") == str(path)
    return path


@pytest.fixture(scope="session")
def gunicorn_conf_tmp_path(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """Create temporary directory for Gunicorn configuration file."""
    return tmp_path_factory.mktemp("gunicorn")


@pytest.fixture
def gunicorn_conf_tmp_file_path(
    gunicorn_conf_tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path_factory: pytest.TempPathFactory,
) -> Path:
    """Copy gunicorn configuration file to temporary directory."""
    tmp_file = Path(f"{gunicorn_conf_tmp_path}/gunicorn_conf.py")
    shutil.copy(Path(gunicorn_conf_module.__file__), tmp_file)
    monkeypatch.setenv("GUNICORN_CONF", str(tmp_file))
    assert os.getenv("GUNICORN_CONF", str(tmp_file))
    return tmp_file


@pytest.fixture
def logging_conf_dict(mocker: MockerFixture) -> dict:
    """Load logging configuration dictionary from logging configuration module."""
    return mocker.patch.dict(logging_conf_module.LOGGING_CONFIG)


@pytest.fixture
def logging_conf_file_path(monkeypatch: pytest.MonkeyPatch) -> Path:
    """Set path to default logging configuration file."""
    path = Path(logging_conf_module.__file__)
    monkeypatch.setenv("LOGGING_CONF", str(path))
    assert os.getenv("LOGGING_CONF") == str(path)
    return path


@pytest.fixture
def logging_conf_module_path(monkeypatch: pytest.MonkeyPatch) -> str:
    """Set module path to logging_conf.py."""
    path = "inboard.logging_conf"
    monkeypatch.setenv("LOGGING_CONF", path)
    assert os.getenv("LOGGING_CONF") == path
    return path


@pytest.fixture(scope="session")
def logging_conf_tmp_file_path(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """Copy logging configuration module to custom temporary location."""
    tmp_dir = tmp_path_factory.mktemp("tmp_log")
    shutil.copy(Path(logging_conf_module.__file__), Path(f"{tmp_dir}/tmp_log.py"))
    return tmp_dir


@pytest.fixture(scope="session")
def logging_conf_tmp_path_no_dict(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """Create temporary logging config file without logging config dict."""
    tmp_dir = tmp_path_factory.mktemp("tmp_log_no_dict")
    tmp_file = tmp_dir / "no_dict.py"
    with open(Path(tmp_file), "x") as f:
        f.write("print('Hello, World!')\n")
    return tmp_dir


@pytest.fixture(scope="session")
def logging_conf_tmp_path_incorrect_extension(
    tmp_path_factory: pytest.TempPathFactory,
) -> Path:
    """Create custom temporary logging config file with incorrect extension."""
    tmp_dir = tmp_path_factory.mktemp("tmp_log_incorrect_extension")
    tmp_file = tmp_dir / "tmp_logging_conf"
    with open(Path(tmp_file), "x") as f:
        f.write("This file doesn't have the correct extension.\n")
    return tmp_dir


@pytest.fixture(scope="session")
def logging_conf_tmp_path_incorrect_type(
    tmp_path_factory: pytest.TempPathFactory,
) -> Path:
    """Create temporary logging config file with incorrect LOGGING_CONFIG type."""
    tmp_dir = tmp_path_factory.mktemp("tmp_log_incorrect_type")
    tmp_file = tmp_dir / "incorrect_type.py"
    with open(Path(tmp_file), "x") as f:
        f.write("LOGGING_CONFIG: list = ['Hello', 'World']\n")
    return tmp_dir


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


@pytest.fixture(scope="session")
def uvicorn_options_default() -> dict:
    """Return default options used by `uvicorn.run()` for use in test assertions."""
    return dict(
        host="0.0.0.0",
        port=80,
        log_config=None,
        log_level="info",
        reload=False,
        reload_delay=None,
        reload_dirs=None,
        reload_excludes=None,
        reload_includes=None,
    )


@pytest.fixture
def uvicorn_options_custom(logging_conf_dict: dict) -> dict:
    """Return custom options used by `uvicorn.run()` for use in test assertions."""
    return dict(
        host="0.0.0.0",
        port=80,
        log_config=logging_conf_dict,
        log_level="debug",
        reload=True,
        reload_delay=0.5,
        reload_dirs=["inboard", "tests"],
        reload_excludes=["*[Dd]ockerfile"],
        reload_includes=["*.py", "*.md"],
    )
