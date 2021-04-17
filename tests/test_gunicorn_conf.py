import multiprocessing
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
        result = gunicorn_conf.calculate_workers(max_workers, None)
        assert result == int(max_workers) if max_workers else max(cores, 2)

    @pytest.mark.parametrize("total_workers", (None, "1", "2", "5", "10"))
    def test_calculate_workers_total(self, total_workers: Optional[str]) -> None:
        """Test Gunicorn worker process calculation with custom total."""
        cores = multiprocessing.cpu_count()
        result = gunicorn_conf.calculate_workers(None, total_workers)
        assert result == int(total_workers) if total_workers else max(cores, 2)

    @pytest.mark.parametrize("workers_per_core", ("0.5", "1.5", "10"))
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
