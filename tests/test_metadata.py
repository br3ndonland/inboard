from importlib.metadata import metadata, version
from pathlib import Path
from typing import Any, Dict, List

import toml
from pydantic import BaseSettings


def load_pyproject(pyproject_path: Path = Path("pyproject.toml")) -> Dict[str, Any]:
    """Load pyproject.toml into a dictionary, with a default dict as a fallback."""
    try:
        return dict(toml.load(pyproject_path))
    except Exception:
        return {
            "tool": {"poetry": {"name": "inboard", "description": "", "version": ""}}
        }


class Settings(BaseSettings):
    """Instantiate a Pydantic Settings model."""

    pyproject: Dict[str, Any] = load_pyproject(pyproject_path=Path("pyproject.toml"))
    name: str = str(pyproject["tool"]["poetry"]["name"])
    version: str = str(pyproject["tool"]["poetry"]["version"])
    description: str = str(pyproject["tool"]["poetry"]["description"])
    authors: List[str] = list(pyproject["tool"]["poetry"]["authors"])
    license_name: str = str(pyproject["tool"]["poetry"]["license"])
    homepage: str = str(pyproject["tool"]["poetry"]["homepage"])
    readme: str = str(pyproject["tool"]["poetry"]["readme"])
    include: List[str] = list(pyproject["tool"]["poetry"]["include"])
    keywords: List[str] = list(pyproject["tool"]["poetry"]["keywords"])
    classifiers: List[str] = list(pyproject["tool"]["poetry"]["classifiers"])


settings = Settings()


def test_load_pyproject() -> None:
    """Assert that pyproject.toml is successfully loaded and parsed."""
    pyproject = load_pyproject(pyproject_path=Path("pyproject.toml"))
    assert pyproject == settings.pyproject
    assert str(pyproject["tool"]["poetry"]["name"]) == settings.name == "inboard"
    assert str(pyproject["tool"]["poetry"]["version"]) == settings.version
    assert str(pyproject["tool"]["poetry"]["description"]) == settings.description
    assert list(pyproject["tool"]["poetry"]["authors"]) == settings.authors
    assert "Brendon Smith <br3ndonland@protonmail.com>" in settings.authors
    assert str(pyproject["tool"]["poetry"]["license"]) == settings.license_name == "MIT"
    assert str(pyproject["tool"]["poetry"]["homepage"]) == settings.homepage
    assert str(pyproject["tool"]["poetry"]["readme"]) == settings.readme
    assert list(pyproject["tool"]["poetry"]["include"]) == settings.include
    assert "inboard/py.typed" in settings.include
    assert list(pyproject["tool"]["poetry"]["keywords"]) == settings.keywords
    assert "fastapi" in settings.keywords
    assert list(pyproject["tool"]["poetry"]["classifiers"]) == settings.classifiers
    assert "Topic :: Internet :: WWW/HTTP :: HTTP Servers" in settings.classifiers


def test_load_pyproject_error() -> None:
    """Assert that default dict is loaded when pyproject.toml is not found."""
    pyproject = load_pyproject(pyproject_path=Path("pyproject.toml"))
    pyproject_default = load_pyproject(pyproject_path=Path("error"))
    assert pyproject != pyproject_default
    assert pyproject_default == {
        "tool": {"poetry": {"name": "inboard", "description": "", "version": ""}}
    }


def test_package_version() -> None:
    """Assert that version number parsed from pyproject.toml matches
    version number of installed package obtained by importlib.metadata.
    """
    assert version("inboard") == settings.version
    assert metadata("inboard")["name"] == settings.name == "inboard"
    assert metadata("inboard")["summary"] == settings.description
