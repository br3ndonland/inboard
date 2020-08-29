import os
from pathlib import Path

# import pytest  # type: ignore
from _pytest.monkeypatch import MonkeyPatch  # type: ignore

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
