from __future__ import annotations

import os
import shutil
from pathlib import Path
from typing import TYPE_CHECKING

import pytest
from fastapi.testclient import TestClient

from inboard import gunicorn_conf as gunicorn_conf_module
from inboard import logging_conf as logging_conf_module
from inboard.app import prestart as pre_start_module
from inboard.app.main_base import app as base_app
from inboard.app.main_fastapi import app as fastapi_app
from inboard.app.main_starlette import app as starlette_app

if TYPE_CHECKING:
    from pytest_mock import MockerFixture

    from inboard.types import DictConfig, UvicornOptions


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
) -> tuple[str, str]:
    """Set username and password for HTTP Basic auth."""
    monkeypatch.setenv("BASIC_AUTH_USERNAME", username)
    monkeypatch.setenv("BASIC_AUTH_PASSWORD", password)
    assert os.getenv("BASIC_AUTH_USERNAME") == username
    assert os.getenv("BASIC_AUTH_PASSWORD") == password
    return username, password


@pytest.fixture(scope="session")
def client_asgi() -> TestClient:
    """Instantiate test client with a plain ASGI app instance.

    Note that Uvicorn and Starlette use different types.
    The type signature expected by the Starlette/FastAPI `TestClient`
    therefore does not match `uvicorn._types.ASGIApplication`. A mypy
    `type: ignore[arg-type]` comment is used to resolve this difference.

    https://asgi.readthedocs.io/en/stable/specs/main.html#applications
    """
    return TestClient(base_app)  # type: ignore[arg-type]


@pytest.fixture(params=(fastapi_app, starlette_app), scope="session")
def client(request: pytest.FixtureRequest) -> TestClient:
    """Instantiate test client with an app instance.

    This is a parametrized fixture. When the fixture is used in a test, the test
    will be automatically parametrized, running once for each fixture parameter.
    https://docs.pytest.org/en/latest/how-to/fixtures.html
    """
    app = getattr(request, "param")
    return TestClient(app)


@pytest.fixture(
    params=(gunicorn_conf_module.__file__, "python:inboard.gunicorn_conf"),
    scope="session",
)
def gunicorn_conf_path(request: pytest.FixtureRequest) -> str:
    """Set path to default Gunicorn configuration file.

    This is a parametrized fixture. When the fixture is used in a test, the test
    will be automatically parametrized, running once for each fixture parameter.
    https://docs.pytest.org/en/latest/how-to/fixtures.html
    """
    request_param = getattr(request, "param")
    path = str(request_param)
    if "python:" not in path:
        assert Path(path).is_file()
    return path


@pytest.fixture(scope="session")
def gunicorn_conf_tmp_file_path(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """Copy gunicorn configuration file to temporary directory."""
    gunicorn_conf_tmp_path = tmp_path_factory.mktemp("gunicorn")
    tmp_file = Path(f"{gunicorn_conf_tmp_path}/gunicorn_conf.py")
    shutil.copy(Path(gunicorn_conf_module.__file__), tmp_file)
    return tmp_file


@pytest.fixture
def logging_conf_dict(mocker: MockerFixture) -> DictConfig:
    """Load logging configuration dictionary from logging configuration module."""
    dict_config: DictConfig = mocker.patch.dict(logging_conf_module.LOGGING_CONFIG)
    return dict_config


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


@pytest.fixture(
    params=(
        (
            "prestart_error.py",
            'raise RuntimeError("Testing pre-start script error behavior")\n',
        ),
        ("prestart_error.sh", "exit 1\n"),
    )
)
def pre_start_script_error(request: pytest.FixtureRequest, tmp_path: Path) -> Path:
    """Create custom temporary pre-start scripts for testing errors.

    This is a parametrized fixture. When the fixture is used in a test, the test
    will be automatically parametrized, running once for each fixture parameter.
    https://docs.pytest.org/en/latest/how-to/fixtures.html
    """
    file_name, file_content = getattr(request, "param")
    tmp_file = tmp_path / file_name
    with open(Path(tmp_file), "x") as f:
        f.write(file_content)
    return Path(tmp_file)


@pytest.fixture(scope="session")
def uvicorn_options_default() -> UvicornOptions:
    """Return default options used by `uvicorn.run()` for use in test assertions."""
    return dict(
        app="inboard.app.main_base:app",
        host="0.0.0.0",
        port=80,
        log_config=None,
        log_level="info",
        reload=False,
        reload_delay=0.25,
        reload_dirs=None,
        reload_excludes=None,
        reload_includes=None,
    )


@pytest.fixture
def uvicorn_options_custom(logging_conf_dict: DictConfig) -> UvicornOptions:
    """Return custom options used by `uvicorn.run()` for use in test assertions."""
    return dict(
        app="inboard.app.main_fastapi:app",
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
