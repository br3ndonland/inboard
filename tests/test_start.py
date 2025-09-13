from __future__ import annotations

import json
import logging
import os
import subprocess
from typing import TYPE_CHECKING, final

import pytest

from inboard import start

if TYPE_CHECKING:
    from pathlib import Path

    from pytest_mock import MockerFixture

    from inboard.types import DictConfig, UvicornOptions


class TestRunPreStartScript:
    """Run pre-start scripts using the method in `start.py`.
    ---
    """

    def test_run_pre_start_script_py(
        self,
        mocker: MockerFixture,
        monkeypatch: pytest.MonkeyPatch,
        pre_start_script_tmp_py: Path,
    ) -> None:
        """Test `start.run_pre_start_script` using temporary Python pre-start script."""
        logger = mocker.patch.object(logging, "root", autospec=True)
        monkeypatch.setenv("PRE_START_PATH", str(pre_start_script_tmp_py))
        pre_start_path = os.getenv("PRE_START_PATH")
        _ = start.run_pre_start_script(logger=logger)
        logger.debug.assert_has_calls(
            calls=[
                mocker.call("Checking for pre-start script."),
                mocker.call(f"Running pre-start script with python {pre_start_path}."),
                mocker.call(f"Ran pre-start script with python {pre_start_path}."),
            ]
        )

    def test_run_pre_start_script_sh(
        self,
        mocker: MockerFixture,
        monkeypatch: pytest.MonkeyPatch,
        pre_start_script_tmp_sh: Path,
    ) -> None:
        """Test `start.run_pre_start_script` using temporary pre-start shell script."""
        logger = mocker.patch.object(logging, "root", autospec=True)
        monkeypatch.setenv("PRE_START_PATH", str(pre_start_script_tmp_sh))
        pre_start_path = os.getenv("PRE_START_PATH")
        _ = start.run_pre_start_script(logger=logger)
        logger.debug.assert_has_calls(
            calls=[
                mocker.call("Checking for pre-start script."),
                mocker.call(f"Running pre-start script with sh {pre_start_path}."),
                mocker.call(f"Ran pre-start script with sh {pre_start_path}."),
            ]
        )

    def test_run_pre_start_script_no_file(
        self,
        mocker: MockerFixture,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Test `start.run_pre_start_script` with an incorrect file path."""
        logger = mocker.patch.object(logging, "root", autospec=True)
        monkeypatch.setenv("PRE_START_PATH", "/no/file/here")
        _ = start.run_pre_start_script(logger=logger)
        logger.debug.assert_has_calls(
            calls=[
                mocker.call("Checking for pre-start script."),
                mocker.call("No pre-start script found."),
            ]
        )

    def test_run_pre_start_script_none(self, mocker: MockerFixture) -> None:
        """Test `start.run_pre_start_script` with `PRE_START_PATH` set to `None`."""
        logger = mocker.patch.object(logging, "root", autospec=True)
        _ = start.run_pre_start_script(logger=logger)
        logger.debug.assert_has_calls(
            calls=[
                mocker.call("Checking for pre-start script."),
                mocker.call("No pre-start script specified."),
            ]
        )

    def test_run_pre_start_script_error(
        self,
        mocker: MockerFixture,
        monkeypatch: pytest.MonkeyPatch,
        pre_start_script_error: Path,
    ) -> None:
        """Test `start.run_pre_start_script` with an error exit code."""
        logger = mocker.patch.object(logging, "root", autospec=True)
        monkeypatch.setenv("PRE_START_PATH", str(pre_start_script_error))
        pre_start_path = os.getenv("PRE_START_PATH")
        process = "python" if pre_start_script_error.suffix == ".py" else "sh"
        with pytest.raises(subprocess.CalledProcessError):
            _ = start.run_pre_start_script(logger=logger)
        assert logger.debug.call_count == 2
        logger.debug.assert_has_calls(
            calls=[
                mocker.call("Checking for pre-start script."),
                mocker.call(
                    f"Running pre-start script with {process} {pre_start_path}."
                ),
            ]
        )


class TestSetAppModule:
    """Set app module string using the method in `start.py`.
    ---
    """

    @pytest.mark.parametrize("module", ("base", "fastapi", "starlette"))
    def test_set_app_module(
        self, module: str, mocker: MockerFixture, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test `start.set_app_module` with default module path."""
        logger = mocker.patch.object(logging, "root", autospec=True)
        monkeypatch.setenv("APP_MODULE", f"inboard.app.main_{module}:app")
        _ = start.set_app_module(logger=logger)
        assert mocker.call(f"App module set to inboard.app.main_{module}:app.")

    @pytest.mark.parametrize("module", ("base", "fastapi", "starlette"))
    @pytest.mark.parametrize("module_variable_name", ("APP_MODULE", "UVICORN_APP"))
    def test_set_app_module_custom(
        self,
        app_module_tmp_path: Path,
        module: str,
        module_variable_name: str,
        mocker: MockerFixture,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Test `start.set_app_module` with custom module path."""
        logger = mocker.patch.object(logging, "root", autospec=True)
        monkeypatch.syspath_prepend(app_module_tmp_path)
        monkeypatch.setenv(module_variable_name, f"tmp_app.main_{module}:app")
        _ = start.set_app_module(logger=logger)
        assert mocker.call(f"App module set to tmp_app.main_{module}:app.")

    def test_set_app_module_incorrect(
        self,
        mocker: MockerFixture,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Test `start.set_app_module` with incorrect module path."""
        logger = mocker.patch.object(logging, "root", autospec=True)
        monkeypatch.setenv("APP_MODULE", "inboard.app.incorrect:app")
        logger_error_msg = "Error when setting app module"
        incorrect_module_msg = "Unable to find or import inboard.app.incorrect"
        with pytest.raises(ImportError):
            _ = start.set_app_module(logger=logger)
        assert mocker.call(f"{logger_error_msg}: ImportError {incorrect_module_msg}.")

    def test_set_app_module_when_environment_variable_not_set(
        self,
        mocker: MockerFixture,
    ) -> None:
        """Test `start.set_app_module` when the environment variable
        `APP_MODULE` is not set.
        """
        logger = mocker.patch.object(logging, "root", autospec=True)
        logger_error_msg = "Error when setting app module"
        missing_value_msg = "Please set the APP_MODULE environment variable"
        with pytest.raises(ValueError):
            _ = start.set_app_module(logger=logger)
        assert mocker.call(f"{logger_error_msg}: ImportError {missing_value_msg}.")


class TestSetGunicornOptions:
    """Test Gunicorn configuration options method.
    ---
    """

    def test_set_gunicorn_options_default(
        self, gunicorn_conf_path: str, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test default Gunicorn server options."""
        app_module = "inboard.app.main_fastapi:app"
        monkeypatch.setenv("APP_MODULE", app_module)
        monkeypatch.setenv("GUNICORN_CONF", gunicorn_conf_path)
        result = start.set_gunicorn_options(app_module)
        assert "gunicorn_conf" in gunicorn_conf_path
        assert "logging" not in gunicorn_conf_path
        assert isinstance(result, list)
        assert result == [
            "gunicorn",
            "-k",
            "inboard.gunicorn_workers.UvicornWorker",
            "-c",
            gunicorn_conf_path,
            app_module,
        ]

    def test_set_gunicorn_options_custom(
        self,
        gunicorn_conf_tmp_file_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Test custom Gunicorn server options with temporary configuration file."""
        app_module = "inboard.app.main_starlette:app"
        monkeypatch.setenv("APP_MODULE", app_module)
        monkeypatch.setenv("GUNICORN_CONF", str(gunicorn_conf_tmp_file_path))
        result = start.set_gunicorn_options(app_module)
        assert "/gunicorn_conf.py" in str(gunicorn_conf_tmp_file_path)
        assert "logging" not in str(gunicorn_conf_tmp_file_path)
        assert isinstance(result, list)
        assert result == [
            "gunicorn",
            "-k",
            "inboard.gunicorn_workers.UvicornWorker",
            "-c",
            str(gunicorn_conf_tmp_file_path),
            app_module,
        ]

    def test_set_incorrect_conf_path(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Set path to non-existent file and raise an error."""
        monkeypatch.setenv("GUNICORN_CONF", "/no/file/here")
        with pytest.raises(FileNotFoundError):
            _ = start.set_gunicorn_options("inboard.app.main_fastapi:app")


@final
class TestSetUvicornOptions:
    """Test Uvicorn configuration options method.
    ---
    """

    uvicorn_options_custom_environment_variables = (
        ("APP_MODULE", "inboard.app.main_fastapi:app"),
        ("LOG_LEVEL", "debug"),
        ("WITH_RELOAD", "true"),
        ("RELOAD_DELAY", "0.5"),
        ("RELOAD_DIRS", "inboard, tests"),
        ("RELOAD_EXCLUDES", "*[Dd]ockerfile"),
        ("RELOAD_INCLUDES", "*.py, *.md"),
    )

    def test_set_uvicorn_options_default(
        self,
        uvicorn_options_default: UvicornOptions,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Test default Uvicorn server options."""
        monkeypatch.setenv("WITH_RELOAD", "false")
        result = start.set_uvicorn_options("inboard.app.main_base:app")
        assert result == uvicorn_options_default

    def test_set_uvicorn_options_custom(
        self,
        logging_conf_dict: DictConfig,
        uvicorn_options_custom: UvicornOptions,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Test custom Uvicorn server options."""
        for environment_variable in self.uvicorn_options_custom_environment_variables:
            key, value = environment_variable
            monkeypatch.setenv(key, value)
        result = start.set_uvicorn_options(
            "inboard.app.main_fastapi:app", log_config=logging_conf_dict
        )
        assert result == uvicorn_options_custom

    def test_set_uvicorn_options_default_from_json(
        self,
        uvicorn_options_default: UvicornOptions,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Assert that the correct Uvicorn server options are set, in the correct order,
        when the `UVICORN_CONFIG_OPTIONS` environment variable is also set.
        """
        uvicorn_options_json = (
            '{"app": "inboard.app.main_base:app", "host": "0.0.0.0", "port": 80, '
            '"log_config": null, "log_level": "info", "reload": false}'
        )
        monkeypatch.setenv("UVICORN_CONFIG_OPTIONS", uvicorn_options_json)
        monkeypatch.setenv("WITH_RELOAD", "true")
        result = start.set_uvicorn_options("inboard.app.main_fastapi:app")
        assert result == uvicorn_options_default

    def test_set_uvicorn_options_custom_from_json(
        self,
        uvicorn_options_custom: UvicornOptions,
        mocker: MockerFixture,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Assert that the correct Uvicorn server options are set, in the correct order,
        when the `UVICORN_CONFIG_OPTIONS` environment variable is also set.

        The `LOGGING_CONFIG` dictionary can't be encoded as a JSON string when it has
        a class definition (the filter class), so the "filters" dict has to be removed.
        """
        log_config = uvicorn_options_custom.get("log_config")
        assert log_config is not None
        filters = log_config.get("filters")
        assert filters is not None
        mocker.patch.dict(filters, clear=True)
        uvicorn_options_json = json.dumps(uvicorn_options_custom)
        monkeypatch.setenv("UVICORN_CONFIG_OPTIONS", uvicorn_options_json)
        monkeypatch.setenv("WITH_RELOAD", "false")
        result = start.set_uvicorn_options("inboard.app.main_base:app")
        assert result == uvicorn_options_custom


class TestStartServer:
    """Start Uvicorn and Gunicorn servers using the method in `start.py`.
    ---
    """

    @pytest.mark.parametrize(
        "app_module",
        (
            "inboard.app.main_base:app",
            "inboard.app.main_fastapi:app",
            "inboard.app.main_starlette:app",
        ),
    )
    @pytest.mark.timeout(2)
    def test_start_server_uvicorn(
        self,
        app_module: str,
        logging_conf_dict: DictConfig,
        mocker: MockerFixture,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Test `start.start_server` with Uvicorn."""
        logger = mocker.patch.object(logging, "root", autospec=True)
        run = mocker.patch("inboard.start.uvicorn.run", autospec=True)
        monkeypatch.setenv("PROCESS_MANAGER", "uvicorn")
        start.start_server(
            str(os.getenv("PROCESS_MANAGER")),
            app_module=app_module,
            logger=logger,
            logging_conf_dict=logging_conf_dict,
        )
        logger.debug.assert_called_once_with("Running Uvicorn without Gunicorn.")
        run.assert_called_once_with(
            app_module,
            host="0.0.0.0",
            port=80,
            log_config=logging_conf_dict,
            log_level="info",
            reload=False,
            reload_delay=0.25,
            reload_dirs=None,
            reload_excludes=None,
            reload_includes=None,
        )

    @pytest.mark.parametrize(
        "app_module",
        (
            "inboard.app.main_base:app",
            "inboard.app.main_fastapi:app",
            "inboard.app.main_starlette:app",
        ),
    )
    @pytest.mark.parametrize(
        "reload_dirs", ("inboard", "inboard,tests", " inboard, tests ")
    )
    @pytest.mark.timeout(2)
    def test_start_server_uvicorn_reload_dirs(
        self,
        app_module: str,
        logging_conf_dict: DictConfig,
        mocker: MockerFixture,
        monkeypatch: pytest.MonkeyPatch,
        reload_dirs: str,
    ) -> None:
        """Test `start.start_server` with Uvicorn."""
        logger = mocker.patch.object(logging, "root", autospec=True)
        monkeypatch.setenv("PROCESS_MANAGER", "uvicorn")
        monkeypatch.setenv("WITH_RELOAD", "true")
        monkeypatch.setenv("RELOAD_DELAY", "0.5")
        monkeypatch.setenv("RELOAD_DIRS", reload_dirs)
        split_dirs = [d.strip() for d in str(os.getenv("RELOAD_DIRS")).split(sep=",")]
        if reload_dirs == "inboard":
            assert split_dirs == [reload_dirs]
        else:
            assert split_dirs == ["inboard", "tests"]
        run = mocker.patch("inboard.start.uvicorn.run", autospec=True)
        start.start_server(
            str(os.getenv("PROCESS_MANAGER")),
            app_module=app_module,
            logger=logger,
            logging_conf_dict=logging_conf_dict,
        )
        logger.debug.assert_called_once_with("Running Uvicorn without Gunicorn.")
        run.assert_called_once_with(
            app_module,
            host="0.0.0.0",
            port=80,
            log_config=logging_conf_dict,
            log_level="info",
            reload=True,
            reload_delay=0.5,
            reload_dirs=split_dirs,
            reload_includes=None,
            reload_excludes=None,
        )

    @pytest.mark.parametrize(
        "app_module",
        (
            "inboard.app.main_base:app",
            "inboard.app.main_fastapi:app",
            "inboard.app.main_starlette:app",
        ),
    )
    @pytest.mark.timeout(2)
    def test_start_server_uvicorn_gunicorn(
        self,
        app_module: str,
        gunicorn_conf_path: str,
        logging_conf_dict: DictConfig,
        mocker: MockerFixture,
        monkeypatch: pytest.MonkeyPatch,
        tmp_path: Path,
    ) -> None:
        """Test `start.start_server` with Uvicorn managed by Gunicorn."""
        logger = mocker.patch.object(logging, "root", autospec=True)
        run = mocker.patch("subprocess.run", autospec=True)
        monkeypatch.setenv(
            "GUNICORN_CMD_ARGS",
            f"--worker-tmp-dir {tmp_path}",
        )
        monkeypatch.setenv("GUNICORN_CONF", gunicorn_conf_path)
        monkeypatch.setenv("PROCESS_MANAGER", "gunicorn")
        start.start_server(
            str(os.getenv("PROCESS_MANAGER")),
            app_module=app_module,
            logger=logger,
            logging_conf_dict=logging_conf_dict,
        )
        logger.debug.assert_called_once_with("Running Uvicorn with Gunicorn.")
        run.assert_called_once_with(
            [
                "gunicorn",
                "-k",
                "inboard.gunicorn_workers.UvicornWorker",
                "-c",
                gunicorn_conf_path,
                app_module,
            ]
        )

    @pytest.mark.parametrize(
        "app_module",
        (
            "inboard.app.main_base:app",
            "inboard.app.main_fastapi:app",
            "inboard.app.main_starlette:app",
        ),
    )
    @pytest.mark.timeout(2)
    def test_start_server_uvicorn_gunicorn_custom_config(
        self,
        app_module: str,
        gunicorn_conf_tmp_file_path: Path,
        logging_conf_dict: DictConfig,
        mocker: MockerFixture,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Test customized `start.start_server` with Uvicorn managed by Gunicorn."""
        logger = mocker.patch.object(logging, "root", autospec=True)
        monkeypatch.setenv(
            "GUNICORN_CMD_ARGS",
            f"--worker-tmp-dir {gunicorn_conf_tmp_file_path.parent}",
        )
        monkeypatch.setenv("GUNICORN_CONF", str(gunicorn_conf_tmp_file_path))
        monkeypatch.setenv("LOG_FORMAT", "gunicorn")
        monkeypatch.setenv("LOG_LEVEL", "debug")
        monkeypatch.setenv("PROCESS_MANAGER", "gunicorn")
        run = mocker.patch("subprocess.run", autospec=True)
        start.start_server(
            str(os.getenv("PROCESS_MANAGER")),
            app_module=app_module,
            logger=logger,
            logging_conf_dict=logging_conf_dict,
        )
        assert gunicorn_conf_tmp_file_path.is_file()
        logger.debug.assert_called_with("Running Uvicorn with Gunicorn.")
        run.assert_called_with(
            [
                "gunicorn",
                "-k",
                "inboard.gunicorn_workers.UvicornWorker",
                "-c",
                str(gunicorn_conf_tmp_file_path),
                app_module,
            ]
        )

    @pytest.mark.parametrize(
        "app_module",
        (
            "inboard.app.main_base:app",
            "inboard.app.main_fastapi:app",
            "inboard.app.main_starlette:app",
        ),
    )
    @pytest.mark.timeout(2)
    def test_start_server_uvicorn_incorrect_process_manager(
        self,
        app_module: str,
        gunicorn_conf_path: str,
        logging_conf_dict: DictConfig,
        mocker: MockerFixture,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Test `start.start_server` with Uvicorn and an incorrect process manager."""
        logger = mocker.patch.object(logging, "root", autospec=True)
        logger_error_msg = "Error when starting server"
        process_error_msg = "Process manager needs to be either uvicorn or gunicorn"
        monkeypatch.setenv("GUNICORN_CONF", gunicorn_conf_path)
        with pytest.raises(NameError) as e:
            start.start_server(
                "incorrect",
                app_module=app_module,
                logger=logger,
                logging_conf_dict=logging_conf_dict,
            )
        assert str(e.value) == process_error_msg
        logger.error.assert_called_once_with(
            f"{logger_error_msg}: NameError {process_error_msg}."
        )
