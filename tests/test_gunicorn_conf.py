import multiprocessing
import os
from typing import Optional

import pytest

from inboard import gunicorn_conf


class TestCalculateWorkers:
    """Test calculation of the number of Gunicorn worker processes.
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
            gunicorn_conf.calculate_workers(
                None, concurrency, workers_per_core, cores=cores
            )
            == 10
            if concurrency
            else max(int(cores * float(workers_per_core)), 2)
        )
