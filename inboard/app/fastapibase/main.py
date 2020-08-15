import os
import sys
from typing import Dict

from fastapi import FastAPI

server = "Uvicorn" if bool(os.getenv("WITH_RELOAD")) else "Uvicorn, Gunicorn"
version = f"{sys.version_info.major}.{sys.version_info.minor}"

app = FastAPI()


@app.get("/")
async def root() -> Dict[str, str]:
    message = f"Hello World, from {server}, FastAPI, and Python {version}!"
    return {"message": message}
