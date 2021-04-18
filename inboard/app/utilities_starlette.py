import base64
import os
import secrets
from typing import Optional, Tuple

from starlette.authentication import (
    AuthCredentials,
    AuthenticationBackend,
    AuthenticationError,
    SimpleUser,
)
from starlette.requests import HTTPConnection


class BasicAuth(AuthenticationBackend):
    """Configure HTTP Basic auth for Starlette."""

    async def authenticate(
        self, request: HTTPConnection
    ) -> Optional[Tuple[AuthCredentials, SimpleUser]]:
        """Authenticate a Starlette request with HTTP Basic auth."""
        if "Authorization" not in request.headers:
            return None
        try:
            auth = request.headers["Authorization"]
            basic_auth_username = os.getenv("BASIC_AUTH_USERNAME")
            basic_auth_password = os.getenv("BASIC_AUTH_PASSWORD")
            if not (basic_auth_username and basic_auth_password):
                raise AuthenticationError("Server HTTP Basic auth credentials not set")
            scheme, credentials = auth.split()
            decoded = base64.b64decode(credentials).decode("ascii")
            username, _, password = decoded.partition(":")
            correct_username = secrets.compare_digest(username, basic_auth_username)
            correct_password = secrets.compare_digest(password, basic_auth_password)
            if not (correct_username and correct_password):
                raise AuthenticationError("HTTP Basic auth credentials not correct")
            return AuthCredentials(["authenticated"]), SimpleUser(username)
        except Exception:
            raise
