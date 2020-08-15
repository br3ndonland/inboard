import os
import sys

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse

server = "Uvicorn" if bool(os.getenv("WITH_RELOAD")) else "Uvicorn, Gunicorn"
version = f"{sys.version_info.major}.{sys.version_info.minor}"

app = Starlette()


@app.route("/")
async def homepage(request: Request) -> JSONResponse:
    message = f"Hello World, from {server}, Starlette, and Python {version}!"
    return JSONResponse({"message": message})
