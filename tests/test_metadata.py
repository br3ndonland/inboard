from pathlib import Path

from inboard.app.utilities_fastapi import Settings, set_fields_from_pyproject

settings = Settings()


def test_set_fields_from_pyproject() -> None:
    """Assert that pyproject.toml is successfully loaded and parsed."""
    pyproject = set_fields_from_pyproject(
        Settings.__fields__,
        pyproject_path=Path("pyproject.toml"),
    )
    assert pyproject != {"name": "inboard", "version": "0.1.0"}
    assert str(pyproject["name"]) == settings.name == "inboard"
    assert str(pyproject["version"]) == settings.version
    assert str(pyproject["description"]) == settings.description
    assert list(pyproject["authors"]) == settings.authors
    assert "Brendon Smith <br3ndonland@protonmail.com>" in settings.authors
    assert str(pyproject["license"]) == settings.license == "MIT"
    assert str(pyproject["homepage"]) == settings.homepage
    assert str(pyproject["readme"]) == settings.readme
    assert list(pyproject["include"]) == settings.include
    assert "inboard/py.typed" in settings.include
    assert list(pyproject["keywords"]) == settings.keywords
    assert "fastapi" in settings.keywords
    assert list(pyproject["classifiers"]) == settings.classifiers
    assert "Topic :: Internet :: WWW/HTTP :: HTTP Servers" in settings.classifiers


def test_load_pyproject_error() -> None:
    """Assert that default dict is loaded when pyproject.toml is not found."""
    pyproject = set_fields_from_pyproject(
        Settings.__fields__,
        pyproject_path=Path("pyproject.toml"),
    )
    pyproject_default = set_fields_from_pyproject(
        Settings.__fields__,
        pyproject_path=Path("error"),
    )
    assert pyproject != pyproject_default
    assert pyproject_default == {"name": "inboard", "version": "0.1.0"}
