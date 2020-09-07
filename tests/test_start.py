import logging
import os
from pathlib import Path
from typing import Any, Dict

import pytest
from _pytest.monkeypatch import MonkeyPatch
from pytest_mock import MockerFixture

from inboard import start


class TestConfPaths:
    """Test paths to configuration files.
    ---
    """

    def test_set_default_conf_path_gunicorn(self, gunicorn_conf_path: Path) -> None:
        """Test default Gunicorn configuration file path (different without Docker)."""
        assert "inboard/gunicorn_conf.py" in str(gunicorn_conf_path)
        assert "logging" not in str(gunicorn_conf_path)
        assert start.set_conf_path("gunicorn") == str(gunicorn_conf_path)

    def test_set_custom_conf_path_gunicorn(
        self, gunicorn_conf_path_tmp: Path, monkeypatch: MonkeyPatch, tmp_path: Path
    ) -> None:
        """Set path to custom temporary Gunicorn configuration file."""
        monkeypatch.setenv("GUNICORN_CONF", str(gunicorn_conf_path_tmp))
        assert os.getenv("GUNICORN_CONF") == str(gunicorn_conf_path_tmp)
        assert f"{tmp_path}/gunicorn_conf.py" in str(gunicorn_conf_path_tmp)
        assert "logging" not in str(gunicorn_conf_path_tmp)
        assert start.set_conf_path("gunicorn") == str(gunicorn_conf_path_tmp)

    def test_set_incorrect_conf_path(self, monkeypatch: MonkeyPatch) -> None:
        """Set path to non-existent file and raise an error."""
        with pytest.raises(FileNotFoundError):
            monkeypatch.setenv("GUNICORN_CONF", "/no/file/here")
            start.set_conf_path("gunicorn")


class TestConfigureLogging:
    """Test logging configuration methods.
    ---
    """

    def test_configure_logging_file(
        self, logging_conf_file_path: Path, mock_logger: logging.Logger
    ) -> None:
        """Test `start.configure_logging` with correct logging config file path."""
        start.configure_logging(
            logger=mock_logger, logging_conf=str(logging_conf_file_path)
        )
        mock_logger.debug.assert_called_once_with(  # type: ignore[attr-defined]
            f"Logging dict config loaded from {logging_conf_file_path}."
        )

    def test_configure_logging_module(
        self, logging_conf_module_path: str, mock_logger: logging.Logger
    ) -> None:
        """Test `start.configure_logging` with correct logging config module path."""
        start.configure_logging(
            logger=mock_logger, logging_conf=logging_conf_module_path
        )
        mock_logger.debug.assert_called_once_with(  # type: ignore[attr-defined]
            f"Logging dict config loaded from {logging_conf_module_path}."
        )

    def test_configure_logging_tmp_file(
        self, logging_conf_tmp_file_path: Path, mock_logger: logging.Logger
    ) -> None:
        """Test `start.configure_logging` with correct logging config file path."""
        start.configure_logging(
            logger=mock_logger, logging_conf=f"{logging_conf_tmp_file_path}/tmp_log.py"
        )
        mock_logger.debug.assert_called_once_with(  # type: ignore[attr-defined]
            f"Logging dict config loaded from {logging_conf_tmp_file_path}/tmp_log.py."
        )

    def test_configure_logging_tmp_file_incorrect_extension(
        self,
        logging_conf_tmp_path_incorrect_extension: Path,
        mock_logger: logging.Logger,
    ) -> None:
        """Test `start.configure_logging` with incorrect temporary file type."""
        with pytest.raises(ImportError):
            start.configure_logging(
                logger=mock_logger,
                logging_conf=str(logging_conf_tmp_path_incorrect_extension),
            )
            import_error_msg = (
                f"Unable to import {logging_conf_tmp_path_incorrect_extension}."
            )
            logger_error_msg = "Error when configuring logging:"
            mock_logger.debug.assert_called_once_with(  # type: ignore[attr-defined]
                f"{logger_error_msg} {import_error_msg}."
            )

    def test_configure_logging_tmp_module(
        self,
        logging_conf_tmp_file_path: Path,
        mock_logger: logging.Logger,
        monkeypatch: MonkeyPatch,
    ) -> None:
        """Test `start.configure_logging` with temporary logging config path."""
        monkeypatch.syspath_prepend(logging_conf_tmp_file_path)
        monkeypatch.setenv("LOGGING_CONF", "tmp_log")
        assert os.getenv("LOGGING_CONF") == "tmp_log"
        start.configure_logging(logger=mock_logger, logging_conf="tmp_log")
        mock_logger.debug.assert_called_once_with(  # type: ignore[attr-defined]
            "Logging dict config loaded from tmp_log."
        )

    def test_configure_logging_tmp_module_incorrect_type(
        self,
        logging_conf_tmp_path_incorrect_type: Path,
        mock_logger: logging.Logger,
        monkeypatch: MonkeyPatch,
    ) -> None:
        """Test `start.configure_logging` with temporary logging config path.
        - Correct module name
        - `LOGGING_CONFIG` object with incorrect type
        """
        monkeypatch.syspath_prepend(logging_conf_tmp_path_incorrect_type)
        monkeypatch.setenv("LOGGING_CONF", "incorrect_type")
        assert os.getenv("LOGGING_CONF") == "incorrect_type"
        with pytest.raises(TypeError):
            start.configure_logging(logger=mock_logger, logging_conf="incorrect_type")
            logger_error_msg = "Error when configuring logging:"
            type_error_msg = "LOGGING_CONFIG is not a dictionary instance."
            mock_logger.debug.assert_called_once_with(  # type: ignore[attr-defined]
                f"{logger_error_msg} {type_error_msg}."
            )

    def test_configure_logging_tmp_module_no_dict(
        self,
        logging_conf_tmp_path_no_dict: Path,
        mock_logger: logging.Logger,
        monkeypatch: MonkeyPatch,
    ) -> None:
        """Test `start.configure_logging` with temporary logging config path.
        - Correct module name
        - No `LOGGING_CONFIG` object
        """
        monkeypatch.syspath_prepend(logging_conf_tmp_path_no_dict)
        monkeypatch.setenv("LOGGING_CONF", "no_dict")
        assert os.getenv("LOGGING_CONF") == "no_dict"
        with pytest.raises(AttributeError):
            start.configure_logging(logger=mock_logger, logging_conf="no_dict")
            logger_error_msg = "Error when configuring logging:"
            attribute_error_msg = "No LOGGING_CONFIG in no_dict."
            mock_logger.debug.assert_called_once_with(  # type: ignore[attr-defined]
                f"{logger_error_msg} {attribute_error_msg}."
            )


class TestSetAppModule:
    """Set app module string using the method in `start.py`.
    ---
    """

    def test_set_app_module_asgi(
        self, mock_logger: logging.Logger, monkeypatch: MonkeyPatch
    ) -> None:
        """Test `start.set_app_module` using module path to base ASGI app."""
        monkeypatch.setenv("APP_MODULE", "inboard.app.base.main:app")
        start.set_app_module(logger=mock_logger)
        mock_logger.debug.assert_called_once_with(  # type: ignore[attr-defined]
            "App module set to inboard.app.base.main:app."
        )

    def test_set_app_module_fastapi(
        self, mock_logger: logging.Logger, monkeypatch: MonkeyPatch
    ) -> None:
        """Test `start.set_app_module` using module path to FastAPI app."""
        monkeypatch.setenv("APP_MODULE", "inboard.app.fastapibase.main:app")
        start.set_app_module(logger=mock_logger)
        mock_logger.debug.assert_called_once_with(  # type: ignore[attr-defined]
            "App module set to inboard.app.fastapibase.main:app."
        )

    def test_set_app_module_starlette(
        self, mock_logger: logging.Logger, monkeypatch: MonkeyPatch
    ) -> None:
        """Test `start.set_app_module` using module path to Starlette app."""
        monkeypatch.setenv("APP_MODULE", "inboard.app.starlettebase.main:app")
        start.set_app_module(logger=mock_logger)
        mock_logger.debug.assert_called_once_with(  # type: ignore[attr-defined]
            "App module set to inboard.app.starlettebase.main:app."
        )

    def test_set_app_module_custom_asgi(
        self,
        app_module_tmp_path: Path,
        mock_logger: logging.Logger,
        monkeypatch: MonkeyPatch,
    ) -> None:
        """Test `start.set_app_module` with custom module path to base ASGI app."""
        monkeypatch.syspath_prepend(app_module_tmp_path)
        monkeypatch.setenv("APP_MODULE", "tmp_app.base.main:app")
        start.set_app_module(logger=mock_logger)
        mock_logger.debug.assert_called_once_with(  # type: ignore[attr-defined]
            "App module set to tmp_app.base.main:app."
        )

    def test_set_app_module_custom_fastapi(
        self,
        app_module_tmp_path: Path,
        mock_logger: logging.Logger,
        monkeypatch: MonkeyPatch,
    ) -> None:
        """Test `start.set_app_module` with custom module path to FastAPI app."""
        monkeypatch.syspath_prepend(app_module_tmp_path)
        monkeypatch.setenv("APP_MODULE", "tmp_app.fastapibase.main:app")
        start.set_app_module(logger=mock_logger)
        mock_logger.debug.assert_called_once_with(  # type: ignore[attr-defined]
            "App module set to tmp_app.fastapibase.main:app."
        )

    def test_set_app_module_custom_starlette(
        self,
        app_module_tmp_path: Path,
        mock_logger: logging.Logger,
        monkeypatch: MonkeyPatch,
    ) -> None:
        """Test `start.set_app_module` with custom module path to Starlette app."""
        monkeypatch.syspath_prepend(app_module_tmp_path)
        monkeypatch.setenv("APP_MODULE", "tmp_app.starlettebase.main:app")
        start.set_app_module(logger=mock_logger)
        mock_logger.debug.assert_called_once_with(  # type: ignore[attr-defined]
            "App module set to tmp_app.starlettebase.main:app."
        )

    def test_set_app_module_incorrect(
        self,
        mocker: MockerFixture,
        mock_logger: logging.Logger,
        monkeypatch: MonkeyPatch,
    ) -> None:
        """Test `start.set_app_module` with incorrect module path."""
        with pytest.raises(ModuleNotFoundError):
            incorrect_module = "inboard.app.incorrect.main:app"
            monkeypatch.setenv("APP_MODULE", incorrect_module)
            logger_error_msg = "Error when setting app module:"
            incorrect_module_msg = f"No module named {incorrect_module}"
            start.set_app_module(logger=mock_logger)
            mock_logger.debug.assert_called_once_with(  # type: ignore[attr-defined]
                f"{logger_error_msg} {incorrect_module_msg}."
            )


class TestRunPreStartScript:
    """Run pre-start scripts using the method in `start.py`.
    ---
    """

    def test_run_pre_start_script_py(
        self,
        mock_logger: logging.Logger,
        mocker: MockerFixture,
        monkeypatch: MonkeyPatch,
        pre_start_script_tmp_py: Path,
    ) -> None:
        """Test `start.run_pre_start_script` using temporary Python pre-start script."""
        monkeypatch.setenv("PRE_START_PATH", str(pre_start_script_tmp_py))
        start.run_pre_start_script(logger=mock_logger)
        mock_logger.debug.assert_has_calls(  # type: ignore[attr-defined]
            calls=[
                mocker.call("Checking for pre-start script."),
                mocker.call(
                    f"Running pre-start script with python {os.getenv('PRE_START_PATH')}."  # noqa: E501
                ),
                mocker.call(
                    f"Ran pre-start script with python {os.getenv('PRE_START_PATH')}."
                ),
            ]
        )

    def test_run_pre_start_script_sh(
        self,
        mock_logger: logging.Logger,
        mocker: MockerFixture,
        monkeypatch: MonkeyPatch,
        pre_start_script_tmp_sh: Path,
    ) -> None:
        """Test `start.run_pre_start_script` using temporary pre-start shell script."""
        monkeypatch.setenv("PRE_START_PATH", str(pre_start_script_tmp_sh))
        start.run_pre_start_script(logger=mock_logger)
        mock_logger.debug.assert_has_calls(  # type: ignore[attr-defined]
            calls=[
                mocker.call("Checking for pre-start script."),
                mocker.call(
                    f"Running pre-start script with sh {os.getenv('PRE_START_PATH')}."
                ),
                mocker.call(
                    f"Ran pre-start script with sh {os.getenv('PRE_START_PATH')}."
                ),
            ]
        )

    def test_run_pre_start_script_no_file(
        self,
        mock_logger: logging.Logger,
        mocker: MockerFixture,
        monkeypatch: MonkeyPatch,
    ) -> None:
        """Test `start.run_pre_start_script` with an incorrect file path."""
        monkeypatch.setenv("PRE_START_PATH", "/no/file/here")
        start.run_pre_start_script(logger=mock_logger)
        mock_logger.debug.assert_has_calls(  # type: ignore[attr-defined]
            calls=[
                mocker.call("Checking for pre-start script."),
                mocker.call("No pre-start script found."),
            ]
        )


class TestStartServer:
    """Start Uvicorn and Gunicorn servers using the method in `start.py`.
    ---
    """

    @pytest.mark.parametrize(
        "app_module",
        [
            "inboard.app.base.main:app",
            "inboard.app.fastapibase.main:app",
            "inboard.app.starlettebase.main:app",
        ],
    )
    def test_start_server_uvicorn(
        self,
        app_module: str,
        logging_conf_dict: Dict[str, Any],
        mock_logger: logging.Logger,
        mocker: MockerFixture,
        monkeypatch: MonkeyPatch,
    ) -> None:
        """Test `start.start_server` with Uvicorn."""
        monkeypatch.setenv("LOG_FORMAT", "uvicorn")
        monkeypatch.setenv("LOG_LEVEL", "debug")
        monkeypatch.setenv("PROCESS_MANAGER", "uvicorn")
        assert os.getenv("LOG_FORMAT") == "uvicorn"
        assert os.getenv("LOG_LEVEL") == "debug"
        assert os.getenv("PROCESS_MANAGER") == "uvicorn"
        mocker.patch("uvicorn.run", autospec=True)
        start.start_server(
            str(os.getenv("PROCESS_MANAGER")),
            app_module=app_module,
            logger=mock_logger,
            logging_conf_dict=logging_conf_dict,
        )
        mock_logger.debug.assert_called_once_with("Running Uvicorn without Gunicorn.")  # type: ignore[attr-defined]  # noqa: E501

    @pytest.mark.parametrize(
        "app_module",
        [
            "inboard.app.base.main:app",
            "inboard.app.fastapibase.main:app",
            "inboard.app.starlettebase.main:app",
        ],
    )
    def test_start_server_uvicorn_gunicorn(
        self,
        app_module: str,
        gunicorn_conf_path: Path,
        logging_conf_dict: Dict[str, Any],
        mock_logger: logging.Logger,
        mocker: MockerFixture,
        monkeypatch: MonkeyPatch,
    ) -> None:
        """Test `start.start_server` with Uvicorn managed by Gunicorn."""
        assert os.getenv("GUNICORN_CONF", str(gunicorn_conf_path))
        monkeypatch.setenv("LOG_FORMAT", "gunicorn")
        monkeypatch.setenv("LOG_LEVEL", "debug")
        monkeypatch.setenv("PROCESS_MANAGER", "gunicorn")
        assert os.getenv("LOG_FORMAT") == "gunicorn"
        assert os.getenv("LOG_LEVEL") == "debug"
        assert os.getenv("PROCESS_MANAGER") == "gunicorn"
        start.start_server(
            str(os.getenv("PROCESS_MANAGER")),
            app_module=app_module,
            logger=mock_logger,
            logging_conf_dict=logging_conf_dict,
        )
        mock_logger.debug.assert_called_once_with("Running Uvicorn with Gunicorn.")  # type: ignore[attr-defined]  # noqa: E501

    def test_start_server_uvicorn_incorrect_module(
        self,
        logging_conf_dict: Dict[str, Any],
        mock_logger: logging.Logger,
        mocker: MockerFixture,
        monkeypatch: MonkeyPatch,
    ) -> None:
        """Test `start.start_server` with Uvicorn and an incorrect module path."""
        with pytest.raises(ModuleNotFoundError):
            monkeypatch.setenv("LOG_LEVEL", "debug")
            monkeypatch.setenv("WITH_RELOAD", "false")
            start.start_server(
                "uvicorn",
                app_module="incorrect.base.main:app",
                logger=mock_logger,
                logging_conf_dict=logging_conf_dict,
            )
            logger_error_msg = "Error when starting server with start script:"
            module_error_msg = "No module named incorrect.base.main:app"
            mock_logger.debug.assert_has_calls(  # type: ignore[attr-defined]
                calls=[
                    mocker.call("Running Uvicorn without Gunicorn."),
                    mocker.call(f"{logger_error_msg} {module_error_msg}"),
                ]
            )

    @pytest.mark.parametrize(
        "app_module",
        [
            "inboard.app.base.main:app",
            "inboard.app.fastapibase.main:app",
            "inboard.app.starlettebase.main:app",
        ],
    )
    def test_start_server_uvicorn_incorrect_process_manager(
        self,
        app_module: str,
        gunicorn_conf_path: Path,
        logging_conf_dict: Dict[str, Any],
        mock_logger: logging.Logger,
        mocker: MockerFixture,
        monkeypatch: MonkeyPatch,
    ) -> None:
        """Test `start.start_server` with Uvicorn and an incorrect process manager."""
        with pytest.raises(NameError):
            monkeypatch.setenv("LOG_LEVEL", "debug")
            monkeypatch.setenv("WITH_RELOAD", "false")
            start.start_server(
                "incorrect",
                app_module=app_module,
                logger=mock_logger,
                logging_conf_dict=logging_conf_dict,
            )
            logger_error_msg = "Error when starting server with start script:"
            process_error_msg = (
                "Process manager needs to be either uvicorn or gunicorn."
            )
            mock_logger.debug.assert_called_once_with(  # type: ignore[attr-defined]
                f"{logger_error_msg} {process_error_msg}"
            )
