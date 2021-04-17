import multiprocessing
import os
from typing import Optional

from inboard.start import configure_logging


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


# Gunicorn setup
max_workers_str = os.getenv("MAX_WORKERS")
web_concurrency_str = os.getenv("WEB_CONCURRENCY")
workers_per_core_str = os.getenv("WORKERS_PER_CORE", "1")
workers = calculate_workers(max_workers_str, web_concurrency_str, workers_per_core_str)
worker_tmp_dir = "/dev/shm"
host = os.getenv("HOST", "0.0.0.0")
port = os.getenv("PORT", "80")
bind_env = os.getenv("BIND")
use_bind = bind_env or f"{host}:{port}"
use_loglevel = os.getenv("LOG_LEVEL", "info")
accesslog_var = os.getenv("ACCESS_LOG", "-")
use_accesslog = accesslog_var or None
errorlog_var = os.getenv("ERROR_LOG", "-")
use_errorlog = errorlog_var or None
graceful_timeout_str = os.getenv("GRACEFUL_TIMEOUT", "120")
timeout_str = os.getenv("TIMEOUT", "120")
keepalive_str = os.getenv("KEEP_ALIVE", "5")

# Gunicorn config variables
logconfig_dict = configure_logging(
    logging_conf=os.getenv("LOGGING_CONF", "inboard.logging_conf")
)
loglevel = use_loglevel
bind = use_bind
errorlog = use_errorlog
accesslog = use_accesslog
graceful_timeout = int(graceful_timeout_str)
timeout = int(timeout_str)
keepalive = int(keepalive_str)
