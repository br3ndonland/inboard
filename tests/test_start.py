import logging
import multiprocessing
import os
from pathlib import Path
from typing import Any, Dict, Optional

import pytest
from pytest_mock import MockerFixture

from inboard import gunicorn_conf, start


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
        self,
        gunicorn_conf_tmp_file_path: Path,
        monkeypatch: pytest.MonkeyPatch,
        tmp_path: Path,
    ) -> None:
        """Set path to custom temporary Gunicorn configuration file."""
        monkeypatch.setenv("GUNICORN_CONF", str(gunicorn_conf_tmp_file_path))
        assert os.getenv("GUNICORN_CONF") == str(gunicorn_conf_tmp_file_path)
        assert "/gunicorn_conf.py" in str(gunicorn_conf_tmp_file_path)
        assert "logging" not in str(gunicorn_conf_tmp_file_path)
        assert start.set_conf_path("gunicorn") == str(gunicorn_conf_tmp_file_path)

    def test_set_incorrect_conf_path(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Set path to non-existent file and raise an error."""
        with pytest.raises(FileNotFoundError):
            monkeypatch.setenv("GUNICORN_CONF", "/no/file/here")
            start.set_conf_path("gunicorn")


class TestConfigureGunicorn:
    """Test Gunicorn configuration independently of Gunicorn server.
    ---
    """

    def test_gunicorn_conf_workers_default(self) -> None:
        """Test default number of Gunicorn worker processes."""
        assert gunicorn_conf.workers >= 2
        assert gunicorn_conf.workers == multiprocessing.cpu_count()

    def test_gunicorn_conf_workers_custom_max(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test custom Gunicorn worker process calculation."""
        monkeypatch.setenv("MAX_WORKERS", "1")
        monkeypatch.setenv("WEB_CONCURRENCY", "4")
        monkeypatch.setenv("WORKERS_PER_CORE", "0.5")
        assert os.getenv("MAX_WORKERS") == "1"
        assert os.getenv("WEB_CONCURRENCY") == "4"
        assert os.getenv("WORKERS_PER_CORE") == "0.5"
        assert (
            gunicorn_conf.calculate_workers(
                str(os.getenv("MAX_WORKERS")),
                str(os.getenv("WEB_CONCURRENCY")),
                str(os.getenv("WORKERS_PER_CORE")),
            )
            == 1
        )

    @pytest.mark.parametrize("number_of_workers", ["1", "2", "4"])
    def test_gunicorn_conf_workers_custom_concurrency(
        self, monkeypatch: pytest.MonkeyPatch, number_of_workers: str
    ) -> None:
        """Test custom Gunicorn worker process calculation."""
        monkeypatch.setenv("WEB_CONCURRENCY", number_of_workers)
        monkeypatch.setenv("WORKERS_PER_CORE", "0.5")
        assert os.getenv("WEB_CONCURRENCY") == number_of_workers
        assert os.getenv("WORKERS_PER_CORE") == "0.5"
        assert (
            gunicorn_conf.calculate_workers(
                None,
                str(os.getenv("WEB_CONCURRENCY")),
                str(os.getenv("WORKERS_PER_CORE")),
            )
            == int(number_of_workers)
        )

    @pytest.mark.parametrize("concurrency", [None, "10"])
    def test_gunicorn_conf_workers_custom_cores(
        self, monkeypatch: pytest.MonkeyPatch, concurrency: Optional[str]
    ) -> None:
        """Test custom Gunicorn worker process calculation.
        - Assert that number of workers equals `WORKERS_PER_CORE`, and is at least 2.
        - Assert that setting `WEB_CONCURRENCY` overrides `WORKERS_PER_CORE`.
        """
        monkeypatch.setenv("WORKERS_PER_CORE", "0.5")
        workers_per_core = os.getenv("WORKERS_PER_CORE")
        assert workers_per_core == "0.5"
        cores: int = multiprocessing.cpu_count()
        assert gunicorn_conf.calculate_workers(
            None, None, workers_per_core, cores=cores
        ) == max(int(cores * float(workers_per_core)), 2)
        assert (
            gunicorn_conf.calculate_workers(None, "10", workers_per_core, cores=cores)
            == 10
        )
        monkeypatch.setenv("WEB_CONCURRENCY", concurrency) if concurrency else None
        assert os.getenv("WEB_CONCURRENCY") == concurrency
        assert (
            (
                gunicorn_conf.calculate_workers(
                    None, concurrency, workers_per_core, cores=cores
                )
                == 10
            )
            if concurrency
            else max(int(cores * float(workers_per_core)), 2)
        )


class TestConfigureLogging:
    """Test logging configuration methods.
    ---
    """

    def test_configure_logging_file(
        self, logging_conf_file_path: Path, mocker: MockerFixture
    ) -> None:
        """Test `start.configure_logging` with correct logging config file path."""
        mock_logger = mocker.patch.object(start.logging, "root", autospec=True)
        start.configure_logging(
            logger=mock_logger, logging_conf=str(logging_conf_file_path)
        )
        mock_logger.debug.assert_called_once_with(
            f"Logging dict config loaded from {logging_conf_file_path}."
        )

    def test_configure_logging_module(
        self, logging_conf_module_path: str, mocker: MockerFixture
    ) -> None:
        """Test `start.configure_logging` with correct logging config module path."""
        mock_logger = mocker.patch.object(start.logging, "root", autospec=True)
        start.configure_logging(
            logger=mock_logger, logging_conf=logging_conf_module_path
        )
        mock_logger.debug.assert_called_once_with(
            f"Logging dict config loaded from {logging_conf_module_path}."
        )

    def test_configure_logging_module_incorrect(self, mocker: MockerFixture) -> None:
        """Test `start.configure_logging` with incorrect logging config module path."""
        mock_logger = mocker.patch.object(start.logging, "root", autospec=True)
        mock_logger_error_msg = "Error when setting logging module"
        with pytest.raises(ModuleNotFoundError):
            start.configure_logging(logger=mock_logger, logging_conf="no.module.here")
        assert mock_logger_error_msg in mock_logger.error.call_args.args[0]
        assert "ModuleNotFoundError" in mock_logger.error.call_args.args[0]

    def test_configure_logging_tmp_file(
        self, logging_conf_tmp_file_path: Path, mocker: MockerFixture
    ) -> None:
        """Test `start.configure_logging` with temporary logging config file path."""
        mock_logger = mocker.patch.object(start.logging, "root", autospec=True)
        logging_conf_file = f"{logging_conf_tmp_file_path}/tmp_log.py"
        start.configure_logging(logger=mock_logger, logging_conf=logging_conf_file)
        mock_logger.debug.assert_called_once_with(
            f"Logging dict config loaded from {logging_conf_file}."
        )

    def test_configure_logging_tmp_file_incorrect_extension(
        self,
        logging_conf_tmp_path_incorrect_extension: Path,
        mocker: MockerFixture,
    ) -> None:
        """Test `start.configure_logging` with incorrect temporary file type."""
        mock_logger = mocker.patch.object(start.logging, "root", autospec=True)
        incorrect_logging_conf = logging_conf_tmp_path_incorrect_extension.joinpath(
            "tmp_logging_conf"
        )
        logger_error_msg = "Error when setting logging module"
        import_error_msg = f"Unable to import {incorrect_logging_conf}"
        with pytest.raises(ImportError) as e:
            start.configure_logging(
                logger=mock_logger,
                logging_conf=str(incorrect_logging_conf),
            )
        assert str(e.value) in import_error_msg
        mock_logger.error.assert_called_once_with(
            f"{logger_error_msg}: ImportError {import_error_msg}."
        )
        with open(incorrect_logging_conf, "r") as f:
            contents = f.read()
            assert "This file doesn't have the correct extension" in contents

    def test_configure_logging_tmp_module(
        self,
        logging_conf_tmp_file_path: Path,
        mocker: MockerFixture,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Test `start.configure_logging` with temporary logging config path."""
        mock_logger = mocker.patch.object(start.logging, "root", autospec=True)
        monkeypatch.syspath_prepend(logging_conf_tmp_file_path)
        monkeypatch.setenv("LOGGING_CONF", "tmp_log")
        assert os.getenv("LOGGING_CONF") == "tmp_log"
        start.configure_logging(logger=mock_logger, logging_conf="tmp_log")
        mock_logger.debug.assert_called_once_with(
            "Logging dict config loaded from tmp_log."
        )

    def test_configure_logging_tmp_module_incorrect_type(
        self,
        logging_conf_tmp_path_incorrect_type: Path,
        mocker: MockerFixture,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Test `start.configure_logging` with temporary logging config path.
        - Correct module name
        - `LOGGING_CONFIG` object with incorrect type
        """
        mock_logger = mocker.patch.object(start.logging, "root", autospec=True)
        monkeypatch.syspath_prepend(logging_conf_tmp_path_incorrect_type)
        monkeypatch.setenv("LOGGING_CONF", "incorrect_type")
        logger_error_msg = "Error when setting logging module"
        type_error_msg = "LOGGING_CONFIG is not a dictionary instance"
        assert os.getenv("LOGGING_CONF") == "incorrect_type"
        with pytest.raises(TypeError):
            start.configure_logging(logger=mock_logger, logging_conf="incorrect_type")
        mock_logger.error.assert_called_once_with(
            f"{logger_error_msg}: TypeError {type_error_msg}."
        )

    def test_configure_logging_tmp_module_no_dict(
        self,
        logging_conf_tmp_path_no_dict: Path,
        mocker: MockerFixture,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Test `start.configure_logging` with temporary logging config path.
        - Correct module name
        - No `LOGGING_CONFIG` object
        """
        mock_logger = mocker.patch.object(start.logging, "root", autospec=True)
        monkeypatch.syspath_prepend(logging_conf_tmp_path_no_dict)
        monkeypatch.setenv("LOGGING_CONF", "no_dict")
        logger_error_msg = "Error when setting logging module"
        attribute_error_msg = "No LOGGING_CONFIG in no_dict"
        assert os.getenv("LOGGING_CONF") == "no_dict"
        with pytest.raises(AttributeError):
            start.configure_logging(logger=mock_logger, logging_conf="no_dict")
        mock_logger.error.assert_called_once_with(
            f"{logger_error_msg}: AttributeError {attribute_error_msg}."
        )


class TestSetAppModule:
    """Set app module string using the method in `start.py`.
    ---
    """

    def test_set_app_module_asgi(
        self, mocker: MockerFixture, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test `start.set_app_module` using module path to base ASGI app."""
        mock_logger = mocker.patch.object(start.logging, "root", autospec=True)
        monkeypatch.setenv("APP_MODULE", "inboard.app.main_base:app")
        start.set_app_module(logger=mock_logger)
        mock_logger.debug.assert_called_once_with(
            "App module set to inboard.app.main_base:app."
        )

    def test_set_app_module_fastapi(
        self, mocker: MockerFixture, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test `start.set_app_module` using module path to FastAPI app."""
        mock_logger = mocker.patch.object(start.logging, "root", autospec=True)
        monkeypatch.setenv("APP_MODULE", "inboard.app.main_fastapi:app")
        start.set_app_module(logger=mock_logger)
        mock_logger.debug.assert_called_once_with(
            "App module set to inboard.app.main_fastapi:app."
        )

    def test_set_app_module_starlette(
        self, mocker: MockerFixture, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test `start.set_app_module` using module path to Starlette app."""
        mock_logger = mocker.patch.object(start.logging, "root", autospec=True)
        monkeypatch.setenv("APP_MODULE", "inboard.app.main_starlette:app")
        start.set_app_module(logger=mock_logger)
        mock_logger.debug.assert_called_once_with(
            "App module set to inboard.app.main_starlette:app."
        )

    def test_set_app_module_custom_asgi(
        self,
        app_module_tmp_path: Path,
        mocker: MockerFixture,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Test `start.set_app_module` with custom module path to base ASGI app."""
        mock_logger = mocker.patch.object(start.logging, "root", autospec=True)
        monkeypatch.syspath_prepend(app_module_tmp_path)
        monkeypatch.setenv("APP_MODULE", "tmp_app.main_base:app")
        start.set_app_module(logger=mock_logger)
        mock_logger.debug.assert_called_once_with(
            "App module set to tmp_app.main_base:app."
        )

    def test_set_app_module_custom_fastapi(
        self,
        app_module_tmp_path: Path,
        mocker: MockerFixture,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Test `start.set_app_module` with custom module path to FastAPI app."""
        mock_logger = mocker.patch.object(start.logging, "root", autospec=True)
        monkeypatch.syspath_prepend(app_module_tmp_path)
        monkeypatch.setenv("APP_MODULE", "tmp_app.main_fastapi:app")
        start.set_app_module(logger=mock_logger)
        mock_logger.debug.assert_called_once_with(
            "App module set to tmp_app.main_fastapi:app."
        )

    def test_set_app_module_custom_starlette(
        self,
        app_module_tmp_path: Path,
        mocker: MockerFixture,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Test `start.set_app_module` with custom module path to Starlette app."""
        mock_logger = mocker.patch.object(start.logging, "root", autospec=True)
        monkeypatch.syspath_prepend(app_module_tmp_path)
        monkeypatch.setenv("APP_MODULE", "tmp_app.main_starlette:app")
        start.set_app_module(logger=mock_logger)
        mock_logger.debug.assert_called_once_with(
            "App module set to tmp_app.main_starlette:app."
        )

    def test_set_app_module_incorrect(
        self,
        mocker: MockerFixture,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Test `start.set_app_module` with incorrect module path."""
        mock_logger = mocker.patch.object(start.logging, "root", autospec=True)
        monkeypatch.setenv("APP_MODULE", "inboard.app.incorrect:app")
        logger_error_msg = "Error when setting app module"
        incorrect_module_msg = "Unable to find or import inboard.app.incorrect"
        with pytest.raises(ImportError):
            start.set_app_module(logger=mock_logger)
        mock_logger.error.assert_called_once_with(
            f"{logger_error_msg}: ImportError {incorrect_module_msg}."
        )


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
        mock_logger = mocker.patch.object(start.logging, "root", autospec=True)
        monkeypatch.setenv("PRE_START_PATH", str(pre_start_script_tmp_py))
        pre_start_path = os.getenv("PRE_START_PATH")
        start.run_pre_start_script(logger=mock_logger)
        mock_logger.debug.assert_has_calls(
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
        mock_logger = mocker.patch.object(start.logging, "root", autospec=True)
        monkeypatch.setenv("PRE_START_PATH", str(pre_start_script_tmp_sh))
        pre_start_path = os.getenv("PRE_START_PATH")
        start.run_pre_start_script(logger=mock_logger)
        mock_logger.debug.assert_has_calls(
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
        mock_logger = mocker.patch.object(start.logging, "root", autospec=True)
        monkeypatch.setenv("PRE_START_PATH", "/no/file/here")
        start.run_pre_start_script(logger=mock_logger)
        mock_logger.debug.assert_has_calls(
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
            "inboard.app.main_base:app",
            "inboard.app.main_fastapi:app",
            "inboard.app.main_starlette:app",
        ],
    )
    @pytest.mark.timeout(2)
    def test_start_server_uvicorn(
        self,
        app_module: str,
        logging_conf_dict: Dict[str, Any],
        mock_logger: logging.Logger,
        mocker: MockerFixture,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Test `start.start_server` with Uvicorn."""
        monkeypatch.setenv("PROCESS_MANAGER", "uvicorn")
        assert os.getenv("PROCESS_MANAGER") == "uvicorn"
        mock_run = mocker.patch("inboard.start.uvicorn.run", autospec=True)
        start.start_server(
            str(os.getenv("PROCESS_MANAGER")),
            app_module=app_module,
            logger=mock_logger,
            logging_conf_dict=logging_conf_dict,
        )
        mock_logger.debug.assert_called_once_with(  # type: ignore[attr-defined]
            "Running Uvicorn without Gunicorn."
        )
        mock_run.assert_called_once_with(
            app_module,
            host="0.0.0.0",
            port=80,
            log_config=logging_conf_dict,
            log_level="info",
            reload=False,
            reload_dirs=None,
        )

    @pytest.mark.parametrize(
        "app_module",
        [
            "inboard.app.main_base:app",
            "inboard.app.main_fastapi:app",
            "inboard.app.main_starlette:app",
        ],
    )
    @pytest.mark.parametrize(
        "reload_dirs", ["inboard", "inboard,tests", "inboard, tests"]
    )
    @pytest.mark.timeout(2)
    def test_start_server_uvicorn_reload_dirs(
        self,
        app_module: str,
        logging_conf_dict: Dict[str, Any],
        mock_logger: logging.Logger,
        mocker: MockerFixture,
        monkeypatch: pytest.MonkeyPatch,
        reload_dirs: str,
    ) -> None:
        """Test `start.start_server` with Uvicorn."""
        monkeypatch.setenv("PROCESS_MANAGER", "uvicorn")
        monkeypatch.setenv("RELOAD_DIRS", reload_dirs)
        split_dirs = [d.lstrip() for d in str(os.getenv("RELOAD_DIRS")).split(sep=",")]
        assert os.getenv("PROCESS_MANAGER") == "uvicorn"
        assert os.getenv("RELOAD_DIRS") == reload_dirs
        if reload_dirs == "inboard":
            assert len(split_dirs) == 1
        else:
            assert len(split_dirs) == 2
        mock_run = mocker.patch("inboard.start.uvicorn.run", autospec=True)
        start.start_server(
            str(os.getenv("PROCESS_MANAGER")),
            app_module=app_module,
            logger=mock_logger,
            logging_conf_dict=logging_conf_dict,
        )
        mock_logger.debug.assert_called_once_with(  # type: ignore[attr-defined]
            "Running Uvicorn without Gunicorn."
        )
        mock_run.assert_called_once_with(
            app_module,
            host="0.0.0.0",
            port=80,
            log_config=logging_conf_dict,
            log_level="info",
            reload=False,
            reload_dirs=split_dirs,
        )

    @pytest.mark.parametrize(
        "app_module",
        [
            "inboard.app.main_base:app",
            "inboard.app.main_fastapi:app",
            "inboard.app.main_starlette:app",
        ],
    )
    @pytest.mark.timeout(2)
    def test_start_server_uvicorn_gunicorn(
        self,
        app_module: str,
        gunicorn_conf_path: Path,
        logging_conf_dict: Dict[str, Any],
        mock_logger: logging.Logger,
        mocker: MockerFixture,
        monkeypatch: pytest.MonkeyPatch,
        tmp_path: Path,
    ) -> None:
        """Test `start.start_server` with Uvicorn managed by Gunicorn."""
        monkeypatch.setenv(
            "GUNICORN_CMD_ARGS",
            f"--worker-tmp-dir {tmp_path}",
        )
        monkeypatch.setenv("PROCESS_MANAGER", "gunicorn")
        assert gunicorn_conf_path.parent.exists()
        assert os.getenv("GUNICORN_CONF") == str(gunicorn_conf_path)
        assert os.getenv("PROCESS_MANAGER") == "gunicorn"
        mock_run = mocker.patch("inboard.start.subprocess.run", autospec=True)
        start.start_server(
            str(os.getenv("PROCESS_MANAGER")),
            app_module=app_module,
            logger=mock_logger,
            logging_conf_dict=logging_conf_dict,
        )
        mock_logger.debug.assert_called_once_with(  # type: ignore[attr-defined]
            "Running Uvicorn with Gunicorn."
        )
        mock_run.assert_called_once_with(
            [
                "gunicorn",
                "-k",
                "uvicorn.workers.UvicornWorker",
                "-c",
                str(gunicorn_conf_path),
                app_module,
            ]
        )

    @pytest.mark.parametrize(
        "app_module",
        [
            "inboard.app.main_base:app",
            "inboard.app.main_fastapi:app",
            "inboard.app.main_starlette:app",
        ],
    )
    @pytest.mark.timeout(2)
    def test_start_server_uvicorn_gunicorn_custom_config(
        self,
        app_module: str,
        gunicorn_conf_tmp_file_path: Path,
        logging_conf_dict: Dict[str, Any],
        mock_logger: logging.Logger,
        mocker: MockerFixture,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Test customized `start.start_server` with Uvicorn managed by Gunicorn."""
        monkeypatch.setenv(
            "GUNICORN_CMD_ARGS",
            f"--worker-tmp-dir {gunicorn_conf_tmp_file_path.parent}",
        )
        monkeypatch.setenv("LOG_FORMAT", "gunicorn")
        monkeypatch.setenv("LOG_LEVEL", "debug")
        monkeypatch.setenv("PROCESS_MANAGER", "gunicorn")
        assert gunicorn_conf_tmp_file_path.parent.exists()
        assert os.getenv("GUNICORN_CONF") == str(gunicorn_conf_tmp_file_path)
        assert os.getenv("LOG_FORMAT") == "gunicorn"
        assert os.getenv("LOG_LEVEL") == "debug"
        assert os.getenv("PROCESS_MANAGER") == "gunicorn"
        mock_run = mocker.patch("inboard.start.subprocess.run", autospec=True)
        start.start_server(
            str(os.getenv("PROCESS_MANAGER")),
            app_module=app_module,
            logger=mock_logger,
            logging_conf_dict=logging_conf_dict,
        )
        mock_logger.debug.assert_called_with(  # type: ignore[attr-defined]
            "Running Uvicorn with Gunicorn."
        )
        mock_run.assert_called_with(
            [
                "gunicorn",
                "-k",
                "uvicorn.workers.UvicornWorker",
                "-c",
                str(gunicorn_conf_tmp_file_path),
                app_module,
            ]
        )

    @pytest.mark.parametrize(
        "app_module",
        [
            "inboard.app.main_base:app",
            "inboard.app.main_fastapi:app",
            "inboard.app.main_starlette:app",
        ],
    )
    @pytest.mark.timeout(2)
    def test_start_server_uvicorn_incorrect_process_manager(
        self,
        app_module: str,
        gunicorn_conf_path: Path,
        logging_conf_dict: Dict[str, Any],
        mock_logger: logging.Logger,
        mocker: MockerFixture,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Test `start.start_server` with Uvicorn and an incorrect process manager."""
        monkeypatch.setenv("LOG_LEVEL", "debug")
        monkeypatch.setenv("WITH_RELOAD", "false")
        logger_error_msg = "Error when starting server with start script:"
        process_error_msg = "Process manager needs to be either uvicorn or gunicorn."
        with pytest.raises(NameError) as e:
            start.start_server(
                "incorrect",
                app_module=app_module,
                logger=mock_logger,
                logging_conf_dict=logging_conf_dict,
            )
            assert e.value == process_error_msg
        mock_logger.error.assert_called_once_with(  # type: ignore[attr-defined]
            f"{logger_error_msg} {process_error_msg}"
        )
