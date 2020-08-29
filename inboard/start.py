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


def set_conf_path(module: str) -> Path:
    """Set the path to a configuration file."""
    conf_var = str(os.getenv(f"{module.upper()}_CONF"))
    if Path(conf_var).is_file():
        conf_path = conf_var
    elif Path(f"/app/{module}_conf.py").is_file():
        conf_path = f"/app/{module}_conf.py"
    elif Path(f"/app/app/{module}_conf.py").is_file():
        conf_path = f"/app/app/{module}_conf.py"
    else:
        conf_path = f"/{module}_conf.py"
    os.environ[f"{module.upper()}_CONF"] = conf_path
    return Path(conf_path)


def configure_logging(
    logger: Logger = logging.getLogger(), logging_conf: Path = Path("/logging_conf.py")
) -> Dict[str, Any]:
    """Configure Python logging based on a path to a logging configuration file."""
    try:
        if isinstance(logging_conf, Path) and logging_conf.suffix == ".py":
            spec = importlib.util.spec_from_file_location("confspec", logging_conf)
            logging_conf_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(logging_conf_module)  # type: ignore
            if hasattr(logging_conf_module, "LOGGING_CONFIG"):
                logging_conf_dict = getattr(logging_conf_module, "LOGGING_CONFIG")
            else:
                raise AttributeError(f"No LOGGING_CONFIG in {logging_conf_module}.")
            if isinstance(logging_conf_dict, dict):
                logging.config.dictConfig(logging_conf_dict)
                message = f"Logging dict config loaded from {logging_conf}."
                logger.debug(message)
                return logging_conf_dict
            else:
                raise TypeError("LOGGING_CONFIG is not a dictionary instance.")
        else:
            raise ImportError("Valid path to .py logging config file required.")
    except Exception as e:
        message = f"Error when configuring logging: {e}"
        logger.debug(message)
        raise


def set_app_module(logger: Logger = logging.getLogger()) -> str:
    """Set the name of the Python module with the app instance to run."""
    if Path("/app/main.py").is_file():
        default_module_name = "main"
    elif Path("/app/app/main.py").is_file():
        default_module_name = "app.main"
    else:
        default_module_name = "base.main"
    module_name = os.getenv("MODULE_NAME", default_module_name)
    variable_name = os.getenv("VARIABLE_NAME", "app")
    app_module = os.getenv("APP_MODULE", f"{module_name}:{variable_name}")
    os.environ["APP_MODULE"] = app_module
    logger.debug(f"App module set to {app_module}.")
    return app_module


def run_pre_start_script(logger: Logger = logging.getLogger()) -> str:
    """Run a pre-start script at the provided path."""
    try:
        logger.debug("Checking for pre-start script.")
        pre_start_path = None
        pre_start_path_var = os.getenv("PRE_START_PATH", "/app/prestart.py")
        if Path(pre_start_path_var).is_file():
            pre_start_path = pre_start_path_var
        elif Path("/app/app/prestart.py").is_file():
            pre_start_path = "/app/app/prestart.py"
        else:
            message = "No pre-start script found."
        if pre_start_path:
            process = "python" if Path(pre_start_path).suffix == ".py" else "sh"
            run_message = f"Running pre-start script with {process} {pre_start_path}."
            logger.debug(run_message)
            subprocess.run([process, pre_start_path])
            message = f"Ran pre-start script with {process} {pre_start_path}."
    except Exception as e:
        message = f"Error from pre-start script: {e}"
    finally:
        logger.debug(message)
        return message


def start_server(
    app_module: str = str(os.getenv("APP_MODULE", "base.main:app")),
    gunicorn_conf: Path = Path("/gunicorn_conf.py"),
    logger: Logger = logging.getLogger(),
    logging_conf_dict: Dict[str, Any] = None,
    with_reload: bool = bool(os.getenv("WITH_RELOAD", False)),
    worker_class: str = str(os.getenv("WORKER_CLASS", "uvicorn.workers.UvicornWorker")),
) -> None:
    """Start the Uvicorn or Gunicorn server."""
    try:
        if with_reload:
            logger.debug("Running Uvicorn without Gunicorn and with reloading")
            uvicorn.run(
                app_module,
                host=os.getenv("HOST", "0.0.0.0"),
                port=int(os.getenv("PORT", "80")),
                log_config=logging_conf_dict,
                log_level=os.getenv("LOG_LEVEL", "info"),
                reload=True,
            )
        else:
            logger.debug("Running Uvicorn with Gunicorn.")
            subprocess.run(
                ["gunicorn", "-k", worker_class, "-c", gunicorn_conf.name, app_module]
            )
    except Exception as e:
        logger.debug(f"Error when starting server with start script: {e}")


if __name__ == "__main__":
    logger = logging.getLogger()
    logging_conf_path = set_conf_path("logging")
    logging_conf_dict = configure_logging(logger=logger, logging_conf=logging_conf_path)
    gunicorn_conf_path = set_conf_path("gunicorn")
    app_module = set_app_module(logger=logger)
    run_pre_start_script(logger=logger)
    start_server(
        app_module=app_module,
        gunicorn_conf=gunicorn_conf_path,
        logger=logger,
        logging_conf_dict=logging_conf_dict,
    )
