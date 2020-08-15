import os
import sys
from typing import Awaitable, Callable, Dict


class App:
    """Define a simple ASGI interface for use with Uvicorn.
    ---
    https://www.uvicorn.org/
    """

    def __init__(self, scope: Dict) -> None:
        assert scope["type"] == "http"
        self.scope = scope

    async def __call__(
        self, receive: Dict, send: Callable[[Dict], Awaitable]
    ) -> Dict[str, str]:
        await send(
            {
                "type": "http.response.start",
                "status": 200,
                "headers": [[b"content-type", b"text/plain"]],
            }
        )
        version = f"{sys.version_info.major}.{sys.version_info.minor}"
        server = "Uvicorn" if bool(os.getenv("WITH_RELOAD")) else "Uvicorn, Gunicorn,"
        message = f"Hello World, from {server} and Python {version}!"
        response: Dict = {"type": "http.response.body", "body": message.encode("utf-8")}
        await send(response)
        return response


app = App
