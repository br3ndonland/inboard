I recommend three Inboard releases, taking FastAPI from the current `>=0.140,<0.141` constraint through 0.162. The batches follow the main upstream topics and keep the request-validation changes together, including the reversal of the temporary boolean form behavior.

| Proposed Inboard release | FastAPI target | Main topic |
| --- | --- | --- |
| 0.100.0 | 0.143.x | OpenTelemetry and frontend fixes |
| 0.101.0 | 0.146.x | WebSocket security and app configuration |
| 0.102.0 | 0.162.x | Request validation, forms, and parameter models |

These version numbers assume 0.99.0 remains the latest Inboard release. Each target includes all earlier FastAPI releases in the range since the preceding Inboard release. In particular, 0.100.0 also picks up the 0.140 patch releases and 0.141 frontend changes. The existing [contributing guide](/Users/brendon/code/github/br3ndonland/inboard/docs/contributing.md:252) calls for a separate Inboard release for each FastAPI minor version, so it should be updated if batching becomes the new practice.

The following drafts follow the style of the existing [changelog](/Users/brendon/code/github/br3ndonland/inboard/docs/changelog.md:151). Commit references and dates can be added when the releases are prepared.

## Inboard 0.100.0

### Changes

**Update to FastAPI 0.143**

This release will update to [FastAPI 0.143](https://github.com/fastapi/fastapi/releases/tag/0.143.0). FastAPI 0.141-0.143 are grouped together, including the introduction of native OpenTelemetry support and subsequent fixes.

FastAPI 0.143 makes automatic OpenTelemetry exporter configuration opt-in. To configure exporters from `OTEL_*` environment variables, set `FASTAPI_OTEL_AUTO_CONFIGURE=true` or pass `telemetry={"auto_configure": True}` to `FastAPI()`. Applications that configure their own providers and exporters do not need this setting.

FastAPI 0.141 also adds `app.frontend(check_dir="auto")` for local development. The included patch releases fix frontend behavior, streaming, and other issues. See the [FastAPI release notes](https://fastapi.tiangolo.com/release-notes/) for details. ([0.141.0](https://github.com/fastapi/fastapi/releases/tag/0.141.0), [0.142.0](https://github.com/fastapi/fastapi/releases/tag/0.142.0), [0.143.2](https://github.com/fastapi/fastapi/releases/tag/0.143.2))

## Inboard 0.101.0

### Changes

**Update to FastAPI 0.146**

This release will update to [FastAPI 0.146](https://github.com/fastapi/fastapi/releases/tag/0.146.0). FastAPI 0.144-0.146 are grouped together because they update security dependencies and application configuration.

FastAPI 0.144 adds WebSocket support to security dependencies. FastAPI 0.145 removes the deprecated `openapi_prefix` and unused extra keyword arguments from `FastAPI()`. FastAPI 0.146 deprecates the `root_path` argument to `FastAPI()`. Configure the ASGI server's root path instead. See the [FastAPI release notes](https://fastapi.tiangolo.com/release-notes/) for migration details. ([0.144.0](https://github.com/fastapi/fastapi/releases/tag/0.144.0), [0.145.0](https://github.com/fastapi/fastapi/releases/tag/0.145.0))

## Inboard 0.102.0

### Changes

**Update to FastAPI 0.162**

This release will update to [FastAPI 0.162](https://github.com/fastapi/fastapi/releases/tag/0.162.0). FastAPI 0.147-0.162 are grouped together because they revise request validation and add support for combining and using optional parameter models.

These releases include **BREAKING CHANGES** to request handling:

- Defaults for omitted query, header, cookie, and form parameters are no longer treated as user input or validated by default. Use `validate_default=True` when validation of a default is needed. ([FastAPI 0.148](https://github.com/fastapi/fastapi/releases/tag/0.148.0))
- Empty scalar fields in form models and unselected browser file inputs are treated as missing. Required fields can therefore produce validation errors. Named zero-byte files remain valid. ([FastAPI 0.149](https://github.com/fastapi/fastapi/releases/tag/0.149.0), [0.150](https://github.com/fastapi/fastapi/releases/tag/0.150.0))
- JSON `null` is distinguished from an omitted body value. Clients relying on `null` to select a default should omit the value instead. ([FastAPI 0.151](https://github.com/fastapi/fastapi/releases/tag/0.151.0))
- Deprecated extra keyword arguments have been removed from request parameter functions such as `Query()` and `Body()`. Use `json_schema_extra` for additional JSON Schema properties. ([FastAPI 0.155](https://github.com/fastapi/fastapi/releases/tag/0.155.0))
- A parameter model's `extra` configuration now applies to all submitted fields at the same location, including fields declared by other parameters or dependencies. For example, `extra="forbid"` can reject those sibling fields. ([FastAPI 0.160](https://github.com/fastapi/fastapi/releases/tag/0.160.0))
- Omitted boolean form fields use their declared defaults or produce missing-field errors. For an HTML checkbox that should default to `False`, declare that default explicitly. FastAPI 0.162 restores this behavior after 0.147 temporarily inferred `False`. ([FastAPI 0.162](https://github.com/fastapi/fastapi/releases/tag/0.162.0))

FastAPI also adds support for combining query, header, cookie, and form models, as well as optional parameter models and unions of form models. See the [FastAPI release notes](https://fastapi.tiangolo.com/release-notes/) to evaluate the changes against existing applications. ([0.157](https://github.com/fastapi/fastapi/releases/tag/0.157.0), [0.158](https://github.com/fastapi/fastapi/releases/tag/0.158.0), [0.159](https://github.com/fastapi/fastapi/releases/tag/0.159.0), [0.161](https://github.com/fastapi/fastapi/releases/tag/0.161.0))

Before publishing each batch, the dependency constraint and tests should be updated for its target. The current FastAPI constraint permits 0.140 patch updates, so the precise 0.140 fixes an existing installation receives depend on its resolved version. These are planning drafts; no dependencies or changelog files have been changed.
