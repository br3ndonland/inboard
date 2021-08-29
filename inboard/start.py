#!/usr/bin/env python3
import importlib.util
import json
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


def _split_uvicorn_option(option: str) -> Optional[list]:
    return (
        [option_item.strip() for option_item in str(option_value).split(sep=",")]
        if (option_value := os.getenv(option.upper()))
        else None
    )


def _update_uvicorn_config_options(uvicorn_config_options: dict) -> dict:
    if uvicorn.__version__ >= "0.15.0":
        reload_delay = float(value) if (value := os.getenv("RELOAD_DELAY")) else None
        reload_excludes = _split_uvicorn_option("RELOAD_EXCLUDES")
        reload_includes = _split_uvicorn_option("RELOAD_INCLUDES")
        uvicorn_config_options_015 = dict(
            reload_delay=reload_delay,
            reload_excludes=reload_excludes,
            reload_includes=reload_includes,
        )
        uvicorn_config_options.update(uvicorn_config_options_015)
    if value := os.getenv("UVICORN_CONFIG_OPTIONS"):
        uvicorn_config_options_json = json.loads(value)
        uvicorn_config_options.update(uvicorn_config_options_json)
    return uvicorn_config_options


def set_uvicorn_options(log_config: Optional[dict] = None) -> dict:
    """Set options for running the Uvicorn server."""
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "80"))
    log_level = os.getenv("LOG_LEVEL", "info")
    reload_dirs = _split_uvicorn_option("RELOAD_DIRS")
    use_reload = bool((value := os.getenv("WITH_RELOAD")) and value.lower() == "true")
    uvicorn_config_options = dict(
        host=host,
        port=port,
        log_config=log_config,
        log_level=log_level,
        reload=use_reload,
        reload_dirs=reload_dirs,
    )
    return _update_uvicorn_config_options(uvicorn_config_options)


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
