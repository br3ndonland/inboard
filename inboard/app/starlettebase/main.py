import os
import sys

from starlette.applications import Starlette
from starlette.authentication import requires
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from inboard.app.utilities import BasicAuth

server = "Uvicorn" if bool(os.getenv("WITH_RELOAD")) else "Uvicorn, Gunicorn"
version = f"{sys.version_info.major}.{sys.version_info.minor}"


def on_auth_error(request: Request, e: Exception) -> JSONResponse:
    return JSONResponse(
        {"detail": "Incorrect username or password", "error": str(e)}, status_code=401
    )


app = Starlette()
app.add_middleware(
    AuthenticationMiddleware,
    backend=BasicAuth(),
    on_error=on_auth_error,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins="https://br3ndon.land",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.route("/")
async def get_root(request: Request) -> JSONResponse:
    return JSONResponse({"Hello": "World"})


@app.route("/health")
@requires("authenticated")
def get_health(request: Request) -> JSONResponse:
    return JSONResponse({"application": "inboard", "status": "active"})


@app.route("/status")
@requires("authenticated")
def get_status(request: Request) -> JSONResponse:
    message = f"Hello World, from {server}, Starlette, and Python {version}!"
    return JSONResponse(
        {"application": "inboard", "status": "active", "message": message}
    )


@app.route("/users/me")
@requires("authenticated")
def get_current_user(request: Request) -> JSONResponse:
    return JSONResponse({"username": request.user.display_name})
