import sys
from typing import Dict

from fastapi import FastAPI

version = f"{sys.version_info.major}.{sys.version_info.minor}"

app = FastAPI()


@app.get("/")
async def root() -> Dict[str, str]:
    message = f"Hello World, from Uvicorn, Gunicorn, FastAPI, and Python {version}!"
    return {"message": message}
