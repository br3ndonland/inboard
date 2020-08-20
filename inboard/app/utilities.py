import os
from secrets import compare_digest

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials


def basic_auth(credentials: HTTPBasicCredentials = Depends(HTTPBasic())) -> str:
    correct_username = compare_digest(
        credentials.username, str(os.getenv("BASIC_AUTH_USERNAME"))
    )
    correct_password = compare_digest(
        credentials.password, str(os.getenv("BASIC_AUTH_PASSWORD"))
    )
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username
