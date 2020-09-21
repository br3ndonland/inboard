import multiprocessing
import os
from typing import Optional

from inboard.start import configure_logging


def calculate_workers(
    max_workers_str: Optional[str],
    web_concurrency_str: Optional[str],
    workers_per_core_str: str,
    cores: int = multiprocessing.cpu_count(),
) -> int:
    """Calculate the number of Gunicorn worker processes."""
    use_default_workers = max(int(float(workers_per_core_str) * cores), 2)
    if max_workers_str and int(max_workers_str) > 0:
        use_max_workers = int(max_workers_str)
    if web_concurrency_str and int(web_concurrency_str) > 0:
        use_web_concurrency = int(web_concurrency_str)
    return (
        min(use_max_workers, use_web_concurrency)
        if max_workers_str and web_concurrency_str
        else use_web_concurrency
        if web_concurrency_str
        else use_default_workers
    )


# Gunicorn setup
max_workers_str = os.getenv("MAX_WORKERS", None)
web_concurrency_str = os.getenv("WEB_CONCURRENCY", None)
workers_per_core_str = os.getenv("WORKERS_PER_CORE", "1")
workers = calculate_workers(max_workers_str, web_concurrency_str, workers_per_core_str)
worker_tmp_dir = "/dev/shm"
host = os.getenv("HOST", "0.0.0.0")
port = os.getenv("PORT", "80")
bind_env = os.getenv("BIND", None)
use_bind = bind_env if bind_env else f"{host}:{port}"
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
