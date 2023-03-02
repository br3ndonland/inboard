import os
import sys

from starlette.applications import Starlette
from starlette.authentication import requires
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

from inboard.app.utilities_starlette import BasicAuth

origin_regex = r"^(https?:\/\/)(localhost|([\w\.]+\.)?br3ndon.land)(:[0-9]+)?$"
server = (
    "Uvicorn"
    if (value := os.getenv("PROCESS_MANAGER")) and value.title() == "Uvicorn"
    else "Uvicorn, Gunicorn"
)
version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"


def on_auth_error(request: Request, e: Exception) -> JSONResponse:
    return JSONResponse(
        {"error": "Incorrect username or password", "detail": str(e)}, status_code=401
    )


async def get_root(request: Request) -> JSONResponse:
    return JSONResponse({"Hello": "World"})


@requires("authenticated")
async def get_health(request: Request) -> JSONResponse:
    return JSONResponse({"application": "inboard", "status": "active"})


@requires("authenticated")
async def get_status(request: Request) -> JSONResponse:
    message = f"Hello World, from {server}, Starlette, and Python {version}!"
    return JSONResponse(
        {"application": "inboard", "status": "active", "message": message}
    )


@requires("authenticated")
async def get_current_user(request: Request) -> JSONResponse:
    return JSONResponse({"username": request.user.display_name})


routes = [
    Route("/", endpoint=get_root),
    Route("/health", endpoint=get_health),
    Route("/status", endpoint=get_status),
    Route("/users/me", endpoint=get_current_user),
]
app = Starlette(routes=routes)
app.add_middleware(
    AuthenticationMiddleware,
    backend=BasicAuth(),
    on_error=on_auth_error,
)
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"],
    allow_origin_regex=origin_regex,
)
