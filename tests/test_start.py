from pathlib import Path

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
