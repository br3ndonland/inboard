#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import logging
import os
import subprocess
from pathlib import Path
from typing import TYPE_CHECKING

import uvicorn

from inboard.logging_conf import configure_logging

if TYPE_CHECKING:
    from inboard.types import DictConfig, UvicornOptions


def run_pre_start_script(logger: logging.Logger = logging.getLogger()) -> str:
    """Run a pre-start script at the provided path."""
    pre_start_path = os.getenv("PRE_START_PATH")
    logger.debug("Checking for pre-start script.")
    if not pre_start_path:
        message = "No pre-start script specified."
    elif Path(pre_start_path).is_file():
        process = "python" if Path(pre_start_path).suffix == ".py" else "sh"
        run_message = f"Running pre-start script with {process} {pre_start_path}."
        logger.debug(run_message)
        subprocess.run([process, pre_start_path], check=True)
        message = f"Ran pre-start script with {process} {pre_start_path}."
    else:
        message = "No pre-start script found."
    logger.debug(message)
    return message


def set_app_module(logger: logging.Logger = logging.getLogger()) -> str:
    """Set the name of the Python module with the app instance to run."""
    try:
        app_module = os.getenv("APP_MODULE")
        if not app_module:
            raise ValueError("Please set the APP_MODULE environment variable")
        if not importlib.util.find_spec((module := app_module.split(sep=":")[0])):
            raise ImportError(f"Unable to find or import {module}")
        logger.debug(f"App module set to {app_module}.")
        return app_module
    except Exception as e:
        logger.error(f"Error when setting app module: {e.__class__.__name__} {e}.")
        raise


def set_gunicorn_options(app_module: str) -> list[str]:
    """Set options for running the Gunicorn server."""
    gunicorn_conf_path = os.getenv("GUNICORN_CONF", "python:inboard.gunicorn_conf")
    worker_class = os.getenv("WORKER_CLASS", "uvicorn.workers.UvicornWorker")
    if "python:" not in gunicorn_conf_path and not Path(gunicorn_conf_path).is_file():
        raise FileNotFoundError(f"Unable to find {gunicorn_conf_path}")
    return ["gunicorn", "-k", worker_class, "-c", gunicorn_conf_path, app_module]


def _split_uvicorn_option(option: str) -> list[str] | None:
    return (
        [option_item.strip() for option_item in str(option_value).split(sep=",")]
        if (option_value := os.getenv(option.upper()))
        else None
    )


def _update_uvicorn_options(uvicorn_options: UvicornOptions) -> UvicornOptions:
    if uvicorn.__version__ >= "0.15.0":
        reload_delay = float(value) if (value := os.getenv("RELOAD_DELAY")) else 0.25
        reload_excludes = _split_uvicorn_option("RELOAD_EXCLUDES")
        reload_includes = _split_uvicorn_option("RELOAD_INCLUDES")
        uvicorn_options["reload_delay"] = reload_delay
        uvicorn_options["reload_includes"] = reload_includes
        uvicorn_options["reload_excludes"] = reload_excludes
    if value := os.getenv("UVICORN_CONFIG_OPTIONS"):
        uvicorn_options_json = json.loads(value)
        uvicorn_options.update(uvicorn_options_json)
    return uvicorn_options


def set_uvicorn_options(
    app_module: str,
    log_config: DictConfig | None = None,
) -> UvicornOptions:
    """Set options for running the Uvicorn server."""
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "80"))
    log_level = os.getenv("LOG_LEVEL", "info")
    reload_dirs = _split_uvicorn_option("RELOAD_DIRS")
    use_reload = bool((value := os.getenv("WITH_RELOAD")) and value.lower() == "true")
    uvicorn_options: UvicornOptions = dict(
        app=app_module,
        host=host,
        port=port,
        log_config=log_config,
        log_level=log_level,
        reload=use_reload,
        reload_dirs=reload_dirs,
    )
    return _update_uvicorn_options(uvicorn_options)


def start_server(
    process_manager: str,
    app_module: str,
    logger: logging.Logger = logging.getLogger(),
    logging_conf_dict: DictConfig | None = None,
) -> None:
    """Start the Uvicorn or Gunicorn server."""
    try:
        if process_manager == "gunicorn":
            logger.debug("Running Uvicorn with Gunicorn.")
            gunicorn_options: list[str] = set_gunicorn_options(app_module)
            subprocess.run(gunicorn_options)
        elif process_manager == "uvicorn":
            logger.debug("Running Uvicorn without Gunicorn.")
            uvicorn_options: UvicornOptions = set_uvicorn_options(
                app_module, log_config=logging_conf_dict
            )
            uvicorn.run(**uvicorn_options)  # type: ignore[arg-type]
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
