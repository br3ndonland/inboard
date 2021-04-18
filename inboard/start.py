#!/usr/bin/env python3
import importlib.util
import logging
import os
import subprocess
from pathlib import Path
from typing import Optional

import uvicorn  # type: ignore

from inboard.logging_conf import configure_logging


def run_pre_start_script(logger: logging.Logger = logging.getLogger()) -> str:
    """Run a pre-start script at the provided path."""
    logger.debug("Checking for pre-start script.")
    pre_start_path = os.getenv("PRE_START_PATH", "/app/inboard/app/prestart.py")
    if Path(pre_start_path).is_file():
        process = "python" if Path(pre_start_path).suffix == ".py" else "sh"
        run_message = f"Running pre-start script with {process} {pre_start_path}."
        logger.debug(run_message)
        subprocess.run([process, pre_start_path])
        message = f"Ran pre-start script with {process} {pre_start_path}."
    else:
        message = "No pre-start script found."
    logger.debug(message)
    return message


def set_app_module(logger: logging.Logger = logging.getLogger()) -> str:
    """Set the name of the Python module with the app instance to run."""
    try:
        app_module = str(os.getenv("APP_MODULE"))
        if not importlib.util.find_spec((module := app_module.split(sep=":")[0])):
            raise ImportError(f"Unable to find or import {module}")
        logger.debug(f"App module set to {app_module}.")
        return app_module
    except Exception as e:
        logger.error(f"Error when setting app module: {e.__class__.__name__} {e}.")
        raise


def set_gunicorn_options(app_module: str) -> list:
    """Set options for running the Gunicorn server."""
    gunicorn_conf_path = os.getenv("GUNICORN_CONF", "/app/inboard/gunicorn_conf.py")
    worker_class = os.getenv("WORKER_CLASS", "uvicorn.workers.UvicornWorker")
    if not Path(gunicorn_conf_path).is_file():
        raise FileNotFoundError(f"Unable to find {gunicorn_conf_path}")
    return ["gunicorn", "-k", worker_class, "-c", gunicorn_conf_path, app_module]


def set_uvicorn_options(log_config: Optional[dict] = None) -> dict:
    """Set options for running the Uvicorn server."""
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "80"))
    log_level = os.getenv("LOG_LEVEL", "info")
    reload_dirs = (
        [d.lstrip() for d in str(os.getenv("RELOAD_DIRS")).split(sep=",")]
        if os.getenv("RELOAD_DIRS")
        else None
    )
    use_reload = (
        True
        if (value := os.getenv("WITH_RELOAD")) and value.lower() == "true"
        else False
    )
    return dict(
        host=host,
        port=port,
        log_config=log_config,
        log_level=log_level,
        reload_dirs=reload_dirs,
        reload=use_reload,
    )


def start_server(
    process_manager: str,
    app_module: str,
    logger: logging.Logger = logging.getLogger(),
    logging_conf_dict: Optional[dict] = None,
) -> None:
    """Start the Uvicorn or Gunicorn server."""
    try:
        if process_manager == "gunicorn":
            logger.debug("Running Uvicorn with Gunicorn.")
            gunicorn_options: list = set_gunicorn_options(app_module)
            subprocess.run(gunicorn_options)
        elif process_manager == "uvicorn":
            logger.debug("Running Uvicorn without Gunicorn.")
            uvicorn_options: dict = set_uvicorn_options(log_config=logging_conf_dict)
            uvicorn.run(app_module, **uvicorn_options)
        else:
            raise NameError("Process manager needs to be either uvicorn or gunicorn")
    except Exception as e:
        logger.error(f"Error when starting server: {e.__class__.__name__} {e}.")
        raise


if __name__ == "__main__":  # pragma: no cover
    logger = logging.getLogger()
    logging_conf_dict = configure_logging(logger=logger)
    run_pre_start_script(logger=logger)
    start_server(
        str(os.getenv("PROCESS_MANAGER", "gunicorn")),
        app_module=set_app_module(logger=logger),
        logger=logger,
        logging_conf_dict=logging_conf_dict,
    )
