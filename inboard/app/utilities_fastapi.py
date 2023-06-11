import os
import secrets
import sys

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

if sys.version_info < (3, 9):  # pragma: no cover
    from typing_extensions import Annotated
else:  # pragma: no cover
    from typing import Annotated

HTTPBasicCredentialsDependency = Annotated[HTTPBasicCredentials, Depends(HTTPBasic())]


async def basic_auth(credentials: HTTPBasicCredentialsDependency) -> str:
    """Authenticate a FastAPI request with HTTP Basic auth."""
    basic_auth_username = os.getenv("BASIC_AUTH_USERNAME")
    basic_auth_password = os.getenv("BASIC_AUTH_PASSWORD")
    if not (basic_auth_username and basic_auth_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Server HTTP Basic auth credentials not set",
            headers={"WWW-Authenticate": "Basic"},
        )
    correct_username = secrets.compare_digest(credentials.username, basic_auth_username)
    correct_password = secrets.compare_digest(credentials.password, basic_auth_password)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="HTTP Basic auth credentials not correct",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username
