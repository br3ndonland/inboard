from __future__ import annotations

import sys

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from starlette.applications import Starlette


class TestCors:
    """Test CORS middleware integration.
    ---
    See the [FastAPI CORS tutorial](https://fastapi.tiangolo.com/tutorial/cors/) and
    [Starlette CORS docs](https://www.starlette.io/middleware/#corsmiddleware).
    """

    origins: dict[str, list[str]] = {
        "allowed": [
            "http://br3ndon.land",
            "https://br3ndon.land",
            "https://inboard.br3ndon.land",
            "https://inboard.docker.br3ndon.land",
            "https://www.br3ndon.land",
            "http://localhost:8000",
        ],
        "disallowed": [
            "https://br3ndon.com",
            "https://inboar.dbr3ndon.land",
            "https://example.land",
            "htttp://localhost:8000",
            "httpss://br3ndon.land",
            "othersite.com",
        ],
    }

    @pytest.mark.parametrize("allowed_origin", origins["allowed"])
    def test_cors_preflight_response_allowed(
        self, allowed_origin: str, client: TestClient
    ) -> None:
        """Test pre-flight response to cross-origin request from allowed origin."""
        headers: dict[str, str] = {
            "Origin": allowed_origin,
            "Access-Control-Request-Method": "GET",
            "Access-Control-Request-Headers": "X-Example",
        }
        response = client.options("/", headers=headers)
        assert response.status_code == 200, response.text
        assert response.text == "OK"
        assert response.headers["access-control-allow-origin"] == allowed_origin
        assert response.headers["access-control-allow-headers"] == "X-Example"

    @pytest.mark.parametrize("disallowed_origin", origins["disallowed"])
    def test_cors_preflight_response_disallowed(
        self, disallowed_origin: str, client: TestClient
    ) -> None:
        """Test pre-flight response to cross-origin request from disallowed origin."""
        headers: dict[str, str] = {
            "Origin": disallowed_origin,
            "Access-Control-Request-Method": "GET",
            "Access-Control-Request-Headers": "X-Example",
        }
        response = client.options("/", headers=headers)
        assert response.status_code >= 400
        assert "Disallowed CORS origin" in response.text
        assert not response.headers.get("access-control-allow-origin")

    @pytest.mark.parametrize("allowed_origin", origins["allowed"])
    def test_cors_response_allowed(
        self, allowed_origin: str, client: TestClient
    ) -> None:
        """Test response to cross-origin request from allowed origin."""
        headers = {"Origin": allowed_origin}
        response = client.get("/", headers=headers)
        assert response.status_code == 200, response.text
        assert response.json() == {"Hello": "World"}
        assert response.headers["access-control-allow-origin"] == allowed_origin

    @pytest.mark.parametrize("disallowed_origin", origins["disallowed"])
    def test_cors_response_disallowed(
        self, disallowed_origin: str, client: TestClient
    ) -> None:
        """Test response to cross-origin request from disallowed origin.
        As explained in the Starlette test suite in tests/middleware/`test_cors.py`,
        enforcement of CORS allowed origins is the responsibility of the client.
        On the server side, the "disallowed-ness" results in lack of an
        "Access-Control-Allow-Origin" header in the response.
        """
        headers = {"Origin": disallowed_origin}
        response = client.get("/", headers=headers)
        assert response.status_code == 200
        assert not response.headers.get("access-control-allow-origin")

    def test_non_cors(self, client: TestClient) -> None:
        """Test non-CORS response."""
        response = client.get("/")
        assert response.status_code == 200, response.text
        assert response.json() == {"Hello": "World"}
        assert "access-control-allow-origin" not in response.headers


class TestEndpoints:
    """Test API endpoints.
    ---
    See the [FastAPI testing docs](https://fastapi.tiangolo.com/tutorial/testing/),
    [Starlette TestClient docs](https://www.starlette.io/testclient/), and the
    [pytest docs](https://docs.pytest.org/en/latest/how-to/parametrize.html).
    """

    def test_get_asgi_uvicorn(
        self, client_asgi: TestClient, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test `GET` request to base ASGI app set for Uvicorn without Gunicorn."""
        monkeypatch.setenv("PROCESS_MANAGER", "uvicorn")
        monkeypatch.setenv("WITH_RELOAD", "false")
        version = sys.version_info
        response = client_asgi.get("/")
        assert response.status_code == 200
        assert response.text == (
            f"Hello World, from Uvicorn and Python "
            f"{version.major}.{version.minor}.{version.micro}!"
        )

    def test_get_asgi_uvicorn_gunicorn(
        self, client_asgi: TestClient, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test `GET` request to base ASGI app set for Uvicorn with Gunicorn."""
        monkeypatch.setenv("PROCESS_MANAGER", "gunicorn")
        monkeypatch.setenv("WITH_RELOAD", "false")
        version = sys.version_info
        response = client_asgi.get("/")
        assert response.status_code == 200
        assert response.text == (
            f"Hello World, from Uvicorn, Gunicorn, and Python "
            f"{version.major}.{version.minor}.{version.micro}!"
        )

    def test_get_asgi_incorrect_process_manager(
        self, client_asgi: TestClient, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test `GET` request to base ASGI app with incorrect `PROCESS_MANAGER`."""
        monkeypatch.setenv("PROCESS_MANAGER", "incorrect")
        monkeypatch.setenv("WITH_RELOAD", "false")
        with pytest.raises(NameError) as e:
            client_asgi.get("/")
        assert "Process manager needs to be either uvicorn or gunicorn" in str(e.value)

    def test_get_root(self, client: TestClient) -> None:
        """Test a `GET` request to the root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"Hello": "World"}

    @pytest.mark.parametrize("endpoint", ("/health", "/status"))
    def test_gets_with_basic_auth(
        self, basic_auth: tuple[str, str], client: TestClient, endpoint: str
    ) -> None:
        """Test `GET` requests to endpoints that require HTTP Basic auth."""
        error_response = client.get(endpoint)
        response = client.get(endpoint, auth=basic_auth)
        response_json = response.json()
        assert error_response.status_code in {401, 403}
        assert response.status_code == 200
        assert "application" in response_json
        assert "status" in response_json
        assert response_json["application"] == "inboard"
        assert response_json["status"] == "active"

    @pytest.mark.parametrize("endpoint", ("/health", "/status"))
    def test_gets_with_basic_auth_no_credentials(
        self, client: TestClient, endpoint: str
    ) -> None:
        """Test `GET` requests without HTTP Basic auth credentials set."""
        error_response = client.get(endpoint, auth=("user", "pass"))
        error_response_json = error_response.json()
        assert error_response.status_code in {401, 403}
        if isinstance(client.app, FastAPI):
            expected_json = {"detail": "Server HTTP Basic auth credentials not set"}
        elif isinstance(client.app, Starlette):
            expected_json = {
                "detail": "Server HTTP Basic auth credentials not set",
                "error": "Incorrect username or password",
            }
        else:  # pragma: no cover
            raise AssertionError("TestClient should have a FastAPI or Starlette app.")
        assert error_response_json == expected_json

    @pytest.mark.parametrize(
        "basic_auth_incorrect",
        (
            ("incorrect_username", "incorrect_password"),
            ("incorrect_username", "r4ndom_bUt_memorable"),
            ("test_user", "incorrect_password"),
        ),
    )
    @pytest.mark.parametrize("endpoint", ("/health", "/status"))
    def test_gets_with_basic_auth_incorrect_credentials(
        self,
        basic_auth_incorrect: tuple[str, str],
        client: TestClient,
        endpoint: str,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Test `GET` requests with incorrect HTTP Basic auth credentials."""
        monkeypatch.setenv("BASIC_AUTH_USERNAME", "test_user")
        monkeypatch.setenv("BASIC_AUTH_PASSWORD", "r4ndom_bUt_memorable")
        error_response = client.get(endpoint, auth=basic_auth_incorrect)
        error_response_json = error_response.json()
        assert error_response.status_code in {401, 403}
        if isinstance(client.app, FastAPI):
            expected_json = {"detail": "HTTP Basic auth credentials not correct"}
        elif isinstance(client.app, Starlette):
            expected_json = {
                "detail": "HTTP Basic auth credentials not correct",
                "error": "Incorrect username or password",
            }
        else:  # pragma: no cover
            raise AssertionError("TestClient should have a FastAPI or Starlette app.")
        assert error_response_json == expected_json

    def test_get_status_message(
        self,
        basic_auth: tuple[str, str],
        client: TestClient,
        endpoint: str = "/status",
    ) -> None:
        """Test the message returned by a `GET` request to a status endpoint."""
        error_response = client.get(endpoint)
        response = client.get(endpoint, auth=basic_auth)
        response_json = response.json()
        assert error_response.status_code in {401, 403}
        assert response.status_code == 200
        assert "message" in response_json
        for word in ("Hello", "World", "Uvicorn", "Python"):
            assert word in response_json["message"]
        if isinstance(client.app, FastAPI):
            assert "FastAPI" in response_json["message"]
        elif isinstance(client.app, Starlette):
            assert "Starlette" in response_json["message"]
        else:  # pragma: no cover
            raise AssertionError("TestClient should have a FastAPI or Starlette app.")

    def test_get_user(
        self,
        basic_auth: tuple[str, str],
        client: TestClient,
        endpoint: str = "/users/me",
    ) -> None:
        """Test a `GET` request to an endpoint providing user information."""
        error_response = client.get(endpoint)
        response = client.get(endpoint, auth=basic_auth)
        response_json = response.json()
        assert error_response.status_code in {401, 403}
        assert response.status_code == 200
        assert "application" not in response_json
        assert "status" not in response_json
        assert response_json["username"] == "test_user"
