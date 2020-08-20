import os
import sys
from typing import Dict

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from inboard.app.utilities import basic_auth

server = "Uvicorn" if bool(os.getenv("WITH_RELOAD")) else "Uvicorn, Gunicorn"
version = f"{sys.version_info.major}.{sys.version_info.minor}"

app = FastAPI(title="inboard")

app.add_middleware(
    CORSMiddleware,
    allow_origins="https://br3ndon.land",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def get_root() -> Dict[str, str]:
    return {"Hello": "World"}


@app.get("/health")
def get_health(auth: str = Depends(basic_auth)) -> Dict[str, str]:
    return {"application": app.title, "status": "active"}


@app.get("/status")
def get_status(auth: str = Depends(basic_auth)) -> Dict[str, str]:
    message = f"Hello World, from {server}, FastAPI, and Python {version}!"
    return {"application": app.title, "status": "active", "message": message}


@app.get("/users/me")
def get_current_user(username: str = Depends(basic_auth)) -> Dict[str, str]:
    return {"username": username}
