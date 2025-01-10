from __future__ import annotations

import contextlib
import signal
import socket
import ssl
import subprocess
import sys
import tempfile
import time
from typing import TYPE_CHECKING

import httpx
import pytest
import trustme

if TYPE_CHECKING:
    from collections.abc import Generator
    from ssl import SSLContext
    from typing import IO

    from uvicorn._types import (
        ASGIReceiveCallable,
        ASGISendCallable,
        HTTPResponseBodyEvent,
        HTTPResponseStartEvent,
        LifespanStartupFailedEvent,
        Scope,
    )

pytestmark = pytest.mark.skipif(sys.platform == "win32", reason="requires unix")
gunicorn_arbiter = pytest.importorskip("gunicorn.arbiter", reason="requires gunicorn")
gunicorn_workers = pytest.importorskip(
    "inboard.gunicorn_workers", reason="requires gunicorn"
)


class Process(subprocess.Popen[str]):
    client: httpx.Client
    output: IO[bytes]

    def read_output(self) -> str:
        self.output.seek(0)
        return self.output.read().decode()


async def app(
    scope: Scope, receive: ASGIReceiveCallable, send: ASGISendCallable
) -> None:
    """An ASGI app for testing requests to Gunicorn workers."""
    assert scope["type"] == "http"
    start_event: HTTPResponseStartEvent = {
        "type": "http.response.start",
        "status": 204,
        "headers": [],
    }
    body_event: HTTPResponseBodyEvent = {
        "type": "http.response.body",
        "body": b"",
        "more_body": False,
    }
    await send(start_event)
    await send(body_event)


async def app_with_lifespan_startup_failure(
    scope: Scope, receive: ASGIReceiveCallable, send: ASGISendCallable
) -> None:
    """An ASGI app for testing Gunicorn worker boot errors."""
    if scope["type"] == "lifespan":
        message = await receive()
        if message["type"] == "lifespan.startup":
            lifespan_startup_failed_event: LifespanStartupFailedEvent = {
                "type": "lifespan.startup.failed",
                "message": "ASGI application failed to start",
            }
            await send(lifespan_startup_failed_event)


@pytest.fixture
def tls_certificate_authority() -> trustme.CA:
    return trustme.CA()


@pytest.fixture
def tls_ca_certificate_pem_path(
    tls_certificate_authority: trustme.CA,
) -> Generator[str, None, None]:
    with tls_certificate_authority.cert_pem.tempfile() as ca_pem_path:
        yield ca_pem_path


@pytest.fixture
def tls_ca_ssl_context(tls_certificate_authority: trustme.CA) -> ssl.SSLContext:
    ssl_ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    tls_certificate_authority.configure_trust(ssl_ctx)
    return ssl_ctx


@pytest.fixture
def tls_certificate(tls_certificate_authority: trustme.CA) -> trustme.LeafCert:
    return tls_certificate_authority.issue_cert("localhost", "127.0.0.1", "::1")


@pytest.fixture
def tls_certificate_private_key_path(
    tls_certificate: trustme.CA,
) -> Generator[str, None, None]:
    with tls_certificate.private_key_pem.tempfile() as private_key_path:
        yield private_key_path


@pytest.fixture
def tls_certificate_server_cert_path(
    tls_certificate: trustme.LeafCert,
) -> Generator[str, None, None]:
    with tls_certificate.cert_chain_pems[0].tempfile() as cert_pem_path:
        yield cert_pem_path


def _unused_port(socket_type: int) -> int:
    with contextlib.closing(socket.socket(type=socket_type)) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


@pytest.fixture
def unused_tcp_port() -> int:
    return _unused_port(socket.SOCK_STREAM)


@pytest.fixture(
    params=(
        pytest.param(gunicorn_workers.UvicornWorker, marks=pytest.mark.subprocess),
        pytest.param(gunicorn_workers.UvicornH11Worker, marks=pytest.mark.subprocess),
    )
)
def worker_class(request: pytest.FixtureRequest) -> str:
    """Gunicorn worker class names to test.

    This is a parametrized fixture. When the fixture is used in a test, the test
    will be automatically parametrized, running once for each fixture parameter. All
    tests using the fixture will be automatically marked with `pytest.mark.subprocess`.

    https://docs.pytest.org/en/latest/how-to/fixtures.html
    https://docs.pytest.org/en/latest/proposals/parametrize_with_fixtures.html
    """
    worker_class = request.param
    return f"{worker_class.__module__}.{worker_class.__name__}"


@pytest.fixture(
    params=(
        pytest.param(False, id="TLS off"),
        pytest.param(True, id="TLS on"),
    )
)
def gunicorn_process(
    request: pytest.FixtureRequest,
    tls_ca_certificate_pem_path: str,
    tls_ca_ssl_context: SSLContext,
    tls_certificate_private_key_path: str,
    tls_certificate_server_cert_path: str,
    unused_tcp_port: int,
    worker_class: str,
) -> Generator[Process, None, None]:
    """Yield a subprocess running a Gunicorn arbiter with a Uvicorn worker.

    An instance of `httpx.Client` is available on the `client` attribute.
    Output is saved to a temporary file and accessed with `read_output()`.
    """
    app_module = f"{__name__}:{app.__name__}"
    bind = f"127.0.0.1:{unused_tcp_port}"
    use_tls: bool = request.param
    args = [
        "gunicorn",
        "--bind",
        bind,
        "--graceful-timeout",
        "1",
        "--log-level",
        "debug",
        "--worker-class",
        worker_class,
        "--workers",
        "1",
    ]
    if use_tls is True:
        args_for_tls = [
            "--ca-certs",
            tls_ca_certificate_pem_path,
            "--certfile",
            tls_certificate_server_cert_path,
            "--keyfile",
            tls_certificate_private_key_path,
        ]
        args.extend(args_for_tls)
        base_url = f"https://{bind}"
        verify: SSLContext | bool = tls_ca_ssl_context
    else:
        base_url = f"http://{bind}"
        verify = False
    args.append(app_module)
    with (
        httpx.Client(base_url=base_url, verify=verify) as client,
        tempfile.TemporaryFile() as output,
    ):
        with Process(args, stdout=output, stderr=output) as process:
            time.sleep(2)
            assert not process.poll()
            process.client = client
            process.output = output
            yield process
            process.terminate()
            process.wait(timeout=2)


@pytest.fixture
def gunicorn_process_with_lifespan_startup_failure(
    unused_tcp_port: int, worker_class: str
) -> Generator[Process, None, None]:
    """Yield a subprocess running a Gunicorn arbiter with a Uvicorn worker.

    Output is saved to a temporary file and accessed with `read_output()`.
    The lifespan startup error in the ASGI app helps test worker boot errors.
    """
    app_module = f"{__name__}:{app_with_lifespan_startup_failure.__name__}"
    args = [
        "gunicorn",
        "--bind",
        f"127.0.0.1:{unused_tcp_port}",
        "--graceful-timeout",
        "1",
        "--log-level",
        "debug",
        "--worker-class",
        worker_class,
        "--workers",
        "1",
        app_module,
    ]
    with tempfile.TemporaryFile() as output:
        with Process(args, stdout=output, stderr=output) as process:
            time.sleep(2)
            process.output = output
            yield process
            process.terminate()
            process.wait(timeout=2)


def test_get_request_to_asgi_app(gunicorn_process: Process) -> None:
    """Test a GET request to the Gunicorn Uvicorn worker's ASGI app."""
    response = gunicorn_process.client.get("/")
    output_text = gunicorn_process.read_output()
    assert response.status_code == 204
    assert "inboard.gunicorn_workers", "startup complete" in output_text


@pytest.mark.parametrize("signal_to_send", gunicorn_arbiter.Arbiter.SIGNALS)
def test_gunicorn_arbiter_signal_handling(
    gunicorn_process: Process, signal_to_send: signal.Signals
) -> None:
    """Test Gunicorn arbiter signal handling.

    This test iterates over the signals handled by the Gunicorn arbiter,
    sends each signal to the process running the arbiter, and asserts that
    Gunicorn handles the signal and logs the signal handling event accordingly.

    https://docs.gunicorn.org/en/latest/signals.html
    """
    signal_abbreviation = gunicorn_arbiter.Arbiter.SIG_NAMES[signal_to_send]
    expected_text = f"Handling signal: {signal_abbreviation}"
    gunicorn_process.send_signal(signal_to_send)
    time.sleep(1)
    output_text = gunicorn_process.read_output()
    try:
        assert expected_text in output_text
    except AssertionError:  # pragma: no cover
        # occasional flakes are seen with certain signals
        flaky_signals = [
            getattr(signal, "SIGHUP", None),
            getattr(signal, "SIGTERM", None),
            getattr(signal, "SIGTTIN", None),
            getattr(signal, "SIGTTOU", None),
            getattr(signal, "SIGUSR2", None),
            getattr(signal, "SIGWINCH", None),
        ]
        if signal_to_send not in flaky_signals:
            time.sleep(2)
            output_text = gunicorn_process.read_output()
            assert expected_text in output_text


def test_uvicorn_worker_boot_error(
    gunicorn_process_with_lifespan_startup_failure: Process,
) -> None:
    """Test Gunicorn arbiter shutdown behavior after Uvicorn worker boot errors.

    Previously, if Uvicorn workers raised exceptions during startup,
    Gunicorn continued trying to boot workers ([#1066]). To avoid this,
    the Uvicorn worker was updated to exit with `Arbiter.WORKER_BOOT_ERROR`,
    but no tests were included at that time ([#1077]). This test verifies
    that Gunicorn shuts down appropriately after a Uvicorn worker boot error.

    When a worker exits with `Arbiter.WORKER_BOOT_ERROR`, the Gunicorn arbiter will
    also terminate, so there is no need to send a separate signal to the arbiter.

    [#1066]: https://github.com/encode/uvicorn/issues/1066
    [#1077]: https://github.com/encode/uvicorn/pull/1077
    """
    output_text = gunicorn_process_with_lifespan_startup_failure.read_output()
    gunicorn_process_with_lifespan_startup_failure.wait(timeout=2)
    assert gunicorn_process_with_lifespan_startup_failure.poll() is not None
    assert "Worker failed to boot" in output_text
