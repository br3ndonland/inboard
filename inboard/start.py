#!/usr/bin/env python3
import importlib.util
import logging
import logging.config
import os
import subprocess
from logging import Logger
from pathlib import Path
from typing import Any, Dict

import uvicorn  # type: ignore


def set_conf_path(module_stem: str) -> str:
    """Set the path to a configuration file."""
    conf_var = str(
        os.getenv(f"{module_stem.upper()}_CONF", f"/app/inboard/{module_stem}_conf.py")
    )
    if conf_var and Path(conf_var).is_file():
        conf_path = conf_var
    else:
        raise FileNotFoundError(f"Unable to find {conf_var}")
    return conf_path


def configure_logging(
    logger: Logger = logging.getLogger(),
    logging_conf: str = os.getenv("LOGGING_CONF", "inboard.logging_conf"),
) -> Dict[str, Any]:
    """Configure Python logging based on a path to a logging module or file."""
    try:
        logging_conf_path = Path(logging_conf)
        spec = (
            importlib.util.spec_from_file_location("confspec", logging_conf_path)
            if logging_conf_path.is_file() and logging_conf_path.suffix == ".py"
            else importlib.util.find_spec(logging_conf)
        )
        if spec:
            logging_conf_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(logging_conf_module)  # type: ignore[union-attr]
        if hasattr(logging_conf_module, "LOGGING_CONFIG"):
            logging_conf_dict = getattr(logging_conf_module, "LOGGING_CONFIG")
        else:
            raise AttributeError(f"No LOGGING_CONFIG in {logging_conf_module}.")
        if isinstance(logging_conf_dict, dict):
            logging.config.dictConfig(logging_conf_dict)
            message = f"Logging dict config loaded from {logging_conf_path}."
            logger.debug(message)
            return logging_conf_dict
        else:
            raise TypeError("LOGGING_CONFIG is not a dictionary instance.")
    except Exception as e:
        message = f"Error when setting logging module: {e}."
        logger.debug(message)
        raise


def set_app_module(logger: Logger = logging.getLogger()) -> str:
    """Set the name of the Python module with the app instance to run."""
    try:
        app_module = str(os.getenv("APP_MODULE"))
        importlib.util.find_spec(app_module)
        logger.debug(f"App module set to {app_module}.")
        return app_module
    except Exception as e:
        message = f"Error when setting app module: {e}."
        logger.debug(message)
        raise


def run_pre_start_script(logger: Logger = logging.getLogger()) -> str:
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


def start_server(
    process_manager: str,
    app_module: str = str(os.getenv("APP_MODULE", "inboard.app.base.main:app")),
    logger: Logger = logging.getLogger(),
    logging_conf_dict: Dict[str, Any] = None,
    with_reload: bool = bool(os.getenv("WITH_RELOAD", False)),
    worker_class: str = str(os.getenv("WORKER_CLASS", "uvicorn.workers.UvicornWorker")),
) -> None:
    """Start the Uvicorn or Gunicorn server."""
    try:
        if process_manager == "gunicorn":
            logger.debug("Running Uvicorn with Gunicorn.")
            gunicorn_conf_path = set_conf_path("gunicorn")
            subprocess.run(
                ["gunicorn", "-k", worker_class, "-c", gunicorn_conf_path, app_module]
            )
        elif process_manager == "uvicorn":
            logger.debug("Running Uvicorn without Gunicorn.")
            uvicorn.run(
                app_module,
                host=os.getenv("HOST", "0.0.0.0"),
                port=int(os.getenv("PORT", "80")),
                log_config=logging_conf_dict,
                log_level=os.getenv("LOG_LEVEL", "info"),
                reload=with_reload,
            )
        else:
            raise NameError("Process manager needs to be either uvicorn or gunicorn.")
    except Exception as e:
        logger.debug(f"Error when starting server with start script: {e}")
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
