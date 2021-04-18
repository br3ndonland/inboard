import os
from pathlib import Path

import pytest
from pytest_mock import MockerFixture

from inboard import logging_conf


class TestConfigureLogging:
    """Test logging configuration method.
    ---
    """

    def test_configure_logging_file(
        self, logging_conf_file_path: Path, mocker: MockerFixture
    ) -> None:
        """Test logging configuration with correct logging config file path."""
        logger = mocker.patch.object(logging_conf.logging, "root", autospec=True)
        logging_conf.configure_logging(
            logger=logger, logging_conf=str(logging_conf_file_path)
        )
        logger.debug.assert_called_once_with(
            f"Logging dict config loaded from {logging_conf_file_path}."
        )

    def test_configure_logging_module(
        self, logging_conf_module_path: str, mocker: MockerFixture
    ) -> None:
        """Test logging configuration with correct logging config module path."""
        logger = mocker.patch.object(logging_conf.logging, "root", autospec=True)
        logging_conf.configure_logging(
            logger=logger, logging_conf=logging_conf_module_path
        )
        logger.debug.assert_called_once_with(
            f"Logging dict config loaded from {logging_conf_module_path}."
        )

    def test_configure_logging_module_incorrect(self, mocker: MockerFixture) -> None:
        """Test logging configuration with incorrect logging config module path."""
        logger = mocker.patch.object(logging_conf.logging, "root", autospec=True)
        logger_error_msg = "Error when setting logging module"
        with pytest.raises(ModuleNotFoundError):
            logging_conf.configure_logging(logger=logger, logging_conf="no.module.here")
        assert logger_error_msg in logger.error.call_args.args[0]
        assert "ModuleNotFoundError" in logger.error.call_args.args[0]

    def test_configure_logging_tmp_file(
        self, logging_conf_tmp_file_path: Path, mocker: MockerFixture
    ) -> None:
        """Test logging configuration with temporary logging config file path."""
        logger = mocker.patch.object(logging_conf.logging, "root", autospec=True)
        logging_conf_file = f"{logging_conf_tmp_file_path}/tmp_log.py"
        logging_conf.configure_logging(logger=logger, logging_conf=logging_conf_file)
        logger.debug.assert_called_once_with(
            f"Logging dict config loaded from {logging_conf_file}."
        )

    def test_configure_logging_tmp_file_incorrect_extension(
        self,
        logging_conf_tmp_path_incorrect_extension: Path,
        mocker: MockerFixture,
    ) -> None:
        """Test logging configuration with incorrect temporary file type."""
        logger = mocker.patch.object(logging_conf.logging, "root", autospec=True)
        incorrect_logging_conf = logging_conf_tmp_path_incorrect_extension.joinpath(
            "tmp_logging_conf"
        )
        logger_error_msg = "Error when setting logging module"
        import_error_msg = f"Unable to import {incorrect_logging_conf}"
        with pytest.raises(ImportError) as e:
            logging_conf.configure_logging(
                logger=logger,
                logging_conf=str(incorrect_logging_conf),
            )
        assert str(e.value) in import_error_msg
        logger.error.assert_called_once_with(
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
        """Test logging configuration with temporary logging config path."""
        logger = mocker.patch.object(logging_conf.logging, "root", autospec=True)
        monkeypatch.syspath_prepend(logging_conf_tmp_file_path)
        monkeypatch.setenv("LOGGING_CONF", "tmp_log")
        assert os.getenv("LOGGING_CONF") == "tmp_log"
        logging_conf.configure_logging(logger=logger, logging_conf="tmp_log")
        logger.debug.assert_called_once_with("Logging dict config loaded from tmp_log.")

    def test_configure_logging_tmp_module_incorrect_type(
        self,
        logging_conf_tmp_path_incorrect_type: Path,
        mocker: MockerFixture,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Test logging configuration with temporary logging config path.
        - Correct module name
        - `LOGGING_CONFIG` object with incorrect type
        """
        logger = mocker.patch.object(logging_conf.logging, "root", autospec=True)
        monkeypatch.syspath_prepend(logging_conf_tmp_path_incorrect_type)
        monkeypatch.setenv("LOGGING_CONF", "incorrect_type")
        logger_error_msg = "Error when setting logging module"
        type_error_msg = "LOGGING_CONFIG is not a dictionary instance"
        assert os.getenv("LOGGING_CONF") == "incorrect_type"
        with pytest.raises(TypeError):
            logging_conf.configure_logging(logger=logger, logging_conf="incorrect_type")
        logger.error.assert_called_once_with(
            f"{logger_error_msg}: TypeError {type_error_msg}."
        )

    def test_configure_logging_tmp_module_no_dict(
        self,
        logging_conf_tmp_path_no_dict: Path,
        mocker: MockerFixture,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Test logging configuration with temporary logging config path.
        - Correct module name
        - No `LOGGING_CONFIG` object
        """
        logger = mocker.patch.object(logging_conf.logging, "root", autospec=True)
        monkeypatch.syspath_prepend(logging_conf_tmp_path_no_dict)
        monkeypatch.setenv("LOGGING_CONF", "no_dict")
        logger_error_msg = "Error when setting logging module"
        attribute_error_msg = "No LOGGING_CONFIG in no_dict"
        assert os.getenv("LOGGING_CONF") == "no_dict"
        with pytest.raises(AttributeError):
            logging_conf.configure_logging(logger=logger, logging_conf="no_dict")
        logger.error.assert_called_once_with(
            f"{logger_error_msg}: AttributeError {attribute_error_msg}."
        )
