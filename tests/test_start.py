import os
from pathlib import Path

import pytest
from pytest_mock import MockerFixture

from inboard import start


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


class TestSetAppModule:
    """Set app module string using the method in `start.py`.
    ---
    """

    @pytest.mark.parametrize("module", ("base", "fastapi", "starlette"))
    def test_set_app_module(
        self, module: str, mocker: MockerFixture, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test `start.set_app_module` with default module path."""
        mock_logger = mocker.patch.object(start.logging, "root", autospec=True)
        monkeypatch.setenv("APP_MODULE", f"inboard.app.main_{module}:app")
        start.set_app_module(logger=mock_logger)
        assert mocker.call(f"App module set to inboard.app.main_{module}:app.")

    @pytest.mark.parametrize("module", ("base", "fastapi", "starlette"))
    def test_set_app_module_custom(
        self,
        app_module_tmp_path: Path,
        module: str,
        mocker: MockerFixture,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Test `start.set_app_module` with custom module path."""
        mock_logger = mocker.patch.object(start.logging, "root", autospec=True)
        monkeypatch.syspath_prepend(app_module_tmp_path)
        monkeypatch.setenv("APP_MODULE", f"tmp_app.main_{module}:app")
        start.set_app_module(logger=mock_logger)
        assert mocker.call(f"App module set to tmp_app.main_{module}:app.")

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
        assert mocker.call(f"{logger_error_msg}: ImportError {incorrect_module_msg}.")


class TestSetGunicornOptions:
    """Test Gunicorn configuration options method.
    ---
    """

    def test_set_gunicorn_options_default(
        self, gunicorn_conf_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test default Gunicorn server options."""
        monkeypatch.setenv("GUNICORN_CONF", str(gunicorn_conf_path))
        result = start.set_gunicorn_options()
        assert os.getenv("GUNICORN_CONF") == str(gunicorn_conf_path)
        assert "/gunicorn_conf.py" in str(gunicorn_conf_path)
        assert "logging" not in str(gunicorn_conf_path)
        assert isinstance(result, list)
        assert result == [
            "gunicorn",
            "-k",
            "uvicorn.workers.UvicornWorker",
            "-c",
            str(gunicorn_conf_path),
        ]

    def test_set_gunicorn_options_custom(
        self,
        gunicorn_conf_tmp_file_path: Path,
        monkeypatch: pytest.MonkeyPatch,
        tmp_path: Path,
    ) -> None:
        """Test custom Gunicorn server options with temporary configuration file."""
        monkeypatch.setenv("GUNICORN_CONF", str(gunicorn_conf_tmp_file_path))
        result = start.set_gunicorn_options()
        assert os.getenv("GUNICORN_CONF") == str(gunicorn_conf_tmp_file_path)
        assert "/gunicorn_conf.py" in str(gunicorn_conf_tmp_file_path)
        assert "logging" not in str(gunicorn_conf_tmp_file_path)
        assert isinstance(result, list)
        assert result == [
            "gunicorn",
            "-k",
            "uvicorn.workers.UvicornWorker",
            "-c",
            str(gunicorn_conf_tmp_file_path),
        ]

    def test_set_incorrect_conf_path(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Set path to non-existent file and raise an error."""
        monkeypatch.setenv("GUNICORN_CONF", "/no/file/here")
        with pytest.raises(FileNotFoundError):
            start.set_gunicorn_options()


class TestSetUvicornOptions:
    """Test Uvicorn configuration options method.
    ---
    """

    def test_set_uvicorn_options_default(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test default Uvicorn server options."""
        monkeypatch.setenv("WITH_RELOAD", "false")
        result = start.set_uvicorn_options()
        assert isinstance(result, dict)
        assert result == dict(
            host="0.0.0.0",
            port=80,
            log_config=None,
            log_level="info",
            reload=False,
            reload_dirs=None,
        )

    def test_set_uvicorn_options_custom(
        self, logging_conf_dict: dict, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test custom Uvicorn server options."""
        monkeypatch.setenv("LOG_LEVEL", "debug")
        monkeypatch.setenv("WITH_RELOAD", "true")
        monkeypatch.setenv("RELOAD_DIRS", "inboard, tests")
        result = start.set_uvicorn_options(log_config=logging_conf_dict)
        assert isinstance(result, dict)
        assert result == dict(
            host="0.0.0.0",
            port=80,
            log_config=logging_conf_dict,
            log_level="debug",
            reload=True,
            reload_dirs=["inboard", "tests"],
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
        logging_conf_dict: dict,
        mocker: MockerFixture,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Test `start.start_server` with Uvicorn."""
        mock_logger = mocker.patch.object(start.logging, "root", autospec=True)
        mock_run = mocker.patch("inboard.start.uvicorn.run", autospec=True)
        monkeypatch.setenv("PROCESS_MANAGER", "uvicorn")
        monkeypatch.setenv("WITH_RELOAD", "false")
        start.start_server(
            str(os.getenv("PROCESS_MANAGER")),
            app_module=app_module,
            logger=mock_logger,
            logging_conf_dict=logging_conf_dict,
        )
        assert os.getenv("PROCESS_MANAGER") == "uvicorn"
        assert os.getenv("WITH_RELOAD") == "false"
        mock_logger.debug.assert_called_once_with("Running Uvicorn without Gunicorn.")
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
        logging_conf_dict: dict,
        mocker: MockerFixture,
        monkeypatch: pytest.MonkeyPatch,
        reload_dirs: str,
    ) -> None:
        """Test `start.start_server` with Uvicorn."""
        mock_logger = mocker.patch.object(start.logging, "root", autospec=True)
        monkeypatch.setenv("PROCESS_MANAGER", "uvicorn")
        monkeypatch.setenv("WITH_RELOAD", "true")
        monkeypatch.setenv("RELOAD_DIRS", reload_dirs)
        split_dirs = [d.lstrip() for d in str(os.getenv("RELOAD_DIRS")).split(sep=",")]
        assert os.getenv("PROCESS_MANAGER") == "uvicorn"
        assert os.getenv("WITH_RELOAD") == "true"
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
        mock_logger.debug.assert_called_once_with("Running Uvicorn without Gunicorn.")
        mock_run.assert_called_once_with(
            app_module,
            host="0.0.0.0",
            port=80,
            log_config=logging_conf_dict,
            log_level="info",
            reload=True,
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
        logging_conf_dict: dict,
        mocker: MockerFixture,
        monkeypatch: pytest.MonkeyPatch,
        tmp_path: Path,
    ) -> None:
        """Test `start.start_server` with Uvicorn managed by Gunicorn."""
        mock_logger = mocker.patch.object(start.logging, "root", autospec=True)
        mock_run = mocker.patch("inboard.start.subprocess.run", autospec=True)
        monkeypatch.setenv(
            "GUNICORN_CMD_ARGS",
            f"--worker-tmp-dir {tmp_path}",
        )
        monkeypatch.setenv("PROCESS_MANAGER", "gunicorn")
        start.start_server(
            str(os.getenv("PROCESS_MANAGER")),
            app_module=app_module,
            logger=mock_logger,
            logging_conf_dict=logging_conf_dict,
        )
        assert gunicorn_conf_path.parent.exists()
        assert os.getenv("GUNICORN_CONF") == str(gunicorn_conf_path)
        assert os.getenv("PROCESS_MANAGER") == "gunicorn"
        mock_logger.debug.assert_called_once_with("Running Uvicorn with Gunicorn.")
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
        logging_conf_dict: dict,
        mocker: MockerFixture,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Test customized `start.start_server` with Uvicorn managed by Gunicorn."""
        mock_logger = mocker.patch.object(start.logging, "root", autospec=True)
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
        mock_logger.debug.assert_called_with("Running Uvicorn with Gunicorn.")
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
        logging_conf_dict: dict,
        mocker: MockerFixture,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Test `start.start_server` with Uvicorn and an incorrect process manager."""
        mock_logger = mocker.patch.object(start.logging, "root", autospec=True)
        monkeypatch.setenv("LOG_LEVEL", "debug")
        monkeypatch.setenv("WITH_RELOAD", "false")
        logger_error_msg = "Error when starting server"
        process_error_msg = "Process manager needs to be either uvicorn or gunicorn"
        with pytest.raises(NameError) as e:
            start.start_server(
                "incorrect",
                app_module=app_module,
                logger=mock_logger,
                logging_conf_dict=logging_conf_dict,
            )
        assert str(e.value) == process_error_msg
        mock_logger.error.assert_called_once_with(
            f"{logger_error_msg}: NameError {process_error_msg}."
        )
