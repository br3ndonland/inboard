from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal, TypedDict

if TYPE_CHECKING:
    import sys
    from asyncio import Protocol
    from collections.abc import Sequence
    from os import PathLike

    if sys.version_info < (3, 11):
        from typing_extensions import Required
    else:
        from typing import Required  # pyright: ignore[reportUnreachable]

    from uvicorn._types import ASGIApplication
    from uvicorn.config import (
        HTTPProtocolType,
        InterfaceType,
        LifespanType,
        LoopSetupType,
        WSProtocolType,
    )


class _RootLoggerConfiguration(TypedDict, total=False):
    level: int | str
    filters: Sequence[str]
    handlers: Sequence[str]


class _LoggerConfiguration(_RootLoggerConfiguration, TypedDict, total=False):
    propagate: bool


_FormatterConfigurationTypedDict = TypedDict(
    "_FormatterConfigurationTypedDict",
    {"class": str, "format": str, "datefmt": str, "style": Literal["%", "{", "$"]},
    total=False,
)


class _FilterConfigurationTypedDict(TypedDict):
    name: str


# Formatter and filter configs can specify custom factories via the special `()` key.
# If that is the case, the dictionary can contain any additional keys
# https://docs.python.org/3/library/logging.config.html#user-defined-objects
_FormatterConfiguration = (
    _FormatterConfigurationTypedDict | dict[str, Any]  # pyright: ignore[reportExplicitAny]
)
_FilterConfiguration = (
    _FilterConfigurationTypedDict | dict[str, Any]  # pyright: ignore[reportExplicitAny]
)
# Handler config can have additional keys even when not providing a custom factory so we just use `dict`.
_HandlerConfiguration = dict[str, Any]  # pyright: ignore[reportExplicitAny]


class DictConfig(TypedDict):
    """Python standard library logging module dict config type.
    ---

    https://docs.python.org/3/library/logging.config.html
    https://github.com/python/typeshed/blob/main/stdlib/logging/config.pyi
    """

    version: Required[Literal[1]]
    formatters: dict[str, _FormatterConfiguration]
    filters: dict[str, _FilterConfiguration]
    handlers: dict[str, _HandlerConfiguration]
    loggers: dict[str, _LoggerConfiguration]
    root: _RootLoggerConfiguration
    incremental: bool
    disable_existing_loggers: bool


class UvicornOptions(TypedDict, total=False):
    """Type for options passed to `uvicorn.run` and `uvicorn.Config`.
    ---

    "Options" are positional or keyword arguments passed to `uvicorn.run()` or
    `uvicorn.Config.__init__()`. The signatures of the two functions are not exactly
    the same ([encode/uvicorn#1545]). This type is primarily intended to match the
    arguments to `uvicorn.run()`.

    The `app` argument to `uvicorn.run()` accepts a `Callable` because Uvicorn tests use
    callables ([encode/uvicorn#1067]). It is not necessary for other packages to accept
    `Callable`, so `Callable` is not accepted in the `app` field of this type.

    The `log_config` argument in this type uses the inboard `DictConfig` type
    instead of `dict[str, Any]` for stricter type checking.

    It would be convenient to generate this type dynamically from `uvicorn.run`
    by accessing its [annotations dict][type annotation practices]
    with `getattr(uvicorn.run, "__annotations__")` (Python 3.9 or earlier)
    or `inspect.get_annotations(uvicorn.run)` (Python 3.10 or later).

    It could look like this with [`TypedDict` functional syntax][typing docs]:

    ```py
    UvicornArgs = TypedDict(  # type: ignore[misc]
        "UvicornArgs",
        inspect.get_annotations(uvicorn.run),
        total=False,
    )
    ```

    Note the `type: ignore[misc]` comment. Mypy raises a `misc` error:
    `TypedDict() expects a dictionary literal as the second argument`.
    Unfortunately, `TypedDict` types are not intended to be generated
    dynamically, because they exist for the benefit of static type checking
    ([python/mypy#3932], [python/mypy#4128], [python/mypy#13940]).

    [encode/uvicorn#1067]: https://github.com/encode/uvicorn/pull/1067
    [encode/uvicorn#1545]: https://github.com/encode/uvicorn/pull/1545
    [python/mypy#3932]: https://github.com/python/mypy/issues/3932
    [python/mypy#4128]: https://github.com/python/mypy/issues/4128
    [python/mypy#13940]: https://github.com/python/mypy/issues/13940
    [type annotation practices]: https://docs.python.org/3/howto/annotations.html
    [typing docs]: https://docs.python.org/3/library/typing.html#typing.TypedDict
    """

    app: Required[ASGIApplication | str]
    host: str
    port: int
    uds: str | None
    fd: int | None
    loop: LoopSetupType
    http: type[Protocol] | HTTPProtocolType
    ws: type[Protocol] | WSProtocolType
    ws_max_queue: int
    ws_max_size: int
    ws_ping_interval: float | None
    ws_ping_timeout: float | None
    ws_per_message_deflate: bool
    lifespan: LifespanType
    interface: InterfaceType
    reload: bool
    reload_dirs: list[str] | str | None
    reload_includes: list[str] | str | None
    reload_excludes: list[str] | str | None
    reload_delay: float
    workers: int | None
    env_file: str | PathLike[str] | None
    log_config: DictConfig | None
    log_level: str | int | None
    access_log: bool
    proxy_headers: bool
    server_header: bool
    date_header: bool
    forwarded_allow_ips: list[str] | str | None
    root_path: str
    limit_concurrency: int | None
    backlog: int
    limit_max_requests: int | None
    timeout_keep_alive: int
    timeout_graceful_shutdown: int | None
    ssl_keyfile: str | None
    ssl_certfile: str | PathLike[str] | None
    ssl_keyfile_password: str | None
    ssl_version: int
    ssl_cert_reqs: int
    ssl_ca_certs: str | None
    ssl_ciphers: str
    headers: list[tuple[str, str]] | None
    use_colors: bool | None
    app_dir: str | None
    factory: bool
    h11_max_incomplete_event_size: int
