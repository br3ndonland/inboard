import os
import secrets

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials


async def basic_auth(credentials: HTTPBasicCredentials = Depends(HTTPBasic())) -> str:
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
