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
        process_manager = os.getenv("PROCESS_MANAGER", "gunicorn")
        if process_manager not in ["gunicorn", "uvicorn"]:
            raise NameError("Process manager needs to be either uvicorn or gunicorn.")
        server = "Uvicorn" if process_manager == "uvicorn" else "Uvicorn, Gunicorn,"
        message = f"Hello World, from {server} and Python {version}!"
        response: Dict = {"type": "http.response.body", "body": message.encode("utf-8")}
        await send(response)
        return response


app: Callable = App
