#!/usr/bin/env python3
import os
import subprocess
from pathlib import Path

import uvicorn  # type: ignore


def set_app_module() -> str:
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
    return app_module


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


def run_pre_start_script(
    pre_start_path: str = os.getenv("PRE_START_PATH", "/app/prestart.py")
) -> None:
    """Run a pre-start script at the provided path."""
    try:
        print(f"Checking for pre-start script in {pre_start_path}.")
        if Path(pre_start_path).is_file():
            process = "python" if Path(pre_start_path).suffix == ".py" else "sh"
            print(f"Running pre-start script {process} {pre_start_path}.")
            subprocess.run([process, pre_start_path])
        else:
            print("No pre-start script found.")
    except Exception as e:
        print(f"Error when running pre-start script: {e}")


def start_server(
    app_module: str = str(os.getenv("APP_MODULE", "base.main:app")),
    gunicorn_conf: Path = Path("/gunicorn_conf.py"),
    with_reload: bool = bool(os.getenv("WITH_RELOAD", False)),
    worker_class: str = str(os.getenv("WORKER_CLASS", "uvicorn.workers.UvicornWorker")),
) -> None:
    """Start the Uvicorn or Gunicorn server."""
    if with_reload:
        uvicorn.run(
            app_module,
            host=os.getenv("HOST", "0.0.0.0"),
            port=int(os.getenv("PORT", "80")),
            log_level=os.getenv("LOG_LEVEL", "info"),
            reload=True,
        )
    else:
        subprocess.run(
            ["gunicorn", "-k", worker_class, "-c", gunicorn_conf.name, app_module]
        )


if __name__ == "__main__":
    app_module = set_app_module()
    gunicorn_conf_path = set_conf_path("gunicorn")
    logging_conf_path = set_conf_path("logging")
    run_pre_start_script()
    start_server(
        app_module=app_module, gunicorn_conf=gunicorn_conf_path,
    )
