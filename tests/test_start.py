import importlib.util
import logging
import os
from pathlib import Path
from typing import Any, Dict

import pytest  # type: ignore
from _pytest.monkeypatch import MonkeyPatch  # type: ignore
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
        assert start.set_conf_path("gunicorn") == gunicorn_conf_path

    def test_set_default_conf_path_logging(self, logging_conf_path: Path) -> None:
        """Test default logging configuration file path (different without Docker)."""
        assert "inboard/logging_conf.py" in str(logging_conf_path)
        assert "gunicorn" not in str(logging_conf_path)
        assert start.set_conf_path("logging") == logging_conf_path

    def test_set_custom_conf_path_gunicorn(
        self, gunicorn_conf_path_tmp: Path, monkeypatch: MonkeyPatch, tmp_path: Path
    ) -> None:
        """Set path to custom temporary Gunicorn configuration file."""
        monkeypatch.setenv("GUNICORN_CONF", str(gunicorn_conf_path_tmp))
        assert os.getenv("GUNICORN_CONF") == str(gunicorn_conf_path_tmp)
        assert f"{tmp_path}/gunicorn_conf.py" in str(gunicorn_conf_path_tmp)
        assert "logging" not in str(gunicorn_conf_path_tmp)
        assert start.set_conf_path("gunicorn") == gunicorn_conf_path_tmp

    def test_set_custom_conf_path_logging(
        self, logging_conf_path_tmp: Path, monkeypatch: MonkeyPatch, tmp_path: Path
    ) -> None:
        """Set path to custom temporary logging configuration file."""
        monkeypatch.setenv("LOGGING_CONF", str(logging_conf_path_tmp))
        assert os.getenv("LOGGING_CONF") == str(logging_conf_path_tmp)
        assert f"{tmp_path}/logging_conf.py" in str(logging_conf_path_tmp)
        assert "gunicorn" not in str(logging_conf_path_tmp)
        assert start.set_conf_path("logging") == logging_conf_path_tmp


class TestConfigureLogging:
    """Test logging configuration methods.
    ---
    """

    def test_configure_logging_conf_path(
        self, logging_conf_path: Path, mock_logger: logging.Logger
    ) -> None:
        """Test `start.configure_logging` with correct logging config path."""
        start.configure_logging(logger=mock_logger, logging_conf=logging_conf_path)
        mock_logger.debug.assert_called_once_with(  # type: ignore
            f"Logging dict config loaded from {logging_conf_path}."
        )

    def test_configure_logging_conf_path_tmp(
        self, logging_conf_path_tmp: Path, mock_logger: logging.Logger
    ) -> None:
        """Test `start.configure_logging` with temporary logging config file."""
        start.configure_logging(logger=mock_logger, logging_conf=logging_conf_path_tmp)
        mock_logger.debug.assert_called_once_with(  # type: ignore
            f"Logging dict config loaded from {logging_conf_path_tmp}."
        )

    def test_configure_logging_incorrect_extension(
        self, logging_conf_path_tmp_txt: Path, mock_logger: logging.Logger
    ) -> None:
        """Test `start.configure_logging` with incorrect temporary file type."""
        with pytest.raises(ImportError):
            start.configure_logging(
                logger=mock_logger, logging_conf=logging_conf_path_tmp_txt
            )
            import_error_msg = "Valid path to .py logging config file required."
            logger_error_msg = "Error when configuring logging:"
            mock_logger.debug.assert_called_once_with(  # type: ignore
                f"{logger_error_msg} {import_error_msg}"
            )

    def test_configure_logging_no_dict(
        self, logging_conf_path_tmp_no_dict: Path, mock_logger: logging.Logger
    ) -> None:
        """Test `start.configure_logging` with temporary logging config file.
        - Correct extension
        - No `LOGGING_CONFIG` object
        """
        with pytest.raises(AttributeError):
            start.configure_logging(
                logger=mock_logger, logging_conf=logging_conf_path_tmp_no_dict
            )
            spec = importlib.util.spec_from_file_location(
                "confspec", logging_conf_path_tmp_no_dict
            )
            logging_conf_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(logging_conf_module)  # type: ignore
            attribute_error_msg = f"No LOGGING_CONFIG in {logging_conf_module}."
            logger_error_msg = "Error when configuring logging:"
            mock_logger.debug.assert_called_once_with(  # type: ignore
                f"{logger_error_msg} {attribute_error_msg}"
            )

    def test_configure_logging_incorrect_type(
        self, logging_conf_path_tmp_incorrect_type: Path, mock_logger: logging.Logger
    ) -> None:
        """Test `start.configure_logging` with temporary logging config file.
        - Correct extension
        - Incorrect data type for `LOGGING_CONFIG` object
        """
        with pytest.raises(TypeError):
            start.configure_logging(
                logger=mock_logger, logging_conf=logging_conf_path_tmp_incorrect_type
            )
            type_error_msg = "LOGGING_CONFIG is not a dictionary instance."
            logger_error_msg = "Error when configuring logging:"
            mock_logger.debug.assert_called_once_with(  # type: ignore
                f"{logger_error_msg} {type_error_msg}"
            )


class TestSetAppModule:
    """Set app module string using the method in `start.py`.
    ---
    """

    def test_set_app_module_asgi(
        self, mock_logger: logging.Logger, monkeypatch: MonkeyPatch
    ) -> None:
        """Test `start.set_app_module` using module path to base ASGI app."""
        monkeypatch.setenv("APP_MODULE", "base.main:app")
        start.set_app_module(logger=mock_logger)
        mock_logger.debug.assert_called_once_with("App module set to base.main:app.")  # type: ignore  # noqa: E501

    def test_set_app_module_fastapi(
        self, mock_logger: logging.Logger, monkeypatch: MonkeyPatch
    ) -> None:
        """Test `start.set_app_module` using module path to FastAPI app."""
        monkeypatch.setenv("APP_MODULE", "fastapibase.main:app")
        start.set_app_module(logger=mock_logger)
        mock_logger.debug.assert_called_once_with(  # type: ignore
            "App module set to fastapibase.main:app."
        )

    def test_set_app_module_starlette(
        self, mock_logger: logging.Logger, monkeypatch: MonkeyPatch
    ) -> None:
        """Test `start.set_app_module` using module path to Starlette app."""
        monkeypatch.setenv("APP_MODULE", "starlettebase.main:app")
        start.set_app_module(logger=mock_logger)
        mock_logger.debug.assert_called_once_with(  # type: ignore
            "App module set to starlettebase.main:app."
        )

    def test_set_app_variables_asgi_custom(
        self, mock_logger: logging.Logger, monkeypatch: MonkeyPatch
    ) -> None:
        """Test `start.set_app_module` using custom module path to base ASGI app."""
        monkeypatch.setenv("MODULE_NAME", "custom_base.main")
        monkeypatch.setenv("VARIABLE_NAME", "api")
        start.set_app_module(logger=mock_logger)
        assert os.getenv("APP_MODULE") == "custom_base.main:api"
        mock_logger.debug.assert_called_once_with(  # type: ignore
            "App module set to custom_base.main:api."
        )

    def test_set_app_variables_fastapi_custom(
        self, mock_logger: logging.Logger, monkeypatch: MonkeyPatch
    ) -> None:
        """Test `start.set_app_module` using custom module path to FastAPI app."""
        monkeypatch.setenv("MODULE_NAME", "custom_fastapibase.main")
        monkeypatch.setenv("VARIABLE_NAME", "api")
        monkeypatch.setenv("APP_MODULE", "custom_fastapibase.main:api")
        start.set_app_module(logger=mock_logger)
        assert os.getenv("MODULE_NAME") == "custom_fastapibase.main"
        assert os.getenv("VARIABLE_NAME") == "api"
        assert os.getenv("APP_MODULE") == "custom_fastapibase.main:api"
        mock_logger.debug.assert_called_once_with(  # type: ignore
            "App module set to custom_fastapibase.main:api."
        )

    def test_set_app_variables_starlette_custom(
        self, mock_logger: logging.Logger, monkeypatch: MonkeyPatch
    ) -> None:
        """Test `start.set_app_module` using custom module path to Starlette app."""
        monkeypatch.setenv("MODULE_NAME", "custom_starlettebase.main")
        monkeypatch.setenv("VARIABLE_NAME", "api")
        monkeypatch.setenv("APP_MODULE", "custom_starlettebase.main:api")
        start.set_app_module(logger=mock_logger)
        assert os.getenv("MODULE_NAME") == "custom_starlettebase.main"
        assert os.getenv("VARIABLE_NAME") == "api"
        assert os.getenv("APP_MODULE") == "custom_starlettebase.main:api"
        mock_logger.debug.assert_called_once_with(  # type: ignore
            "App module set to custom_starlettebase.main:api."
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
        mock_logger.debug.assert_has_calls(  # type: ignore
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
        mock_logger.debug.assert_has_calls(  # type: ignore
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
        mock_logger.debug.assert_has_calls(  # type: ignore
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
            "inboard.base.main:app",
            "inboard.fastapibase.main:app",
            "inboard.starlettebase.main:app",
        ],
    )
    def test_start_server_uvicorn(
        self,
        app_module: str,
        gunicorn_conf_path: Path,
        logging_conf_dict: Dict[str, Any],
        mock_logger: logging.Logger,
        mocker: MockerFixture,
        monkeypatch: MonkeyPatch,
    ) -> None:
        """Test `start.start_server` with Uvicorn."""
        monkeypatch.setenv("LOG_FORMAT", "uvicorn")
        monkeypatch.setenv("LOG_LEVEL", "debug")
        monkeypatch.setenv("PROCESS_MANAGER", "uvicorn")
        start.start_server(
            app_module=app_module,
            gunicorn_conf=gunicorn_conf_path,
            logger=mock_logger,
            logging_conf_dict=logging_conf_dict,
            with_reload=False,
        )
        mock_logger.debug.assert_called_once_with("Running Uvicorn with Gunicorn.")  # type: ignore  # noqa: E501

    @pytest.mark.parametrize(
        "app_module",
        [
            "inboard.base.main:app",
            "inboard.fastapibase.main:app",
            "inboard.starlettebase.main:app",
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
        monkeypatch.setenv("LOG_FORMAT", "gunicorn")
        monkeypatch.setenv("LOG_LEVEL", "debug")
        monkeypatch.setenv("PROCESS_MANAGER", "gunicorn")
        start.start_server(
            app_module=app_module,
            gunicorn_conf=gunicorn_conf_path,
            logger=mock_logger,
            logging_conf_dict=logging_conf_dict,
        )
        mock_logger.debug.assert_called_once_with("Running Uvicorn with Gunicorn.")  # type: ignore  # noqa: E501

    def test_start_server_uvicorn_incorrect_module(
        self,
        gunicorn_conf_path: Path,
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
                app_module="incorrect.base.main:app",
                gunicorn_conf=gunicorn_conf_path,
                logger=mock_logger,
                logging_conf_dict=logging_conf_dict,
                process_manager="uvicorn",
            )
            logger_error_msg = "Error when starting server with start script:"
            module_error_msg = "No module named incorrect.base.main:app"
            mock_logger.debug.assert_has_calls(  # type: ignore
                calls=[
                    mocker.call("Running Uvicorn without Gunicorn."),
                    mocker.call(f"{logger_error_msg} {module_error_msg}"),
                ]
            )

    @pytest.mark.parametrize(
        "app_module",
        [
            "inboard.base.main:app",
            "inboard.fastapibase.main:app",
            "inboard.starlettebase.main:app",
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
                app_module=app_module,
                gunicorn_conf=gunicorn_conf_path,
                logger=mock_logger,
                logging_conf_dict=logging_conf_dict,
                process_manager="incorrect",
            )
            logger_error_msg = "Error when starting server with start script:"
            process_error_msg = (
                "Process manager needs to be either uvicorn or gunicorn."
            )
            mock_logger.debug.assert_called_once_with(  # type: ignore
                f"{logger_error_msg} {process_error_msg}"
            )
