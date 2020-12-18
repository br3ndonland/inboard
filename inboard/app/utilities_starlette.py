import base64
import os
from secrets import compare_digest
from typing import Optional, Tuple

from starlette.authentication import (
    AuthCredentials,
    AuthenticationBackend,
    AuthenticationError,
    SimpleUser,
)
from starlette.requests import HTTPConnection


class BasicAuth(AuthenticationBackend):
    async def authenticate(
        self, request: HTTPConnection
    ) -> Optional[Tuple[AuthCredentials, SimpleUser]]:
        if "Authorization" not in request.headers:
            return None

        auth = request.headers["Authorization"]
        try:
            scheme, credentials = auth.split()
            decoded = base64.b64decode(credentials).decode("ascii")
            username, _, password = decoded.partition(":")
            correct_username = compare_digest(
                username, str(os.getenv("BASIC_AUTH_USERNAME", "test_username"))
            )
            correct_password = compare_digest(
                password,
                str(os.getenv("BASIC_AUTH_PASSWORD", "plunge-germane-tribal-pillar")),
            )
            if not (correct_username and correct_password):
                raise AuthenticationError("Invalid basic auth credentials")
            return AuthCredentials(["authenticated"]), SimpleUser(username)
        except Exception:
            raise
