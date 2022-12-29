from __future__ import annotations

import os
import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from asgiref.typing import (
        ASGIReceiveCallable,
        ASGISendCallable,
        HTTPResponseBodyEvent,
        HTTPResponseStartEvent,
        Scope,
    )


def _compose_message() -> str:
    version = (
        f"{sys.version_info.major}.{sys.version_info.minor}"
        f".{sys.version_info.micro}"
    )
    process_manager = os.getenv("PROCESS_MANAGER", "gunicorn")
    if process_manager not in {"gunicorn", "uvicorn"}:
        raise NameError("Process manager needs to be either uvicorn or gunicorn.")
    server = "Uvicorn" if process_manager == "uvicorn" else "Uvicorn, Gunicorn,"
    return f"Hello World, from {server} and Python {version}!"


async def app(
    scope: Scope, receive: ASGIReceiveCallable, send: ASGISendCallable
) -> None:
    """Define a simple ASGI 3 application for use with Uvicorn.

    https://asgi.readthedocs.io/en/stable/introduction.html
    https://asgi.readthedocs.io/en/stable/specs/main.html#applications
    https://www.uvicorn.org/
    """
    assert scope["type"] == "http"
    message = _compose_message()
    start_event: HTTPResponseStartEvent = {
        "type": "http.response.start",
        "status": 200,
        "headers": [(b"content-type", b"text/plain")],
        "trailers": False,
    }
    body_event: HTTPResponseBodyEvent = {
        "type": "http.response.body",
        "body": message.encode("utf-8"),
        "more_body": False,
    }
    await send(start_event)
    await send(body_event)
