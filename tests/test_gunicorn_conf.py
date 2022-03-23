import multiprocessing
import subprocess
from pathlib import Path
from typing import Optional

import pytest

from inboard import gunicorn_conf


class TestCalculateWorkers:
    """Test calculation of the number of Gunicorn worker processes.
    ---
    """

    def test_calculate_workers_default(self) -> None:
        """Test default number of Gunicorn worker processes."""
        cores = multiprocessing.cpu_count()
        assert gunicorn_conf.workers >= 2
        assert gunicorn_conf.workers == max(cores, 2)

    @pytest.mark.parametrize("max_workers", (None, "1", "2", "5", "10"))
    def test_calculate_workers_max(self, max_workers: Optional[str]) -> None:
        """Test Gunicorn worker process calculation with custom maximum."""
        cores = multiprocessing.cpu_count()
        default = max(cores, 2)
        result = gunicorn_conf.calculate_workers(max_workers, None)
        if max_workers and default > (m := int(max_workers)):
            assert result == m
        else:
            assert result == default

    @pytest.mark.parametrize("total_workers", (None, "1", "2", "5", "10"))
    def test_calculate_workers_total(self, total_workers: Optional[str]) -> None:
        """Test Gunicorn worker process calculation with custom total."""
        cores = multiprocessing.cpu_count()
        result = gunicorn_conf.calculate_workers(None, total_workers)
        assert result == int(total_workers) if total_workers else max(cores, 2)

    @pytest.mark.parametrize("workers_per_core", ("0.5", "1.5", "5", "10"))
    def test_calculate_workers_per_core(self, workers_per_core: str) -> None:
        """Test Gunicorn worker process calculation with custom workers per core.
        Worker number should be the greater of 2 or the workers per core setting.
        """
        cores = multiprocessing.cpu_count()
        result = gunicorn_conf.calculate_workers(workers_per_core=workers_per_core)
        assert result == max(int(float(workers_per_core) * cores), 2)

    @pytest.mark.parametrize("max_workers", ("1", "2", "5", "10"))
    @pytest.mark.parametrize("total_workers", ("1", "2", "5", "10"))
    def test_calculate_workers_both_max_and_total(
        self, max_workers: str, total_workers: str
    ) -> None:
        """Test Gunicorn worker process calculation if max workers and total workers
        (web concurrency) are both set. Worker number should be the lesser of the two.
        """
        result = gunicorn_conf.calculate_workers(max_workers, total_workers)
        assert result == min(int(max_workers), int(total_workers))

    @pytest.mark.parametrize("max_workers", ("1", "2", "5", "10"))
    @pytest.mark.parametrize("workers_per_core", ("0.5", "1.5", "5", "10"))
    def test_calculate_workers_both_max_and_workers_per_core(
        self, max_workers: str, workers_per_core: str
    ) -> None:
        """Test Gunicorn worker process calculation if max workers and workers per core
        are both set. Worker number should always be less than the maximum.
        """
        result = gunicorn_conf.calculate_workers(
            max_workers, None, workers_per_core=workers_per_core
        )
        assert result <= int(max_workers)


class TestGunicornSettings:
    """Test Gunicorn configuration setup and settings.
    ---
    """

    @pytest.mark.parametrize("module", ("base", "fastapi", "starlette"))
    @pytest.mark.timeout(2)
    def test_gunicorn_config(
        self, capfd: pytest.CaptureFixture, gunicorn_conf_path: str, module: str
    ) -> None:
        """Load Gunicorn configuration file and verify output."""
        app_module = f"inboard.app.main_{module}:app"
        gunicorn_conf_path = gunicorn_conf.__file__
        gunicorn_options = [
            "gunicorn",
            "--print-config",
            "-c",
            gunicorn_conf_path,
            "-k",
            "uvicorn.workers.UvicornWorker",
            app_module,
        ]
        subprocess.run(gunicorn_options)
        captured = capfd.readouterr()
        captured_and_cleaned = captured.out.replace(" ", "").splitlines()
        assert app_module in captured.out
        assert gunicorn_conf_path in captured.out
        assert "INFO" in captured.out
        assert "uvicorn.logging.DefaultFormatter" in captured.out
        assert "graceful_timeout=120" in captured_and_cleaned
        assert "keepalive=5" in captured_and_cleaned
        assert "loglevel=info" in captured_and_cleaned
        assert "timeout=120" in captured_and_cleaned
        assert f"workers={max(multiprocessing.cpu_count(), 2)}" in captured_and_cleaned

    @pytest.mark.parametrize("module", ("base", "fastapi", "starlette"))
    @pytest.mark.timeout(2)
    def test_gunicorn_config_with_custom_options(
        self,
        capfd: pytest.CaptureFixture,
        gunicorn_conf_tmp_file_path: Path,
        logging_conf_tmp_file_path: Path,
        monkeypatch: pytest.MonkeyPatch,
        module: str,
    ) -> None:
        """Customize options, load Gunicorn configuration file and verify output."""
        app_module = f"inboard.app.main_{module}:app"
        gunicorn_conf_path = str(gunicorn_conf_tmp_file_path)
        logging_conf_file = f"{logging_conf_tmp_file_path}/tmp_log.py"
        monkeypatch.setenv("GRACEFUL_TIMEOUT", "240")
        monkeypatch.setenv("KEEP_ALIVE", "10")
        monkeypatch.setenv("LOG_FORMAT", "verbose")
        monkeypatch.setenv("LOG_LEVEL", "debug")
        monkeypatch.setenv("LOGGING_CONF", logging_conf_file)
        monkeypatch.setenv("MAX_WORKERS", "10")
        monkeypatch.setenv("TIMEOUT", "240")
        monkeypatch.setenv("WEB_CONCURRENCY", "15")
        gunicorn_options = [
            "gunicorn",
            "--print-config",
            "-c",
            gunicorn_conf_path,
            "-k",
            "uvicorn.workers.UvicornWorker",
            app_module,
        ]
        subprocess.run(gunicorn_options)
        captured = capfd.readouterr()
        captured_and_cleaned = captured.out.replace(" ", "").splitlines()
        assert app_module in captured.out
        assert gunicorn_conf_path in captured.out
        assert "DEBUG" in captured.out
        assert "uvicorn.logging.DefaultFormatter" in captured.out
        assert "graceful_timeout=240" in captured_and_cleaned
        assert "keepalive=10" in captured_and_cleaned
        assert "loglevel=debug" in captured_and_cleaned
        assert "timeout=240" in captured_and_cleaned
        assert "workers=10" in captured_and_cleaned
