import multiprocessing
import os
from typing import Optional

from inboard.logging_conf import configure_logging


def calculate_workers(
    max_workers: Optional[str] = None,
    total_workers: Optional[str] = None,
    workers_per_core: str = "1",
) -> int:
    """Calculate the number of Gunicorn worker processes."""
    cores = multiprocessing.cpu_count()
    use_default = max(int(float(workers_per_core) * cores), 2)
    use_max = m if max_workers and (m := int(max_workers)) > 0 else False
    use_total = t if total_workers and (t := int(total_workers)) > 0 else False
    use_least = min(use_max, use_total) if use_max and use_total else False
    return use_least or use_max or use_total or use_default


# Gunicorn settings
bind = os.getenv("BIND") or f'{os.getenv("HOST", "0.0.0.0")}:{os.getenv("PORT", "80")}'
accesslog = os.getenv("ACCESS_LOG", "-")
errorlog = os.getenv("ERROR_LOG", "-")
graceful_timeout = int(os.getenv("GRACEFUL_TIMEOUT", "120"))
keepalive = int(os.getenv("KEEP_ALIVE", "5"))
logconfig_dict = configure_logging()
loglevel = os.getenv("LOG_LEVEL", "info")
timeout = int(os.getenv("TIMEOUT", "120"))
worker_tmp_dir = "/dev/shm"
workers = calculate_workers(
    os.getenv("MAX_WORKERS"),
    os.getenv("WEB_CONCURRENCY"),
    workers_per_core=os.getenv("WORKERS_PER_CORE", "1"),
)
