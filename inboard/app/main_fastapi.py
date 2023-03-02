import os
import sys
from typing import Optional

from fastapi import Depends, FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from inboard.app.utilities_fastapi import basic_auth

origin_regex = r"^(https?:\/\/)(localhost|([\w\.]+\.)?br3ndon.land)(:[0-9]+)?$"
server = (
    "Uvicorn"
    if (value := os.getenv("PROCESS_MANAGER")) and value.title() == "Uvicorn"
    else "Uvicorn, Gunicorn"
)
version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"


class GetRoot(BaseModel):
    Hello: str = "World"


class GetStatus(BaseModel):
    application: str
    status: str
    message: Optional[str]


class GetUser(BaseModel):
    username: str


app = FastAPI(title="inboard")
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"],
    allow_origin_regex=origin_regex,
)


@app.get("/", status_code=status.HTTP_200_OK)
async def get_root() -> GetRoot:
    return GetRoot()


@app.get("/health", status_code=status.HTTP_200_OK)
async def get_health(auth: str = Depends(basic_auth)) -> GetStatus:
    return GetStatus(application=app.title, status="active")


@app.get("/status", status_code=status.HTTP_200_OK)
async def get_status(auth: str = Depends(basic_auth)) -> GetStatus:
    return GetStatus(
        application=app.title,
        status="active",
        message=f"Hello World, from {server}, FastAPI, and Python {version}!",
    )


@app.get("/users/me", status_code=status.HTTP_200_OK)
async def get_current_user(username: str = Depends(basic_auth)) -> GetUser:
    return GetUser(username=username)
