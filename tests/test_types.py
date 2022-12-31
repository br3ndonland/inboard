import uvicorn

import inboard.types


def test_type_checking_attrs() -> None:
    """Verify basic import functionality and attributes of the inboard type module.

    Type annotations are not used at runtime. The standard library `typing` module
    includes a `TYPE_CHECKING` constant that is `False` at runtime, or `True` when
    conducting static type checking prior to runtime. The inboard type module will
    therefore have `TYPE_CHECKING == False` when tests are running, but should
    still make its public types available for other modules to import.

    The `type: ignore[attr-defined]` comment is needed to allow `implicit_reexport`
    for mypy. The inboard types module imports `typing.TYPE_CHECKING`, but does not
    re-export it. Mypy would therefore raise an error in strict mode.

    https://docs.python.org/3/library/typing.html
    https://mypy.readthedocs.io/en/stable/config_file.html
    """
    assert inboard.types.TYPE_CHECKING is False  # type: ignore[attr-defined]
    for attr in ("DictConfig", "UvicornOptions"):
        assert hasattr(inboard.types, attr)


def test_uvicorn_options_type_matches_uvicorn_args() -> None:
    """Test that fields in the inboard Uvicorn options type match arguments passed to
    `uvicorn.run()` and `uvicorn.Config.__init__()`.

    The inboard Uvicorn options type can be used to type-check arguments passed
    to `uvicorn.run()`. `uvicorn.run()` then uses these arguments to instantiate
    `uvicorn.Config`.

    Prior to Uvicorn 0.18.0, `uvicorn.run()` didn't enumerate keyword arguments,
    but instead accepted `kwargs` and passed them to `uvicorn.Config.__init__()`
    ([encode/uvicorn#1423]). Even after Uvicorn 0.18.0, the signatures of the two
    functions are not exactly the same ([encode/uvicorn#1545]). This test normalizes
    the differences.

    The signatures of `uvicorn.run()` and `uvicorn.Config.__init__()` are not exactly
    the same ([encode/uvicorn#1545]), so this test normalizes the differences.

    `uvicorn.run()` is a function with a return type, so its `__annotations__` dict
    will include an item `return` to specify its return type. The inboard Uvicorn
    options type is not a function, so it will not have this `return` item.

    While it is straightforward to compare keys in the `__annotations__` dicts,
    it is less straightforward to compare the values (the type annotations).
    This is partially because `from __future__ import annotations`, which is used
    by inboard but not by Uvicorn, "stringizes" the annotations into `ForwardRef`s.

    [encode/uvicorn#1423]: https://github.com/encode/uvicorn/pull/1423
    [encode/uvicorn#1545]: https://github.com/encode/uvicorn/pull/1545
    """
    options_for_config_only = ("callback_notify", "timeout_notify")
    options_for_run_only = ("app_dir",)
    inboard_keys = list(sorted(inboard.types.UvicornOptions.__annotations__.keys()))
    uvicorn_config_keys = list(sorted(uvicorn.Config.__init__.__annotations__.keys()))
    uvicorn_run_keys = list(sorted(uvicorn.run.__annotations__.keys()))
    if "return" in uvicorn_run_keys:
        uvicorn_run_keys.remove("return")
    for option in options_for_config_only:
        assert option not in inboard_keys
        assert option in uvicorn_config_keys
        assert option not in uvicorn_run_keys
        uvicorn_config_keys.remove(option)
    for option in options_for_run_only:
        assert option in inboard_keys
        assert option not in uvicorn_config_keys
        assert option in uvicorn_run_keys
        inboard_keys.remove(option)
        uvicorn_run_keys.remove(option)
    assert inboard_keys == uvicorn_config_keys == uvicorn_run_keys
