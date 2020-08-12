import sys

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse

version = f"{sys.version_info.major}.{sys.version_info.minor}"

app = Starlette()


@app.route("/")
async def homepage(request: Request) -> JSONResponse:
    message = f"Hello World, from Uvicorn, Gunicorn, Starlette, and Python {version}!"
    return JSONResponse({"message": message})
