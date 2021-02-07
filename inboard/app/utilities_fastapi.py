import os
from pathlib import Path
from secrets import compare_digest
from typing import List, Optional

import toml
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel, BaseSettings


async def basic_auth(credentials: HTTPBasicCredentials = Depends(HTTPBasic())) -> str:
    correct_username = compare_digest(
        credentials.username, str(os.getenv("BASIC_AUTH_USERNAME", "test_username"))
    )
    correct_password = compare_digest(
        credentials.password,
        str(os.getenv("BASIC_AUTH_PASSWORD", "plunge-germane-tribal-pillar")),
    )
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


def set_fields_from_pyproject(
    fields: dict,
    pyproject_path: Path = Path(__file__).parents[2].joinpath("pyproject.toml"),
    name: str = "inboard",
    version: str = "0.1.0",
) -> dict:
    """Create a dictionary of keys and values corresponding to pydantic model fields.
    When instantiating the pydantic model, the dictionary can be unpacked and used to
    set fields in the model. Model fields not present in the TOML dictionary should be
    optional, because `dictionary.get(key_not_present)` will return `None`.
    """
    try:
        pyproject = dict(toml.load(pyproject_path))["tool"]["poetry"]
        return {key: pyproject.get(key) for key in list(fields.keys())}
    except Exception:
        return {"name": name, "version": version}


class Settings(BaseSettings):
    """[_pydantic_ settings model](https://pydantic-docs.helpmanual.io/usage/settings/)
    ---
    Settings are from [`pyproject.toml`](https://python-poetry.org/docs/pyproject/),
    and are tested by `test_metadata.py`.  The `__fields__` attribute provides a
    dictionary of pydantic model fields, without having to instantiate the model.
    """

    name: str
    version: str
    description: Optional[str]
    authors: Optional[List[str]]
    license: Optional[str]
    homepage: Optional[str]
    readme: Optional[str]
    include: Optional[List[str]]
    keywords: Optional[List[str]]
    classifiers: Optional[List[str]]

    def __init__(self) -> None:
        super().__init__(**set_fields_from_pyproject(self.__fields__))


class GetRoot(BaseModel):
    Hello: str = "World"


class GetStatus(BaseModel):
    application: str
    status: str
    message: Optional[str]


class GetUser(BaseModel):
    username: str
