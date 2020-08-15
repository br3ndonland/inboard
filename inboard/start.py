#!/usr/bin/env python3
import os
import subprocess
from pathlib import Path
from typing import Tuple

import uvicorn


def set_app_module() -> str:
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


def set_gunicorn_conf() -> Tuple[str, str]:
    if Path("/app/gunicorn_conf.py").is_file():
        default_gunicorn_conf = "/app/gunicorn_conf.py"
    elif Path("/app/app/gunicorn_conf.py").is_file():
        default_gunicorn_conf = "/app/app/gunicorn_conf.py"
    else:
        default_gunicorn_conf = "/gunicorn_conf.py"
    gunicorn_conf = os.getenv("GUNICORN_CONF", default_gunicorn_conf)
    os.environ["GUNICORN_CONF"] = gunicorn_conf
    worker_class = os.getenv("WORKER_CLASS", "uvicorn.workers.UvicornWorker")
    os.environ["WORKER_CLASS"] = worker_class
    return gunicorn_conf, worker_class


def run_pre_start_script(
    pre_start_path: str = os.getenv("PRE_START_PATH", "/app/prestart.py")
) -> None:
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
    gunicorn_conf: str = str(os.getenv("GUNICORN_CONF", "/gunicorn_conf.py")),
    with_reload: bool = bool(os.getenv("WITH_RELOAD", False)),
    worker_class: str = str(os.getenv("WORKER_CLASS", "uvicorn.workers.UvicornWorker")),
) -> None:
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
            ["gunicorn", "-k", worker_class, "-c", gunicorn_conf, app_module]
        )


if __name__ == "__main__":
    set_app_module()
    set_gunicorn_conf()
    run_pre_start_script()
    start_server()
