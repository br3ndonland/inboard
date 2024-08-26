# Changelog

## 0.70.0 - 2024-08-26

### Changes

**Update to FastAPI 0.112 and Starlette 0.38**
(b4cf65de8bbda51447cd30033b6c52d51b418d79)

This release will update/upgrade to
[FastAPI 0.112](https://fastapi.tiangolo.com/release-notes/)
and
[Starlette 0.38](https://www.starlette.io/release-notes/).
This is a minor release to align with FastAPI and Starlette versioning.

FastAPI 0.112 moves dependencies for the FastAPI CLI introduced in 0.111
to an optional extra, `fastapi[standard]`. Although the FastAPI release
notes consider this a breaking change, the FastAPI CLI was not used by
inboard, so FastAPI 0.112 will likely not be breaking for inboard users.

Starlette 0.38 makes various small changes, including removal of support
for an ASGI extension called
[path send](https://asgi.readthedocs.io/en/latest/extensions.html#path-send)
(aka "path-send" or `pathsend`) that was introduced in Starlette 0.36.
Support was removed because of issues with `BaseHTTPMiddleware`, though
note that `BaseHTTPMiddleware` may eventually be deprecated
([encode/starlette#2160](https://github.com/encode/starlette/discussions/2160),
[encode/starlette#2654](https://github.com/encode/starlette/discussions/2654)).
The Starlette release notes do not list this as a breaking change, but
it could be breaking for users who have started working with path send.
Note that FastAPI updated the Starlette minor version to allow 0.38 in
the 0.112.1 patch release.

**Use dedicated GitHub Actions job for PyPI**
(08044c6034346b745f4a210cef928c7114497e78,
180d353a9487afd003aa630ed14a24f4065b451f)

This project uses pypa/gh-action-pypi-publish to publish Python packages
to PyPI with an
[OIDC trusted publisher](https://docs.pypi.org/trusted-publishers/)
(59ec546cb39ea05cf8ac37c5f7fdbf8ac6bb289d).

pypa/gh-action-pypi-publish is set up as a
[Docker action](https://docs.github.com/en/actions/creating-actions/creating-a-docker-container-action)
referencing its Dockerfile. The downside to using the Dockerfile for
the action is that the Docker image must be built every time the action
is used. This will hopefully change in the near future if Docker images
are built and pushed to a registry (pypa/gh-action-pypi-publish#230).
In the meantime, PyPI steps steps will be moved to a dedicated GitHub
Actions job so that the Docker image is not built every time GitHub
Actions jobs run.

### Commits

- Bump version from 0.69.0 to 0.70.0 (01835ec)
- Update to FastAPI 0.112 and Starlette 0.38 (b4cf65d)
- Don't hard-code repo name in GitHub Actions jobs (180d353)
- Use dedicated GitHub Actions job for PyPI (08044c6)
- Update to `hatch==1.12.0` (f950d28)
- Update to `pipx==1.6.0` (8066be3)
- Update to `mypy==1.10.1` (08ba81a)
- Update to Ruff 0.5 (101fdb3)
- Update to Prettier 3 (67ee89d)
- Add `--platform` to Docker CLI examples in docs (dd3a53c)
- Fix Docker `FromAsCasing` warning (49914dd)
- Update changelog for version 0.69.0 (#110) (294e8c8)

Tagger: Brendon Smith <bws@bws.bio>

Date: 2024-08-26 18:33:23 -0400

```text
-----BEGIN SSH SIGNATURE-----
U1NIU0lHAAAAAQAAADMAAAALc3NoLWVkMjU1MTkAAAAgwLDNmire1DHY/g9GC1rGGr+mrE
kJ3FC96XsyoFKzm6IAAAADZ2l0AAAAAAAAAAZzaGE1MTIAAABTAAAAC3NzaC1lZDI1NTE5
AAAAQPqh0hb15zIfbXTdfFeM+AvzAeSakCjVg5z4IuCJN7kk1iViRXO3quKYJlmQNZJbGC
gvCeG2qt49XexAso2TOQE=
-----END SSH SIGNATURE-----
```

## 0.69.0 - 2024-07-14

### Changes

This release will update/upgrade to
[FastAPI 0.111](https://fastapi.tiangolo.com/release-notes/).
This is a minor release to align with FastAPI versioning.

FastAPI 0.111.0 adds a `fastapi` CLI that is not relevant to inboard.
FastAPI 0.111.1 removes `orjson` and `ujson` from default dependencies.
Users who depend on `orjson` or `ujson` should add these dependencies to
their requirements files.

### Commits

- Bump version from 0.68.0 to 0.69.0 (af06254)
- Update to FastAPI 0.111 (5f9ee0a)
- Update changelog for version 0.68.0 (#109) (2416a23)

Tagger: Brendon Smith <bws@bws.bio>

Date: 2024-07-14 14:40:56 -0400

```text
-----BEGIN SSH SIGNATURE-----
U1NIU0lHAAAAAQAAADMAAAALc3NoLWVkMjU1MTkAAAAgwLDNmire1DHY/g9GC1rGGr+mrE
kJ3FC96XsyoFKzm6IAAAADZ2l0AAAAAAAAAAZzaGE1MTIAAABTAAAAC3NzaC1lZDI1NTE5
AAAAQKl8MnPlFZ51cBAk7RA5zd42Ggi6JwHyuV1G+l1m28l2naB1ZeG0Ubr/lGXqejiMku
9lg73rNFFOXlrLkM4A4Ag=
-----END SSH SIGNATURE-----
```

## 0.68.0 - 2024-04-26

### Changes

**Update to Uvicorn 0.28.1** (6166a668d9019fc90adc5f268041f9bc1dd6df43)

This release will update/upgrade to Uvicorn 0.28.1.
[Changes](https://github.com/encode/uvicorn/compare/0.25.0...0.28.1)
to Uvicorn between 0.25.0 and 0.28.1 include updates to `root_path`/
`--root-path` to comply with the ASGI spec, and fixes to `Keep-Alive`
behavior to avoid timeouts and `h11.LocalProtocolError` exceptions that
occur when processing pipelined requests.

**Update to Gunicorn 22.0.0** (#108,
bf4661ed83f09db7bf4dcb95ff0cedced14f92c4)

This release will update/upgrade to
[Gunicorn 22.0.0](https://docs.gunicorn.org/en/stable/news.html).
Gunicorn 22.0.0 resolves a high-severity security vulnerability
([CVE-2024-1135](https://nvd.nist.gov/vuln/detail/CVE-2024-1135),
[GHSA-w3h3-4rj7-4ph4](https://github.com/advisories/GHSA-w3h3-4rj7-4ph4)):

> Gunicorn fails to properly validate Transfer-Encoding headers, leading
> to HTTP Request Smuggling (HRS) vulnerabilities. By crafting requests
> with conflicting Transfer-Encoding headers, attackers can bypass
> security restrictions and access restricted endpoints. This issue is
> due to Gunicorn's handling of Transfer-Encoding headers, where it
> incorrectly processes requests with multiple, conflicting
> Transfer-Encoding headers, treating them as chunked regardless of the
> final encoding specified. This vulnerability has been shown to allow
> access to endpoints restricted by gunicorn. This issue has been
> addressed in version 22.0.0.
>
> To be affected users must have a network path which does not filter
> out invalid requests. These users are advised to block access to
> restricted endpoints via a firewall or other mechanism if they are
> unable to update.

### Commits

- Bump version from 0.67.1 to 0.68.0 (3fc1f79)
- Quote `&` in GitHub Actions workflow YAML (0043237)
- Update to Uvicorn 0.28.1 (6166a66)
- Bump gunicorn from 21.2.0 to 22.0.0 (#108) (bf4661e)
- Update changelog for version 0.67.1 (#107) (9579bba)

Tagger: Brendon Smith <bws@bws.bio>

Date: 2024-04-26 22:11:28 -0400

```text
-----BEGIN SSH SIGNATURE-----
U1NIU0lHAAAAAQAAADMAAAALc3NoLWVkMjU1MTkAAAAgwLDNmire1DHY/g9GC1rGGr+mrE
kJ3FC96XsyoFKzm6IAAAADZ2l0AAAAAAAAAAZzaGE1MTIAAABTAAAAC3NzaC1lZDI1NTE5
AAAAQP3RzZnd8mb0DehzvdJSKrJPWcFzhL2yz6SOt3vPRmB5ZifcG29/9gAovSbvGxa8EC
sSlxWxflkAIp2n05yk2QE=
-----END SSH SIGNATURE-----
```

## 0.67.1 - 2024-04-11

### Changes

**Fix Docker tags for specific Debian version** (e84fc8b24817acb3c8b7e0a96c4574ddb0f88d7d)

PR br3ndonland/inboard#105 and
commit br3ndonland/inboard@6a99cd09f04c000167432970b044b23623df887a
introduced support for specifying the Debian version when building
Docker images, ensuring that the version does not change unexpectedly.
This change altered Docker tag syntax by adding the Debian version
release name (currently "bookworm") to all Debian Docker images.
For example, `ghcr.io/br3ndonland/inboard:latest` became
`ghcr.io/br3ndonland/inboard:latest-bookworm`. inboard is not planning
to support multiple Debian versions simultaneously. inboard will update
to the next Debian version, Debian 13 ("trixie") when it is stable and
will provide a new release after the update. This means there is no need
to add the Debian version release name to the Docker tags.

This commit will update the code in the GitHub Actions workflow job and
Dockerfile to match the previous tag syntax. The latest Debian image
will return to `ghcr.io/br3ndonland/inboard:latest` and the latest
Debian slim image to `ghcr.io/br3ndonland/inboard:latest-slim`.
Syntax for Alpine Docker images remains unaltered, so tags like
`ghcr.io/br3ndonland/inboard:latest-alpine` are still valid.

### Commits

- Bump version from 0.67.0 to 0.67.1 (2bfe218)
- Fix Docker tags for specific Debian version (#105) (e84fc8b)
- Update changelog for version 0.67.0 (#106) (1d20b7d)

Tagger: Brendon Smith <bws@bws.bio>

Date: 2024-04-11 19:04:37 -0400

```text
-----BEGIN SSH SIGNATURE-----
U1NIU0lHAAAAAQAAADMAAAALc3NoLWVkMjU1MTkAAAAgwLDNmire1DHY/g9GC1rGGr+mrE
kJ3FC96XsyoFKzm6IAAAADZ2l0AAAAAAAAAAZzaGE1MTIAAABTAAAAC3NzaC1lZDI1NTE5
AAAAQNksE9FyAppa86DBR/C92TCqCQkLpz4YZhv8tF8tK9scQYhVWEEVZZXSHv68VA7fUR
uLpz3hNjvEzj/vuD3/lwo=
-----END SSH SIGNATURE-----
```

## 0.67.0 - 2024-04-11

### Changes

**Specify Debian version** (#105, 6a99cd09f04c000167432970b044b23623df887a)

On 2023-06-14, Docker updated the default Debian Linux version in its
Python official images from Debian bullseye to Debian bookworm
([docker-library/official-images#14854](https://github.com/docker-library/official-images/pull/14854)).
As inboard uses the default Debian Linux version from the Docker Python
official images, this meant that the next release of inboard
(0.50.0 - 2023-06-22) automatically updated to bookworm. There were some
[issues](https://github.com/docker-library/python/issues?q=bookworm)
noted by the community after this update. This was noted in inboard
[0.51.0 - 2023-07-09](https://inboard.bws.bio/changelog#0510-2023-07-09).
Thanks to @bodograumann for pointing this out in the related discussion
([br3ndonland/inboard#80](https://github.com/br3ndonland/inboard/discussions/80)).

inboard will now specify the Debian version when building Docker images,
ensuring that the version does not change unexpectedly.
The current Debian version is still Debian 12 ("bookworm").
The next Debian version, Debian 13 ("trixie") does not have a release
date yet, but inboard will update to trixie when it is stable and will
provide a new release after the update.

**Add support for Python 3.12** (#104, ba83a67cafe94b9ce5c2306dfaad0f29c346b2f1)

This release will add
[Python 3.12](https://docs.python.org/3/whatsnew/3.12.html)
support to inboard.

- inboard will now run tests with Python 3.12, in addition to 3.8-3.11
- inboard will now build and publish its PyPI package using Python 3.12
- inboard will now include a Python 3.12 classifier in its PyPI package
- inboard will now ship Docker images running Python 3.12, in addition
  to 3.8-3.11, and Docker images tagged with `latest` will now use 3.12

Related projects that have released support for Python 3.12 include:

- AnyIO ([4.0.0 - 2023-08-30](https://github.com/agronholm/anyio/releases/tag/4.0.0))
- FastAPI ([0.109.0 - 2024-01-11](https://github.com/tiangolo/fastapi/releases/tag/0.109.0))
- Hatch ([1.8.0 - 2023-12-11](https://github.com/pypa/hatch/releases/tag/hatch-v1.8.0))
- `pipx` ([1.3.0 - 2023-12-02](https://github.com/pypa/pipx/releases/tag/1.3.0))
- Starlette ([0.31.0 - 2023-07-24](https://github.com/encode/starlette/releases/tag/0.31.0))
- Uvicorn ([0.24.0 - 2023-11-04](https://github.com/encode/uvicorn/releases/tag/0.24.0))

Related projects that have not released support for Python 3.12 include:

- [Gunicorn](https://github.com/benoitc/gunicorn) (has not released
  Python 3.12 support, but is testing with Python 3.12 in development)
- [Pydantic](https://github.com/pydantic/pydantic) (extent of Python
  3.12 support unclear, see
  [pydantic/pydantic#6704](https://github.com/pydantic/pydantic/discussions/6704))

### Commits

- Bump version from 0.66.1 to 0.67.0 (325ed9b)
- Update to pytest 8 (c462c90)
- Specify Debian version (#105) (6a99cd0)
- Add support for Python 3.12 (#104) (ba83a67)
- Fix GitHub Actions badge in README (145313e)
- Update changelog for version 0.66.1 (#103) (552ebaa)

Tagger: Brendon Smith <bws@bws.bio>

Date: 2024-04-11 17:41:05 -0400

```text
-----BEGIN SSH SIGNATURE-----
U1NIU0lHAAAAAQAAADMAAAALc3NoLWVkMjU1MTkAAAAgwLDNmire1DHY/g9GC1rGGr+mrE
kJ3FC96XsyoFKzm6IAAAADZ2l0AAAAAAAAAAZzaGE1MTIAAABTAAAAC3NzaC1lZDI1NTE5
AAAAQPlwcflQF/+WkcLYUk8CqDwrV9hDWCGSluKZTJ2rmw2SbU30RriTdumN1dX53rF4rb
vKEZhZfa5UOLGcq9vz3AU=
-----END SSH SIGNATURE-----
```

## 0.66.1 - 2024-04-09

### Changes

**Publish to PyPI with OIDC trusted publisher** (59ec546)

This release will update Python package publishing to the newest format
recommended by PyPI. This project previously published packages with the
`hatch publish` command and a project-scoped PyPI API token (token only
valid for this project) stored in GitHub Secrets. The project will now
publish packages using a
[PyPI OIDC](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-pypi)
(OpenID Connect)
[trusted publisher](https://docs.pypi.org/trusted-publishers/) with the
[pypa/gh-action-pypi-publish](https://github.com/pypa/gh-action-pypi-publish)
action. This is the method that Hatch itself uses (pypa/hatch#891)
(Hatch does not "dogfood" its own `hatch publish` feature).

The advantage to OIDC is that authentication is performed with temporary
API tokens (only valid for 15 minutes) instead of persistent tokens that
must be manually generated on PyPI and pasted into GitHub Secrets. The
disadvantage is that authentication is more complicated.

To use PyPI OIDC, a
[trusted publisher](https://docs.pypi.org/trusted-publishers/) was set
up for the PyPI project. Next, a dedicated
[GitHub Actions deployment environment](https://docs.github.com/en/actions/deployment/targeting-different-environments/using-environments-for-deployment)
was created for PyPI with protection rules that only allow use of the
environment with Git tags. The environment protection rules combine with
tag protection rules in the existing
[GitHub rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets)
to ensure PyPI packages can only be published if a maintainer triggers a
workflow run with a Git tag ref.

The GitHub Actions workflow will be updated to use the deployment
environment. Deployment environments must be selected at the job level
before the job begins, so a setup job will be added that selects the
appropriate deployment environment and passes it to the PyPI job.
Each use of a deployment environment creates a deployment that can be
either active or inactive. GitHub Actions auto-inactivates deployments,
and although this behavior is not configurable or documented, there are
some possible workarounds/hacks suggested by a community discussion
[comment](https://github.com/orgs/community/discussions/67982#discussioncomment-7086962).
The workaround used here will be to provide each deployment with its own
unique URL.

To publish the Python package to PyPI, `hatch build` will output package
build files to the `dist/` directory, then pypa/gh-action-pypi-publish
will authenticate and upload the files. pypa/gh-action-pypi-publish
provides exact version tags like pypa/gh-action-pypi-publish@v1.8.14 and
branches for major and minor version numbers like
pypa/gh-action-pypi-publish@release/v1.8.

**Update to FastAPI 0.110.1 and Starlette 0.37.2** (73eaadd)

This release will update/upgrade to
[FastAPI 0.110.1](https://fastapi.tiangolo.com/release-notes/)
and
[Starlette 0.37.2](https://www.starlette.io/release-notes/).
FastAPI 0.110 makes a change to dependencies with `yield` and `except`.
Dependencies must now raise exceptions after `except`. This change is
intended to address memory leak issues and may be a breaking change in
some projects if dependencies with `yield` and `except` used `pass`
instead of `raise`. See the
[FastAPI docs](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/)
for further info. FastAPI 0.110.1 makes a small type annotation change
to the `Depends` dependency class.

Starlette 0.37 modifies the exception handling behavior of the `Config`
class used for application settings. The `Config` class accepts an
`env_file` arg that can be used to load environment variables from a
"dotenv" (`.env`) file. Previously, if the file was not found, the
`Config` class would silently pass without any exception. In 0.36, the
`Config` class was updated to raise a `FileNotFoundError` exception if
`env_file` was not not found. This was a breaking change but was not
documented as such (encode/starlette#2422, encode/starlette#2446).
In 0.37, the exception handling behavior has been changed again to raise
a warning instead of an exception (encode/starlette#2485), which could
also be a breaking change if users had rewritten their code to catch the
`FileNotFoundError`.
See the [fastenv docs](https://fastenv.bws.bio/comparisons#starlette)
for a detailed description of the Starlette `Config` class. Note that
FastAPI updated the Starlette minor version from 0.36 to 0.37 in the
0.110.1 patch release.

### Commits

- Bump version from 0.66.0 to 0.66.1 (474c722)
- Publish to PyPI with OIDC trusted publisher (59ec546)
- Update to `peter-evans/create-pull-request@v6` (5b499a3)
- Update to Ruff 0.3 (e42213c)
- Update to `mypy==1.9.0` (1cd64a7)
- Update to `hatch==1.9.4` (38a4e58)
- Update to `pipx==1.5.0` (8dfb90b)
- Update to FastAPI 0.110.1 and Starlette 0.37.2 (73eaadd)
- Disable CodeQL `setup-python-dependencies` (507c68c)
- Update to Node.js 20 actions (6972c7b)
- Update changelog for version 0.66.0 (#102) (7f4ff4e)

Tagger: Brendon Smith <bws@bws.bio>

Date: 2024-04-09 05:58:15 -0400

```text
-----BEGIN SSH SIGNATURE-----
U1NIU0lHAAAAAQAAADMAAAALc3NoLWVkMjU1MTkAAAAgwLDNmire1DHY/g9GC1rGGr+mrE
kJ3FC96XsyoFKzm6IAAAADZ2l0AAAAAAAAAAZzaGE1MTIAAABTAAAAC3NzaC1lZDI1NTE5
AAAAQKS6kAq3o+Spoc+d2rYpLAJVY67L7NYQNGlSzlkn5ZRyvwlJxgmvBxrpvs0BSh7O5a
FqS78jcq4EBq+uUpo+xg8=
-----END SSH SIGNATURE-----
```

## 0.66.0 - 2024-03-11

### Changes

**Update to FastAPI 0.110 and Starlette 0.36** (dfa4822)

This release will update/upgrade to
[FastAPI 0.110](https://fastapi.tiangolo.com/release-notes/)
and
[Starlette 0.36](https://www.starlette.io/release-notes/).
This is a minor release to align with FastAPI and Starlette versioning.

FastAPI 0.110 makes a change to dependencies with `yield` and `except`.
Dependencies must now raise exceptions after `except`, like this:

```py
def my_dep():
    try:
        yield
    except SomeException:
        raise
```

This change addresses memory leak issues and may be a breaking change in
some projects if dependencies with `yield` and `except` used `pass`
instead of `raise`. See the
[FastAPI docs](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/)
for further info.

Changes to Starlette between 0.35 and 0.36 include exception handling
updates and AnyIO compatibility updates. Note that FastAPI updated the
Starlette minor version from 0.35 to 0.36 in the 0.109.2 patch release.

### Commits

- Bump version from 0.65.0 to 0.66.0 (ae160a0)
- Update to FastAPI 0.110 and Starlette 0.36 (dfa4822)
- Update to `peter-evans/create-pull-request@v5` (2f9b88f)
- Update to `actions/checkout@v4` (8d888d0)
- Update changelog for version 0.65.0 (#100) (8725661)

Tagger: Brendon Smith <bws@bws.bio>

Date: 2024-03-11 20:49:50 -0400

```text
-----BEGIN SSH SIGNATURE-----
U1NIU0lHAAAAAQAAADMAAAALc3NoLWVkMjU1MTkAAAAgwLDNmire1DHY/g9GC1rGGr+mrE
kJ3FC96XsyoFKzm6IAAAADZ2l0AAAAAAAAAAZzaGE1MTIAAABTAAAAC3NzaC1lZDI1NTE5
AAAAQL32WdiYCJC7uWy4e0Dgpl8E9aqQz+pDZTAY2BeUFt1fFi3m8A9wQEXasq7ypEosw1
SIp2yAPLd0+Bl5Fl7LMAw=
-----END SSH SIGNATURE-----
```

## 0.65.0 - 2024-01-13

### Changes

**Update to FastAPI 0.109 and Starlette 0.35** (b68b991)

This release will update/upgrade to
[FastAPI 0.109](https://fastapi.tiangolo.com/release-notes/)
and
[Starlette 0.35](https://www.starlette.io/release-notes/).
This is a minor release to align with FastAPI and Starlette versioning.
FastAPI 0.109 adds Python 3.12 support. Changes to Starlette between
0.32 and 0.35 include support for middleware in `Router`, `Route`, and
`WebSocketRoute`, and updates to `Middleware` args.

**Use Ruff for linting and formatting** (#99, 35e37a7)

[Ruff](https://docs.astral.sh/ruff/) is a Python linter and formatter
that has gained popularity due to its high performance and numerous
capabilities. Now that Ruff has released its
[first minor version series](https://astral.sh/blog/ruff-v0.1.0) (0.1)
and has a [versioning policy](https://docs.astral.sh/ruff/versioning/),
it's a good time to consider adopting it.

As of this release, the project's Python linting and formatting checks
will be migrated from the previous tools (Black, Flake8, isort) to Ruff.
See br3ndonland/inboard#99 for further details.

### Commits

- Bump version from 0.64.0 to 0.65.0 (ca0a10b)
- Update to FastAPI 0.109 and Starlette 0.35 (b68b991)
- Use Ruff for linting and formatting (#99) (35e37a7)
- Add "pypa" to CSpell words (696c43d)
- Add references on syncing dependencies with Hatch (1e9512a)
- Update Docker links in docs (e3ad60b)
- Avoid `metadata-generation-failed` in Dockerfiles (a231b11)
- Add wheel build target to avoid Hatch `ValueError` (c1328ee)
- Update to `pipx==1.4.1` (f902387)
- Update changelog for version 0.64.0 (#97) (78adc33)

Tagger: Brendon Smith <bws@bws.bio>

Date: 2024-01-13 21:22:20 -0500

```text
-----BEGIN SSH SIGNATURE-----
U1NIU0lHAAAAAQAAADMAAAALc3NoLWVkMjU1MTkAAAAgwLDNmire1DHY/g9GC1rGGr+mrE
kJ3FC96XsyoFKzm6IAAAADZ2l0AAAAAAAAAAZzaGE1MTIAAABTAAAAC3NzaC1lZDI1NTE5
AAAAQN0NsHI0NRGFnLFF3MDZW5nez8ULCLwCIs+Eq+ipQz6tDvcHfSnRp4Fqo5S7m+4WiB
1dSCVYc/TnXiM0rgZrPgI=
-----END SSH SIGNATURE-----
```

## 0.64.0 - 2023-12-30

### Changes

**Update to Gunicorn 21.2.0** (7993e61)

This release will update/upgrade to Gunicorn 21.2.0. See the Gunicorn
[docs](https://docs.gunicorn.org/en/stable/2023-news.html) and
[GitHub repo](https://github.com/benoitc/gunicorn/compare/20.1.0...21.2.0)
for more details on the changes since 20.1.0.

### Commits

- Bump version from 0.63.0 to 0.64.0 (384907b)
- Update to Gunicorn 21.2.0 (7993e61)
- Update changelog for version 0.63.0 (#96) (3bd8be1)

Tagger: Brendon Smith <bws@bws.bio>

Date: 2023-12-30 23:52:09 -0500

```text
-----BEGIN SSH SIGNATURE-----
U1NIU0lHAAAAAQAAADMAAAALc3NoLWVkMjU1MTkAAAAgwLDNmire1DHY/g9GC1rGGr+mrE
kJ3FC96XsyoFKzm6IAAAADZ2l0AAAAAAAAAAZzaGE1MTIAAABTAAAAC3NzaC1lZDI1NTE5
AAAAQIS/5tugCWRCJ1Ea6v+ULmsSD31Y6yc+CDAdvmQ8V8ToWGtHo5wHXv09lqPxlczwP+
HrsHdXn9qPiXB+V6tPpgA=
-----END SSH SIGNATURE-----
```

## 0.63.0 - 2023-12-30

### Changes

**Update to Uvicorn 0.25.0** (4cc018b)

This release will update/upgrade to
[Uvicorn 0.25.0](https://github.com/encode/uvicorn/releases).
This is a minor release to align with Uvicorn versioning.

Uvicorn 0.25.0 adds support for the WebSocket Denial Response ASGI
extension. This is used in certain cases in which a WebSocket app needs
to reject a connection and return a custom response.

Uvicorn 0.25.0 also includes some corrections to the type annotations on
`uvicorn.run()`. `inboard.types.UvicornOptions` already included correct
type annotations that match these corrections, so no changes are needed.

### Commits

- Bump version from 0.62.0 to 0.63.0 (634d094)
- Update to Uvicorn 0.25.0 (4cc018b)
- Update changelog for version 0.62.0 (#95) (a1cfb84)

Tagger: Brendon Smith <bws@bws.bio>

Date: 2023-12-30 23:32:52 -0500

```text
-----BEGIN SSH SIGNATURE-----
U1NIU0lHAAAAAQAAADMAAAALc3NoLWVkMjU1MTkAAAAgwLDNmire1DHY/g9GC1rGGr+mrE
kJ3FC96XsyoFKzm6IAAAADZ2l0AAAAAAAAAAZzaGE1MTIAAABTAAAAC3NzaC1lZDI1NTE5
AAAAQAF3qFeNTp+kyvuT1TShVDDEiVFHX1Q8awRvEOUeWvVWwwqbMG16SQRpa0IZTqS0su
rNjK8+Q4ehjpIdJf9ZHQo=
-----END SSH SIGNATURE-----
```

## 0.62.0 - 2023-12-30

### Changes

**Update to Uvicorn 0.24.0** (65883a9, 0d5ec23)

This release will update/upgrade to
[Uvicorn 0.24.0](https://github.com/encode/uvicorn/releases).
This is a minor release to align with Uvicorn versioning.

Uvicorn 0.24.0 adds support for Python 3.12 and for setting the app
instance with the environment variable `UVICORN_APP`. inboard already
has an environment variable for this purpose, `APP_MODULE`. Either
`APP_MODULE` or `UVICORN_APP` can be used to set the app module for
inboard, with precedence given to `APP_MODULE` for backward
compatibility.

### Commits

- Bump version from 0.61.0 to 0.62.0 (2270900)
- Support `UVICORN_APP` (0d5ec23)
- Update to Uvicorn 0.24.0 (65883a9)
- Update changelog for version 0.61.0 (#94) (665eaca)

Tagger: Brendon Smith <bws@bws.bio>

Date: 2023-12-30 22:54:49 -0500

```text
-----BEGIN SSH SIGNATURE-----
U1NIU0lHAAAAAQAAADMAAAALc3NoLWVkMjU1MTkAAAAgwLDNmire1DHY/g9GC1rGGr+mrE
kJ3FC96XsyoFKzm6IAAAADZ2l0AAAAAAAAAAZzaGE1MTIAAABTAAAAC3NzaC1lZDI1NTE5
AAAAQIyrvP6/M9MJfPIZnj6b/mOjUqg8ccL62HkThr4Qc+mHrVU9MzUUXEjviQ79QWdgep
sdduXo2l+rS6LRTlNiKAE=
-----END SSH SIGNATURE-----
```

## 0.61.0 - 2023-12-30

### Changes

**Update to FastAPI 0.108 and Starlette 0.32** (738d54a)

This release will update/upgrade to
[FastAPI 0.108](https://fastapi.tiangolo.com/release-notes/)
and
[Starlette 0.32](https://www.starlette.io/release-notes/).
This is a minor release to align with FastAPI versioning.

Changes to Starlette between 0.29 and 0.32 include dropping support for
Python 3.7, and adding support for Python 3.12 and AnyIO 4.

### Commits

- Bump version from 0.60.0 to 0.61.0 (ccc7bf2)
- Update to FastAPI 0.108 and Starlette 0.32 (738d54a)
- Update changelog for version 0.60.0 (#93) (b0d4a4a)

Tagger: Brendon Smith <bws@bws.bio>

Date: 2023-12-30 21:45:18 -0500

```text
-----BEGIN SSH SIGNATURE-----
U1NIU0lHAAAAAQAAADMAAAALc3NoLWVkMjU1MTkAAAAgwLDNmire1DHY/g9GC1rGGr+mrE
kJ3FC96XsyoFKzm6IAAAADZ2l0AAAAAAAAAAZzaGE1MTIAAABTAAAAC3NzaC1lZDI1NTE5
AAAAQPVNYaXJu4GQ4XkLI6QdfR3Hu+cW9wCtUhMa/mx5TwTKNG/LJFa/tN70EkqjFhYChW
dvle3+y/ats0Pbx+orKQ8=
-----END SSH SIGNATURE-----
```

## 0.60.0 - 2023-12-30

### Changes

**Update to FastAPI 0.107 and Starlette 0.28** (7d19e10)

This release will update/upgrade to
[FastAPI 0.107](https://fastapi.tiangolo.com/release-notes/)
and
[Starlette 0.28](https://www.starlette.io/release-notes/).
This is a minor release to align with FastAPI and Starlette versioning.

FastAPI 0.107 updates to Starlette 0.28. Starlette 0.28 moves exception
handling to the `Route` class and adds an error message if `TestClient`
runs without HTTPX installed.

### Commits

- Bump version from 0.59.0 to 0.60.0 (2be52ab)
- Update to FastAPI 0.107 and Starlette 0.28 (7d19e10)
- Update changelog for version 0.59.0 (#92) (92d281d)

Tagger: Brendon Smith <bws@bws.bio>

Date: 2023-12-30 20:39:34 -0500

```text
-----BEGIN SSH SIGNATURE-----
U1NIU0lHAAAAAQAAADMAAAALc3NoLWVkMjU1MTkAAAAgwLDNmire1DHY/g9GC1rGGr+mrE
kJ3FC96XsyoFKzm6IAAAADZ2l0AAAAAAAAAAZzaGE1MTIAAABTAAAAC3NzaC1lZDI1NTE5
AAAAQFWl5oLrbNwp0Xp0koktWi0MZppIjuyGbW1KSKlCrKllRhVRDWQyQ/hDoxZEw+TvKZ
s69MTHJ0xnrBSHYpeoewg=
-----END SSH SIGNATURE-----
```

## 0.59.0 - 2023-12-30

### Changes

**Update to FastAPI 0.106** (e3ece81)

This release will update/upgrade to
[FastAPI 0.106](https://fastapi.tiangolo.com/release-notes/).
This is a minor release to align with FastAPI versioning.

In FastAPI 0.74 (released in inboard 0.18.0 - 2022-03-05), the internal
`AsyncExitStack` was updated so that dependencies with `yield` could
catch exceptions like `HTTPException`.

FastAPI 0.106 builds on the 0.74 updates by introducing the ability to
raise exceptions after `yield`. This update includes a BREAKING CHANGE
because objects from dependencies with `yield` can no longer be used in
background tasks. The recommendation in the
[FastAPI docs](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/)
for updating background tasks is:

> If you used to rely on this behavior, now you should create the
> resources for background tasks inside the background task itself, and
> use internally only data that doesn't depend on the resources of
> dependencies with `yield`.
>
> For example, instead of using the same database session, you would
> create a new database session inside of the background task, and you
> would obtain the objects from the database using this new session. And
> then instead of passing the object from the database as a parameter to
> the background task function, you would pass the ID of that object and
> then obtain the object again inside the background task function.

### Commits

- Bump version from 0.58.0 to 0.59.0 (893fa7e)
- Update to FastAPI 0.106 (e3ece81)
- Update changelog for version 0.58.0 (#91) (0997ad3)

Tagger: Brendon Smith <bws@bws.bio>

Date: 2023-12-30 20:19:49 -0500

```text
-----BEGIN SSH SIGNATURE-----
U1NIU0lHAAAAAQAAADMAAAALc3NoLWVkMjU1MTkAAAAgwLDNmire1DHY/g9GC1rGGr+mrE
kJ3FC96XsyoFKzm6IAAAADZ2l0AAAAAAAAAAZzaGE1MTIAAABTAAAAC3NzaC1lZDI1NTE5
AAAAQPv4ymxbUuQV59Uuk606UuL6939xE/imK4T3T4VW5rTzgBd8ENkoG2e0wGaRVU8rH2
7Dj65ChjO8eaaJ1mu9Ags=
-----END SSH SIGNATURE-----
```

## 0.58.0 - 2023-12-30

### Changes

**Update to FastAPI 0.105** (5bc3013)

This release will update/upgrade to
[FastAPI 0.105](https://fastapi.tiangolo.com/release-notes/).
This is a minor release to align with FastAPI versioning.

FastAPI 0.105 adds support for `Annotated` dependencies with multiple
type annotations.

### Commits

- Bump version from 0.57.0 to 0.58.0 (e3eee4d)
- Update to FastAPI 0.105 (5bc3013)
- Update to `mypy==1.8.0` (2529780)
- Update to `hatch==1.9.1` (65e7363)
- Update to `pipx==1.4.0` (66f9560)
- Update to `pipx==1.3.3` (fb08b72)
- Update changelog for version 0.57.0 (#90) (f867910)

Tagger: Brendon Smith <bws@bws.bio>

Date: 2023-12-30 19:19:38 -0500

```text
-----BEGIN SSH SIGNATURE-----
U1NIU0lHAAAAAQAAADMAAAALc3NoLWVkMjU1MTkAAAAgwLDNmire1DHY/g9GC1rGGr+mrE
kJ3FC96XsyoFKzm6IAAAADZ2l0AAAAAAAAAAZzaGE1MTIAAABTAAAAC3NzaC1lZDI1NTE5
AAAAQOC/dNO7Uw4WziT5porc2n4a6QNN39T+tXWg4MNhcNNcnkmNbQDG+q4ousjb7tB/Kd
lWhXlwyzqZKqV/LsyTtQw=
-----END SSH SIGNATURE-----
```

## 0.57.0 - 2023-11-12

### Changes

**Update to FastAPI 0.104** (882084c)

This release will update/upgrade to
[FastAPI 0.104](https://fastapi.tiangolo.com/release-notes/).
This is a minor release to align with FastAPI versioning.

FastAPI 0.104 drops support for Python 3.7 and adds API reference docs
available [here](https://fastapi.tiangolo.com/reference/).

**Switch from pre-commit to Hatch scripts** (#89, 1a5450b)

pre-commit runs Git hooks. It can run on different Git events like
`pre-push` and can also easily run on CI (continuous integration)
platforms like GitHub Actions. These pre-commit hooks are often related
to code quality and help ensure code quality checks are continuously
enforced. While it is helpful for continuously running code quality
checks, pre-commit also has some downsides as detailed in #89.

This project was previously migrated from Poetry to Hatch in version
0.38.0 - 2023-02-26. As of this release, the project's code quality
checks will be migrated from pre-commit to Hatch scripts.

### Commits

- Bump version from 0.56.1 to 0.57.0 (a500ab1)
- Update to FastAPI 0.104 (882084c)
- Switch from pre-commit to Hatch scripts (#89) (1a5450b)
- Add attribute lists to CSpell `ignoreRegExpList` (03ac3f7)
- Update changelog for version 0.56.1 (#88) (1006821)

Tagger: Brendon Smith <bws@bws.bio>

Date: 2023-11-12 19:24:40 -0500

```text
-----BEGIN SSH SIGNATURE-----
U1NIU0lHAAAAAQAAADMAAAALc3NoLWVkMjU1MTkAAAAgwLDNmire1DHY/g9GC1rGGr+mrE
kJ3FC96XsyoFKzm6IAAAADZ2l0AAAAAAAAAAZzaGE1MTIAAABTAAAAC3NzaC1lZDI1NTE5
AAAAQBGlGdZ8YJ3lb8amnXO8qCufA0VAHXk7ah6NVYP7+JKdp8whnd5eSesgbq/h0hpGcx
OP/GebwS7COFBVDRLtcAU=
-----END SSH SIGNATURE-----
```

## 0.56.1 - 2023-11-12

### Changes

**Fix `uvicorn[standard]` version** (be409c4)

Uvicorn was updated to version 0.23.2 in 2590d8a and 0.56.0, but the
version number for `uvicorn[standard]` was not updated correspondingly.
This release will update `uvicorn[standard]` to 0.23.2.

**Update to Material for MkDocs 9** (ab692a3, 90f75b0)

Docs will now be built with
[Material for MkDocs 9](https://squidfunk.github.io/mkdocs-material/changelog/).
The most notable user-facing change is the new dark theme color palette,
which has undergone a few small changes since its release in version
9.4.0 (https://github.com/squidfunk/mkdocs-material/issues/6061).
Code block copy behavior has undergone some small changes as well. Code
blocks in the documentation have been reformatted for easier copying.

### Commits

- Bump version from 0.56.0 to 0.56.1 (0dba457)
- Fix `uvicorn[standard]` version (be409c4)
- Add docs deployment info to contributing.md (141d8e5)
- Remove Material for MkDocs version from README (b415bf4)
- Configure Material for MkDocs code block copy (90f75b0)
- Update to Material for MkDocs 9 (ab692a3)
- Relax upper bound on HTTPX (f49d205)
- Update to `mypy==1.7.0` (140dac6)
- Update changelog for version 0.56.0 (#86) (18f2052)

Tagger: Brendon Smith <bws@bws.bio>

Date: 2023-11-12 16:12:24 -0500

```text
-----BEGIN SSH SIGNATURE-----
U1NIU0lHAAAAAQAAADMAAAALc3NoLWVkMjU1MTkAAAAgwLDNmire1DHY/g9GC1rGGr+mrE
kJ3FC96XsyoFKzm6IAAAADZ2l0AAAAAAAAAAZzaGE1MTIAAABTAAAAC3NzaC1lZDI1NTE5
AAAAQL6WBwGZdDVKFstxw3kQbhFNhbF+veYd9SUL2/Ow96kSl+4IHdtP2Bt0Q/fHUTGWTN
myCfgotFST8FYZrUXVXg4=
-----END SSH SIGNATURE-----
```

## 0.56.0 - 2023-09-09

### Changes

**Update to Uvicorn 0.23.2** (2590d8a)

This release will update/upgrade from Uvicorn 0.22.0 to
[Uvicorn 0.23.2](https://github.com/encode/uvicorn/blob/HEAD/CHANGELOG.md).
This is a minor release to align with Uvicorn versioning.

[Changes](https://github.com/encode/uvicorn/compare/0.22.0...0.23.2)
to Uvicorn since 0.22.0 include:

- Drop support for Python 3.7
- Switch to a vendored copy of `asgiref.typing` at `uvicorn._types`
- Add a new option `--ws-max-queue`
- Make a small scope change in
  `uvicorn.middleware.proxy_headers.ProxyHeadersMiddleware`.

### Commits

- Bump version from 0.55.0 to 0.56.0 (4b92cef)
- Update to Uvicorn 0.23.2 (2590d8a)
- Update changelog for version 0.55.0 (#85) (62ec752)

Tagger: Brendon Smith <bws@bws.bio>

Date: 2023-09-09 02:49:44 -0400

```text
-----BEGIN SSH SIGNATURE-----
U1NIU0lHAAAAAQAAADMAAAALc3NoLWVkMjU1MTkAAAAgwLDNmire1DHY/g9GC1rGGr+mrE
kJ3FC96XsyoFKzm6IAAAADZ2l0AAAAAAAAAAZzaGE1MTIAAABTAAAAC3NzaC1lZDI1NTE5
AAAAQMyogYm3InfkXujOKK1leXR8UvO+nhEvBkD9BYJQBAuvWDscvGw/2iWsOes9ed71z0
eY0f7p7yvJTTChCKqZHgs=
-----END SSH SIGNATURE-----
```

## 0.55.0 - 2023-09-09

### Changes

**Update to FastAPI 0.103** (b6aef8b)

This release will update/upgrade to
[FastAPI 0.103](https://fastapi.tiangolo.com/release-notes/).
This is a minor release to align with FastAPI versioning

FastAPI 0.103 adds support for an `openapi_examples` keyword argument
as described in the
[docs](https://fastapi.tiangolo.com/tutorial/schema-extra-example/#openapi-specific-examples)
and sets a temporary upper bound on AnyIO of `anyio>=3.7.1,<4.0.0`,
separately from Starlette, to help with the update to Starlette 0.31.

### Commits

- Bump version from 0.54.0 to 0.55.0 (f2acd2c)
- Update to FastAPI 0.103 (b6aef8b)
- Update changelog for version 0.54.0 (#84) (b348793)

Tagger: Brendon Smith <bws@bws.bio>

Date: 2023-09-09 01:59:11 -0400

```text
-----BEGIN SSH SIGNATURE-----
U1NIU0lHAAAAAQAAADMAAAALc3NoLWVkMjU1MTkAAAAgwLDNmire1DHY/g9GC1rGGr+mrE
kJ3FC96XsyoFKzm6IAAAADZ2l0AAAAAAAAAAZzaGE1MTIAAABTAAAAC3NzaC1lZDI1NTE5
AAAAQKnGlapkHaYsj2+BnN2iwPI/GhszOKudq0nULAQxlwm+lVm4kFiUDadbzPjZLQyp3j
V94wCWuOsz1mQkj8XsTwI=
-----END SSH SIGNATURE-----
```

## 0.54.0 - 2023-09-09

### Changes

**Update to FastAPI 0.102**

This release will update/upgrade to
[FastAPI 0.102](https://fastapi.tiangolo.com/release-notes/).
This is a minor release to align with FastAPI versioning.

FastAPI 0.101 added support for
[Pydantic computed fields](https://docs.pydantic.dev/latest/usage/computed_fields/)
and altered responses to use
[Pydantic serialization](https://docs.pydantic.dev/latest/usage/serialization/).
The change to Pydantic serialization in FastAPI 0.101 separated input
and output schemas, altering responses and OpenAPI schema generation.
Due to the lack of backwards compatibility and the associated issues
([tiangolo/fastapi#10011 (comment)](https://github.com/tiangolo/fastapi/pull/10011#issuecomment-1676624793),
[tiangolo/fastapi#10019](https://github.com/tiangolo/fastapi/discussions/10019),
[tiangolo/fastapi#10041](https://github.com/tiangolo/fastapi/discussions/10041)),
the update to FastAPI 0.101 may be a **BREAKING CHANGE** for some users.

FastAPI 0.102 builds on the serialization changes introduced in 0.101 by
adding docs explaining the serialization behavior and by adding a new
optional keyword argument for disabling the new behavior.

If the Pydantic serialization behavior affects your project adversely,
disable it with `separate_input_output_schemas=False` on the FastAPI app
(`app = FastAPI(separate_input_output_schemas=False)`) as shown in the
[FastAPI docs](https://fastapi.tiangolo.com/how-to/separate-openapi-schemas/).

### Commits

- Bump version from 0.53.0 to 0.54.0 (59a3dd0)
- Update changelog for version 0.53.0 (#83) (04dfec9)
- Update to FastAPI 0.102 (05abd20)

Tagger: Brendon Smith <bws@bws.bio>

Date: 2023-09-09 01:38:29 -0400

```text
-----BEGIN SSH SIGNATURE-----
U1NIU0lHAAAAAQAAADMAAAALc3NoLWVkMjU1MTkAAAAgwLDNmire1DHY/g9GC1rGGr+mrE
kJ3FC96XsyoFKzm6IAAAADZ2l0AAAAAAAAAAZzaGE1MTIAAABTAAAAC3NzaC1lZDI1NTE5
AAAAQNuHAVn5dYf9p58K567zJ9JKb+tGY5i7rBDBvRv4Wg95dzyQem2FJw86AAIKVeWbdI
+RTrFee2U+ob95nufGCAc=
-----END SSH SIGNATURE-----
```

## 0.53.0 - 2023-09-08

### Changes

**Update to FastAPI 0.101** (9d54839)

This release will update/upgrade to
[FastAPI 0.101](https://fastapi.tiangolo.com/release-notes/).

FastAPI 0.101 adds support for
[Pydantic computed fields](https://docs.pydantic.dev/latest/usage/computed_fields/)
and alters responses to use
[Pydantic serialization](https://docs.pydantic.dev/latest/usage/serialization/).
The change to Pydantic serialization in FastAPI 0.101 separates input
and output schemas, altering responses and OpenAPI schema generation.
Due to the lack of backwards compatibility and the associated issues
([tiangolo/fastapi#10011 (comment)](https://github.com/tiangolo/fastapi/pull/10011#issuecomment-1676624793),
[tiangolo/fastapi#10019](https://github.com/tiangolo/fastapi/discussions/10019),
[tiangolo/fastapi#10041](https://github.com/tiangolo/fastapi/discussions/10041)),
the update to FastAPI 0.101 may be a **BREAKING CHANGE** for some users.

How to deal with this breaking change:

- If this change affects your project adversely, skip FastAPI 0.101 and
  update to FastAPI 0.102 (upcoming in the next inboard release).
- Set `separate_input_output_schemas=False` on the FastAPI app instance
  (`app = FastAPI(separate_input_output_schemas=False)`) as shown in the
  [FastAPI docs](https://fastapi.tiangolo.com/how-to/separate-openapi-schemas/).

### Commits

- Bump version from 0.52.0 to 0.53.0 (825b08c)
- Update to FastAPI 0.101 (9d54839)
- Update changelog for version 0.52.0 (#82) (9c18aa0)

Tagger: Brendon Smith <bws@bws.bio>

Date: 2023-09-08 21:12:24 -0400

```text
-----BEGIN SSH SIGNATURE-----
U1NIU0lHAAAAAQAAADMAAAALc3NoLWVkMjU1MTkAAAAgwLDNmire1DHY/g9GC1rGGr+mrE
kJ3FC96XsyoFKzm6IAAAADZ2l0AAAAAAAAAAZzaGE1MTIAAABTAAAAC3NzaC1lZDI1NTE5
AAAAQDzobOTKnKOTl9Afrg6x4S0Bp5AQhi/LSHKb7DTDG9iQZj0AhrWcPB8H2oKoVtM4vS
s629NlSWTlkwSktrP5hgU=
-----END SSH SIGNATURE-----
```

## 0.52.0 - 2023-08-20

### Changes

**Update to FastAPI 0.100** (de4d583)

This release will update/upgrade to
[FastAPI 0.100](https://fastapi.tiangolo.com/release-notes/).
This is a minor release to align with FastAPI versioning.

FastAPI 0.100 includes support for
[Pydantic 2](https://docs.pydantic.dev/2.0/migration/)
and installs Pydantic 2 by default, which can be a **BREAKING CHANGE**
depending on each project's usage of Pydantic.

How to deal with this breaking change:

- First, update requirements files with `"pydantic==1.*"` to avoid
  automatically updating to Pydantic 2.
- Next, remove `"pydantic==1.*"` from requirements files,
  install Pydantic 2, and follow the
  [Pydantic 2 migration guide](https://docs.pydantic.dev/2.0/migration/).

**Remove Poetry 1.1 from Docker images** (b36b351)

As described in the changelog entry for
[inboard 0.38](https://inboard.bws.bio/changelog#0380-2023-02-26) and
the [inboard docs](https://inboard.bws.bio/docker#docker-and-poetry),
inboard switched its dependency management and packaging from Poetry 1.1
to Hatch. Poetry 1.1 was retained in the inboard Docker images for
backwards compatibility, but Poetry 1.1 is unmaintained and so it must
eventually be removed.

This release will remove Poetry 1.1 from the inboard Docker images.
This is a **BREAKING CHANGE**.

How to deal with this breaking change:

- If you are not using Poetry there are no changes needed.
- If you are still using Poetry add `RUN pipx install poetry`
  to your Dockerfile.

### Commits

- Bump version from 0.51.0 to 0.52.0 (be3c16c)
- Update to FastAPI 0.100 (de4d583)
- Remove Poetry 1.1 from Docker images (b36b351)
- Update changelog for version 0.51.0 (#81) (fbda899)

Tagger: Brendon Smith <bws@bws.bio>

Date: 2023-08-20 16:40:57 -0400

```text
-----BEGIN SSH SIGNATURE-----
U1NIU0lHAAAAAQAAADMAAAALc3NoLWVkMjU1MTkAAAAgwLDNmire1DHY/g9GC1rGGr+mrE
kJ3FC96XsyoFKzm6IAAAADZ2l0AAAAAAAAAAZzaGE1MTIAAABTAAAAC3NzaC1lZDI1NTE5
AAAAQDtnqxHqpV4mf/QSxERfC1ypdVPb8cpDp6TpvBGcxM1iDQ/a62BbMgZ0ja7JpKRTIT
cZZYkLRlZyJEmV85IzVwE=
-----END SSH SIGNATURE-----
```

## 0.51.0 - 2023-07-09

### Changes

**Update to FastAPI 0.99** (19be870)

This release will update/upgrade to
[FastAPI 0.99](https://fastapi.tiangolo.com/release-notes/).
This is a minor release to align with FastAPI versioning.

FastAPI 0.99 adds support for OpenAPI 3.1.0, which allows webhooks to be
documented as described in the
[FastAPI docs](https://fastapi.tiangolo.com/advanced/openapi-webhooks/).

FastAPI 0.99 is also the last minor version before introducing support
for Pydantic 2.

**UPCOMING BREAKING CHANGE**: Update to FastAPI 0.100 and Pydantic 2

The next minor release of inboard will update to
[FastAPI 0.100](https://fastapi.tiangolo.com/release-notes/).
FastAPI 0.100 includes support for
[Pydantic 2](https://docs.pydantic.dev/2.0/migration/)
and installs Pydantic 2 by default, which can be a breaking change
depending on each project's usage of Pydantic.

How to deal with this breaking change:

- First, update requirements files with `"pydantic==1.*"` to avoid
  automatically updating to Pydantic 2.
- Next, remove `"pydantic==1.*"` from requirements files,
  install Pydantic 2, and follow the
  [Pydantic 2 migration guide](https://docs.pydantic.dev/2.0/migration/).

**UPCOMING BREAKING CHANGE**: Remove Poetry 1.1 from Docker images

As described in the changelog entry for
[inboard 0.38](https://inboard.bws.bio/changelog#0380-2023-02-26) and
the [inboard docs](https://inboard.bws.bio/docker#docker-and-poetry),
inboard switched its dependency management and packaging from Poetry 1.1
to Hatch. Poetry 1.1 was retained in the inboard Docker images for
backwards compatibility, but Poetry 1.1 is unmaintained and so it must
eventually be removed.

The next minor release of inboard will remove Poetry 1.1 from the
inboard Docker images.

How to deal with this breaking change:

- If you are not using Poetry there are no changes needed.
- If you are still using Poetry add `RUN pipx install poetry`
  to your Dockerfile.

**Note about automatic update to Debian bookworm**

On 2023-06-14, Docker updated the default Debian Linux version in its
Python official images from Debian bullseye to Debian bookworm
(https://github.com/docker-library/official-images/pull/14854).
As inboard uses the default Debian Linux version from the Docker Python
official images, this meant that the next release of inboard
(0.50.0 - 2023-06-22) automatically updated to bookworm. There have been
[some issues](https://github.com/docker-library/python/issues?q=bookworm)
noted by the community after this update. Thanks to @bodograumann for
pointing this out in the related
[discussion](https://github.com/br3ndonland/inboard/discussions/80).

### Commits

- Bump version from 0.50.0 to 0.51.0 (be5c444)
- Update to FastAPI 0.99 (19be870)
- Update changelog for version 0.50.0 (#79) (a38228a)

Tagger: Brendon Smith <bws@bws.bio>

Date: 2023-07-09 17:29:02 -0400

```text
-----BEGIN SSH SIGNATURE-----
U1NIU0lHAAAAAQAAADMAAAALc3NoLWVkMjU1MTkAAAAgwLDNmire1DHY/g9GC1rGGr+mrE
kJ3FC96XsyoFKzm6IAAAADZ2l0AAAAAAAAAAZzaGE1MTIAAABTAAAAC3NzaC1lZDI1NTE5
AAAAQNOcjc4cqdPs/U4UBsp8YSXLn7D6L+vntLOPbcRPYwrh1LcfmsJiTTksFpSH1/Txdj
+dCD3poVckre2P0PqqXQo=
-----END SSH SIGNATURE-----
```

## 0.50.0 - 2023-06-22

### Changes

**Update to FastAPI 0.98** (0484e11)

This release will update/upgrade to
[FastAPI 0.98](https://fastapi.tiangolo.com/release-notes/).
This is a minor release to align with FastAPI versioning.

FastAPI 0.98 adds support for an app-level `redirect_slashes` argument.

### Commits

- Bump version from 0.49.0 to 0.50.0 (174e02c)
- Update to FastAPI 0.98 (0484e11)
- Update changelog for version 0.49.0 (#78) (a9670c1)

Tagger: Brendon Smith <bws@bws.bio>

Date: 2023-06-22 19:12:15 -0400

```text
-----BEGIN SSH SIGNATURE-----
U1NIU0lHAAAAAQAAADMAAAALc3NoLWVkMjU1MTkAAAAgwLDNmire1DHY/g9GC1rGGr+mrE
kJ3FC96XsyoFKzm6IAAAADZ2l0AAAAAAAAAAZzaGE1MTIAAABTAAAAC3NzaC1lZDI1NTE5
AAAAQBsAeIUdwCMuOWMCI8UMu/v8FiRnP3qzwe7rJrLnbYhGs7y/x1HmQNkVJf9BdipqMK
bBBOoUsyGmpLO3WH26jgU=
-----END SSH SIGNATURE-----
```

## 0.49.0 - 2023-06-12

### Changes

**Update to FastAPI 0.97** (438e4e1)

This release will update/upgrade to FastAPI 0.97.
This is a minor release to align with FastAPI versioning.
[FastAPI 0.97](https://fastapi.tiangolo.com/release-notes/)
adds support for dependencies in WebSocket routes.

### Commits

- Bump version from 0.48.0 to 0.49.0 (cc49fa0)
- Update to FastAPI 0.97 (438e4e1)
- Update changelog for version 0.48.0 (#77) (edef011)

Tagger: Brendon Smith <bws@bws.bio>

Date: 2023-06-12 08:27:56 -0400

```text
-----BEGIN SSH SIGNATURE-----
U1NIU0lHAAAAAQAAADMAAAALc3NoLWVkMjU1MTkAAAAgwLDNmire1DHY/g9GC1rGGr+mrE
kJ3FC96XsyoFKzm6IAAAADZ2l0AAAAAAAAAAZzaGE1MTIAAABTAAAAC3NzaC1lZDI1NTE5
AAAAQNx0m6uq+6v5P8lZYB8pvTyyHlbwIgqNYVP7kck092h/N6jCeYE+7y8y7Sgpaibvpl
dbzX9Iuxpx3pRCR0vOqAc=
-----END SSH SIGNATURE-----
```

## 0.48.0 - 2023-06-11

### Changes

**Update to Uvicorn 0.22** (#74, 32a0ae8)

This release will update/upgrade to Uvicorn 0.22.
This is a minor release to align with Uvicorn versioning.

[Uvicorn 0.22](https://github.com/encode/uvicorn/blob/HEAD/CHANGELOG.md)
adds a `--timeout-graceful-shutdown` option and
fixes the `--reload-delay` option when using `watchfiles`.

### Commits

- Bump version from 0.47.0 to 0.48.0 (91aaa54)
- Update to Uvicorn 0.22 (#74) (32a0ae8) by @bodograumann
- Update changelog for version 0.47.0 (#76) (532553c)

Tagger: Brendon Smith <bws@bws.bio>

Date: 2023-06-11 12:56:16 -0400

```text
-----BEGIN SSH SIGNATURE-----
U1NIU0lHAAAAAQAAADMAAAALc3NoLWVkMjU1MTkAAAAgwLDNmire1DHY/g9GC1rGGr+mrE
kJ3FC96XsyoFKzm6IAAAADZ2l0AAAAAAAAAAZzaGE1MTIAAABTAAAAC3NzaC1lZDI1NTE5
AAAAQPF6NZXShLkK5G/aMfKDFkbJBj98adenYtMSMxHISlhVTBldfoF4pg/oWB8o9+m4Sd
I41WXRci/2+J5Y+tQ9nQE=
-----END SSH SIGNATURE-----
```

## 0.47.0 - 2023-06-11

### Changes

**Update to FastAPI 0.96** (a83bd71)

This release will update/upgrade to
[FastAPI 0.96](https://fastapi.tiangolo.com/release-notes/).
This is a minor release to align with FastAPI versioning.

FastAPI 0.96 improves the performance of `create_cloned_field`, which is
used by FastAPI internally when instantiating API routes. See FastAPI
[discussions](https://github.com/tiangolo/fastapi/discussions/8609) for
further info.

### Commits

- Bump version from 0.46.0 to 0.47.0 (dc258df)
- Update to FastAPI 0.96 (a83bd71)
- Update changelog for version 0.46.0 (#75) (c22f101)

Tagger: Brendon Smith <bws@bws.bio>

Date: 2023-06-11 12:19:44 -0400

```text
-----BEGIN SSH SIGNATURE-----
U1NIU0lHAAAAAQAAADMAAAALc3NoLWVkMjU1MTkAAAAgwLDNmire1DHY/g9GC1rGGr+mrE
kJ3FC96XsyoFKzm6IAAAADZ2l0AAAAAAAAAAZzaGE1MTIAAABTAAAAC3NzaC1lZDI1NTE5
AAAAQCAcAGisg7HPa0lz8jaCT+/7yVm38R39K6ymsACfg0jNeXX0/+gOOJpHy9peL73ul0
2Bsp802N/DDPvOntc5dgY=
-----END SSH SIGNATURE-----
```

## 0.46.0 - 2023-06-11

### Changes

**Update to FastAPI 0.95 and Starlette 0.27** (e6280fb)

This release will update/upgrade to FastAPI 0.95 and Starlette 0.27.
This is a minor release to align with FastAPI and Starlette versioning.

[FastAPI 0.95](https://fastapi.tiangolo.com/release-notes/) introduces
`Annotated` for
[dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/).
`Annotated` sets up a dependency for easier reuse. This provides some
benefits when specifying dependencies as function arguments because
dependencies don't need to be specified in endpoint function default
arguments. `Annotated` is part of the
[`typing`](https://docs.python.org/3/library/typing.html)
standard library package starting in Python 3.9.

[Starlette 0.27](https://www.starlette.io/release-notes/)
resolves a low-severity security
[vulnerability](https://github.com/encode/starlette/security/advisories/GHSA-v5gw-mw7f-84px)
related to the [`StaticFiles`](https://www.starlette.io/staticfiles/)
class.

### Commits

- Bump version from 0.45.0 to 0.46.0 (8068c53)
- Update to FastAPI 0.95 and Starlette 0.27 (e6280fb)
- Relate inboard, FastAPI, and Uvicorn versions (e413a04)
- Update to `hatch==1.7.0` (6addfac)
- Remove Sourcery configuration file (d8d8c67)
- Update Black in pre-commit (307789a)
- Update to `mypy==1.3.0` (2bffd80)
- Update to pytest-timeout 2 (e79cec3)
- Update to coverage 7 (68a95d1)
- Use `urllib3<2` for HTTPie `DEFAULT_CIPHERS` (0f76e62)
- Prepend `$HATCH_ENV` in GitHub Actions workflow (93e1c40)
- Update to `pipx==1.2.0` (0a50baa)
- Update changelog for version 0.45.0 (#73) (b05c6d4)

Tagger: Brendon Smith <bws@bws.bio>

Date: 2023-06-11 11:39:11 -0400

```text
-----BEGIN SSH SIGNATURE-----
U1NIU0lHAAAAAQAAADMAAAALc3NoLWVkMjU1MTkAAAAgwLDNmire1DHY/g9GC1rGGr+mrE
kJ3FC96XsyoFKzm6IAAAADZ2l0AAAAAAAAAAZzaGE1MTIAAABTAAAAC3NzaC1lZDI1NTE5
AAAAQPeicGEzi2rV33fZJpwPkoEgu1JnDudtNwgdyKzzcqlJiQbieC3rbeIRBG/R3ubS2X
EGsMwYSOJJxe05obOITAE=
-----END SSH SIGNATURE-----
```

## 0.45.0 - 2023-03-18

### Changes

**Update to Uvicorn 0.21.1** (768c95f)

This release will update/upgrade to Uvicorn 0.21.1.
This is a minor release to align with Uvicorn versioning.

Uvicorn 0.21 introduces support for lifespan state.
No docs or PR descriptions were provided to explain how this works. See
the [FastAPI docs](https://fastapi.tiangolo.com/advanced/events/) and
[Starlette docs](https://www.starlette.io/lifespan/) for further info.

### Commits

`0.44.0..0.45.0`

- Bump version from 0.44.0 to 0.45.0 (bdb5be4)
- Update to Uvicorn 0.21.1 (768c95f)
- Update changelog for version 0.44.0 (#72) (58800ce)

Tagger: Brendon Smith <bws@bws.bio>

Date: 2023-03-18 14:18:15 -0400

```text
-----BEGIN SSH SIGNATURE-----
U1NIU0lHAAAAAQAAADMAAAALc3NoLWVkMjU1MTkAAAAgwLDNmire1DHY/g9GC1rGGr+mrE
kJ3FC96XsyoFKzm6IAAAADZ2l0AAAAAAAAAAZzaGE1MTIAAABTAAAAC3NzaC1lZDI1NTE5
AAAAQCNBHs+qA9EuXbfGOyRMo/dnG2hA8nrgEbSsWvVPTWlJcnJbnTdbVfvO6KVOfbw9Cr
LCGuj+m2APXBD+NLZXzwU=
-----END SSH SIGNATURE-----
```

## 0.44.0 - 2023-03-11

### Changes

**Update to FastAPI 0.94 and Starlette 0.26** (f32d492)

This release will update/upgrade to FastAPI 0.94 and Starlette 0.26.
This is a minor release to align with FastAPI and Starlette versioning.

FastAPI 0.94 and Starlette 0.26 introduce support for lifespan state.
See the [FastAPI docs](https://fastapi.tiangolo.com/advanced/events/)
and [Starlette docs](https://www.starlette.io/lifespan/) for more info.

Starlette 0.26 deprecates `on_startup` and `on_shutdown` events. See
[FastAPI 0.93](https://github.com/tiangolo/fastapi/releases/tag/0.93.0),
the [FastAPI docs](https://fastapi.tiangolo.com/advanced/events/), and
[encode/starlette#2067](https://github.com/encode/starlette/discussions/2067)
for more info.

### Commits

`0.43.0..0.44.0`

- Bump version from 0.43.0 to 0.44.0 (c289f24)
- Update to FastAPI 0.94 and Starlette 0.26 (f32d492)
- Update changelog for version 0.43.0 (#71) (133926c)

Tagger: Brendon Smith <bws@bws.bio>

Date: 2023-03-11 17:52:04 -0500

```text
-----BEGIN SSH SIGNATURE-----
U1NIU0lHAAAAAQAAADMAAAALc3NoLWVkMjU1MTkAAAAgwLDNmire1DHY/g9GC1rGGr+mrE
kJ3FC96XsyoFKzm6IAAAADZ2l0AAAAAAAAAAZzaGE1MTIAAABTAAAAC3NzaC1lZDI1NTE5
AAAAQKB4LPEz/W9pdK3fNXhqWAkrA1C+hbAx1WmfyZxGveNKrtOQyGRSZRku5iwQ6mkufK
udwOlmNG6uL4vGvNyY/QE=
-----END SSH SIGNATURE-----
```

## 0.43.0 - 2023-03-11

### Changes

**Update to FastAPI 0.93** (4a52ee2)

This release will update/upgrade to FastAPI 0.93.
This is a minor release to align with FastAPI versioning.

FastAPI 0.93 introduces support for lifespan context managers, which are
intended to supersede startup and shutdown events. See the
[FastAPI docs](https://fastapi.tiangolo.com/advanced/events/) and
[encode/starlette#2067](https://github.com/encode/starlette/discussions/2067)
for more info.

### Commits

`0.42.0..0.43.0`

- Bump version from 0.42.0 to 0.43.0 (631f67b)
- Update to FastAPI 0.93 (4a52ee2)
- Update to mypy 1.1.1 (127c28d)
- Update changelog for version 0.42.0 (#70) (27d2b42)

Tagger: Brendon Smith <bws@bws.bio>

Date: 2023-03-11 17:28:44 -0500

```text
-----BEGIN SSH SIGNATURE-----
U1NIU0lHAAAAAQAAADMAAAALc3NoLWVkMjU1MTkAAAAgwLDNmire1DHY/g9GC1rGGr+mrE
kJ3FC96XsyoFKzm6IAAAADZ2l0AAAAAAAAAAZzaGE1MTIAAABTAAAAC3NzaC1lZDI1NTE5
AAAAQOG7MvohC/o0eWntYFDmC/a9+tccUDXYAYEw8PrO7gdIMjj10WmQ2zdxMRrYVcjWye
d81tdbCy3+LE4DJK60eAY=
-----END SSH SIGNATURE-----
```

## 0.42.0 - 2023-03-05

### Changes

**Update to FastAPI 0.92 and Starlette 0.25** (e8330ea)

This release will update/upgrade to FastAPI 0.92 and Starlette 0.25.
This is a minor release to align with FastAPI and Starlette versioning.

[Starlette 0.25.0](https://github.com/encode/starlette/releases/tag/0.25.0)
fixes a security vulnerability related to forms. The release notes don't
really explain this fix, but the release notes for
[FastAPI 0.92.0](https://github.com/tiangolo/fastapi/releases/tag/0.92.0)
provide some additional explanation.

### Commits

`0.41.0..0.42.0`

- Bump version from 0.41.0 to 0.42.0 (b36b277)
- Update to FastAPI 0.92 and Starlette 0.25 (e8330ea)
- Update changelog for version 0.41.0 (#69) (b370982)

Tagger: Brendon Smith <bws@bws.bio>

Date: 2023-03-05 13:38:53 -0500

```text
-----BEGIN SSH SIGNATURE-----
U1NIU0lHAAAAAQAAADMAAAALc3NoLWVkMjU1MTkAAAAgwLDNmire1DHY/g9GC1rGGr+mrE
kJ3FC96XsyoFKzm6IAAAADZ2l0AAAAAAAAAAZzaGE1MTIAAABTAAAAC3NzaC1lZDI1NTE5
AAAAQEyP2r0uHUQrMctSAE0wMZzS3ZiTa4rRgfYfzhV4wyRA1EkW2n6Cmn50kYsdYwFigr
jc2aDef4dHviQTMp2V7QQ=
-----END SSH SIGNATURE-----
```

## 0.41.0 - 2023-03-05

### Changes

**Update to FastAPI 0.91 and Starlette 0.24** (1474fa9)

This release will update/upgrade to FastAPI 0.91 and Starlette 0.24.
This is a minor release to align with FastAPI and Starlette versioning.

Starlette 0.24 improves handling of middleware stacks
(encode/starlette#2017).

Starlette is no longer documenting (but not yet deprecating) the
`app.add_middleware` syntax in favor of passing a middleware list
as a kwarg to `Starlette()` (`Starlette(middleware=middleware)`)
(encode/starlette#1481). The recommended syntax allows for more
predictable ordering of middleware lists, so that they are added to the
Starlette app and initialized in expected order (encode/starlette#1490).

Use of the `app.add_middleware` syntax in the inboard example Starlette
and FastAPI apps will be replaced with the recommended approach.

### Commits

`0.40.0..0.41.0`

- Bump version from 0.40.0 to 0.41.0 (6ba5a5c)
- Update to recommended Starlette middleware syntax (ec752d2)
- Update to FastAPI 0.91 and Starlette 0.24 (1474fa9)
- Update changelog for version 0.40.0 (#68) (26565af)

Tagger: Brendon Smith <bws@bws.bio>

Date: 2023-03-05 12:40:27 -0500

```text
-----BEGIN SSH SIGNATURE-----
U1NIU0lHAAAAAQAAADMAAAALc3NoLWVkMjU1MTkAAAAgwLDNmire1DHY/g9GC1rGGr+mrE
kJ3FC96XsyoFKzm6IAAAADZ2l0AAAAAAAAAAZzaGE1MTIAAABTAAAAC3NzaC1lZDI1NTE5
AAAAQAoc+1yAEqIvV/Lkx83SlsA+FDvOsaeLgCNcMQCM8NHcU6vwFA5idfXFLFhXN8UaGZ
UmawDEgUHdFm/wiogEawo=
-----END SSH SIGNATURE-----
```

## 0.40.0 - 2023-03-02

### Changes

**Update to FastAPI 0.90 and Starlette 0.23** (89caa66)

This release will update/upgrade to FastAPI 0.90 and Starlette 0.23.
This is a minor release to align with FastAPI and Starlette versioning.

[Starlette 0.23](https://github.com/encode/starlette/releases/tag/0.23.0)
begins a deprecation process for some of the `Router` and `Starlette`
decorators like `route`, as described in the
[Starlette routing docs](https://www.starlette.io/routing/).

Use of the `@app.route` decorator in the inboard example Starlette app
will be replaced with the recommended approach.

### Commits

`0.39.0..0.40.0`

- Bump version from 0.39.0 to 0.40.0 (30c9794)
- Remove deprecated Starlette `route` decorators (44ad641)
- Update to FastAPI 0.90 and Starlette 0.23 (89caa66)
- Update changelog for version 0.39.0 (#67) (544c8d5)

Tagger: Brendon Smith <bws@bws.bio>

Date: 2023-03-02 00:12:35 -0500

```text
-----BEGIN SSH SIGNATURE-----
U1NIU0lHAAAAAQAAADMAAAALc3NoLWVkMjU1MTkAAAAgwLDNmire1DHY/g9GC1rGGr+mrE
kJ3FC96XsyoFKzm6IAAAADZ2l0AAAAAAAAAAZzaGE1MTIAAABTAAAAC3NzaC1lZDI1NTE5
AAAAQLnCn0RoJl32W0QCGgISftL7HZLL5BLtYm2obtagd8dvDPGRdZcQciMWyYY8wJaZnu
+VUWcsS36YU0hKx+kDYwU=
-----END SSH SIGNATURE-----
```

## 0.39.0 - 2023-03-01

### Changes

**Update to FastAPI 0.89** (7f5e76d)

This release will update/upgrade to
[FastAPI 0.89](https://github.com/tiangolo/fastapi/releases).
This is a minor release to align with FastAPI's versioning strategy.

Note that, as of FastAPI 0.89, FastAPI can now infer the response model
from an API endpoint function's return type, so there is no longer need
for the `response_model` argument in most cases. See the
[updated docs](https://fastapi.tiangolo.com/tutorial/response-model/)
for further info.

### Commits

`0.38.0..0.39.0`

- Bump version from 0.38.0 to 0.39.0 (e80f7de)
- Remove `response_model` usage (0ec39d9)
- Update to FastAPI 0.89 (7f5e76d)
- Update changelog for version 0.38.0 (#66) (c437fd8)

Tagger: Brendon Smith <bws@bws.bio>

Date: 2023-03-01 20:49:55 -0500

```text
-----BEGIN SSH SIGNATURE-----
U1NIU0lHAAAAAQAAADMAAAALc3NoLWVkMjU1MTkAAAAgwLDNmire1DHY/g9GC1rGGr+mrE
kJ3FC96XsyoFKzm6IAAAADZ2l0AAAAAAAAAAZzaGE1MTIAAABTAAAAC3NzaC1lZDI1NTE5
AAAAQLW5+w8I2L72+rEa2a2czxhc0lxD5eWA8khMLA0lgx7T7PhPapsoN5jEU5uiff/vIw
QatgDmaLZ/+gOSwZ054Qc=
-----END SSH SIGNATURE-----
```

## 0.38.0 - 2023-02-26

### Changes

**Add Python 3.11 support** (#62)

- inboard will now run tests with Python 3.11, in addition to 3.8-3.10
- inboard will now build and publish its PyPI package using Python 3.11
- inboard will now include a Python 3.11 classifier in its PyPI package
- inboard will now ship Docker images running Python 3.11, in addition
  to 3.8-3.10, and Docker images tagged with `latest` will now use 3.11

**Update to Uvicorn 0.20.0** (13cd921)

This commit will update/upgrade from
[Uvicorn 0.17.6](https://github.com/encode/uvicorn/releases/tag/0.17.6)
to
[Uvicorn 0.20.0](https://github.com/encode/uvicorn/releases/tag/0.20.0).

Uvicorn 0.20.0 will be pinned exactly to avoid problematic or breaking
changes in future patch releases.

[Uvicorn 0.18](https://github.com/encode/uvicorn/releases/tag/0.18.3)
was skipped for the following reasons:

- As of Uvicorn 0.18.0, Uvicorn now prioritizes `watchfiles` instead of
  `watchgod`. `watchfiles` uses Rust binary extensions, which can have
  issues on Alpine Linux and macOS with Apple Silicon (M1/M2), and the
  evaluation process took some time. It does appear that `watchfiles` is
  now publishing wheels with `musllinux` tags, so Alpine Linux should be
  generally compatible. Apple Silicon Macs should be compatible as of
  `watchfiles` 0.16.
- The `h11_max_incomplete_event_size` setting was added in 0.18.0 with
  an incorrect default, then updated in 0.18.1 with a correct default.
- A temporary breaking change was made to the Uvicorn logging module.
  It was renamed from `uvicorn.logging` to `uvicorn._logging` in 0.18.0
  (a breaking change that was not mentioned in the release notes), then
  reverted back to `uvicorn.logging` in 0.18.2. A change to the logging
  module path could break inboard `LOG_FORMAT=uvicorn`.
- A temporary breaking change was made to the Uvicorn logging config.
  The logging config default was changed from `LOGGING_CONFIG` to `None`
  in 0.18.0, which resulted in logs not being shown at all. The default
  was then reverted to `LOGGING_CONFIG` in 0.18.2.
- The type annotation and default value for the `reload_delay` config
  setting were changed in 0.18.3. The type annotation on `reload_delay`
  was changed from `Optional[float]` (`float | None`) to `float`, and
  the default value was changed from `None` to `float`. `reload_delay`
  is only used in one place, in the `uvicorn.supervisors.basereload`
  module, in `BaseReload().pause()`. `BaseReload().pause()` runs
  `threading.Event().wait()`, which uses `None` as its default. It would
  therefore be fine for reloading to pass in `reload_delay=None`, so the
  change in Uvicorn to requiring `float` was confusing and unnecessary.

Changes related to
[Uvicorn 0.19](https://github.com/encode/uvicorn/releases/tag/0.19.0)
include:

- The `debug` setting was removed from `uvicorn.config.Config`.
- As of 0.19.0, Uvicorn now ships with a PEP 563 `py.typed` file,
  marking the package as type-annotated. `type: ignore` comments on
  `import uvicorn` lines can be removed.
- Type annotation updates are needed to match the new type information
  from Uvicorn. The `inboard.types.UvicornOptions` type added in 2cbc99c
  will be updated to more closely match arguments to `uvicorn.run()`,
  particularly by making the `app` field required and removing `debug`.
- **BREAKING CHANGE**: a new required positional argument `app_module`
  will be added to `inboard.start.set_uvicorn_options`. `inboard.start`
  will be updated accordingly, so this change is not likely to affect
  end users. It is technically a change to inboard's public API, so it
  is listed here as a breaking change. This change does have the benefit
  of making the arguments to `inboard.start.set_uvicorn_options` more
  similar to the arguments to `inboard.start.set_gunicorn_options`.

**Break up `uvicorn[standard]` optional dependencies** (#60)

Uvicorn lumps several optional dependencies into a "standard" extra:

- `colorama` (for Windows)
- `httptools`
- `python-dotenv`
- `pyyaml`
- `uvloop`
- `watchgod`/`watchfiles` (`watchgod` was renamed to `watchfiles`)
- `websockets`

There has been some discussion about the drawbacks of this approach:

- encode/uvicorn#219
- encode/uvicorn#1274
- encode/uvicorn#1547

inboard has previously installed the "standard" extra by default. This
commit will change the default to installing Uvicorn without "standard."
This is a **BREAKING CHANGE** to inboard's dependencies.

A new `inboard[uvicorn-fast]` extra will be added for dependencies from
`uvicorn[standard]` related to web server performance, and can be
installed by specifying the extra when installing inboard, like
`python -m pip install 'inboard[fastapi,uvicorn-fast]'`:

- `httptools`
- `uvloop`
- `websockets`

For users who still need all the `uvicorn[standard]` extras, a new
`inboard[uvicorn-standard]` extra will be added to the inboard package,
and can be installed by specifying the extra when installing inboard,
like `python -m pip install 'inboard[fastapi,uvicorn-standard]'`.

**Migrate from Poetry 1.1 to Hatch** (#56, #58, 8deae55, 8644d42, 53e2abb)

inboard has been migrated to [Hatch](https://hatch.pypa.io/latest/).
See br3ndonland/inboard#56 for further explanation.

Projects using inboard are not required to migrate to Hatch. The Docker
images will retain Poetry 1.1 for backwards compatibility for now.
Poetry 1.1 is unmaintained, so it will eventually need to be removed.
Notice will be given at least one minor version prior to removal. If
projects using inboard require `poetry>1.2`, they can add
`pipx upgrade poetry` or `pipx install poetry>1.2 --force` to their
Dockerfiles as described in the
[updated docs](https://inboard.bws.bio/docker#docker-and-poetry)
(on the Docker page, under "Docker and Poetry").

The Python package version will now be available at `inboard.__version__`.

**Auto-generate changelog from Git tags** (b15efff, e6e0490)

A changelog will now be provided at
[CHANGELOG.md](https://github.com/br3ndonland/inboard/blob/develop/CHANGELOG.md)
for viewing on GitHub, and
[in the docs at the `/changelog` endpoint](https://inboard.bws.bio/changelog).

**Update Docker tag syntax for inboard releases** (5617084)

Originally, inboard just provided three Docker images, tagged with
`base`, `fastapi`, and `starlette` based on the dependencies installed,
and appended inboard version numbers when Git tags were pushed.

Appending version numbers to Docker tags can result in confusing syntax.
For example, `ghcr.io/br3ndonland/inboard:fastapi-0.37-alpine` refers to
inboard 0.37, but some users could interpret this as FastAPI 0.37.

The inboard version number will now be added to the beginning of all
Docker tags to avoid this confusion.

- Old: `ghcr.io/br3ndonland/inboard:fastapi-0.38-alpine`
- New: `ghcr.io/br3ndonland/inboard:0.38-fastapi-alpine`

The old syntax will remain supported for backwards compatibility,
so either the old or new syntax shown above will work.

**Enable mypy strict mode** (2cbc99c)

Mypy will run in strict mode on all Python code (source code and tests).
In terms of user-facing improvements, this update will:

- Add a new `inboard.types` module, with a `DictConfig` type that can be
  used to type-annotate logging configuration dictionaries, and a
  `UvicornOptions` type for options (positional and keyword arguments)
  passed to `uvicorn.run()`
- Update the base ASGI application in `inboard.app.main_base` to ASGI3
- Update `contributing.md` with type annotation info and instructions

### Commits

`0.37.0..0.38.0`

- Bump version from 0.38.0-beta.0 to 0.38.0 (4e8d8cb)
- Update to mypy 1 (4630f8a)
- Pin Gunicorn to 20.1.0 (7cc175a)
- Update to Black 23 (1fea27e)
- Update isort to avoid poetry-core breaking change (b289ee9)
- Fix upper bound on HTTPX optional dependency (53e2abb)
- Add note on syncing dependencies with Hatch (029c07f)
- Alphabetize Hatch commands in contributing.md (f617e14)
- Update pre-commit dependencies (7fbde3e)
- Enable `pymdownx.magiclink` (5271a30)
- Update changelog for version 0.38.0-beta.0 (#64) (9968f6f)
- Bump version from 0.38.0-alpha.2 to 0.38.0-beta.0 (fdeae75)
- Update changelog for version 0.38.0-alpha.2 (#63) (19da840)
- Bump version from 0.38.0-alpha.1 to 0.38.0-alpha.2 (98c834e)
- Add Python 3.11 support (#62) (5716eff)
- Update changelog for version 0.38.0-alpha.1 (#61) (971b593)
- Bump version from 0.38.0-alpha.0 to 0.38.0-alpha.1 (b1debfa)
- Move `pyproject.toml` repo URL to `[project.urls]` (8644d42)
- Organize Hatch install info in contributing.md (8deae55)
- Update to Uvicorn 0.20.0 (13cd921)
- Break up `uvicorn[standard]` optional dependencies (#60) (01ad352)
- Update changelog for version 0.38.0-alpha.0 (#59) (49d3b96)
- Bump version from 0.37.0 to 0.38.0-alpha.0 (e9348b0)
- Merge pull request #58 from br3ndonland/hatch (78be3c2)
- Update docs for Hatch (ec344ad)
- Update GitHub Actions workflows for Hatch (9285efb)
- Update Dockerfile for Hatch (93d9e0a)
- Update configuration files for Hatch (5bd4ff5)
- Update to actions/setup-python@v4 (8840873)
- Add required `trailers` key for `asgiref==3.6.0` (d729fdf)
- Update to `asgiref==3.6.0` (d534de8)
- Move changelog updates to PRs (e6e0490)
- Auto-generate changelog from Git tags (b15efff)
- Remove unused `.prettierrc` (ef25ea0)
- Add spell check with CSpell (7361702)
- Remove GitHub issue templates (3797b2d)
- Update GitHub Actions Git tag syntax (c8a0638)
- Update Docker tag syntax for inboard releases (5617084)
- Remove redundant GitHub Actions workflows (4d19501)
- Enable mypy strict mode (2cbc99c)

Tagger: Brendon Smith <bws@bws.bio>

Date: 2023-02-26 13:08:29 -0500

```text
-----BEGIN SSH SIGNATURE-----
U1NIU0lHAAAAAQAAADMAAAALc3NoLWVkMjU1MTkAAAAgwLDNmire1DHY/g9GC1rGGr+mrE
kJ3FC96XsyoFKzm6IAAAADZ2l0AAAAAAAAAAZzaGE1MTIAAABTAAAAC3NzaC1lZDI1NTE5
AAAAQJERVesEeNy9tR1qbY8ZKLJHDPJ2G+azHwKEaNa5/Gp4T85uGfUhLoRYbmAcn/Yrta
Bu0/3JRpbcNA8yN5QI6gA=
-----END SSH SIGNATURE-----
```

## 0.38.0-beta.0 - 2023-01-02

### Changes

**Add Python 3.11 support** (#62)

- inboard will now run tests with Python 3.11, in addition to 3.8-3.10
- inboard will now build and publish its PyPI package using Python 3.11
- inboard will now include a Python 3.11 classifier in its PyPI package
- inboard will now ship Docker images running Python 3.11, in addition
  to 3.8-3.10, and Docker images tagged with `latest` will now use 3.11

**Update to Uvicorn 0.20.0** (13cd921)

This commit will update/upgrade from
[Uvicorn 0.17.6](https://github.com/encode/uvicorn/releases/tag/0.17.6)
to
[Uvicorn 0.20.0](https://github.com/encode/uvicorn/releases/tag/0.20.0).

Uvicorn 0.20.0 will be pinned exactly to avoid problematic or breaking
changes in future patch releases.

[Uvicorn 0.18](https://github.com/encode/uvicorn/releases/tag/0.18.3)
was skipped for the following reasons:

- As of Uvicorn 0.18.0, Uvicorn now prioritizes `watchfiles` instead of
  `watchgod`. `watchfiles` uses Rust binary extensions, which can have
  issues on Alpine Linux and macOS with Apple Silicon (M1/M2), and the
  evaluation process took some time. It does appear that `watchfiles` is
  now publishing wheels with `musllinux` tags, so Alpine Linux should be
  generally compatible. Apple Silicon Macs should be compatible as of
  `watchfiles` 0.16.
- The `h11_max_incomplete_event_size` setting was added in 0.18.0 with
  an incorrect default, then updated in 0.18.1 with a correct default.
- A temporary breaking change was made to the Uvicorn logging module.
  It was renamed from `uvicorn.logging` to `uvicorn._logging` in 0.18.0
  (a breaking change that was not mentioned in the release notes), then
  reverted back to `uvicorn.logging` in 0.18.2. A change to the logging
  module path could break inboard `LOG_FORMAT=uvicorn`.
- A temporary breaking change was made to the Uvicorn logging config.
  The logging config default was changed from `LOGGING_CONFIG` to `None`
  in 0.18.0, which resulted in logs not being shown at all. The default
  was then reverted to `LOGGING_CONFIG` in 0.18.2.
- The type annotation and default value for the `reload_delay` config
  setting were changed in 0.18.3. The type annotation on `reload_delay`
  was changed from `Optional[float]` (`float | None`) to `float`, and
  the default value was changed from `None` to `float`. `reload_delay`
  is only used in one place, in the `uvicorn.supervisors.basereload`
  module, in `BaseReload().pause()`. `BaseReload().pause()` runs
  `threading.Event().wait()`, which uses `None` as its default. It would
  therefore be fine for reloading to pass in `reload_delay=None`, so the
  change in Uvicorn to requiring `float` was confusing and unnecessary.

[Uvicorn 0.19](https://github.com/encode/uvicorn/releases/tag/0.19.0)
was less problematic, but did include some noteworthy
changes. inboard will be updated accordingly. Notes:

- The `debug` setting was removed from `uvicorn.config.Config`.
- As of 0.19.0, Uvicorn now ships with a PEP 563 `py.typed` file,
  marking the package as type-annotated. `type: ignore` comments on
  `import uvicorn` lines can be removed.
- Type annotation updates are needed to match the new type information
  from Uvicorn. The `inboard.types.UvicornOptions` type added in 2cbc99c
  will be updated to more closely match arguments to `uvicorn.run()`,
  particularly by making the `app` field required and removing `debug`.
- **BREAKING CHANGE**: a new required positional argument `app_module`
  will be added to `inboard.start.set_uvicorn_options`. `inboard.start`
  will be updated accordingly, so this change is not likely to affect
  end users. It is technically a change to inboard's public API, so it
  is listed here as a breaking change. This change does have the benefit
  of making the arguments to `inboard.start.set_uvicorn_options` more
  similar to the arguments to `inboard.start.set_gunicorn_options`.

**Break up `uvicorn[standard]` optional dependencies** (#60)

Uvicorn lumps several optional dependencies into a "standard" extra:

- `colorama` (for Windows)
- `httptools`
- `python-dotenv`
- `pyyaml`
- `uvloop`
- `watchgod`/`watchfiles` (`watchgod` was renamed to `watchfiles`)
- `websockets`

There has been some discussion about the drawbacks of this approach:

- encode/uvicorn#219
- encode/uvicorn#1274
- encode/uvicorn#1547

inboard has previously installed the "standard" extra by default. This
commit will change the default to installing Uvicorn without "standard."
This is a **BREAKING CHANGE** to inboard's dependencies.

A new `inboard[uvicorn-fast]` extra will be added for dependencies from
`uvicorn[standard]` related to web server performance, and can be
installed by specifying the extra when installing inboard, like
`python -m pip install 'inboard[fastapi,uvicorn-fast]'`:

- `httptools`
- `uvloop`
- `websockets`

For users who still need all the `uvicorn[standard]` extras, a new
`inboard[uvicorn-standard]` extra will be added to the inboard package,
and can be installed by specifying the extra when installing inboard,
like `python -m pip install 'inboard[fastapi,uvicorn-standard]'`.

**Migrate from Poetry 1.1 to Hatch** (#56, #58, 8deae55, 8644d42)

inboard has been migrated to [Hatch](https://hatch.pypa.io/latest/).
See br3ndonland/inboard#56 for more details and context around the
motivations for this.

Projects using inboard are not required to migrate to Hatch. The Docker
images will retain Poetry 1.1 for backwards compatibility for now.
Poetry 1.1 is unmaintained, so it will eventually need to be removed.
Notice will be given at least one minor version prior to removal. If
projects using inboard require `poetry>1.2`, they can add
`pipx upgrade poetry` or `pipx install poetry>1.2 --force` to their
Dockerfiles as described in the
[updated docs](https://inboard.bws.bio/docker#docker-and-poetry)
(on the Docker page, under "Docker and Poetry").

The Python package version will now be available at `inboard.__version__`.

**Auto-generate changelog from Git tags** (b15efff, e6e0490)

A changelog will now be provided at
[CHANGELOG.md](https://github.com/br3ndonland/inboard/blob/develop/CHANGELOG.md)
for viewing on GitHub, and
[in the docs at the `/changelog` endpoint](https://inboard.bws.bio/changelog).

**Update Docker tag syntax for inboard releases** (5617084)

Originally, inboard just provided three Docker images, tagged with
`base`, `fastapi`, and `starlette` based on the dependencies installed,
and appended inboard version numbers when Git tags were pushed.

Appending version numbers to Docker tags can result in confusing syntax.
For example, `ghcr.io/br3ndonland/inboard:fastapi-0.37-alpine` refers to
inboard 0.37, but some users could interpret this as FastAPI 0.37.

The inboard version number will now be added to the beginning of all
Docker tags to avoid this confusion.

- Old: `ghcr.io/br3ndonland/inboard:fastapi-0.38-alpine`
- New: `ghcr.io/br3ndonland/inboard:0.38-fastapi-alpine`

The original syntax will remain supported for backwards compatibility,
so either the old or new syntax shown above will work.

**Enable mypy strict mode** (2cbc99c)

Mypy will run in strict mode on all Python code (source code and tests).
In terms of user-facing improvements, this update will:

- Add a new `inboard.types` module, with a `DictConfig` type that can be
  used to type-annotate logging configuration dictionaries, and a
  `UvicornOptions` type for options (positional and keyword arguments)
  passed to `uvicorn.run()`
- Update the base ASGI application in `inboard.app.main_base` to ASGI3
- Update `contributing.md` with type annotation info and instructions

### Commits

- Bump version from 0.38.0-alpha.2 to 0.38.0-beta.0 (fdeae75)
- Update changelog for version 0.38.0-alpha.2 (#63) (19da840)
- Bump version from 0.38.0-alpha.1 to 0.38.0-alpha.2 (98c834e)
- Add Python 3.11 support (#62) (5716eff)
- Update changelog for version 0.38.0-alpha.1 (#61) (971b593)
- Bump version from 0.38.0-alpha.0 to 0.38.0-alpha.1 (b1debfa)
- Move `pyproject.toml` repo URL to `[project.urls]` (8644d42)
- Organize Hatch install info in contributing.md (8deae55)
- Update to Uvicorn 0.20.0 (13cd921)
- Break up `uvicorn[standard]` optional dependencies (#60) (01ad352)
- Update changelog for version 0.38.0-alpha.0 (#59) (49d3b96)
- Bump version from 0.37.0 to 0.38.0-alpha.0 (e9348b0)
- Merge pull request #58 from br3ndonland/hatch (78be3c2)
- Update docs for Hatch (ec344ad)
- Update GitHub Actions workflows for Hatch (9285efb)
- Update Dockerfile for Hatch (93d9e0a)
- Update configuration files for Hatch (5bd4ff5)
- Update to actions/setup-python@v4 (8840873)
- Add required `trailers` key for `asgiref==3.6.0` (d729fdf)
- Update to `asgiref==3.6.0` (d534de8)
- Move changelog updates to PRs (e6e0490)
- Auto-generate changelog from Git tags (b15efff)
- Remove unused `.prettierrc` (ef25ea0)
- Add spell check with CSpell (7361702)
- Remove GitHub issue templates (3797b2d)
- Update GitHub Actions Git tag syntax (c8a0638)
- Update Docker tag syntax for inboard releases (5617084)
- Remove redundant GitHub Actions workflows (4d19501)
- Enable mypy strict mode (2cbc99c)

Tagger: Brendon Smith <bws@bws.bio>

Date: 2023-01-02 15:35:43 -0500

```text
-----BEGIN SSH SIGNATURE-----
U1NIU0lHAAAAAQAAADMAAAALc3NoLWVkMjU1MTkAAAAgwLDNmire1DHY/g9GC1rGGr+mrE
kJ3FC96XsyoFKzm6IAAAADZ2l0AAAAAAAAAAZzaGE1MTIAAABTAAAAC3NzaC1lZDI1NTE5
AAAAQK0mJue6+q/OhxuscIsdLgFgb+4cNPSvIsKe2mWV+zzIt/OokJNsJlpjKlq+DuM0Sg
U47sCUf0EAff62JtjaqQs=
-----END SSH SIGNATURE-----
```

## 0.38.0-alpha.2 - 2023-01-01

Changes:

**Add Python 3.11 support** (#62)

- inboard will now run tests with Python 3.11, in addition to 3.8-3.10
- inboard will now build and publish its PyPI package using Python 3.11
- inboard will now include a Python 3.11 classifier in its PyPI package
- inboard will now ship Docker images running Python 3.11, in addition
  to 3.8-3.10, and Docker images tagged with `latest` will now use 3.11

Commits:

- Bump version from 0.38.0-alpha.1 to 0.38.0-alpha.2 (98c834e)
- Add Python 3.11 support (#62) (5716eff)
- Update changelog for version 0.38.0-alpha.1 (#61) (971b593)

Tagger: Brendon Smith <bws@bws.bio>

Date: 2023-01-01 11:34:42 -0500

```text
-----BEGIN SSH SIGNATURE-----
U1NIU0lHAAAAAQAAADMAAAALc3NoLWVkMjU1MTkAAAAgwLDNmire1DHY/g9GC1rGGr+mrE
kJ3FC96XsyoFKzm6IAAAADZ2l0AAAAAAAAAAZzaGE1MTIAAABTAAAAC3NzaC1lZDI1NTE5
AAAAQCH6Vh/nyNz9L+QuZwt02ljrP/X6oOA0q8Vx+yhns/vQHLgJqK4xdbW0U+dGhPtZzf
hC1kw2q08TAFZkwF0K/Q0=
-----END SSH SIGNATURE-----
```

## 0.38.0-alpha.1 - 2022-12-31

Changes:

**Update to Uvicorn 0.20.0** (13cd921)

This commit will update/upgrade to Uvicorn 0.20.0.

https://github.com/encode/uvicorn/releases/tag/0.20.0

Uvicorn 0.20.0 will be pinned exactly to avoid problematic or breaking
changes in future patch releases.

Uvicorn 0.18 was skipped for the following reasons:

- As of Uvicorn 0.18.0, Uvicorn now prioritizes `watchfiles` instead of
  `watchgod`. `watchfiles` uses Rust binary extensions, which can have
  issues on Alpine Linux and macOS with Apple Silicon (M1/M2), and the
  evaluation process took some time. It does appear that `watchfiles` is
  now publishing wheels with `musllinux` tags, so Alpine Linux should be
  generally compatible. Apple Silicon Macs should be compatible as of
  `watchfiles` 0.16.
- The `h11_max_incomplete_event_size` setting was added in 0.18.0 with
  an incorrect default, then updated in 0.18.1 with a correct default.
- A temporary breaking change was made to the Uvicorn logging module.
  It was renamed from `uvicorn.logging` to `uvicorn._logging` in 0.18.0
  (a breaking change that was not mentioned in the release notes), then
  reverted back to `uvicorn.logging` in 0.18.2. A change to the logging
  module path could break inboard `LOG_FORMAT=uvicorn`.
- A temporary breaking change was made to the Uvicorn logging config.
  The logging config default was changed from `LOGGING_CONFIG` to `None`
  in 0.18.0, which resulted in logs not being shown at all. The default
  was then reverted to `LOGGING_CONFIG` in 0.18.2.
- The type annotation and default value for the `reload_delay` config
  setting were changed in 0.18.3. The type annotation on `reload_delay`
  was changed from `Optional[float]` (`float | None`) to `float`, and
  the default value was changed from `None` to `float`. `reload_delay`
  is only used in one place, in the `uvicorn.supervisors.basereload`
  module, in `BaseReload().pause()`. `BaseReload().pause()` runs
  `threading.Event().wait()`, which uses `None` as its default. It would
  therefore be fine for reloading to pass in `reload_delay=None`, so the
  change in Uvicorn to requiring `float` was confusing and unnecessary.

https://github.com/encode/uvicorn/releases/tag/0.18.3

Uvicorn 0.19 was less problematic, but did include some noteworthy
changes. inboard will be updated accordingly. Notes:

- The `debug` setting was removed from `uvicorn.config.Config`.
- As of 0.19.0, Uvicorn now ships with a PEP 563 `py.typed` file,
  marking the package as type-annotated. `type: ignore` comments on
  `import uvicorn` lines can be removed.
- Type annotation updates are needed to match the new type information
  from Uvicorn. The `inboard.types.UvicornOptions` type added in 2cbc99c
  will be updated to more closely match arguments to `uvicorn.run()`,
  particularly by making the `app` field required and removing `debug`.
- **BREAKING CHANGE**: a new required positional argument `app_module`
  will be added to `inboard.start.set_uvicorn_options`. `inboard.start`
  will be updated accordingly, so this change is not likely to affect
  end users. It is technically a change to inboard's public API, so it
  is listed here as a breaking change. This change does have the benefit
  of making the arguments to `inboard.start.set_uvicorn_options` more
  similar to the arguments to `inboard.start.set_gunicorn_options`.

https://github.com/encode/uvicorn/releases/tag/0.19.0

**Break up `uvicorn[standard]` optional dependencies** (#60)

Uvicorn lumps several optional dependencies into a "standard" extra:

- `colorama` (for Windows)
- `httptools`
- `python-dotenv`
- `pyyaml`
- `uvloop`
- `watchgod`/`watchfiles` (`watchgod` was renamed to `watchfiles`)
- `websockets`

There has been some discussion about the drawbacks of this approach:

- encode/uvicorn#219
- encode/uvicorn#1274
- encode/uvicorn#1547

inboard has previously installed the "standard" extra by default. This
commit will change the default to installing Uvicorn without "standard."
This is a **BREAKING CHANGE** to inboard's dependencies.

A new `inboard[uvicorn-fast]` extra will be added for dependencies from
`uvicorn[standard]` related to web server performance, and can be
installed by specifying the extra when installing inboard, like
`python -m pip install 'inboard[fastapi,uvicorn-fast]'`:

- `httptools`
- `uvloop`
- `websockets`

For users who still need all the `uvicorn[standard]` extras, a new
`inboard[uvicorn-standard]` extra will be added to the inboard package,
and can be installed by specifying the extra when installing inboard,
like `python -m pip install 'inboard[fastapi,uvicorn-standard]'`.

Commits:

- Bump version from 0.38.0-alpha.0 to 0.38.0-alpha.1 (b1debfa)
- Move `pyproject.toml` repo URL to `[project.urls]` (8644d42)
- Organize Hatch install info in contributing.md (8deae55)
- Update to Uvicorn 0.20.0 (13cd921)
- Break up `uvicorn[standard]` optional dependencies (#60) (01ad352)
- Update changelog for version 0.38.0-alpha.0 (#59) (49d3b96)

Tagger: Brendon Smith <bws@bws.bio>

Date: 2022-12-31 18:59:49 -0500

```text
-----BEGIN SSH SIGNATURE-----
U1NIU0lHAAAAAQAAADMAAAALc3NoLWVkMjU1MTkAAAAgwLDNmire1DHY/g9GC1rGGr+mrE
kJ3FC96XsyoFKzm6IAAAADZ2l0AAAAAAAAAAZzaGE1MTIAAABTAAAAC3NzaC1lZDI1NTE5
AAAAQBhe/frXRYxcFQZPOc/5KEPt2TiJyLgBlHoWE/bvOYJRNfaIUd4OuLdpDh+8vjaxZk
Qo+n22YhuYnxv0pEeuxg8=
-----END SSH SIGNATURE-----
```

## 0.38.0-alpha.0 - 2022-12-30

Changes:

**Migrate from Poetry 1.1 to Hatch** (#56, #58)

inboard has been migrated to [Hatch](https://hatch.pypa.io/latest/).
See #56 for more details and context around the motivations for this.

The inboard Python version is now available at `inboard.__version__`.

Projects using inboard are not required to migrate to Hatch. The Docker
images will retain Poetry 1.1 for backwards compatibility for now.
Poetry 1.1 is unmaintained, so it will eventually need to be removed.
Notice will be given at least one minor version prior to removal. If
projects using inboard require `poetry>1.2`, they can add
`pipx upgrade poetry` or `pipx install poetry>1.2 --force` to their
Dockerfiles as described in the updated docs (on the Docker page,
under "Docker and Poetry").

**Auto-generate changelog from Git tags** (b15efff, e6e0490)

A changelog will now be provided at CHANGELOG.md for viewing on GitHub,
and in the docs at the `/changelog` endpoint.

**Update Docker tag syntax for inboard releases** (5617084)

Originally, inboard just provided three Docker images, tagged with
`base`, `fastapi`, and `starlette` based on the dependencies installed,
and appended inboard version numbers when Git tags were pushed.

Appending version numbers to Docker tags can result in confusing syntax.
For example, `ghcr.io/br3ndonland/inboard:fastapi-0.37-alpine` refers to
inboard 0.37, but some users could interpret this as FastAPI 0.37.

The inboard version number will now be added to the beginning of all
Docker tags to avoid this confusion.

- Before: `ghcr.io/br3ndonland/inboard:fastapi-0.37-alpine`
- After: `ghcr.io/br3ndonland/inboard:0.37-fastapi-alpine`

The original syntax will remain supported for backwards compatibility,
so either the "before" or "after" syntax shown above will work.

**Enable mypy strict mode** (2cbc99c)

Mypy will run in strict mode on all Python code (source code and tests).
In terms of user-facing improvements, this update will:

- Add a new `inboard.types` module, with a `DictConfig` type that can be
  used to type-annotate logging configuration dictionaries, and a
  `UvicornOptions` type that can be used to type-annotate options passed
  to Uvicorn via `uvicorn.run()` or `uvicorn.Config`
- Update the base ASGI application in `inboard.app.main_base` to ASGI3
- Update `contributing.md` with type annotation info and instructions

Commits:

- Bump version from 0.37.0 to 0.38.0-alpha.0 (e9348b0)
- Merge pull request #58 from br3ndonland/hatch (78be3c2)
- Update docs for Hatch (ec344ad)
- Update GitHub Actions workflows for Hatch (9285efb)
- Update Dockerfile for Hatch (93d9e0a)
- Update configuration files for Hatch (5bd4ff5)
- Update to actions/setup-python@v4 (8840873)
- Add required `trailers` key for `asgiref==3.6.0` (d729fdf)
- Update to `asgiref==3.6.0` (d534de8)
- Move changelog updates to PRs (e6e0490)
- Auto-generate changelog from Git tags (b15efff)
- Remove unused `.prettierrc` (ef25ea0)
- Add spell check with CSpell (7361702)
- Remove GitHub issue templates (3797b2d)
- Update GitHub Actions Git tag syntax (c8a0638)
- Update Docker tag syntax for inboard releases (5617084)
- Remove redundant GitHub Actions workflows (4d19501)
- Enable mypy strict mode (2cbc99c)

Tagger: Brendon Smith <bws@bws.bio>

Date: 2022-12-30 15:04:26 -0500

```text
-----BEGIN SSH SIGNATURE-----
U1NIU0lHAAAAAQAAADMAAAALc3NoLWVkMjU1MTkAAAAgwLDNmire1DHY/g9GC1rGGr+mrE
kJ3FC96XsyoFKzm6IAAAADZ2l0AAAAAAAAAAZzaGE1MTIAAABTAAAAC3NzaC1lZDI1NTE5
AAAAQBzt5FXBpT7Li/8pIyb9SGbb8QGUHc0pLt1jdxlHquNFjO0FpaNUvmknvpC9cWCVxl
sEq0/rwYwb4VafulRlqAU=
-----END SSH SIGNATURE-----
```

## 0.37.0 - 2022-11-28

Changes:

Update to FastAPI 0.88 and Starlette 0.22 (7c76538)

This release will update/upgrade to FastAPI 0.88 and Starlette 0.22.
This is a minor release to align with FastAPI and Starlette versioning.

https://github.com/tiangolo/fastapi/releases/tag/0.88.0
https://github.com/encode/starlette/releases/tag/0.22.0

Commits:

- Bump version from 0.36.0 to 0.37.0 (6893b78)
- Update to FastAPI 0.88 and Starlette 0.22 (7c76538)

Tagger: Brendon Smith <bws@bws.bio>

Date: 2022-11-28 18:17:38 -0500

```text
-----BEGIN SSH SIGNATURE-----
U1NIU0lHAAAAAQAAADMAAAALc3NoLWVkMjU1MTkAAAAgwLDNmire1DHY/g9GC1rGGr+mrE
kJ3FC96XsyoFKzm6IAAAADZ2l0AAAAAAAAAAZzaGE1MTIAAABTAAAAC3NzaC1lZDI1NTE5
AAAAQDhUK/SdfNi6MgU0iy1Dhq27fHd6YCUv0sc/JUsUHlTL3UZMQ1difo8LDAHsWAYbWn
5VNDu205Qw1fWKeKD5eQs=
-----END SSH SIGNATURE-----
```

## 0.36.0 - 2022-11-26

Changes:

Update to FastAPI 0.87 and Starlette 0.21 (b429f5c)

This release will update/upgrade to FastAPI 0.87 and Starlette 0.21.
This is a minor release to align with FastAPI and Starlette versioning.

BREAKING CHANGE: Starlette 0.21 updated the test client to run on HTTPX
instead of Requests. Please verify compatibility with your test suite
after updating. Also note that, while Requests is no longer a dependency
of Starlette, it recently became a dependency of mkdocs-material, so it
will still be included when installing mkdocs-material. mkdocs-material
(aka "Material for MkDocs") is used to build the documentation. They
recently achieved their $8000 "Scotch Bonnet" funding goal, and released
a collection of previously insiders-only features to the public. One of
these features is a new built-in social plugin that uses Requests.
https://github.com/tiangolo/fastapi/releases/tag/0.87.0
https://github.com/encode/starlette/releases/tag/0.21.0
https://www.python-httpx.org/compatibility/
https://squidfunk.github.io/mkdocs-material/insiders/
https://squidfunk.github.io/mkdocs-material/setup/setting-up-social-cards/

Commits:

- Bump version from 0.35.0 to 0.36.0 (c74d77c)
- Update to FastAPI 0.87 and Starlette 0.21 (b429f5c)

Tagger: Brendon Smith <bws@bws.bio>

Date: 2022-11-26 17:48:02 -0500

```text
-----BEGIN SSH SIGNATURE-----
U1NIU0lHAAAAAQAAADMAAAALc3NoLWVkMjU1MTkAAAAgwLDNmire1DHY/g9GC1rGGr+mrE
kJ3FC96XsyoFKzm6IAAAADZ2l0AAAAAAAAAAZzaGE1MTIAAABTAAAAC3NzaC1lZDI1NTE5
AAAAQC5gZd6SRTDpnmFGEB2eihzqPFH3jPzMtgQioDcUqRtylrtKmiH+HhtLs1uWduDTte
aPZevW6ezQ8O7lLY36Sw8=
-----END SSH SIGNATURE-----
```

## 0.35.0 - 2022-11-26

Changes:

Update to FastAPI 0.86 (ab869dd)

This release will update/upgrade to FastAPI 0.86.
This is a minor release to align with FastAPI's versioning strategy.
Note that FastAPI 0.86 added support for Python 3.11.

Commits:

- Bump version from 0.34.1 to 0.35.0 (50ba2be)
- Update to FastAPI 0.86 (ab869dd)

Tagger: Brendon Smith <bws@bws.bio>

Date: 2022-11-26 16:31:59 -0500

```text
-----BEGIN SSH SIGNATURE-----
U1NIU0lHAAAAAQAAADMAAAALc3NoLWVkMjU1MTkAAAAgwLDNmire1DHY/g9GC1rGGr+mrE
kJ3FC96XsyoFKzm6IAAAADZ2l0AAAAAAAAAAZzaGE1MTIAAABTAAAAC3NzaC1lZDI1NTE5
AAAAQI6Bw12pRYL5E774A8c4riY3/mHxT9EDD4PTcuf89lzMYkOA6sSQ4/4KS5iE/MFNh5
jlkVJT27YFIQ7wfsgo6gw=
-----END SSH SIGNATURE-----
```

## 0.34.1 - 2022-11-26

Commits:

- Bump version from 0.34.0 to 0.34.1 (4994950)
- Rename VSCode debugger config (20dd052)
- Update to Flake8 6 (e5ab9ee)
- Update dependencies (ab826e1)

Tagger: Brendon Smith <bws@bws.bio>

Date: 2022-11-26 09:46:59 -0500

```text
-----BEGIN SSH SIGNATURE-----
U1NIU0lHAAAAAQAAADMAAAALc3NoLWVkMjU1MTkAAAAgwLDNmire1DHY/g9GC1rGGr+mrE
kJ3FC96XsyoFKzm6IAAAADZ2l0AAAAAAAAAAZzaGE1MTIAAABTAAAAC3NzaC1lZDI1NTE5
AAAAQJX5E/sLeorp2CYV8kC5Euf9bo846+C/W87KYhDEvHOJWLpAH6B0JGoAiK9hyghkwR
Py56XpqtYvQQbeVI6ZEQo=
-----END SSH SIGNATURE-----
```

## 0.34.0 - 2022-09-18

Changes:

Update to FastAPI 0.85 and Starlette 0.20 (0703e7c)

This release will update/upgrade to FastAPI 0.85 and Starlette 0.20.
This is a minor release to align with FastAPI and Starlette versioning.
Note that Starlette has dropped support for Python 3.6. inboard supports
Python 3.8-3.10, so this is not a breaking change for inboard.
https://github.com/tiangolo/fastapi/releases/tag/0.85.0
https://github.com/encode/starlette/releases/tag/0.20.0
https://github.com/encode/starlette/releases/tag/0.20.4

Commits:

- Bump version from 0.33.0 to 0.34.0 (9fc7281)
- Update to FastAPI 0.85 and Starlette 0.20 (0703e7c)

Note about Git commit and tag verification:

The email address bws@bws.bio and associated GPG key 783DBAF23C1D6478
have been used to sign Git commits and tags since 0.10.0 - 2021-05-20.

Git and GitHub now support commit signing and verification with SSH. The
SSH key fingerprint SHA256:w+KL3qQKtku1MfLFSZLCl93kSgxH3O4OvtcxHG5k0Go
will also be used to sign Git commits and tags going forward.

See https://github.com/br3ndonland and br3ndonland/br3ndonland@08257e6
for corroboration of the new info.

Tagger: Brendon Smith <bws@bws.bio>

Date: 2022-09-18 17:49:58 -0400

```text
-----BEGIN PGP SIGNATURE-----

iHUEABYKAB0WIQRUOcb2PA6NDBflNNd4PbryPB1keAUCYyeSwAAKCRB4PbryPB1k
eMvsAQCaKjXGB1xAVqI+dHggAQGHVU+4o+OtpYoTldExxYHw8wD/SM9Og47sX704
IpJsTXRS63SimSxdC2znoydn0UKQfQc=
=hoAt
-----END PGP SIGNATURE-----
```

## 0.33.0 - 2022-09-18

Changes:

Update to FastAPI 0.84 (c12ea2e)

This release will update/upgrade to FastAPI 0.84.
This is a minor release to align with FastAPI's versioning strategy.
Note that FastAPI has dropped support for Python 3.6. inboard supports
Python 3.8-3.10, so this is not a breaking change for inboard.
https://github.com/tiangolo/fastapi/releases/tag/0.84.0

Commits:

- Bump version from 0.32.0 to 0.33.0 (871f492)
- Update to FastAPI 0.84 (c12ea2e)

Tagger: Brendon Smith <bws@bws.bio>

Date: 2022-09-18 17:23:12 -0400

```text
-----BEGIN PGP SIGNATURE-----

iHUEABYKAB0WIQRUOcb2PA6NDBflNNd4PbryPB1keAUCYyeMXQAKCRB4PbryPB1k
eMX8AQChYnzrTcJ6lmzAagq3xDNVLserm7+chy9gl/cUy0+a5wD+IkrtCcE2tQ7J
uXuaeQSxOQU0PBXv9Y48K52O05koqAA=
=PHkK
-----END PGP SIGNATURE-----
```

## 0.32.0 - 2022-09-18

Changes:

Update to FastAPI 0.83 (404df56)

This release will update/upgrade to FastAPI 0.83.
This is a minor release to align with FastAPI's versioning strategy.
https://github.com/tiangolo/fastapi/releases/tag/0.83.0

Commits:

- Bump version from 0.31.0 to 0.32.0 (fbfd228)
- Update to FastAPI 0.83 (404df56)

Tagger: Brendon Smith <bws@bws.bio>

Date: 2022-09-18 16:52:17 -0400

```text
-----BEGIN PGP SIGNATURE-----

iHUEABYKAB0WIQRUOcb2PA6NDBflNNd4PbryPB1keAUCYyeFQQAKCRB4PbryPB1k
ePXgAQDKxkFr80STjXzCQfmmip/A7rt11Cn9PQ4M2wOA7UIPRwEAkjOLDvDfCFZm
u/O9NlUVED4GhqbXRtDIO+Z4fY16bwI=
=oUWm
-----END PGP SIGNATURE-----
```

## 0.31.0 - 2022-09-18

Changes:

Update to FastAPI 0.82 (6313b22)

This release will update/upgrade to FastAPI 0.82.
This is a minor release to align with FastAPI's versioning strategy.
https://github.com/tiangolo/fastapi/releases/tag/0.82.0

Commits:

- Bump version from 0.30.0 to 0.31.0 (8a97844)
- Update to FastAPI 0.82 (6313b22)

Tagger: Brendon Smith <bws@bws.bio>

Date: 2022-09-18 16:26:44 -0400

```text
-----BEGIN PGP SIGNATURE-----

iHUEABYKAB0WIQRUOcb2PA6NDBflNNd4PbryPB1keAUCYyd/qwAKCRB4PbryPB1k
eJMNAP4+GBKQHJrQX6Xt+WqASW150qHgO1bYUYkEtoC72KOXfQEA1WTX2pSDSVHt
J9lzagGNoKR8rS6eBSLSw0XnLRacFg4=
=gDpR
-----END PGP SIGNATURE-----
```

## 0.30.0 - 2022-09-18

Changes:

Update to FastAPI 0.81 (f66214a)

This release will update/upgrade to FastAPI 0.81.
This is a minor release to align with FastAPI's versioning strategy.
https://github.com/tiangolo/fastapi/releases/tag/0.81.0

Commits:

- Bump version from 0.29.0 to 0.30.0 (28c6f6b)
- Update to FastAPI 0.81 (f66214a)

Tagger: Brendon Smith <bws@bws.bio>

Date: 2022-09-18 16:08:16 -0400

```text
-----BEGIN PGP SIGNATURE-----

iHUEABYKAB0WIQRUOcb2PA6NDBflNNd4PbryPB1keAUCYyd7UwAKCRB4PbryPB1k
eHolAQCyVyiAcNkFsqP1S9za8RdsS9BGYpejF8XrEd/Zk5fhFgEA8/DZXvX8n6kZ
Eb13nXD4mje//Va3yVsYM332BlZ9WwA=
=EPTH
-----END PGP SIGNATURE-----
```

## 0.29.0 - 2022-09-18

Update to FastAPI 0.80 (f8bd04a)

This release will update/upgrade to FastAPI 0.80.
This is a minor release to align with FastAPI's versioning strategy.
BREAKING CHANGE: `response_model` will now invalidate `None`.
https://github.com/tiangolo/fastapi/releases/tag/0.80.0

Commits:

- Bump version from 0.28.1 to 0.29.0 (eceeb09)
- Update to FastAPI 0.80 (f8bd04a)
- Update dependencies (cd301e6)

Tagger: Brendon Smith <bws@bws.bio>

Date: 2022-09-18 15:32:57 -0400

```text
-----BEGIN PGP SIGNATURE-----

iHUEABYKAB0WIQRUOcb2PA6NDBflNNd4PbryPB1keAUCYydzGAAKCRB4PbryPB1k
eN+tAP9IBKadJWjo48k/XFb4YXwdj2aO0oika/gjySd9hfrqIgD8DdPoplzI1BYd
tBZth1fdb1eC4IMmtkLaH+SgsAKESAg=
=W9IB
-----END PGP SIGNATURE-----
```

## 0.28.1 - 2022-09-04

Commits:

- Bump version from 0.28.0 to 0.28.1 (d3982f1)
- Update to Flake8 5 (28dc5e4)
- Update dependencies (3536ab2)
- Add justification section to docs and README (a807a11)
- Add test case for Uvicorn log format (087efda)
- Add changelog command to docs (8c474b6)

Tagger: Brendon Smith <bws@bws.bio>

Date: 2022-09-04 14:05:49 -0400

```text
-----BEGIN PGP SIGNATURE-----

iHUEABYKAB0WIQRUOcb2PA6NDBflNNd4PbryPB1keAUCYxTpGwAKCRB4PbryPB1k
eF+8AQDehq5YOcmQcSUJWvcoOI/thcbs9C3Q9QmXvrcspWwO5gEAhVzQTaaFivct
ayBrWs8TK4W2IA9jmQo4OCi9crmRZwI=
=h3Oz
-----END PGP SIGNATURE-----
```

## 0.28.0 - 2022-07-30

Changes:

Update to FastAPI 0.79 (3a34076)

This release will update/upgrade to FastAPI 0.79.
This is a minor release to align with FastAPI's versioning strategy.

Commits:

- Bump version from 0.27.0 to 0.28.0 (dcfa947)
- Update to FastAPI 0.79 (3a34076)
- Update dependencies (121271a)

Tagger: Brendon Smith <bws@bws.bio>

Date: 2022-07-30 14:39:33 -0400

```text
-----BEGIN PGP SIGNATURE-----

iHUEABYKAB0WIQRUOcb2PA6NDBflNNd4PbryPB1keAUCYuV7OwAKCRB4PbryPB1k
eMxRAPwOiTBDZyPwTph6YOsfbSHFVI85wQJbXBhQfhEUyEr05gEAgy9XHrcdh0J6
D59blIDg2Zr/I63A2pqWhzjt+mPQFQM=
=qJMi
-----END PGP SIGNATURE-----
```

## 0.27.0 - 2022-07-09

Changes:

- Use BuildKit for Docker builds (#54)

Commits:

- Bump version from 0.26.1 to 0.27.0 (4f67d82)
- Update dependencies (9d2bf9f)
- Merge pull request #54 from br3ndonland/buildkit (5968ae2)
- Relax Dockerfile syntax version specifier (79ce14e)
- Update `docker build --cache-from` for inboard (8cc569f)
- Add `BUILDKIT_INLINE_CACHE` Docker build argument (173fc51)
- Use `COPY --link` to improve layer caching (1af4421)
- Add heredoc examples and info to docs (d3c6f11)
- Break heredoc across multiple stages (91cbd6f)
- Refactor Dockerfile with heredoc syntax (cd22c8d)
- Add Docker BuildKit info to CONTRIBUTING.md (64fc4a8)
- Enable BuildKit in GitHub Actions (517fcf8)

Tagger: Brendon Smith <bws@bws.bio>

Date: 2022-07-09 15:59:02 -0400

```text
-----BEGIN PGP SIGNATURE-----

iHUEABYKAB0WIQRUOcb2PA6NDBflNNd4PbryPB1keAUCYsneDwAKCRB4PbryPB1k
eP9wAQDEWAVzulzPFXqQB3d05x6ysxWwM2CL/KQ9Ld7h4fc/SgD8CM2Z31x+sDbn
N8qLTDZ6c7ANwdIcy1MwmThblip1hAM=
=roeE
-----END PGP SIGNATURE-----
```

## 0.26.1 - 2022-06-11

Commits:

- Bump version from 0.26.0 to 0.26.1 (0452dde)
- Update to pipx 1.1.0 (3437bdd)
- Update dependencies (c0c7638)
- Add example requirements files to docs (36fd603)
- Remove `<!-- prettier-ignore -->` from docs (ff212f4)
- Simplify CodeQL workflow (59e3dad)

Tagger: Brendon Smith <bws@bws.bio>

Date: 2022-06-11 15:18:44 -0400

```text
-----BEGIN PGP SIGNATURE-----

iHUEABYKAB0WIQRUOcb2PA6NDBflNNd4PbryPB1keAUCYqTqrQAKCRB4PbryPB1k
eNAjAQC7+J8mNXT8nXRqKJsgwJJb/PhRuUGaWQqjYyWAoNsYtgD/X1NWgYfgeS9Q
K8ky+0wTf2RQIfd2GuJvPzQJl7DL3wQ=
=Z8Z0
-----END PGP SIGNATURE-----
```

## 0.26.0 - 2022-05-14

Changes:

This release will update/upgrade (whatever you call it) to FastAPI 0.78.
This is a minor release to align with FastAPI's versioning strategy.

Commits:

- Bump version from 0.25.0 to 0.26.0 (5eb3a12)
- Update to FastAPI 0.78 (acb3533)

Tagger: Brendon Smith <bws@bws.bio>

Date: 2022-05-14 16:57:49 -0400

```text
-----BEGIN PGP SIGNATURE-----

iHUEABYKAB0WIQRUOcb2PA6NDBflNNd4PbryPB1keAUCYoAYEAAKCRB4PbryPB1k
eNB/AQC42dDqRHU5E9zwE/FkFzRh8ls4iE73ONGJsASKe0yzeAEA8LHkhxfOFRXd
RcFf1ieMKK4Qs/vrarAAD4NXZG3gqAg=
=bJjM
-----END PGP SIGNATURE-----
```

## 0.25.0 - 2022-05-14

Changes:

This release will upgrade to FastAPI 0.77 and Starlette 0.19.
This is a minor release to align with FastAPI's versioning strategy.

Commits:

- Bump version from 0.24.0 to 0.25.0 (ddd24f5)
- Upgrade to FastAPI 0.77 and Starlette 0.19 (a41c20f)

Tagger: Brendon Smith <bws@bws.bio>

Date: 2022-05-14 14:11:50 -0400

```text
-----BEGIN PGP SIGNATURE-----

iHUEABYKAB0WIQRUOcb2PA6NDBflNNd4PbryPB1keAUCYn/xHwAKCRB4PbryPB1k
eA+tAP9ub9EBXUO0ZBgAwaZav+FO4e1SKiuxYiipYgIwnxdx4QD/YhfljlQGqaoS
fTT6xUeWBQAYLu2LQUXXS5l4EC4W8wE=
=1N8p
-----END PGP SIGNATURE-----
```

## 0.24.0 - 2022-05-14

Changes:

This release will upgrade to FastAPI 0.76 and Starlette 0.18.
This is a minor release to align with FastAPI's versioning strategy.

Commits:

- Bump version from 0.23.2 to 0.24.0 (a39e595)
- Upgrade to FastAPI 0.76 and Starlette 0.18 (5fb5aed)

Tagger: Brendon Smith <bws@bws.bio>

Date: 2022-05-14 13:20:49 -0400

```text
-----BEGIN PGP SIGNATURE-----

iHUEABYKAB0WIQRUOcb2PA6NDBflNNd4PbryPB1keAUCYn/lEgAKCRB4PbryPB1k
eHqVAQCyWQwSM++VjEoIoTE7gUi3pDMllf0LxckiUu3PgCYW6gEAlfR+GlZfKxBH
CKMvy3Xk6vdv4B9rTLAbMnynODGnggk=
=6aNC
-----END PGP SIGNATURE-----
```

## 0.23.2 - 2022-05-14

Commits:

- Bump version from 0.23.1 to 0.23.2 (24a3da8)
- Update dependencies (e7752b3)

Tagger: Brendon Smith <bws@bws.bio>

Date: 2022-05-14 12:56:15 -0400

```text
-----BEGIN PGP SIGNATURE-----

iHUEABYKAB0WIQRUOcb2PA6NDBflNNd4PbryPB1keAUCYn/fQAAKCRB4PbryPB1k
eGyXAQDvOJujTR6gywDwNIclTd2bDw688sOlbXHzRjofIUChpgEAw9QxNDZ4TaFk
xzZobDEoWHK8aVvtJPGTS/ymgBv0YQc=
=WE7I
-----END PGP SIGNATURE-----
```

## 0.23.1 - 2022-04-19

Commits:

- Bump version from 0.23.0 to 0.23.1 (5f2d247)
- Update dependencies (b6ab26c)
- Update to FastAPI 0.75.2 (ea2fffa)
- Update logging filter docs to use Docker image (342490c)
- Merge pull request #51 from br3ndonland/drop-codecov (e2c8b74)
- Raise coverage of tests to 100% (5143685)
- Update GitHub Actions workflows for coverage.py (5b9beff)
- Remove pytest-cov and just use coverage.py (829e862)
- Update CONTRIBUTING.md for Codecov removal (71d2ede)
- Swap Codecov badge for custom coverage badge (e078ea8)
- Add Sourcery config file to set Python version (455dd65)
- Update to v3 actions (6b73d75)
- Update to codecov/codecov-action@v3 (b0f29a6)
- Drop `typing` import from `test_logging_conf.py` (6624a43)

Tagger: Brendon Smith <bws@bws.bio>

Date: 2022-04-19 14:47:14 -0400

```text
-----BEGIN PGP SIGNATURE-----

iHUEABYKAB0WIQRUOcb2PA6NDBflNNd4PbryPB1keAUCYl8D5gAKCRB4PbryPB1k
eGEsAP4m3J31sTcWbwwgpEFzyw0NfblQHNSgeyGCoMNdMq4b2wD+LCQMW9vuQOgJ
MRhYXAhDLgXH3FG4ph9biz0ef8wraAc=
=TGyV
-----END PGP SIGNATURE-----
```

## 0.23.0 - 2022-04-02

Changes:

Add Python 3.10 support (#36)

- Work began on Python 3.10 support nearly nine months ago.
- inboard is now able to support Python 3.10.
- The primary blockers were Poetry and pydantic.

Add configurable logging filter (#49)

- Filters identify log messages to filter out, so that the logger does
  not log messages containing any of the filters. If any matches are
  present in a log message, the logger will not output the message.
- The environment variable `LOG_FILTERS` can be used to specify filters
  as a comma-separated string, like `LOG_FILTERS="/health, /heartbeat"`.
  To then add the filters to a class instance, the
  `LogFilter.set_filters()` method can make the set of filters from the
  environment variable value.
- One of the primary use cases for log message filters is health checks.
  When applications with APIs are deployed, it is common to perform
  "health checks" on them. Health checks are usually performed by making
  HTTP requests to a designated API endpoint. These checks are made at
  frequent intervals, and so they can fill up the access logs with large
  numbers of unnecessary log records. To avoid logging health checks,
  add those endpoints to the `LOG_FILTERS` environment variable.

Support module paths for Gunicorn config files (e068622, 75b3a48)

- Gunicorn accepts either file paths or module paths. Module paths are
  prefixed with "python:".
- inboard will now support module paths (in addition to file paths) with
  the `GUNICORN_CONF` environment variable.
- inboard will now use a module path as the default.

Commits:

- Bump version from 0.22.0 to 0.23.0 (b1a6855)
- Merge pull request #36 from br3ndonland/python-3.10 (7b2fdf6)
- Update type annotations for Python 3.10 (f3fd95d)
- Use Python 3.10 as default version in Dockerfile (760c071)
- Add Python 3.10 to GitHub Actions workflows (1fbcdeb)
- Merge pull request #49 from br3ndonland/logging-filter (97e35b7)
- Refactor #49 with Sourcery (#50) (fba2fd2)
- Add configurable logging filter (32792cd)
- Update dependencies (80cbaf4)
- Update pre-commit dependencies (0746175)
- Resolve Black pre-commit hook `ImportError` (cb62817)
- Add complete logging override example to docs (94d202b)
- Use Python module path as `gunicorn_conf` default (75b3a48)
- Set default `PRE_START_PATH` to `None` (8c8c6cf)
- Move pydantic response models to `main_fastapi.py` (4990a2e)
- Refactor `test_main.py` (e6a6060)
- Remove the last `# noqa: E501` Flake8 comment (21667c5)
- Clarify pytest fixture request variable names (35d4d2c)
- Support module paths for Gunicorn config files (e068622)

Tagger: Brendon Smith <bws@bws.bio>

Date: 2022-04-02 18:14:39 -0400

```text
-----BEGIN PGP SIGNATURE-----

iHUEABYKAB0WIQRUOcb2PA6NDBflNNd4PbryPB1keAUCYkjK2wAKCRB4PbryPB1k
eEd0AQC9vEmeE3wWZrw/FmlCcYFyqANwyH1NS7OLbqWxHPRbmQEA4vtJ6U07RxEZ
suED08C9/DXAUMeQbKxuFORQ3uf12gM=
=l65A
-----END PGP SIGNATURE-----
```

## 0.22.0 - 2022-03-06

Changes:

Add Docker tags for minor version numbers (a547b68)

- The inboard version in the Python package doesn't automatically
  stay in sync with the inboard version in the Docker container.
  Some users may install the inboard Python package with a
  minor version constraint, like `inboard==0.22.*` for requirements.txt
  or `inboard = "^0.22"` for pyproject.toml with Poetry.
  The Docker images previously only offered exact version numbers.
- This commit will add support for minor version numbers, so the
  Docker images can be specified with something like
  `br3ndonland/inboard:fastapi-0.22`.

Check pre-start script exit code (1a27553) (breaking change)

- inboard optionally runs a pre-start script before starting the server.
  The path to a pre-start script can be specified with the environment
  variable `PRE_START_PATH`. If the environment variable is set to a
  nonzero value, inboard will run the script at the provided path, using
  the `subprocess` standard library package.
- Previously, if the script exited with an error, inboard would continue
  starting the server. However, it may be preferable to stop the server
  if the pre-start script fails.
- This commit will update the subprocess call to include `check=True`.
  If the pre-start script exits with an error, inboard will not start
  the server.
- The behavior of successful pre-start script runs will not change.
  However, failed pre-start script runs will now exit with error codes,
  and prevent the server from starting.

This is a minor release to account for the potentially breaking change.

Commits:

- Bump version from 0.21.0 to 0.22.0 (39b644a)
- Add Docker tags for minor version numbers (a547b68)
- Check pre-start script exit code (1a27553)

Tagger: Brendon Smith <bws@bws.bio>

Date: 2022-03-06 12:52:36 -0500

```text
-----BEGIN PGP SIGNATURE-----

iHUEABYKAB0WIQRUOcb2PA6NDBflNNd4PbryPB1keAUCYiT1NQAKCRB4PbryPB1k
eJQkAQD5AWfpM0w2kqqO3+8KkacgrCu8hZMyt8yDVkxLwqWCagD/Z25pUTy/LnYT
jELC3g4uU+piSLBU8Gi4g42Mg3+MdAU=
=pD94
-----END PGP SIGNATURE-----
```

## 0.21.0 - 2022-03-05

Changes:

This release will upgrade to Uvicorn 0.17.
This is a minor release to align with Uvicorn's versioning strategy.

Commits:

- Bump version from 0.20.0 to 0.21.0 (5436443)
- Upgrade to Uvicorn 0.17 (2d29e13)

Tagger: Brendon Smith <bws@bws.bio>

Date: 2022-03-05 21:28:41 -0500

```text
-----BEGIN PGP SIGNATURE-----

iHUEABYKAB0WIQRUOcb2PA6NDBflNNd4PbryPB1keAUCYiQcgQAKCRB4PbryPB1k
eNcoAQCVudR82ct9kniWd4iWM0W/tBePYQ4bZG0ZEipAQDwwOwD/Rfo8r1LLJRq0
y+Hx02wYUgJzBcB3VHoz4pIzC/FN+Ao=
=LhU7
-----END PGP SIGNATURE-----
```

## 0.20.0 - 2022-03-05

Changes:

This release will upgrade to Uvicorn 0.16.
This is a minor release to align with Uvicorn's versioning strategy.

Commits:

- Bump version from 0.19.0 to 0.20.0 (8b7f6da)
- Upgrade to Uvicorn 0.16 (7cf41c4)

Tagger: Brendon Smith <bws@bws.bio>

Date: 2022-03-05 21:05:29 -0500

```text
-----BEGIN PGP SIGNATURE-----

iHUEABYKAB0WIQRUOcb2PA6NDBflNNd4PbryPB1keAUCYiQXAAAKCRB4PbryPB1k
eO3tAQCXxupBJEDDbgoYqN2JGfIG+z/igsav3t7M1pMoo5xEUAD/Xq1nygEvlZ8b
dh8+utuekxamsDEjU2ChJxpCywf26gs=
=rw1l
-----END PGP SIGNATURE-----
```

## 0.19.0 - 2022-03-05

Changes:

This release will upgrade to FastAPI 0.75.
This is a minor release to align with FastAPI's versioning strategy.

Commits:

- Bump version from 0.18.0 to 0.19.0 (c24eef0)
- Upgrade to FastAPI 0.75 (82df92c)

Tagger: Brendon Smith <bws@bws.bio>

Date: 2022-03-05 20:38:17 -0500

```text
-----BEGIN PGP SIGNATURE-----

iHUEABYKAB0WIQRUOcb2PA6NDBflNNd4PbryPB1keAUCYiQQrwAKCRB4PbryPB1k
eEIiAQC/3G0T9wZb3W5yK0PPANfAS3rNNYBodlrtRA310Ix7MQD8DdZ/wsJWYirS
6NViq6YjNUwsUMZs/6aQD7yehuodmgI=
=2CQq
-----END PGP SIGNATURE-----
```

## 0.18.0 - 2022-03-05

Changes:

This release will upgrade to FastAPI 0.74.
This is a minor release to align with FastAPI's versioning strategy.

Note the important breaking change: The internal `AsyncExitStack` was
updated so that dependencies with `yield` can now catch `HTTPException`
and custom exceptions. See the docs for further details:
https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/

Commits:

- Bump version from 0.17.0 to 0.18.0 (f4cef1f)
- Upgrade to FastAPI 0.74 (570ef57)

Tagger: Brendon Smith <bws@bws.bio>

Date: 2022-03-05 20:09:50 -0500

```text
-----BEGIN PGP SIGNATURE-----

iHUEABYKAB0WIQRUOcb2PA6NDBflNNd4PbryPB1keAUCYiQKGwAKCRB4PbryPB1k
eJSoAQDd8EvJm2/LlIZCyatI6hmqu/9Eqs+9e1Bj64eHnBQeswD/VfSSNxVGW/BT
zwaTv4xBtVxyjdPNKbK3UlEt26CzRAs=
=AvjN
-----END PGP SIGNATURE-----
```

## 0.17.0 - 2022-03-05

Changes:

This release will upgrade to FastAPI 0.73.
This is a minor release to align with FastAPI's versioning strategy.

Commits:

- Bump version from 0.16.0 to 0.17.0 (c0af880)
- Upgrade to FastAPI 0.73 (d9512bb)

Tagger: Brendon Smith <bws@bws.bio>

Date: 2022-03-05 19:42:44 -0500

```text
-----BEGIN PGP SIGNATURE-----

iHUEABYKAB0WIQRUOcb2PA6NDBflNNd4PbryPB1keAUCYiQDogAKCRB4PbryPB1k
eA+lAP4uNrGYxLGSxx7xFVOrYfKu19WEodCkCUm+2jBHyavVQQEA+pRbht9K6Ey3
u6DSpbYoTdrH6PLFIdjssbz2wKJZtAY=
=AmBJ
-----END PGP SIGNATURE-----
```

## 0.16.0 - 2022-03-05

Changes:

This release will upgrade to FastAPI 0.72.
This is a minor release to align with FastAPI's versioning strategy.

Commits:

- Bump version from 0.15.0 to 0.16.0 (c8adeaf)
- Upgrade to FastAPI 0.72 (66686fd)

Tagger: Brendon Smith <bws@bws.bio>

Date: 2022-03-05 19:13:21 -0500

```text
-----BEGIN PGP SIGNATURE-----

iHUEABYKAB0WIQRUOcb2PA6NDBflNNd4PbryPB1keAUCYiP81gAKCRB4PbryPB1k
eMNnAQDwmuWC4jZs7n9XcW95ilb6famBvo3ncMuW2FAJBCOqYgD5AXxO9JEq9Run
y8jFkvDA50UY0civJw3bP9IT9kr+xgY=
=fV1Q
-----END PGP SIGNATURE-----
```

## 0.15.0 - 2022-03-05

Changes:

This release will upgrade to FastAPI 0.71 and Starlette 0.17.
This is a minor release to align with FastAPI's versioning strategy.

Commits:

- Bump version from 0.14.0 to 0.15.0 (2a477d3)
- Add PyPI trove classifier for FastAPI (b164470)
- Upgrade to FastAPI 0.71 and Starlette 0.17 (d2f3295)

Tagger: Brendon Smith <bws@bws.bio>

Date: 2022-03-05 18:49:55 -0500

```text
-----BEGIN PGP SIGNATURE-----

iHUEABYKAB0WIQRUOcb2PA6NDBflNNd4PbryPB1keAUCYiP3xAAKCRB4PbryPB1k
eAXqAP9CNgAxEKQesMu4cVKibX7hYpsjWQ+5PhC1fS1A6+MxvAEAlPjAN3xetJkE
qVaARGP0Hf43MDkLuaho1EqTCdv6yQU=
=muMi
-----END PGP SIGNATURE-----
```

## 0.14.0 - 2022-03-05

Changes:

- Install Poetry with pipx (#47)

Commits:

- Bump version from 0.13.0 to 0.14.0 (d9207e9)
- Update pre-commit dependencies (06a0a85)
- Update to pytest 7 (7a3cd8f)
- Update to stable Black (df6ce8d)
- Update dependencies (f1cde24)
- Update to Material for MkDocs 8 (8454308)
- Update to mypy 0.9x (73d528b)
- Update coverage.py concurrency configuration (0474074)
- Update dependencies (c7c3b32)
- Document `musllinux` binary package distributions (8fc950a)
- Add `virtualenvs.create` setting to poetry.toml (5831c0e)
- Don't install `dev-dependencies` for CodeQL (3c24b5e)
- Run CodeQL with latest Python (4e15f78)
- Remove Python version matrix from CodeQL workflow (5214051)
- Test package version before publishing to PyPI (9a2cf80)
- Remove `POETRY_VIRTUALENVS_IN_PROJECT` variables (b33af2a)
- Disable Poetry experimental new installer (9476d5b)
- Merge pull request #47 from br3ndonland/pipx-poetry (a4691bf)
- Document installation of Poetry with `pipx` (ebd8454)
- Install Poetry with `pipx` (af7bedd)

Tagger: Brendon Smith <bws@bws.bio>

Date: 2022-03-05 18:03:33 -0500

```text
-----BEGIN PGP SIGNATURE-----

iHUEABYKAB0WIQRUOcb2PA6NDBflNNd4PbryPB1keAUCYiPsYAAKCRB4PbryPB1k
eINlAP0bsJgLljhhfBZpuq9xHiTbJ6xmjPjC0oWhihFiUGk+lAEAgM/8ZCDWbwHO
HeJdIRmGq7O2CoSs+k4bJETbQP+hPwM=
=RgFZ
-----END PGP SIGNATURE-----
```

## 0.13.0 - 2021-10-23

Changes:

This release will upgrade to FastAPI 0.70 and Starlette 0.16.
This is a minor release to align with FastAPI's versioning strategy.

Commits:

- Bump version from 0.12.0 to 0.13.0 (48ae350)
- Merge pull request #46 from br3ndonland/fastapi-0.70 (00f70f9)
  Upgrade to FastAPI 0.70 and Starlette 0.16
- Upgrade to FastAPI 0.70 and Starlette 0.16 (9006a15)

Tagger: Brendon Smith <bws@bws.bio>

Date: 2021-10-23 19:50:35 -0400

```text
-----BEGIN PGP SIGNATURE-----

iHUEABYKAB0WIQRUOcb2PA6NDBflNNd4PbryPB1keAUCYXSgQAAKCRB4PbryPB1k
eEJEAP4yvzIxvPAXPJF+ZIZvMfnrAxpVq69ji4YcTFEhoGFgKwEAz6GfNYFA+IOV
OsYz7SCvUHWzaMK0tlnYrKv1rC+0VQE=
=UqB5
-----END PGP SIGNATURE-----
```

## 0.12.0 - 2021-10-23

Changes:

This release will upgrade to FastAPI 0.69 and Starlette 0.15.
This is a minor release to align with FastAPI's versioning strategy.

Commits:

- Bump version from 0.11.0 to 0.12.0 (b5b2eab)
- Merge pull request #45 from br3ndonland/fastapi-0.69 (93ac39a)
  Upgrade to FastAPI 0.69 and Starlette 0.15
- Update dependencies (9935758)

Tagger: Brendon Smith <bws@bws.bio>

Date: 2021-10-23 19:09:30 -0400

```text
-----BEGIN PGP SIGNATURE-----

iHUEABYKAB0WIQRUOcb2PA6NDBflNNd4PbryPB1keAUCYXSX9AAKCRB4PbryPB1k
eNbSAP9jj+6ZkvSbvVkFq1YKZY5oOACLxvKzoLnvR3s+1Z4+eAD9HZYSrnr8VsYN
DcOdxLRnnqFsxYGkC5MkTS5ooCOfJQ0=
=ocHX
-----END PGP SIGNATURE-----
```

## 0.11.0 - 2021-10-23

Changes include (most recent first):

- Pin and test Poetry version
- Drop `toml` dependency
- Implement `UVICORN_CONFIG_OPTIONS` variable for catch-all config
- Upgrade to Uvicorn 0.15, ensuring version-appropriate config options
- Add support for Alpine and Debian "slim" Linux distributions

Commits:

- Bump version from 0.11.0-beta.0 to 0.11.0 (dcfaa60)
- Bump version from 0.11.0-alpha.3 to 0.11.0-beta.0 (a12f12a)
- Update dependencies (e7a23df)
- Use consistent substring match for Poetry version (74deab7)
- Merge pull request #44 from br3ndonland/poetry-version (02066b3)
  Pin and test Poetry version
- Pin and test Poetry version in Docker (036b57c)
- Pin and test Poetry version in GitHub Actions (a38617d)
- Document Rust Python extensions on Alpine Linux (c59805a)
- Merge pull request #43 from br3ndonland/drop-toml (d7eb82a)
  Drop `toml` dependency
- Drop `toml` dependency (619f63c)
- Replace PAT with `GITHUB_TOKEN` for `docker login` (ddffe97)
- Only run `docker login` when pushing to registry (809d413)
- Fix typo in `contributing.md` (#42) (8900a7e)
- Bump version from 0.11.0-alpha.2 to 0.11.0-alpha.3 (9745b25)
- Clarify `inboard.start._split_uvicorn_option` (a93fcbb)
- Ensure Uvicorn options are version-appropriate (242ff7a)
- Bump version from 0.11.0-alpha.1 to 0.11.0-alpha.2 (792c263)
- Merge pull request #41 from br3ndonland/uvicorn-config-options (fe582cb)
  Add `UVICORN_CONFIG_OPTIONS` environment variable for catch-all configuration
- Document `UVICORN_CONFIG_OPTIONS` variable (509b4bf)
- Implement `UVICORN_CONFIG_OPTIONS` variable (a8773b6)
- Use pytest fixtures for test Uvicorn configs (2964358)
- Remove `mock_` prefixes from `tests/test_start.py` (0ef5dfc)
- Strip spaces from both ends of `RELOAD_DIRS` (3808f2c)
- Merge pull request #39 from br3ndonland/uvicorn-0.15 (043c929)
  Upgrade to Uvicorn 0.15 and implement new reload options
- Update #39 with Sourcery refactorings from #40 (75b81a4)
- Document new Uvicorn 0.15 reload config options (95fe201)
- Implement new Uvicorn 0.15 reload config options (f4428dd)
- Upgrade to Uvicorn 0.15 (ffb47df)
- Clarify Debian slim Dockerfile example in docs (8b0ef55)
- Bump version from 0.11.0-alpha.0 to 0.11.0-alpha.1 (7c4647d)
- Merge pull request #38 from br3ndonland/slim (bac938a)
  Add support for Debian slim Docker images
- Document how to use Debian slim Docker images (9389572)
- Add support for Debian slim Docker images (582dcef)
- Bump version from 0.10.4 to 0.11.0-alpha.0 (6f27dc7)
- Document how to use Alpine Linux with inboard (86efc46)
- Delete build dependencies from Alpine Linux images (d85200c)
- Merge pull request #37 from br3ndonland/alpine (11dc393)
  Add support for Alpine Linux
- Document support for Alpine Linux (41ae8b6)
- Add support for Alpine Linux to GitHub Actions (a442b9f)
- Add support for Alpine Linux to Dockerfile (c7d83e7)
- Ensure Poetry is on `$PATH` in all Docker images (efe50b8)

Tagger: Brendon Smith <bws@bws.bio>

Date: 2021-10-23 18:08:28 -0400

```text
-----BEGIN PGP SIGNATURE-----

iHUEABYKAB0WIQRUOcb2PA6NDBflNNd4PbryPB1keAUCYXSI8gAKCRB4PbryPB1k
eN3RAQCAG5jRl5atxzfyg4I2K3Ck74or3V+u8HJVr2V9SYtGwAEA9LoDv/CHWyPc
yPiXwzCC9so1GLJHcm5hvhmSNVjBUQU=
=KXbG
-----END PGP SIGNATURE-----
```

## 0.11.0-beta.0 - 2021-10-11

Changes include:

- Add support for Alpine and Debian "slim" Linux distributions
- Upgrade to Uvicorn 0.15, ensuring version-appropriate config options
- Implement `UVICORN_CONFIG_OPTIONS` variable for catch-all config
- Drop `toml` dependency
- Pin and test Poetry version

Commits:

- Bump version from 0.11.0-alpha.3 to 0.11.0-beta.0 (a12f12a)
- Update dependencies (e7a23df)
- Use consistent substring match for Poetry version (74deab7)
- Merge pull request #44 from br3ndonland/poetry-version (02066b3)
- Pin and test Poetry version in Docker (036b57c)
- Pin and test Poetry version in GitHub Actions (a38617d)
- Document Rust Python extensions on Alpine Linux (c59805a)
- Merge pull request #43 from br3ndonland/drop-toml (d7eb82a)
- Drop `toml` dependency (619f63c)
- Replace PAT with `GITHUB_TOKEN` for `docker login` (ddffe97)
- Only run `docker login` when pushing to registry (809d413)
- Fix typo in `contributing.md` (#42) (8900a7e)
- Bump version from 0.11.0-alpha.2 to 0.11.0-alpha.3 (9745b25)
- Clarify `inboard.start._split_uvicorn_option` (a93fcbb)
- Ensure Uvicorn options are version-appropriate (242ff7a)
- Bump version from 0.11.0-alpha.1 to 0.11.0-alpha.2 (792c263)
- Merge pull request #41 from br3ndonland/uvicorn-config-options (fe582cb)
- Document `UVICORN_CONFIG_OPTIONS` variable (509b4bf)
- Implement `UVICORN_CONFIG_OPTIONS` variable (a8773b6)
- Use pytest fixtures for test Uvicorn configs (2964358)
- Remove `mock_` prefixes from `tests/test_start.py` (0ef5dfc)
- Strip spaces from both ends of `RELOAD_DIRS` (3808f2c)
- Merge pull request #39 from br3ndonland/uvicorn-0.15 (043c929)
- Update #39 with Sourcery refactorings from #40 (75b81a4)
- Document new Uvicorn 0.15 reload config options (95fe201)
- Implement new Uvicorn 0.15 reload config options (f4428dd)
- Upgrade to Uvicorn 0.15 (ffb47df)
- Clarify Debian slim Dockerfile example in docs (8b0ef55)
- Bump version from 0.11.0-alpha.0 to 0.11.0-alpha.1 (7c4647d)
- Merge pull request #38 from br3ndonland/slim (bac938a)
- Document how to use Debian slim Docker images (9389572)
- Add support for Debian slim Docker images (582dcef)
- Bump version from 0.10.4 to 0.11.0-alpha.0 (6f27dc7)
- Document how to use Alpine Linux with inboard (86efc46)
- Delete build dependencies from Alpine Linux images (d85200c)
- Merge pull request #37 from br3ndonland/alpine (11dc393)
- Document support for Alpine Linux (41ae8b6)
- Add support for Alpine Linux to GitHub Actions (a442b9f)
- Add support for Alpine Linux to Dockerfile (c7d83e7)
- Ensure Poetry is on `$PATH` in all Docker images (efe50b8)

Tagger: Brendon Smith <bws@bws.bio>

Date: 2021-10-11 18:55:35 -0400

```text
-----BEGIN PGP SIGNATURE-----

iHUEABYKAB0WIQRUOcb2PA6NDBflNNd4PbryPB1keAUCYWTBPwAKCRB4PbryPB1k
eO/FAP9yERJyiyE5ZdMFYkr2YnFRMr+ulbwTpO+A2LfQWvxRyQEA0vwtuuGbHsyD
dqZ5HggxhnEofBKJWaR3NPUhEAvTnwY=
=xkDN
-----END PGP SIGNATURE-----
```

## 0.11.0-alpha.3 - 2021-08-29

- Bump version from 0.11.0-alpha.2 to 0.11.0-alpha.3 (9745b25)
- Clarify `inboard.start._split_uvicorn_option` (a93fcbb)
- Ensure Uvicorn options are version-appropriate (242ff7a)

Tagger: Brendon Smith <bws@bws.bio>

Date: 2021-08-29 13:24:43 -0400

```text
-----BEGIN PGP SIGNATURE-----

iHUEABYKAB0WIQRUOcb2PA6NDBflNNd4PbryPB1keAUCYSvC6wAKCRB4PbryPB1k
eONCAQC0ppruXhhTSb6puLb/muV4benX1ktU4QFFDL6j31gVbAD/dNJgLL5AvxQJ
fsynM8/z9XIaVT9pFQcaQjbXsjhWMA8=
=dits
-----END PGP SIGNATURE-----
```

## 0.11.0-alpha.2 - 2021-08-27

- Bump version from 0.11.0-alpha.1 to 0.11.0-alpha.2 (792c263)
- Merge pull request #41 from br3ndonland/uvicorn-config-options (fe582cb)
  Add `UVICORN_CONFIG_OPTIONS` environment variable for catch-all configuration
- Document `UVICORN_CONFIG_OPTIONS` variable (509b4bf)
- Implement `UVICORN_CONFIG_OPTIONS` variable (a8773b6)
- Use pytest fixtures for test Uvicorn configs (2964358)
- Remove `mock_` prefixes from `tests/test_start.py` (0ef5dfc)
- Strip spaces from both ends of `RELOAD_DIRS` (3808f2c)
- Merge pull request #39 from br3ndonland/uvicorn-0.15 (043c929)
  Upgrade to Uvicorn 0.15 and implement new reload options
- Update #39 with Sourcery refactorings from #40 (75b81a4)
- Document new Uvicorn 0.15 reload config options (95fe201)
- Implement new Uvicorn 0.15 reload config options (f4428dd)
- Upgrade to Uvicorn 0.15 (ffb47df)
- Clarify Debian slim Dockerfile example in docs (8b0ef55)

Tagger: Brendon Smith <bws@bws.bio>

Date: 2021-08-27 19:50:12 -0400

```text
-----BEGIN PGP SIGNATURE-----

iHUEABYKAB0WIQRUOcb2PA6NDBflNNd4PbryPB1keAUCYSl6xAAKCRB4PbryPB1k
eOb2AQCFkj/fqvZFe5wHweqUlqqrt7rxjVejs7iK+oqEcYxiegD+J48ujXJJGOF5
SAfGWek838og4jbYgfaoXOjtaRA6ggI=
=w9tg
-----END PGP SIGNATURE-----
```

## 0.11.0-alpha.1 - 2021-08-14

- Bump version from 0.11.0-alpha.0 to 0.11.0-alpha.1 (7c4647d)
- Merge pull request #38 from br3ndonland/slim (bac938a)
- Document how to use Debian slim Docker images (9389572)
- Add support for Debian slim Docker images (582dcef)

Tagger: Brendon Smith <bws@bws.bio>

Date: 2021-08-14 16:10:47 -0400

```text
-----BEGIN PGP SIGNATURE-----

iHUEABYKAB0WIQRUOcb2PA6NDBflNNd4PbryPB1keAUCYRgjVwAKCRB4PbryPB1k
eD3/AP9dQRg3Hu7XAh6cs/EVmPwqYvuAF38csaKRN2LXwPab5gEAt/Dfb5HoRXO5
qkJ2525/sf5ay/Pdqe7LD+uJwixb8A4=
=tvE7
-----END PGP SIGNATURE-----
```

## 0.11.0-alpha.0 - 2021-08-14

- Bump version from 0.10.4 to 0.11.0-alpha.0 (6f27dc7)
- Document how to use Alpine Linux with inboard (86efc46)
- Delete build dependencies from Alpine Linux images (d85200c)
- Merge pull request #37 from br3ndonland/alpine (11dc393)
- Document support for Alpine Linux (41ae8b6)
- Add support for Alpine Linux to GitHub Actions (a442b9f)
- Add support for Alpine Linux to Dockerfile (c7d83e7)
- Ensure Poetry is on `$PATH` in all Docker images (efe50b8)

Tagger: Brendon Smith <bws@bws.bio>

Date: 2021-08-14 13:08:05 -0400

```text
-----BEGIN PGP SIGNATURE-----

iHUEABYKAB0WIQRUOcb2PA6NDBflNNd4PbryPB1keAUCYRf4jAAKCRB4PbryPB1k
eI28AP46DF2R2355ADNl0EAC4PJLNCniVM38b9/oK9lPtWUJ2wD/awOz28QwhneF
Pbjb1I+LCtDYwdDh+GKfFrVw41WKxgU=
=N4M+
-----END PGP SIGNATURE-----
```

## 0.10.4 - 2021-08-01

- Bump version from 0.10.3 to 0.10.4 (e81b09e)
- Upgrade to FastAPI 0.68 (741ece7)
- Update dependencies (7ce0c24)

Tagger: Brendon Smith <bws@bws.bio>

Date: 2021-08-01 19:52:57 -0400

```text
-----BEGIN PGP SIGNATURE-----

iHUEABYKAB0WIQRUOcb2PA6NDBflNNd4PbryPB1keAUCYQcz4QAKCRB4PbryPB1k
eMYVAQDvMaVuqLDrau1aBHpx3wUdDRWotaOSI1z8H2Sz7/MEcQEApDdRyvuYoHxp
Hu8mTWERfboUvXYlS/lv9jE3AlKjPQc=
=8v/Y
-----END PGP SIGNATURE-----
```

## 0.10.3 - 2021-07-22

- Bump version from 0.10.2 to 0.10.3 (897b521)
- Upgrade to FastAPI 0.67 (e46604b)
- Update dependencies (1cf46b4)
- Update to codecov-action@v2 and new uploader (2512d3c)
- Update GitHub Container Registry URL to new format (8b9346c)
- Use standard input for GitHub Actions Docker login (23ba613)
- Don't push Python version tags from develop (b41768c)
- Remove `site_url` and trailing slash from docs (9943112)
- Revert "Set site_url for mkdocs" (ec2546c)
- Add newlines between admonitions and code blocks (00a73b2)
- Simplify CodeQL workflow (8eefab6)

Tagger: Brendon Smith <bws@bws.bio>

Date: 2021-07-22 00:21:26 -0400

```text
-----BEGIN PGP SIGNATURE-----

iHUEABYKAB0WIQRUOcb2PA6NDBflNNd4PbryPB1keAUCYPjyZgAKCRB4PbryPB1k
eBwpAQDKGeUCwrV4QPwgGANwwLCt1/A0YWltNWF7USEDF32NrQD9FBTGTw/ozLtG
1eoWUUiKyAhoZeeNkCOrDPPo1h7Vwg4=
=dRhg
-----END PGP SIGNATURE-----
```

## 0.10.2 - 2021-07-05

- Bump version from 0.10.1 to 0.10.2 (9dc08a2)
- Upgrade to Uvicorn 0.14 and Click 8.0 (ea77261)
- Upgrade to FastAPI 0.66 (3255a26)
- Update dependencies (709b9cf)
- Use admonitions consistently in docs (15f3d1a)
- Set site_url for mkdocs (36eca9d)
- Move mkdocs-material to Poetry dev-dependencies (02e2ddd)

Tagger: Brendon Smith <bws@bws.bio>

Date: 2021-07-05 17:45:08 -0400

```text
-----BEGIN PGP SIGNATURE-----

iHUEABYKAB0WIQRUOcb2PA6NDBflNNd4PbryPB1keAUCYON9wQAKCRB4PbryPB1k
ePHaAQD/PQ2xwEqkzZ58qAOA6Z5QWl08fiQWiDP801YQzucw8QEAokos/BCFJ7DL
tASb/oYxQiF7/oz9YRsJdE1cV0UKMgw=
=9PO+
-----END PGP SIGNATURE-----
```

## 0.10.1 - 2021-06-09

- Bump version from 0.10.0 to 0.10.1 (d565cfa)
- Update to FastAPI 0.65.2 to patch CVE (7318243)

Tagger: Brendon Smith <bws@bws.bio>

Date: 2021-06-09 14:18:57 -0400

```text
-----BEGIN PGP SIGNATURE-----

iHUEABYKAB0WIQRUOcb2PA6NDBflNNd4PbryPB1keAUCYMEGHgAKCRB4PbryPB1k
eLrxAP9Ng/rVR4f6HOiM7ofAIZd55D9mqvwqnnvqImHR30d/aQD/Ut+hAbrm5hr5
TlCOBeqsJwuohUBFUjMbVqSB7BhA+A0=
=A9Pj
-----END PGP SIGNATURE-----
```

## 0.10.0 - 2021-05-20

- Bump version from 0.9.5 to 0.10.0 (ab0e3db)
- Update dependencies (6315cba)
- Merge pull request #35 from br3ndonland/fastapi-0.65 (4cb2430)
- Upgrade to FastAPI 0.65 and Starlette 0.14 (92326a2)
- Update project author info (3c8a800)
- Remove relative links from README (6ff9f08)
- Revert "Include inboard logo in Python package" (0d06af1)

These changes merit a minor release for the following reasons:

- Upgrading to FastAPI 0.65 and Starlette 0.14 may be a breaking change.
- Project author info will be updated. The email address bws@bws.bio and
  associated GPG key 783DBAF23C1D6478 will be used going forward. See
  https://github.com/br3ndonland and https://keybase.io/br3ndonland for
  corroboration of the new info.

Tagger: Brendon Smith <bws@bws.bio>

Date: 2021-05-20 20:08:27 -0400

```text
-----BEGIN PGP SIGNATURE-----

iHUEABYKAB0WIQRUOcb2PA6NDBflNNd4PbryPB1keAUCYKb6pgAKCRB4PbryPB1k
eNGzAQD62AeqH6Dfla8nUn711aszRBd8d6lwh+VFVpk7yETeowD+K7sHVbrd6nDJ
CwCWPB3ixdLbx2k8UQXfUrebHXuJPgc=
=dtB1
-----END PGP SIGNATURE-----
```

## 0.9.5 - 2021-05-16

- Bump version from 0.9.4 to 0.9.5 (1330702)
- Include inboard logo in Python package (354ccdf)
- Capitalize Poetry URL for Docker (08668d0)

Tagger: Brendon Smith <br3ndonland@protonmail.com>

Date: 2021-05-16 19:42:57 -0400

```text
-----BEGIN PGP SIGNATURE-----

iQIzBAABCAAdFiEE8JoyBFTTcRFWvTCPrGY4TPqMabAFAmChrhEACgkQrGY4TPqM
abClWhAAyMVLFaXJz+6jmTKVgpRX/x0TyqajeGh/4gPrKC93iMTRh0/5YpNlVDrL
mvcHVrtBNmjRiR2O07HSxIJILPmFBwwfu/08QtslH8eDHklukrCpL4i4mI2SdwOV
ouKxahvLjj/3UIbhQSKVNXtqb4rYOaCYi5Mj6eCV25cHLn9XECVltQ/rEMUtzCEy
XmEJvJt8gZAnJfm1CIA6UGp8ji6wPLFd0bpqymOklz1KaEj8hcW6H83BdD47x/iQ
EqUz02hMfFwbXnWncJ2Kd2QzbjQnXNZafrYtvloKxZQB3b9wVJjJu+ToYXfns/lA
5uwFtt63x34dFTsx2J+5pHjAOpIoKfafdYaCqmjd/DdnKNZQFxH/337gr0fnFtU9
wNM3BmoiQFE/m/HoZ2VGLcQH9p1vQn9BGbxwfRmLa36H8QNgrnqEBh6VwX/qkzcw
cp7ROl69WQpKqqF5848xajoHTkf5gnC5lL4dsCegHvDzMRQdVpyPZ/johJ3eEoxe
kXiMxETzFqY/CCXVvpLf/9bylJnzFtUMajg1byMiPwpHePitjdS29Up/4Zu/r6tW
cUpdBlUE7XWwcLC9QvKcT/Oc725tw1T6bVF6jrI3zHD+JJsMQCBsD5RqZnXXl4OG
RsGjt2xdv9VTbKqE2ThGJSBPVCq9TbkypODPsWCu3g9ZzbiRXgg=
=+wxK
-----END PGP SIGNATURE-----
```

## 0.9.4 - 2021-05-16

- Bump version from 0.9.3 to 0.9.4 (c94687e)
- Add docs URLs to README.md and CONTRIBUTING.md (407b45a)
- Add Poetry URLs for Docker and docs (01dda30)
- Merge pull request #34 from br3ndonland/docs (897ae29)
- Add Vercel config (611b204)
- Add authentication docs (c7b98dd)
- Add logging configuration behavior and design docs (4abb085)
- Refactor README.md and CONTRIBUTING.md into docs (eb8d592)
- Add favicon from Material for MkDocs (8257c86)
- Add inboard logo to docs (ebfb59d)
- Add docs homepage (e0f9ed0)
- Configure MkDocs site (22122c7)
- Create MkDocs site (20065b8)
- Add dependencies for docs (05202f5)

Tagger: Brendon Smith <br3ndonland@protonmail.com>

Date: 2021-05-16 19:27:30 -0400

```text
-----BEGIN PGP SIGNATURE-----

iQIzBAABCAAdFiEE8JoyBFTTcRFWvTCPrGY4TPqMabAFAmChqnkACgkQrGY4TPqM
abAiUhAAhlUuw7SlEuDq1+vE1zf+/Q+5Mv891VtuvDkxyChSUTlJ/YrZfF6LwiVF
OHzRWUNLvlZ87YeovX5hNCMxPluW/1HtEBsv1Mc/XbZDtRTaJHjz8LW/s3b05vt7
GZPM2nGY1fngNBgoG2dBejdNTBoLuleDEOkiHuVMPTYz21CKB4wMuXalEBLMxh19
dFHYL37sZSJZ1/TYsq/pKSTdP/pb1z+bJQFmJtBz86ZVWbxtlQPFImpgDSk8tFmk
ybj/GKZFGpL6W8xE/hwKMUU9x0iugQUdUPfTiQeKQVspUaWFMRSX3/q5yzyfpbiu
/oUPUAI8vcH4hOmXmq91k/MjB+Hyh+WpdKqGqy6nwNXydPB2OGQ0ao2HknJYw/2J
BLk2j4gu8G1EOZd2uDJlpEwC5x06+kK0nNaLmk7sCZUofsaqcaSBCJkUo991W7lQ
u+rNBevIfr7lOS/lqepgXEaADWkyGsGbzaG8xDvcFCJO5rE/fUiMtRi12fu6eDQv
EnFQroC2gQrgw2darN62Lv25ElHCdCrrPKKT1hKBr0A52Sr2v5kFYOjVJYNVhC5G
9lR2ZnP9J4LM7pusonm7YoB/JcgjG0qQWDB88dx7V+mE5Xu4RvTz7jm81IlccrxZ
rzF3WUgWHE6LQydQarPn+jaLoSf3jlXuJUsDe68noBSesjaL488=
=fiQ3
-----END PGP SIGNATURE-----
```

## 0.9.3 - 2021-05-08

- Bump version from 0.9.2 to 0.9.3 (adcdecc)
- Add awesome list badge to README (36216b8)
- Update dependencies (f4d0db9)
- Update FastAPI to 0.64 (2feeb74)
- Update Black to 21.5b0 (bcf89c4)

Tagger: Brendon Smith <br3ndonland@protonmail.com>

Date: 2021-05-08 17:58:18 -0400

```text
-----BEGIN PGP SIGNATURE-----

iQIzBAABCAAdFiEE8JoyBFTTcRFWvTCPrGY4TPqMabAFAmCXCYsACgkQrGY4TPqM
abBMxg//anDRbYDli6A8+dlD9NwUzsyLTFSI8MN55eQCZ8lAWWTTil/XW6T2kBvz
5HSIQKbu1X3K29O1kGlxNdbKt33494+2Y4jkbD06VrQrpY8hCRjcO5EwlY1ER+2j
q1gPoGsEImKH657wwlQGEnRTqX/WmPLOFniHVxsSm7yiCShdEbhmFM6B2KajzDA+
L2zphvDFczFJczsZsRTs+mGOgK3DaB0DZ/k+GOYu7MBw1V6e3cXvsBQ3TqLSYdwE
nGj1tlHEq0N9mgSfwzHCSSMvyL/l80YgJPAzcvCKmArRnAWOgSLp9bLbBtCm195Y
PPuodUslRVe28qJy81/ZpBCAYwLWk99aH0WPui74/n/mNyB+02yREzEwhnIQlzK6
yGBIOD/Q7fX2uxGngXyhzgD7/ikvmzF2fULUdqmHW6p66RTZFCGxqm6uuCxCWYMH
PCjN3Z9OLrlpRiGkf/oZg2iJeHP8zFc8e4pzvV0YuUAJyOB1/52OGw8uXXh063av
oE8FJmjRLwGJ0YpgVTv4qhVOX7d4Xd+ayFNXZbzEJtXovlWkSf6g5/V0j/pPk/9K
JkMBbK2mnyRuvltev1dFk9HMuItnSSKKcOXsH1M+pmT3U6mLLAoAB6onsny0Wowz
x7KC/RYHiAPeC3j4i0N0I2KMV7B/ielC3envrTvSQPuNdT1onEM=
=639W
-----END PGP SIGNATURE-----
```

## 0.9.2 - 2021-05-02

- Bump version from 0.9.1 to 0.9.2 (6d34ecd)
- Only use Gunicorn max_workers setting as a limit (f22c1dc)
- Update mypy configuration file (73204fb)
- Update dependencies (f0a63ff)
- Update Black to 21.4b2 (dfb3044)

Tagger: Brendon Smith <br3ndonland@protonmail.com>

Date: 2021-05-02 01:12:04 -0400

```text
-----BEGIN PGP SIGNATURE-----

iQIzBAABCAAdFiEE8JoyBFTTcRFWvTCPrGY4TPqMabAFAmCONLMACgkQrGY4TPqM
abDZ9Q//ZP6/wSGfwHvJRje4jd+QHKvHqJCfhT7C5vuc4OFGvCUwMhad/ZZyzG/h
T/Oj9jhegy8OtSy0/aP8cFxICz3SH4b150opGCXtztKONPRxyhNCtRfUxzmbjz5S
EJGgYp4G8Wg/mtljWM+h8gZYBHZSCUaLbhdOD7aUrwOBUiSWS5PXhQ9RHj3RGkWJ
NpfTTuMTZg2YKVot5vtLLBO1StKsukdicKQn/3U2Lzbm4ZBNYnO2NSCAriKIj0Oq
JBXD0WDBv0DL6Y7adP2unGalvgEf8K2blJMk5BCtCNDR0AYfSu11MZCkvmZ3IfsX
EFcAzvAdiAkzEv1p4oWEPX1JOi9UP6bGpj9CKh7WWOmkkkBDUobgU5arPc02cZ/v
zlAqW1iLwuRhVXeK6cIqkuEJNWxeononz6F2qlDu4mhymCVWoVT4p6tTt0vCq6UH
FeOsUoSOm76fsU30XgYtiI+p26Ff93K/rdU/P5MQUWvv1BkNEolkQEQR840OEGnU
OIibIeLbeSJhjsRQiGCZZmjBHRgRKii2CniEyP2JXobQicU+dnB6TYQ4B+Ouu9Jx
8YjCRukNtKCttl73GTjlZgWW2M8MRt9GxivZzusSdyLUI+ZeZ3wNAJAQdJTu5r4j
V3t4AsnVOjYbPWcszIZD+ttRY2N9g3sSSjrcs/RyPT/yGcGXzjk=
=FtHU
-----END PGP SIGNATURE-----
```

## 0.9.1 - 2021-04-19

- Bump version from 0.9.0 to 0.9.1 (8364ec4)
- Separate FastAPI and Starlette imports for \_\_all\_\_ (94879d4)

Tagger: Brendon Smith <br3ndonland@protonmail.com>

Date: 2021-04-19 19:42:21 -0400

```text
-----BEGIN PGP SIGNATURE-----

iQIzBAABCAAdFiEE8JoyBFTTcRFWvTCPrGY4TPqMabAFAmB+FX8ACgkQrGY4TPqM
abB3kw//VIbQerxIY6oz273nzltboNT0zV/TZmtavQI1GZz4ICIedPgCFaw9E3N/
mIaMsIgLB2fwYYpKy0UTN1khuCUhhAVJHwFhrdYwt4H/PYhb8po6HeEsSHPdoTzN
JzLqCjjP62c3ExwuHB2zboOP66Lj9rsDrHd0vrUiaIklDuTuF8JQC6EoI/kiZkLB
dc31lqyK0rJDB2YLM7Rnw+YRDHddIkA7bVxmDHWha2dBeWYbcyQmEEIoDLkRWOwk
hw+TZOb/JSyADR74ZQ+eaoL61vLf1didzoG8h5iXByBeJ24i/E3IC5awtZ6OT08Y
9dg6DT0ISoFsUuC2SsX/z+GODQP8yXnQ60ZVdx/hLtrxEEBOsZbE7Ew+Lhxh9Jui
oT0Yvvd65uwyTVlBKBTxy5WSIwjeyiP/EE0EVng5HHcXqv6HT86f3CBk0ymfAW4Z
Us868VX8TdJfiQgMy5RJdfctMGOpvnNay+5I2WdSc2FdcWqrfNLQMH2YcfgHK71i
I8bIfqLKdIfvNPBYV2+FNQhpP62L4Nj7lbTwe1WvaH2cYkIjccq7tm0NnMNPRc3C
1vvFtcR8vfsA00SOOcK8iJ1q6872YaVv9ed+w174LnJDElI07VA2HCSuOdUv+t8E
LC/iq2q5tAgK/WyTEfKhtunrlJkD9xWAzkqjCTLusIgpnpTWcLE=
=obc5
-----END PGP SIGNATURE-----
```

## 0.9.0 - 2021-04-18

- Bump version from 0.8.2 to 0.9.0 (d5ba52a)
- Merge pull request #33 from br3ndonland/\_\_all\_\_ (9f361a9)
- Update LOGGING_CONFIG import in README example (b9b0f2f)
- Add \_\_all\_\_ to \_\_init\_\_.py (827c1c7)
- Update dependencies (aec2cf5)
- Update repo tagline (2615802)
- Update mypy configuration file (96132a6)
- Shorten lines in GitHub Actions builds workflow (ebe9d9c)
- Merge pull request #32 from br3ndonland/update-http-basic-auth (a0ab4d0)
- Update HTTP Basic auth for FastAPI and Starlette (2630dea)
- Merge pull request #31 from br3ndonland/conf-testing (c9dd974)
- Clarify Gunicorn variable descriptions in README (40baca4)
- Update links to pytest docs (aa243dd)
- Test logger output after configuring logging (273f795)
- Remove prefix from mocker objects in logger tests (9a61fc2)
- Split up logging configuration method (373c98d)
- Correct attribute error on module spec loader (0ba94fc)
- Consolidate logging configuration method and tests (8cd8db2)
- Use similar syntax to set up Gunicorn and Uvicorn (1b739ed)
- Test Gunicorn settings (324f88f)
- Organize Gunicorn settings (aaef2f0)
- Refactor Gunicorn worker calculation and tests (315c1c1)
- Move Gunicorn conf tests to separate module (d28753b)
- Parametrize app module tests (35d6772)
- Update flake8 pre-commit hook for new GitHub repo (d0174e5)

Tagger: Brendon Smith <br3ndonland@protonmail.com>

Date: 2021-04-18 18:00:15 -0400

```text
-----BEGIN PGP SIGNATURE-----

iQIzBAABCAAdFiEE8JoyBFTTcRFWvTCPrGY4TPqMabAFAmB8rBkACgkQrGY4TPqM
abABnxAA25J4GoH/CGWtl7hpUmgBny2GNd2Xlvq45gg7hGFj8PgCRzoiWbVCHXQi
7WuYX2kKtyS+jwN97eFCX/3Mcx6LpuPoZEJoMiuW4yf8WlakLAga/Xa28nh2DN7e
0kaD1U3IP7S+9SVQM7GQ/21bBgQ48rwi1A1+I2lJmMadGIXlJDANnksEm+r80r1b
a0sCXnXQvBjPhPPeli8T9eIaasG1mmbVZ7db0rMqybIp2Rp0Bui1tE8sRtcJxLzW
Gb2hyotWaitiNJX6MO2DTPiX5NgkhI/w9lP+aihxH78Wj2EqPHcMtXHZmdbX+cd+
zPsnbYxY42K+dA8cRBVaCkPdrk6ZrAWGTiXUljkF+FKRakCw/1bObM+oxyA2qE63
xJsf3YDpSmCPLdNXRmyxD3C5eloaCtMpNPSbF0xG3XLf420uKzcAB2VMkNrmyK2v
Aa5kvLwat1uDuwYlI9iHYW1RSABAVPL8qf6cRijWn7i2cHYxXZh8Y/yLDQkgA3vF
Acp5jT7RYf+hafSQs5QMjVUjMuroHE29vbOriap1iAm0fxsJdcOlm/eQyjmN/jeW
PU8p/02tUKdFaNB297D3ykAiXKFTHWKRpGC6NIydNVNM5g8C7GqMXwr/np3AzZbF
ECAgPwdMmbEOlne/pCx124MExkDSjMSd2puC3qxJMNVM/I0Rmmo=
=G9Ea
-----END PGP SIGNATURE-----
```

## 0.8.2 - 2021-04-04

- Bump version to 0.8.2 (4893ad5)
- Merge pull request #30 from br3ndonland/refactor-start-script (54b0f25)
- Organize Gunicorn and Uvicorn server settings (ad39efe)

Tagger: Brendon Smith <br3ndonland@protonmail.com>

Date: 2021-04-04 20:16:45 -0400

```text
-----BEGIN PGP SIGNATURE-----

iQIzBAABCAAdFiEE8JoyBFTTcRFWvTCPrGY4TPqMabAFAmBqVvkACgkQrGY4TPqM
abC0Ow//acN7kzDsB87rW6n9ralO3qcQroKEzqRNpDki7JsFzvDNYyf2ubIVQhSz
563laN4COPOzhokrOYBp9BqH8+wtyfzCXk91yPnl0btsVH+a638rO2vwKMtbwv8M
8ryna3TSzd7RajRvs0SL1Pk7ycPNh0WeO8cdTI3q1SWmI+yPgANXHmNwJ+rMmLWl
/1kYYjmztUiN76PdZzD7pPiOApsTnX9zEC4thS5fKW9YrIjmvkJFaX/v3MfYIhG2
lCYenhMjf1a5itz2P3UEbA/m1F5YWcEjhSrSwr0+kVIqkHOfhklNx1UX15hfKYq5
W1ox7RdarQzTuM5M/7oQ/9C53Os3Td79DlZuwVXXNlUYkmiOnrOXLG/TOj47BPJ4
oAYHg1RxCVI684DqAdZ/8Cj6WGZUMYg4acThloUfmLsdY3ebxFRIWj4PV/01rHbU
Jl0IwQqC3Fs0BCyNqHpgrX8lAIaBqO2EqRl958d4nMLQA8O8DgK9+4OhJDVKb7sK
eL4gqLJFD6hNjvbMKfhQow+GUFhUmURzWVnRPYSpOMJbiZbn4mwerW3gl8kWHC5F
8wEIIni8N70zXMHe+i+SNUXASqv0AJ+UFPI8e8/xF/RzFExz1zD4IuhldHqgaqU8
ELomu9tbWnHcAw17BcCG3l2io7eoHVAQXn54e7tlvU6EYNFuwMI=
=mEwK
-----END PGP SIGNATURE-----
```

## 0.8.1 - 2021-04-04

- Bump version to 0.8.1 (75676bb)
- Update dependencies (d5ee6b0)
- Add PyPI trove classifier for typed packages (27c18c4)
- Update Poetry info in CONTRIBUTING.md (12a00a7)
- Remove use of standard library bool class (43d3756)

Tagger: Brendon Smith <br3ndonland@protonmail.com>

Date: 2021-04-04 18:39:13 -0400

```text
-----BEGIN PGP SIGNATURE-----

iQIzBAABCAAdFiEE8JoyBFTTcRFWvTCPrGY4TPqMabAFAmBqQL4ACgkQrGY4TPqM
abB6sw//UYmwngeGkmB9ennKvHMP3tQaFLCtGLYCBhuHZ7pu6aCxXlG1r7hgYqp+
KZ/LI/goECCdw41xmkPAjBJbWFYPYNIlbrMGoeBPeG9gPOlYWszkYVHFeJzX/h7d
PE3GPaXy+Qtxod0t0GNUB6wBc0v+L5u/3E7m8mNBV67hAMbFh+nSUpWFwN5Oo/JG
HM7ZBSSro1jGMKE6hhijvTP6oOXla+IY+TkIAn80iUSgdv8YfRiSFAMhfHzuud70
+UzKltvaEmjQjV3dgOu3IAAxT/4X73SiIHbFOHlxvbot7Uss370Hs3OtXxHwVgx/
5ujm58KaQI54HkEWzrcVCO3tcLS+9ZqvnWC4Cq6wD5fepMda7PLksBdLWGXQl/dp
OZhIoAC+Uxtzv+eInGCcRVw8ts9pE4CkV3DOrosreivu5fvFJWnt4XwmYWyGX8XS
TDzvggh0IfZLpQ3HkShqwPj7PpHaScYGXVMKYRmrGSVO/Bae/kt3BEovg683P3Io
Csmx9xE2OUAVectsnax3cLk/qaj+w5zMVVE3kKwhWwQ9UAuUy0u+Q5Efh3tOEes3
gSre5mAE9FHdVrAo25jQikhJbgI/AiTTwcgTtaMeKbqHrapSMZbHnLFk79rfLS81
YEUTIGoyCenxQ8oqVGi525m3hiOvJLrea/xU79VYueOgxQ2j4tU=
=pzZO
-----END PGP SIGNATURE-----
```

## 0.8.0 - 2021-03-06

- Bump version to 0.8.0 (dcf51c1)
- Update dependencies (95d02e1)
- Improve logging config typing and extension info (4a280ac)
- Merge pull request #29 from br3ndonland/docker-start-path (b51193e)
- Use module path for start script in Dockerfile (8d8ac47)
- Merge pull request #28 from br3ndonland/logging-updates (a263822)
- Remove mock logger pytest fixture (3c0e076)
- Properly mock logger in inboard server tests (815a365)
- Properly mock logger in pre-start script tests (23682a1)
- Properly mock logger in app module tests (7b65853)
- Properly mock logger in logging config tests (fcd7021)
- Add GitHub Discussions link to CONTRIBUTING.md (b99b28a)
- Add link to Docker intro site to CONTRIBUTING.md (892fd45)
- Revert README HTML center alignment (cd4ae86)

Tagger: Brendon Smith <br3ndonland@protonmail.com>

Date: 2021-03-06 18:52:07 -0500

```text
-----BEGIN PGP SIGNATURE-----

iQIzBAABCAAdFiEE8JoyBFTTcRFWvTCPrGY4TPqMabAFAmBEFccACgkQrGY4TPqM
abBnphAA2JgRGv0Z0LhLkMJpADYnRno50fPtON5K5wWlXsPRxkcPwz4/1UOCG21B
EOGrjMPeikgjVWd1FfFBZqCWB3Izsw7PVoxuUVXf1DYhG/4uHYR1pBJrLu7shnB6
boRzKk4K+syYFAjofZM/l5/+kZdcT6KnTtdYoUosTSj07AY1QdPtqkAwRgxVVZKn
AjVcnU0hHTHXigQ+3KvGDF5XcaQQjhYob0V6JoDnu7ztD1/vlYEphnP0HPCbjUWk
axa09mN+nwl3N/FXreqLk8EGs+2swiFeNxm76vphuhgRV2NF/dhd7Rdfhtntgeyh
Upz81iVobd4S9WgN8FTAvEKAu/Tvt+FaXrlpOYLr3BubUAFbHK8kLvz7ESrvcFhe
bQdGfVbTH+enuB0MCsZAiM9hARNZ8oR4MNyik31aqougphrVSC0TAxijst7U2sGs
wkY2INkK6C80ZuIEnBiITlTVLFM/FOV9SA/gOSQHE+YJFpmOAUbnspi5cwVIIGeT
f4kic8hu3VH/p6SKCuNDsp5sh9V6oI6RNc2GpwXpdS3R61kM0Kmy95mKn3t++hF2
J1qYsnlEwD7Ldsh37eFIuqGoTWSkgG4hF25+xQGYRSDx17jAj7pLWQnC9ss2YYtF
nxKlrFPVL9lZswNeSeJyja7gBmGIPmTnysKSItO7mdlLm95e1tA=
=f8FM
-----END PGP SIGNATURE-----
```

## 0.7.4 - 2021-02-13

- Bump version to 0.7.4 (89029d6)
- Correct GitHub Actions Docker push step (8dfd6f3)
- Add prestart path to Uvicorn debugger config (2178bd4)
- Use paragraph tags to improve spacing in README (ff267d8)
- Improve pydantic settings model (aa08fab)
- Add FastAPI response models and status codes (409281e)
- Create pytest fixture for pydantic settings model (bb088ac)
- Use consistent names for tests in test_metadata.py (b6449af)
- Update Uvicorn and FastAPI debugger configs (1f7e5d0)

Tagger: Brendon Smith <br3ndonland@protonmail.com>

Date: 2021-02-13 19:23:05 -0500

```text
-----BEGIN PGP SIGNATURE-----

iQIzBAABCAAdFiEE8JoyBFTTcRFWvTCPrGY4TPqMabAFAmAobXsACgkQrGY4TPqM
abBM4xAAiuqMqEli3cSHhyg9WDY3M5wmSpH03vVovcyHP+cB8luNFyKvn/6XatBD
jUx4cEhkQz78V8NaDGMHRmoXnaOTw9HQ3Xej7IIsmI+21RkCqfncbF+TaeZNdcak
A1vrlX7yoqJzhMrQ9C0QviSD4S6UX8WtOcGNGxR1hEGrIc2Zf3Irq9gV4+Z7AvHp
8fpC5T2oA5yqA4ioHBnw5MtiSJ1u5+Hyp9Ah46ycHl3WNkW7wILG8vLMsty6JDg9
tEn2q2TCfoeE4IDJuCWeftZTbfroIyxvFWMDzOigUGb/UHneqIrdnFUQErR6faj2
m1ZYjnvek/KnZJIHNKdXgBm0aYFbwFb8qwbe7PMSHHUItqCNwoOWg7OMXTybBYVF
HpgXyCiZnwfqyUF66YCcaybzQOlnvgCCsZjkueHP2ja35X9DPg7m3GlsGnE5fE9K
vVrDiHbNqTv/tMRi5oQNL/Cq9TEUOtKb2OaCppQvRW2NRSkXgcROF/Vaiuxistoi
r+Ihfsu17MxuvtAojZ54Oj7XMTKlxYrKeVZuoZc2Mto/rUB3PB2MT+za46ctsUuX
cKMIWvJtvCjc+Y82etBBJVm6V+tKBVqYg9ZtyPMPaw6Q2wZxbF6bhsucY+CsgsZQ
EuCTB2pKCJ0j+H9eXmQfokw2WlKyRO55bFZvVjRAkqSHAcGwD9k=
=Ubag
-----END PGP SIGNATURE-----
```

## 0.7.3 - 2021-02-06

- Bump version to 0.7.3 (9212f3f)
- Use regex for CORS origins (6707159)
- Load pyproject.toml into pydantic settings model (c862c3f)
- Update dependencies (543b1fe)
- Remove flaky importlib.metadata test (8b37585)
- Download Poetry custom installer from Git HEAD (a03f1db)
- Fix HTML syntax in README (b03f62d)
- Update dependencies (8bbfd1c)
- Merge pull request #24 from br3ndonland/docker-smoke-tests (70997b5)
- Add Docker smoke tests with HTTPie (13f0d0b)

Tagger: Brendon Smith <br3ndonland@protonmail.com>

Date: 2021-02-06 21:13:38 -0500

```text
-----BEGIN PGP SIGNATURE-----

iQIzBAABCAAdFiEE8JoyBFTTcRFWvTCPrGY4TPqMabAFAmAfTPgACgkQrGY4TPqM
abAMew//Z3KmlJGYQkTQaQAjgIzhu3HNOKXxCvpr705sK7RtTDTCKdi6CxI0sWqg
6+YFd0MPCj2DNsbW7gYoSY3GBtovE4DJpLbW5aX6KCuUiVNZr32wjZmb/7/CHMNL
t0mPD6fhxhYY7dasnJischwX4V25zTdLw7VUk86jghsNx5j5MTnVTF80LLyHrUf3
Nw5ddUd7Ic1cPtIYtfrT+PVSTQvwGgsOj9pAybwqt8+9onLpXXg3IsubFLNSGIyE
op6xr6I+in4HFPxiP+fazmv9f/4Bw+dVet9HOh///RirD5mmOxTmoGuFzixo5inL
CfvEA1GzBl0lL/R/0Sj8HpfW20DzBZcKVgkZ+GjAOkYt69+CiCbGC/ZVWvg0qCoj
LDwO+9hA/QFeybm0cEX+gJbIDDpwKnTvxa23uNZXg6nY0I1rcPaqtoqJdU84xuat
pPhnIl+cDbecyYZxDlO7xIN0mlb+K1ZbfVs0Qx6mQXB3+mhR+VyJxnrF4r8jrmpO
m3bp8ki9qcLWydJeOE1mR5REfEbT84JvwNJK6b2oIJCGqHh8ZLko6e8/7NIkcMp4
HGD6IA248qHqj67hbiYU30PyWSxG4bonz9/QLs6e3nQc09P8psqDSsnBBcnbt/6I
N5VpKeS9Z/Lp2djoITrtIAiXjzYHyRuef5RXsIuuNFDZddEwDKc=
=jWU7
-----END PGP SIGNATURE-----
```

## 0.7.2 - 2021-01-30

- Bump version to 0.7.2 (8cff451)
- Merge pull request #23 from br3ndonland/master-to-main (cb94fa1)
- Update GitHub Actions workflows for main branch (c03de3d)
- Update CONTRIBUTING.md for main branch (7674081)
- Merge pull request #22 from br3ndonland/logo (a060a4e)
- Center align headings and badges in README (c217e9b)
- Add inboard logo to README (5f2a094)

Tagger: Brendon Smith <br3ndonland@protonmail.com>

Date: 2021-01-30 22:00:08 -0500

```text
-----BEGIN PGP SIGNATURE-----

iQIzBAABCAAdFiEE8JoyBFTTcRFWvTCPrGY4TPqMabAFAmAWHUIACgkQrGY4TPqM
abC6uhAAuzbMaXV4Qmocu/9/PrpIqmoEz2GD1klrajmtS3wR6MMzhtDFeo84Fj3V
vNhx6IZYeqHIBQpSwAEBch0orpoVD/JDP8goG70MxWs2pJoRBlbhMIfhtz+wZXbs
MxnDtPuEKt2xa4zzJyOym6KOrb93JY0xB8lZrAAAZgI4nyoI2Tq/3btF3j5N2I6O
oaoL3beaoSscSeXAY5enBol5KUpU7TATXWkhHAf/Nyt5CoWjTvMjJRlp8aRLTwKA
rDN/hkWHHcxBmbLqFHUrkRHATxcEmc3GANJD/5P2BpZYCitMmxtIdQZfa9zL37Gv
C3QcRt3vQXDCidb//UQRh9dTClwQ2fEiTyi57fCeJ1icVnep1edxvRDVea1M/RU7
FGoeGuUSsJwPSR1SXN1520gN4H1T/nWc9VVoa86RrFsfgwI0ywYwdLiKN52lKzmV
ENMyvdikls/zsGbOg3ZBghTgfQM22j8Quz4VHHjSplBAokKhlf2Lk8B7KxrwBLfx
AGNHnN4zECBKqx7MwEw7HLc71AZOBxW240kK8qy8euR3J0inlsEuzK5elyjZ5GKc
cggFZcOTPp8gSeugWBqQxOGEZIJd9nC3pa8qWPncj0qx0wcJh96o4gxfkkX+X4k4
4fvPgPSEQij85o+TqLrQb2kVHUN7CkEujlWCfpKqf23A0AIig7M=
=NbCI
-----END PGP SIGNATURE-----
```

## 0.7.1 - 2020-12-21

- Bump version to 0.7.1 (fef0a8c)
- Upgrade to FastAPI 0.63 (646aad3)
- Update dependencies (f6ac18b)
- Update to Contributor Covenant v2.0 (0177132)

Tagger: Brendon Smith <br3ndonland@protonmail.com>

Date: 2020-12-21 23:40:05 +0000

```text
-----BEGIN PGP SIGNATURE-----

iQIzBAABCAAdFiEE8JoyBFTTcRFWvTCPrGY4TPqMabAFAl/hMmIACgkQrGY4TPqM
abDnjxAAn4fKiRl7lzE9CxIOD5cDr80mxUME3JkzdFIOAHGXcHvHxC49l0tTKbNJ
uyn0PFnw32WHSbNAXpyHL+4X9LT4ASgLJiab+5vxWFTwcEtOq9eo4VlmovVKQIEW
hw7+qDvAGbZqLG/ZSwWTMxwlCgqjIuu+3svY8p06pU5BQN/L5fkocaamTe1n5DSY
OY9U40aB1+foCtj49k/XyWIJhESL2rtmHTrUlbn01ckWSzQUssZEUp7zoHttbqby
kn9noCrsY5K9m6YRYcfM34BUrmYaWCwikAlK+bEnOdGLq0vUp+ZSEh+hOzspGL/v
sEGua0+8ifvC/nO/x3xMqFLGHDvoPTxi9ydnhBbbRbUFmXzkIAxqlodgGYmTtN7e
i2TBA/WxTpRYwTXYovRNkMF3N7vsgev9N9Rr22h+ist0WdEqHQhcklN2FdUHJXKk
HU2fM3Mf2oHyqDUjvdZaqkV/pjJGroRIqngDbT3BAjKTb4iNHM6ABQyBvx9CnTgZ
xw76hTWYwHF7xVLbxtRRULJYHB1qKlJspfWPSpLteDzjSxjBfxh67XGIVIMsn7oR
HpKi1Lpd9e6dYGCAlGSw4LtckXxNLHybb34vPIvXU09GkxAsN/gWA32u/ge+u7NQ
q1pnXUTRw28fNednbSDbgKepFMwuGpPKDXWUT/CECitK6CiYeYk=
=mLg+
-----END PGP SIGNATURE-----
```

## 0.7.0 - 2020-12-20

- Bump version to 0.7.0 (49f63b3)
- Revert "Enable Starlette 0.14" (12eef2a)
- Add new FastAPI VSCode debugger config (11524b6, 79f9e9c)
- Update README (9a6751b, e82ba73, aa399ef)
- Merge pull request #21 from br3ndonland/uvicorn-reload-dirs (a607d65)
  Implement Uvicorn reload_dirs
- Merge pull request #20 from br3ndonland/fastapi!=starlette (e1e34c7)
  Improve separation between FastAPI and Starlette

Tagger: Brendon Smith <br3ndonland@protonmail.com>

Date: 2020-12-20 03:16:01 +0000

```text
-----BEGIN PGP SIGNATURE-----

iQIzBAABCAAdFiEE8JoyBFTTcRFWvTCPrGY4TPqMabAFAl/ewi0ACgkQrGY4TPqM
abAOBg/9Els9qyCAYsg9P3Ni/KqZ/Afz7QkzWtjtzQnNEFjlfd8lB6cOjq9S0PFG
RXwWtqY0JpIMUxHyJZQ6ufdVE6oiLulX7Y1vxut1+vHEde1CYRT0ajQcryut5RC1
7StObRgXCvPR67F35Xe3Ffz6BgG+2bmTH4uTWbs3KcXyXbM5uoNJuiTRCnotc+/C
Bm+YHFzC7/8UvXGws2OFFFw5l5gPUz0D9YSDhuJN6uGi6j3m7y5JzQqsCpOt82Tl
5BI1BdP0zHHZGUF52YEb3QLdDjQnJjgsO556mdXsg00TW03ZHHB0L0QHJpWQl1IQ
1YKz+UCowHxHEd5+GT5iNDPKpEkeBDRPNNTpc9vATcTw5FJtphYBmMuz4LUrpLMj
YrLRSTgtUNBmyAe0N+lehlXAnElz9ugnplRQzStcUiLeYTl5ZP6WoiR6CXrrr5oY
3ZjRmwYuHFz3gebJEGwN3DRYjjpXKGNjlxJ342fKCD6ctRxDWhJzT/+o15QYEnbr
toZOjcjRAQxDVxW7GBFO3YAl83rT9zei71ok25GGE3zkuEqvi9LvTy/i/ZzbYaNc
GLCn+VOPXfkuWTz7vQOruuslHxW0/3r031TUkO5XbhU/5gKQB1TVZR1MjgWL2yOM
+0M3DKcbd807cgrBWObXcelHO7RmKBjdFQ9rAvPXtKdTiUm/XyA=
=A5cW
-----END PGP SIGNATURE-----
```

## 0.6.1 - 2020-12-18

- Bump version to 0.6.1 (7236cd5)
- Update dependencies (49ccdf3)
- Update test syntax for pytest 6.2 (77fe500)
- Upgrade to pytest 6.2 (24f9372)

Tagger: Brendon Smith <br3ndonland@protonmail.com>

Date: 2020-12-18 21:43:15 +0000

```text
-----BEGIN PGP SIGNATURE-----

iQIzBAABCAAdFiEE8JoyBFTTcRFWvTCPrGY4TPqMabAFAl/dInsACgkQrGY4TPqM
abAgoRAAwfUNGNOgFFdWuBCh97AfrVyTxIGtHa8V1Krr4k13WBtXUoNVa/Hilyob
6uY4seCbiVOCnRurWPIgrSIzY/GTF5Rnc302GdiB/HkjG1GT7n2wdhk/0EzNIs4Z
eTX6bhIH1PcWS2p4SWsiZtrEb6K5p8Z3y28Vf8zsoYs/Em0fsa1qMU/PNoEeFUbO
NhA8lqMR2a5cU4rspgJ1E/YzWFz31VZ/4BkrJ+5+dsMEKmT4/4VuRBYX8uZoHiDW
2IenNR26r5loVnbD0RqT/H4pa4CHhykkxvHpaJnd/Zcamt9rld1q3DrZzFYy6pPO
i1SUbu44blJphFG53cbZTJfepIiXeL5Fd/W38h/DPTHSycwqnHjk0aqVmjyEGbeY
BZ053qF80SA3i8BmlNvLudkOURuSMyyAtcUjtgi54GJ1VVM1ZDMNPzeWi0ZyMNTJ
vvXc4clflaCnD812dfv0TaWdBq6n+hUudMI2bEWKPw9z7dQYwWTfBc/+ulVRhFy3
ZCVILjvWZsxbP1fbJ1sL9H6muDRLjprlRVsfid9LIbacbSnfbbwu0x6xo3PRaA9N
CT4uTF6y9cHDXUowXscaAAiqbwImH1CP8+EQV1UCIwBx1x1V6JCmMwLXjE6f4FdD
FDoBiVeYrYhiB/mfaErWaeRfqDB6H0BNOdsjP2v0o9yUdWbZlBU=
=+K/o
-----END PGP SIGNATURE-----
```

## 0.6.0 - 2020-11-28

- Bump version to 0.6.0 (47b164e)
- Flatten app directory (059c72a)
- Build Python package with latest Python version (5f449e2)
- Merge pull request #19 from br3ndonland/python-versions (b033732)
- Use Python version matrix in Docker job (465c923)
- Add info on specifying Python version to README (c14de7f)
- Build Docker images for multiple Python versions (dc8da18)
- Add Python version build argument to Dockerfile (69ebc5f)
- Add Python version matrices for GitHub Actions (1a7a5ad)
- Specify VSCode debugger port for Linux (d651a92)
- Fix test of custom Gunicorn worker calculations (fabc7fc)
- Add coverage.py multiprocessing config (2effdb0)
- Update Prettier pre-commit hook (0cda29d)
- Update dependencies (2ec6bf8)

Tagger: Brendon Smith <br3ndonland@protonmail.com>

Date: 2020-11-28 17:14:03 -0500

```text
-----BEGIN PGP SIGNATURE-----

iQIzBAABCAAdFiEE8JoyBFTTcRFWvTCPrGY4TPqMabAFAl/Cy9UACgkQrGY4TPqM
abDUjxAAqlUWxeS5m+9hW2+H9rnuULGqfZn9r16Bk2NAejxtzCKbI6bF/323bomy
V1koBqWFm38Y4oN+eZ+VixqjcD/FB8qIs1JONrym8jHKIoNayZUYW7BArdBk3FnI
btm5o7a3PaWdqaEFMWUcp5gd6feNYcI5cM0M5bx65V2t3/XT9qQfXpoNbBlI1xDO
LwpTaOcZf5aBetNvFh5lz5+We5inv2A9kRVORj4rD03FyiJmdPX10fNGMwZemZfZ
A0C0vZSsixnaZY1gJWpMXLKdEni374kOooLmZZrJCakfEAHhzml9C02HdP/0kGM+
ObtULTLWkDkWzAozMN+BpdyxQvlUGBSoMeVmY4PzGO7Y9P1679ky15bTPk7weyz4
VOkzybGyGXGOq5IuIt9V6AFumoscHIkORO7OZClLqW0ce6mxRIH3AjXsQmMpIpwT
kbwxA9q9VSzIyZcfF18THMyWC7WrpPeCZUaAzKEd7BYhYf2wy5L9Yr1/wTEi8eEs
2zWOXfyAWp+FTGa8BPZ2Rjf5CiB/euHiAZfUOwSdQPfWtzlZzLqfqtKcO1Jbgu0g
J+JrOFssBgB3yIJKKAxXZ5acbgTkon6RMboTMVZiKeFJL/h1axG37lDm34KvrVlk
qSKPvAG3dX9tj4mkdlNGusNRRdrN2RfCnuzepYmU9TX9cJDW1Pk=
=BKrj
-----END PGP SIGNATURE-----
```

## 0.5.9 - 2020-10-31

- Bump version to 0.5.9 (f5eb570)
- Update minimum pre-commit version to 2.8 (8ac4a34)
- Migrate to new Prettier pre-commit repo (8866ab4)
- Update .prettierignore to ignore venv (c2a5ddb)
- Update GitHub Actions workflows to Python 3.9 (6f01d75)
- Update Docker image to Python 3.9 (d9734b4)
- Use more specific web server mocks (ac5ff70)
- Make Python version syntax more flexible (6bf3abc)
- Make all FastAPI and Starlette endpoints async (e3959b0)
- Simplify conditionals in gunicorn_conf.py (4914a4b)
- Update HTTPie info in README (1c45f19)
- Update dependencies (e96e263)
- Remove Docker SDK (d529e91)

Tagger: Brendon Smith <br3ndonland@protonmail.com>

Date: 2020-10-31 18:43:44 -0400

```text
-----BEGIN PGP SIGNATURE-----

iQIzBAABCAAdFiEE8JoyBFTTcRFWvTCPrGY4TPqMabAFAl+d6LoACgkQrGY4TPqM
abA9LhAA5w/tzxfY72JxioiHGd/6Gvs2OXxapQ/tZJdj2mtJ6z+/DOhkRFYm+Dib
k82uuodhMJxA8K+EIZjd8VR1BAgBiRUo7PMKnjuNSuuoOU+W8sG8EWvgHhFP9A8z
dZ3xqh5AYlQa2lyp672k52fqm5RchQwZkMQzEZQspr7PoPc2xJH+NzbWcaFbcJ3x
ktDnrIoAS443JjNLqNr2biJ7mXIui/5jxVKOrkT3I15iyXtjuE5qDaghoSRVUHGY
SY0Qavo3eS34aJIRJdFUfjJrtsz5vuFklyTpKogdTYBKPr97o1wXx4/mkZJQW469
w8eNeujRQQAVyY8jz0RkUWyQMmlKBaejTXFMfxvNQc9C+IuXFLpfNsD2ZBPBgGkJ
Z2/K/AcfghKrCy1REE7jFS7jnnrUuZp8BD2mOhDJPAlDe9jhxFVpAG/BA0de+KDX
jsuE7t+M4SqrZPECMQWp9l0M+qLvCyvKfGYY3FTOuKPtWd+e7tQv/mvqhScgwCGv
NP/o2CY2nTcZjTk0QewT64z7DowAXI3kFEIK2EBwRHo37EPqPwBNg8zM+JMzVUzn
xQvRgeACpcuvY4a1uXGzpR7rS7m0DA8hQm3ecQpyoXg9jvChT2XXc6hb/duF4vMd
Y63dfIbrMU6BQ2OExtfKCwRwO2JNpssc43wLZmDDFo/r4iDgmhU=
=XJY/
-----END PGP SIGNATURE-----
```

## 0.5.8 - 2020-10-17

- Bump version to 0.5.8 (b192f32)
- Parse pyproject.toml for testing (ff00f0d)
- Rename package metadata test module (0bf44e3)
- Alphabetize GitHub Actions tests workflow branches (f859052)
- Don't change directory if running VSCode debugger (1bcb9c8)
- Explain how to disable pre-start script in README (16dca97)
- Expand example logging_conf.py in README (d8d9af7)
- Update release instructions in CONTRIBUTING.md (e9868d5)
- Update dependencies (7143e26)

Tagger: Brendon Smith <br3ndonland@protonmail.com>

Date: 2020-10-17 21:57:18 -0400

```text
-----BEGIN PGP SIGNATURE-----

iQIzBAABCAAdFiEE8JoyBFTTcRFWvTCPrGY4TPqMabAFAl+LoRoACgkQrGY4TPqM
abD+rA/9FR7YONNn1W1C3LeS4ag4ed2baCm/iZBgnUQKoFVjpuMCQcWE9z+J4bzb
4jokxzr5RBltZhRb/SHWdtpPg2VQSBwWN04lDK6mUBG3/o31MZ+p3gpuhJu3F0cW
2d8z56mxv6CnxB9z3rXRVNQSSPRc5kdycoEOnyENvrweIincTadRtd9F4rSPL5jC
8eWGY18ujt+7sFr6Dmj+XPXGyAsWtq7JBH8kHxfVVJk7LkMQmQsXZgb+wcJlelgW
323BRGzz6/rAGbo3GWZai+KqYlo0t/51J5r2DVLZAUF1YfRHADuafqnok8XnmsZr
alaYiqYYHxbklSM3Dkr84bNKF2GvAbXuC131yz1GRddMY6Mq3vge18nHPgN7wMhD
UbzSsS0rjND+ruW1DFVJp04g7Bm4oxs6yyxkgmjSmFRmwnHPUCJilg8KYS6Qm/lJ
MH8+hGd4HlOG80YUH6z4hVYn1zeO4NcbVplOjsHnaD8DiNYGLCB0v8S5J7l0zZPw
RnwaeyFH7YbwvM5XmxIVAgZx5aItPYzL94pLI1QVyODUW9bDfUsnS94r7m5ZkjFm
yCLwfSIGJDrJN+0DP2PtXicqeH32HphIQXgwtG8e0GCMLp4o7MUYReujq9E8uldP
t1SB+6jgmB1UtQpVu46zW36a69L9GGvb7IqjmIKiIC3SgSYIZFE=
=ZHr1
-----END PGP SIGNATURE-----
```

## 0.5.7 - 2020-10-10

git log --pretty=format:"- %s (%h)" 0.5.6..HEAD

- Bump version to 0.5.7 (0a6692b)
- Manage pre-commit with Poetry in GitHub Actions (84b25bc)
- Add pytest-mock to pre-commit mypy dependencies (8c9081d)
- Update dependencies (0b472d1)
- Update type annotations in README logging config (d7ddb5e)
- Disable Dependabot dependency updates (0bd02d1)
- Update Poetry Docker command for custom installer (b10ace1)
- Use absolute URLs in README (e585a88)
- Merge pull request #18 from br3ndonland/github-actions-updates (83d09bd)
- Run Docker builds on pull requests (023f4d5)
- Remove deprecated GitHub Actions set-env syntax (05a36a8)
- Simplify CodeQL workflow syntax (90abd1f)

Tagger: Brendon Smith <br3ndonland@protonmail.com>

Date: 2020-10-10 16:01:26 -0400

```text
-----BEGIN PGP SIGNATURE-----

iQIzBAABCAAdFiEE8JoyBFTTcRFWvTCPrGY4TPqMabAFAl+CE68ACgkQrGY4TPqM
abAaRg/+L1laHhpCzaMxzqAk7Ii7I9W28CN4UQw1N8wSg4t5lC5x/80lI8mFNHGX
OvjC300gLr+Wr59amGQpkYqBwOrAFkBBZ8g+JnwmvMpvUR6uUXT1lPBf9r1sgA5v
uNwMMBpeWqCcDgZfwR8EnP7eT/hToauBIoYrGGGOnoqno5fMX49VF69NEAHAuThm
qs+9mGnOnkNgsn664uNJXB7HaTbpK+6t4s+HyDNXDtCTY8NuTMAElRxiFwSeyQLm
FcgwKxA6Peplfn9jMSvry9uOlXPd0GPYITw5wo1ccPHlNdERbKDElLE8k7adG50M
tx5rl1akW2rtIWpUssVVjmOutRGYQSke5AWE6k72kHmi8vyzESbKciP9bkm2Of0T
LpFzXqChnuZT15q8Cwi44Lz8a6gx0DXgp7dqVbKylHOra+o4ApSvw28Bk7ACKn4s
dU1pUlGCm4rhCf+r2RXNy8A/C8iEhK+OaOrC15CBcOMFy3folJz9567BD3LWeRCX
OPypviVk0m/Yq4/0JerQ+7n5MP5F4z+hOibzP1bEE/VOzHwljD7nh8OPwL2DJrSl
5Ym5JPVffYXgBePMlHwbbklBguzKUG1Na/V5/6swYj+tNIX1yDPFl40vSlKwCggN
KqSji5y8VWSsdMv36POyF8PhI8AvBcDEYqpDyX7W9/Laenr8gGo=
=qXZu
-----END PGP SIGNATURE-----
```

## 0.5.6 - 2020-10-03

- Bump version to 0.5.6 (0f35934)
- Update docs (e5f18ff, 42d9e45, ded9841, ac859f0)
- Update for Poetry 1.1.0 (#17, 600c951)
- Update dependencies (#12, #13, #14, #15, #16, 059e28b, 13fa37d)

Tagger: Brendon Smith <br3ndonland@protonmail.com>

Date: 2020-10-03 15:43:20 -0400

```text
-----BEGIN PGP SIGNATURE-----

iQIzBAABCAAdFiEE8JoyBFTTcRFWvTCPrGY4TPqMabAFAl941JcACgkQrGY4TPqM
abBllw//VWEgdQqZ9LoHcCi7Exww01rk9Z7STKzT9R53yaT0tAI6J2qGeojIv51C
6onbbm3Fm75JKwpbfZzxyQzgYwYDfxom1jqw3/qhy/lQpQCviwbb8e2Q3tAH8y1Z
TRQsO7U2AGT11QXBt/AdnM+WyCJE8YOL0Z+lfy1PblFfNB3yvKy6dXvVPvfX2vnc
PHoY2eUwz0V9+1h80SZUAtISlfgCZHatTkwzlANMneMJ+E4btXjMa/bmpa0TedgW
uoUjaUXWXAWItwW1TCmK1BbElTOnDF1C/OO5QgOSXOsx9ltLLu3LTXjr6kjAW4C/
gDdBKk/ykctlbyrsE5ONMDtfii4SGVfXGVCX4uU2qYkPfzOt0Rvqiwyxj6+2yX3v
OxjUx6vjcJZsZ+u9JaZOEPfq+V+o1j0QKhPWl1dx6KM8lFNs1iq6jvhfaBoWxjhM
6SYMG1xedmFO7siX/esDzVz04rgEFNxVQPI7JEeiSGFDKUofsnNPoU8VaZyrziYr
vcwU+dt6JI3AVLabdbqSAOyQIqydp9Wdmo/MM19ymGtsZ37EaQVfkLg5ZvXwren9
C6kFgJK+Y2zUtdwtDlH4/TxfIefBhk6nt8C6OaajDj+LndwaZAIYaEQUQmZ4uYJY
PjOKk96TAfE748t65aLjM8ARdBLYQ7uuH7fRrJdRw0xk1Umga4M=
=6m4p
-----END PGP SIGNATURE-----
```

## 0.5.5 - 2020-09-21

- Bump version to 0.5.5 (62f331b)
- Restore pre-start logging (c6f446f)

Tagger: Brendon Smith <br3ndonland@protonmail.com>

Date: 2020-09-21 02:45:01 -0400

```text
-----BEGIN PGP SIGNATURE-----

iQIzBAABCAAdFiEE8JoyBFTTcRFWvTCPrGY4TPqMabAFAl9oTBQACgkQrGY4TPqM
abDRYQ//Y9NrbSbi8Y7PR9xRPyxA9X9SNMYPdMdMX1G95NTAB0PXPLYbSMAKuGRd
3B/FOMzu/GN5LGFtG7d4/4XN85wbT9PP2RU8ULAaS4R3a5H3wOIBmsc9ysFvoybt
qJPsmM0LuFPy8ebk62Bb6lud7wHs1SN5prQEQqSAza/2BUJqdr7iH8/Mcqw3kvty
vfn+lw6fKKXhGBnYm4SsDk5oFsm+lxFo4oLM9s78nlD1FTo7ZZ/54RnXtAKizmCb
BpKELd04lQO41v94xURfcNRPxGDbQh8jBuhsHiK/i6Uher0sIip6U519MV2Wmubw
v/papsvzm7yR/lUkAIyxwR4RGgR2qSBkWZW2mzgI4CI/FLQGAaRpuKh99+QZM+Dl
822DbG4beH8Cr+muW5myDCn9Qdg6O3Gy9xClbBYTusXMxnSTjGAuuN184oawizaM
dmlnI9M8+wp4kIuzvq7NjZeU4geCEXpCjiGc1cniO8BB1gATzs4+ZIWKLBZYgZcw
GOBifxmptA9ABBizjOnpsKCcCZj1ff4vv7VsJ7TbMvCzA1D3hFP2WrgkYgDBP2tJ
LcOEj9N1TQfkcZyByL6b0s7aIP0lwPWIZXyq4MCVmIaMLbss5Vnc9Z5TrhFfuNqn
nkw3DGaBLRoVD/G2+LSO61KpUFkbv4vyFz7ZLxcRe6BT8dFAP64=
=BeZ1
-----END PGP SIGNATURE-----
```

## 0.5.4 - 2020-09-21

- Bump version to 0.5.4 (6208d9c)
- Use Optional[str] for values that could be None (9c79964)

Tagger: Brendon Smith <br3ndonland@protonmail.com>

Date: 2020-09-21 01:11:59 -0400

```text
-----BEGIN PGP SIGNATURE-----

iQIzBAABCAAdFiEE8JoyBFTTcRFWvTCPrGY4TPqMabAFAl9oNksACgkQrGY4TPqM
abDSrA/8DzsiJBjB/X36NEugquz5XpwCbRNrXkXx5PyhgezBgr1Y1jFu/4MXene7
DmLzpvpRBn00eA5T2MRg6GzjkhwJbX/G2IvxSL5Adf6Dv5OcIsiP/WG0puK6DiM7
ACFAXF8DbjhI3pKPNZQaUVJ/wQn0OeNO/IUanxbdb8ifM/6fsGJasY2UTtCEiFiS
FR3Fw6nBaWvoSHQNKHCwaNxWswldsvKhFSJBKnu8tNy6feSzQ6PWy+q2pATQ8aLm
U4VjHdW3c200kGLleytv/Jh8hJS3+pk5NnOBIOA/qdGWLWzakoVmq0vAoYkqaAjg
kkko5OYBlvspo+4NYX0dc4GjFlic0iYHYbR9YwRtp1OyTwo4mYLwdeSQEDgzfLjG
UZFJHAZ3VMhiQUC8aijyLjJbqoDsso34Hq5uXFYq7Ko1K5q+5K1PUAhwxt5AG2A1
DTQ/j7pd6zJrdE7KR5Ea9koCyHLrKemFiT7fgHmVMItREHvZex8DWK0XPyDWM1J9
D1Bc+f+jyEPNaFw2u5kufW2upEwELRKYN0IuA3AdjSMjyQqkQhFbxjweAcvJ7a6E
XXyQe0ocGIwdmUSOrHj06IooUMbLq0utUoIbc60a0lhMGzJO7CuGEI+L2dD5Y7E+
i0BT0zxCYvQQiB5DEqgL/iHWFPwvt9hXq4aXyBmOmYdqRCBN3sw=
=kDiO
-----END PGP SIGNATURE-----
```

## 0.5.3 - 2020-09-20

- Bump version to 0.5.3 (00d336c)
- Fix web concurrency Gunicorn worker calculation (fd60470)

Tagger: Brendon Smith <br3ndonland@protonmail.com>

Date: 2020-09-20 21:10:09 -0400

```text
-----BEGIN PGP SIGNATURE-----

iQIzBAABCAAdFiEE8JoyBFTTcRFWvTCPrGY4TPqMabAFAl9n/aIACgkQrGY4TPqM
abCIJxAAgcOlnMBdyiTpgvFQmQNrpHVy0dkrg1Lrkhsij44E1OPXpGYtiomhBYyY
Bqc0FFJ2yGT3Z7xPMn6fCjudvmzgc8iEi1h7GLJiS8g0zfcULZZJ2nknXHVnGoQq
4GPipHy/zttGbJcYQm6a7KSXBui98oFHLbJXEnF6yPNBvz3Yc9QbKSSEqc1/1eO1
rWegS/wKEl48muu+UusA+ZblRBpyqd0Dp9d/L/8RBCA9L2SiOYGIhibiqCckXQfs
9M2v2oGwx9QdZSHmIBAKLe2Tm+s3i7/lPx7sYAaT9u2v8AbAXBQ/7vkn/d7p2QpW
Ruz7AnmDKQBgFgZ9eCyzHwpLOgLYq2c7Z0hTzRTg4slj9Woz/Ivi6/zDJosq5WwV
G7NG/pKU9L6ois9olLqP/+gpM8TLjHH5soFqbSwsXw7jVNhZSJG/2+gj96DGbnYn
6H6IBgbF/qW/W1nwj8NPwdIpQSmhkpHGtjrWCrwixJxgQNelsv0Qaij1b2ueH6ze
AMcC+QDWGARPBB75criJ/Nr2eK0062H4irSfncS8yTZQlzIh831nxI9mY1XmDE0Q
PCbePQ78THpr5c9mkZgcNXshE13TrsTJnBEbZxhRQhY2ebeoR0jjXR3D1TegTasT
Rpj4CT8sFU45JQVusOSK90PTKfb4ix/Y9T/0uaNwUUGdFp1MdE8=
=KAyY
-----END PGP SIGNATURE-----
```

## 0.5.2 - 2020-09-19

- Bump version to 0.5.2 (edcc361)
- Improve testing of server configuration (PR #11)
- Run Dependabot updates on Saturdays (55baa72)
- Update Docker image URLs for new GHCR pages (6b55bbc)

Tagger: Brendon Smith <br3ndonland@protonmail.com>

Date: 2020-09-19 22:54:24 -0400

```text
-----BEGIN PGP SIGNATURE-----

iQIzBAABCAAdFiEE8JoyBFTTcRFWvTCPrGY4TPqMabAFAl9mxRMACgkQrGY4TPqM
abBECw/9GGjBQt1MbOS1oNNIT5tBf6xmYOJCjcJ66/r7/rzOdWtp2dA9tIACOeTd
hcUaQtlTDIz48HgTni/NSHyyH+zaoWMvSx7245SJByi/um2bBxB7SCatX4Vr1WI1
FY7xpLE3ZWzTpu6DZkcm7tb/qiPLoHVtDA8Y6dBqWWkvN57RKRAytNv7QUPTu6o8
sdFyBsDnlYG72Uz3pDLjf/BDT5GEGkqj4Y8a9TTEZzBrZDGYobv8xXsGjaYwjHcF
sH9uLilAy+XCjVqgN4MfQ5Wvdwg4qVrW3Q09/nDOkJH9nTE4q5KunG62L30PPolf
p0idhDS8wgbrTo7IFYAxP/i0fSDR5vn4PryZD0KOnTgI0SxkE4XtAVO3TBHyRjBe
kxtYmdsgjVfA28OsMTF9/tyXnEwz/HRank5TE8bwfYYJrgpFbvpZluSu+W8e8evS
Cg9J3PAgKLRXs7EMrVTQ8O2O/OIpbAThU1O+OtdDWgIhUWbGqwKvnq9fylGg3I9A
NlivqvvpvooX5KWRsg4tkY7/+emqWxNLs2w5t7g3U8HVYwMPCsk5SVHuo2YV2agA
hZSlKDyXBkRF07PpbLntyMJ1HmUw8/kJpRcVrwGvHdvviBOy9I3Mf6b2GcJ30kcq
eOY4Wn7a0wsoYZS8Dtob/ASSr5Us/QSUAuzZVADR+WeeSelCW5M=
=Cwev
-----END PGP SIGNATURE-----
```

## 0.5.1 - 2020-09-15

- Bump version to 0.5.1 (727181e)
- Add OCI Docker labels (6750087)
- Update README (894175c, 802b0dd, 82d4d8e)

Tagger: Brendon Smith <br3ndonland@protonmail.com>

Date: 2020-09-15 18:32:30 -0400

```text
-----BEGIN PGP SIGNATURE-----

iQIzBAABCAAdFiEE8JoyBFTTcRFWvTCPrGY4TPqMabAFAl9hQSoACgkQrGY4TPqM
abDwbxAAk99NsYgvNwfpkCLJ1TtOKoyaqfJev1tOabzLXFHn1lA2nqKvgHSejiDb
ytop8XWQrNlb7I8qCyddB2DcpggID7GIIHDJ1AlQC+yY6bEl0fx82G2ClZEYW7Gc
ctuITtvhI54DamjIyXgcIs+BS1Bbyhx8F6rlsgLt//QLjYaLvyM9g+UUfNNYCBNf
uEKhyQwNnyzye22zr2fwPtVYXftZ4FmPEyoP+NUWqEXbhD4kVqCt+IrcEkh/jOrR
nHSsU9O+sKzhIC31SF51QJ/8VfXS3UVRUnnJdl0pD0uijOVICDLDnbPBANiM7oBW
+gfwMGVIShW73GRnb4eYs8tY4gsvLqiOEGCQP+CYFVjEelR+7yF0s1BMqhrJor3W
z1PfMO4PkU/ejboasOeAdtFtg9bP/l3pGisJTY+IYkjWFvwNG/2NzXSaDsafzbrd
5MU+lfvw6Mv9156prCBXHAH4lGXZIKCE+iWEbsZZHe52WxMbrPI659CktowkSFe6
JQXoN43RdX7Ix91uR/47/c1PIZqnjZxptALaWQZU4t0o+1iJB8zgrS52KmoVAKdW
iL9JSQBZI9f6/Rvx5kesUShOWq4AaRDgdVOdiTjd3WAHd9b0XByFRIEVK9kluY7q
m7MWprvLIUcmDlPyl3fQr94o5duy0F77i0NgCc4EJV+dpTmSVSw=
=46Ol
-----END PGP SIGNATURE-----
```

## 0.5.0 - 2020-09-13

- Add test coverage tooling (br3ndonland/inboard#7)
- Increase unit test coverage to 100% (br3ndonland/inboard#8)

Tagger: Brendon Smith <br3ndonland@protonmail.com>

Date: 2020-09-13 19:48:03 -0400

```text
-----BEGIN PGP SIGNATURE-----

iQIzBAABCAAdFiEE8JoyBFTTcRFWvTCPrGY4TPqMabAFAl9er+MACgkQrGY4TPqM
abBUnxAAq8GgznULq9nMuM92AUaqNVHqpZA/lX0BK0Tfj4BW3s8PP13tOhfB45H0
OHGNpepnFMxRMs2s4v83XXLcbrYYEkmEeMDbI16RzuZy22INsEsN5d7Nbv5Ua4e1
WvAQFS0X7J04CGU3qLTCJ/xOv6cSHucTsczwC9ifsR3XzkgCgKY5Z8RJIx+aQ/sy
29Y3oldJsOj8Z6nPntea8kWqW5RujXAMnnbX9/TqrEoKI7KvwiOTweCLkH9klUjc
X+DIKMX3hxoZcpMTg/CDPuQgH5gEFurom58i41aqASWEoT11nowexBdeAJpkcscu
klvqTA+QJrmEIbUXDmOLPValaWY3Gq8j3gWwZn8bCnGtzhhZoTddbEmiMLNV8h2C
g92zMjC3RGkB8ptNSodQDHAENh76O6rjk/HfsQJmYzkoiIwzaCro2KJ53y0HJkGe
hIhsApFfEr7dt8ZIeai3hECYDAkAOoXOLZ7evf08VQYijoQAee0xCqPUtL1GMCLD
dAy4OrrZ/H6Uzew1Wuw14RKFh4g0n6vC4i1VtANN+r+UMQGUVDP2FcyhtohkrjqK
38+RDQc/UaHlMw0HSpFvbX7x+dNN1FMj8MpnsWcctF8PdvhgWOrnT4nbt7OI20FC
oxm1E4c5I7BPvMTpyT4mV38BIL5tOGU63CnjMtU8XvEid9WHf5g=
=ScM+
-----END PGP SIGNATURE-----
```

## 0.4.1 - 2020-09-11

- Bump version to 0.4.1 (108bcda)
- Add PyPI trove classifiers to pyproject.toml (782248a)
- Add Poetry keywords to pyproject.toml (0341582)
- Add py.typed file for PEP 561 compliance (d5f030f)
- Use Poetry custom installer for GitHub Actions (23e097d)
- Avoid creating Poetry virtualenv in GitHub Actions (2eed1fd)
- Hard-code \_\_token\_\_ as PyPI username (b9538aa)
- Add workflow_dispatch triggers to hooks and tests (89f9c17)
- Add CodeQL code scanning (e50684e)

Tagger: Brendon Smith <br3ndonland@protonmail.com>

Date: 2020-09-11 22:21:00 -0400

```text
-----BEGIN PGP SIGNATURE-----

iQIzBAABCAAdFiEE8JoyBFTTcRFWvTCPrGY4TPqMabAFAl9cMeAACgkQrGY4TPqM
abCxxw//W+5QyD+RomfRBcWhEZsDNZyjH5Hk6e2HVq5sEXOUX0k6aqys1FYY5kR8
5cyzrya/mb/lwjG6b69wi5QxGsPEkr/mTfA+tgAbRHeAFbbgyEWsnF1TzYT2hh2r
bb6uccWGATpAwsl2XG7N9OYkHe84F/0OmAunY8uxSvQXUki9ZL0O8Bp7g8OFTR2I
SR+OVTsVpQUDEQ328aMQBne+NF4OLNNZtBCmrhUktoX2OhGpv49GDiw36M8FkIC4
cNUv+O6MmZK9VIyDQdrcUr/FMTTFmUq9tMVxaSj1iD/1pu+4+pDVptrygLRYfCw0
2i0JbIlOO+gxV2fuGUav5BZf1XGIwcBmJVowhE8qnxTcZyIQ2dzIx8HlOAfFxtqu
l0OiNwnuGVs+YrfnQETd/El7z5TOsvpbfGX360xZG5cyU+QoCiMn1HiFw8ucsbFr
iZQR+2YLHW9bJJxS+Mrcrl0u2fPFM8DdY7DXYWcsAoeF0n/Earm76hu9/eVxrLnQ
hd05TXGhUQ1ZsgrSXFCiswUlRKPaRwTrLIOBMh/XvU+Z8k29RGMfcv3BsEXudEaG
e0scpFYYpbmSyiG8V2FGo1t4QqvlK8dVHJNFO2bmMJnHCqaIGkAOcXDjohfx2L8N
9hEGshP5eeUa3TwC1/BGpCU+IOCi+hv+mVzfpJOBNiHND9mNcpw=
=i3z6
-----END PGP SIGNATURE-----
```

## 0.4.0 - 2020-09-07

- Support both file and module paths for logging configs (b0a36de)
- Use more specific Mypy ignore comments (f2b5419)
  - `# type: ignore` -> `type: ignore[attr-defined]`
- Add error handling for start.set_conf_path (1c6a7ec)
- Improve separation of Uvicorn and Gunicorn servers (735618a)
  - Make `process_manager` a required argument for `start.start_server()`
  - Only set Gunicorn conf path when running Gunicorn
- Patch uvicorn.run with pytest-mock to manage server context (3906b3d)
- Update README (a8c5d0e, eaf1d6a, bd26793, 68d86cf)
- Update dependencies (a47c6fa, 28b9019, d2bab44, cc17974)
- Add Dependabot for automated dependency updates (0582667)
- Bump version to 0.4.0 (0734869)

Tagger: Brendon Smith <br3ndonland@protonmail.com>

Date: 2020-09-07 11:50:25 -0400

```text
-----BEGIN PGP SIGNATURE-----

iQIzBAABCAAdFiEE8JoyBFTTcRFWvTCPrGY4TPqMabAFAl9WVwYACgkQrGY4TPqM
abAleg/9G7s8mwTtIA52QoDIhgmUZKgjuBXbMgajiznxptyuDQn1V8pkMtXao5H8
I80Ys5SN2PpEn2p4VJD9SxGgSZAgvwbzyGD/KUsTRH4GfLW5jdeBPxELaUCQj0Pg
/gU87XoZ/CVrMfZLTS9zcvDJ4vifnGzqcl4m5vqFIlHIRjKFoLCZQxdvImw7NNQX
cg9X1VIlYkJ94/+xx8CWYRi+f3GZ3WrYF/RWQjWfzlsc9Ke+w0t4CQbTYXMI7CVd
MFSSa3mB95l9YQckaQaqiAX9soVgFqkKFcZXNSi1wfbtvj713BIyRTMNKg2XH6om
O5MDcon7btbXVkoQJePJ0Z/W8RH7ferl6B1Cz93tqoIa6BWUDqpIEpsPNUr151rj
iLCpbHvFioxT/wsgunCy/Go3H3hIxgTHkdaKKQXJaeFCyDZi9jpPP6cX92uQqWDI
GzetQ8Pv4UoBu8Rafh1VpsdBolqpvDoqVotshnpnr4bfVOFMa2rfqN3GJqJQQ12I
d8OG7WCoqV6wEN+jg9aww4o4KkyP5mPJvE4WQs3sNPBi0dfiJeYUyW0TNNCzYhMP
Bs9LDpwD+OqZZWXraf0WiXhObfNDDQ1FapfQ6fQEeHEBWCRcvkyz2XB/yDuSEv2+
aS4ytNUTSyTHhqsrfxbAPEiOoXD8dFKoH+I9FU7UEUAjLerbcys=
=eJs6
-----END PGP SIGNATURE-----
```

## 0.3.0 - 2020-09-02

- Remove unused pytest type ignores after upgrading to pytest 6 (3dc8085)
- Refactor start.configure_logging for module path (ff9155a)
- Bump version to 0.3.0 (db8a6ac)

Tagger: Brendon Smith <br3ndonland@protonmail.com>

Date: 2020-09-02 18:37:13 -0400

```text
-----BEGIN PGP SIGNATURE-----

iQIzBAABCAAdFiEE8JoyBFTTcRFWvTCPrGY4TPqMabAFAl9QHyYACgkQrGY4TPqM
abDyuhAA0YCPbc7uAsXqKULXx536r0JGOXNVu+nXhMH3r233FhXo96BYP5OF8Qgn
5rNWpluH5FJPK94sl/EtnqgLT63+iOUdsnkGf6DWVRuVjvaRbh+AcEok+pidPhbq
vGxisdBumrcbDpXrgBuQ7kNsdp9cvX+JKfSg4OdW8QbFXGWjqgVwN8jMl1keNRH6
XD5L3ZAFLlaf1E+FHg9IDsQFLztL4G6X7sr0G/astvZ63pAfVpWyN2+k4Zcc3zWt
5Njj/HRWpcp31/ue3d1By4V32NXXV5cbPurAgxENEblFLWRgZl+ZY+Phb/NS2LMM
0msVSwrXJXJeORd6PmnnQtSL0O/Z5PAniVN+bE/xv8Z84V8qhe8/fpyHiHOQxPVJ
ivavDTIoGEBCZMweWME6qL+i9CcNFcY1fCSXTIIzCgdm1yQ5W6GK4IrwqJQfvRfL
ofovAO5Tp+ZeW20ZR7AEbQztsWz4sp5LB8zSZGsMvt2e7zekj3yb9u0vZT4EhNfg
iP5lolxOujwQ9asBmNe7NkpxlfV8fLtPDR2OdHY8th0lrNzaeFkJclQAlNd4mTGW
qBMQ/zSPS9qvaFY6o+AkQCKwqNrFIjv8INRW+CN5b6K5noXpKHLLti9MD6M7VzX8
hys1IslRZStNrOOUbK+G2OykNgjXMySNjpSsXg+xVoOyUVUEWyk=
=ke+H
-----END PGP SIGNATURE-----
```

## 0.2.2 - 2020-09-01

- Install Pytest 6 (95178d2)
- Update Python dependencies (223e078)
- Bump version to 0.2.2 (7f642dc)

Tagger: Brendon Smith <br3ndonland@protonmail.com>

Date: 2020-09-01 23:58:58 -0400

```text
-----BEGIN PGP SIGNATURE-----

iQIzBAABCAAdFiEE8JoyBFTTcRFWvTCPrGY4TPqMabAFAl9PGMUACgkQrGY4TPqM
abAweA/9Elsnft6hBmxF4EdGQVCKauB7JJFTUU+qgi+v1gVktT1q4XJWr9WjNtsP
K2bk3f6kaL0oB89T9Xg+eJIBRrpyzZJPnw+aSRB3NOLrgHNr/1fCvHp/BuoiVgpj
QPvEteOXSCZVpFhm7m5wugJLP+Q78ahRwyg1QDsX4fTkRZ3PGo6H6GG3mGfIY4xq
u71jPY67rvewPFF2J00mFk4D01xtWLg6FKnOgF3yiQrQtEJ1hTYnNfpXXSSBxR4D
sK+F4pkl/iJYX7+GcSKYDg8D5hzsdHtYNX7MlTYK/1k78zoKD3hCVlUC+OXXYUym
lloLpdDS2kpDz1rMVgiYeCiqclWwht4OsIQakyUbYTycuJr+PgVHsieIYSFK+SpH
e4yVlYVpS6Mju8Paz1hIRPuE20+NBwUJS2XAkXo5K6Cz3HubJMb8pYIlmHf7RZDS
cVfwQ/iw0ynW2lbG+XOjILeypBEP0TzslVKSnWTcsFO6KDx6cCL/zxCoKm8rIawb
n6NI3MnP6rpSK/0v9rvI5q2PuJYhTfq7MKA70YtoB/wygKcARgGUNBxzOyERUbow
eICh9y6Zqfw0mZnKEGjOU4Eq1YGAfDIIAH8oZgDWHA8dl2iP3s3pGq7dLG9r6OjR
7aW/Do/H43kebjNIaR8i3d9BS8o+o1KqgnA3usWjORDbVyROqOM=
=+4lH
-----END PGP SIGNATURE-----
```

## 0.2.1 - 2020-09-01

- Move latest tag to final workflow step (cf907fe)
- Bump version to 0.2.1 (c47f545)

Tagger: Brendon Smith <br3ndonland@protonmail.com>

Date: 2020-09-01 22:44:17 -0400

```text
-----BEGIN PGP SIGNATURE-----

iQIzBAABCAAdFiEE8JoyBFTTcRFWvTCPrGY4TPqMabAFAl9PB0AACgkQrGY4TPqM
abCN+g//Xtem1ORO5oiie+m6CDWP+ssexVgO5JZx10TckANMLL/mbKA8hYZljKu8
XBCLDtYdJds1etdR40IFavTszmwViueugYifh0/uVarmgywdnpolz6tpO3qC2Tqe
ORznNDyXRh8LEf1uNl37VLf1JJQhqUFgM8wDNex+yA0ziW81/zQzh2gUXSZH5IBA
0kIh0K26ruLTr3+uKjlup/0GXLGVO/4inmAO8AK08Uqwj/fofh3vEKOvhw8m59Eb
v2UvD25CF1YzGLFD8c1Zz9DtK3iHNZFMXMKxr6dGSazvHh5WfF7l8xleSAJp3686
mpvds8Z6xDUijni8OwwDrbDTgBkykLz8Xb6IabLy5iF2+DPOhddmoCSvU1TSSS/T
/WvP8jouQW/Jg3+QBSEgIvT0ETIILjnuVVsdDdXxoueUAC0A5Qa8u+aaUfpA9Of9
m43gTBHCyZ1IaP/4KYNm2e/dnhefiWnoc/fElPWWERUfhm5/LlWp7b8JFgHGwbn7
wWhLU43d2wFKrJjLhwonLgMaiQp5NfFljo+P0R+znPJk+2u3i0FaB+DvS7afs7w6
ydNHvNGvK+yqQDhseCUDA1C5cra5Lf3gHX0wXQVwgAgianG7rL9Hv+x2RYoTlIoQ
z7Gxj3T8NsVczPD4tw4Qxt8DMs/wsBpmcziHrjWH4z8NyMZY9fk=
=BlRp
-----END PGP SIGNATURE-----
```

## 0.2.0 - 2020-09-01

Update Docker builds for GitHub Container Registry

- br3ndonland/inboard#6
- br3ndonland/inboard@723bc98
- br3ndonland/inboard@f3d829c
- br3ndonland/inboard@21c3bcd

Tagger: Brendon Smith <br3ndonland@protonmail.com>

Date: 2020-09-01 22:20:30 -0400

```text
-----BEGIN PGP SIGNATURE-----

iQIzBAABCAAdFiEE8JoyBFTTcRFWvTCPrGY4TPqMabAFAl9PAcwACgkQrGY4TPqM
abBjfg//bA+hCOAoEeWhGfhT2gfQT4mBVNyUzGTefcp7NkUXvSwY74rygkoF0qlp
jCjCiiIFTlIObB33xnwUx/8SPV3OxfauxpK6PvWN/QAan5wOIX3eKtGjoU1p9qNM
9AqEYWxRWcvcmjFm3aG4Iwe1JRmfEpbM57KqAwF1XbK9fi+AE3MS8AmWoBkTQCVU
Sbz04j1LLlbs+SOueU8Pk/2/dlErjw8P9siu3UzPecRXOOMe6z0IGFwHBrW/acof
kKAUC+96nQMdEgwdfA6MeLEL5ERXhe+PmtGyEgE6SuT46LHCL65H/xMpv/GMrYvS
dTNPUdkJWoxu+Vsoc8MVp2dqX2JFIFM1nPOU94atTVdcs4Nnd+WjXBQQCEK1w3sM
MOAyD2xxrGCrTs5uiyrH3S29Ih2Rw453kzaKWXMnC0vmOtjxRY8y7sxlAVFohovg
XD+bX9mMz//Jc8fXFJ+7ShKtmQggNIJ0vYVdFQVmYnt+HzDXDL2QNOOdID56+gax
uik/yCofEZHWe3IWYzyYOt5gvKOYQ4dwym08biRh6aoaExx6lYJOLVhGaUSZVXPs
8r/QOy8AFAteQ+7GotPIf4b9HmUe62Uo1SGc96NQ70DOWtTvhtdYZwgah9xtJbAO
AckzB7Fh3eoJdsZy6jf5JCUGvZHJb8d290FF7Pu19mHDrJ+4XXQ=
=CYH1
-----END PGP SIGNATURE-----
```

## 0.1.3 - 2020-08-31

Bump version to 0.1.3 (51fc961)

Tagger: Brendon Smith <br3ndonland@protonmail.com>

Date: 2020-08-31 11:10:41 -0400

```text
-----BEGIN PGP SIGNATURE-----

iQIzBAABCAAdFiEE8JoyBFTTcRFWvTCPrGY4TPqMabAFAl9NExgACgkQrGY4TPqM
abARVhAArzJxU7ylBibARRP90vgH7Z816lzjkQHXpv9vBc6Z7P0q/+CDkFF1XpBW
Rj1cXOeBbnd8D1zjZ5BW3NU1aVO7X/iGEH8O1/SgpifgEgS6EC/JN/v1xOoGruXs
p1Is2kqLtUxrE6EoQC5zWzaydEpOfl4oBWfTLIatCfjIpJsL+/IJqzEjP4rvRzEv
rUDyaY60yZnuYxofTPrSIkC3y83nFJHAnftvnrMOm5aCJ2URzGeIbhu4Ri0yGJbZ
xhTTJ2pKAhKcmkotvFC2sVb7eqZ4v49J2eaqQURJA/+rC43m4dQl5yrnvLLnECwB
SBLYA7QeNYnaq3VDyf9H464dGKnWMKi64yRZBjXmk7rrwwlye9Ii67hpaef/NHix
IzZCdyhBwLHe7ITiZ9gQ5+kxJ64tS7LDsavq88SIq9RJQNv92Vzv8yTa7PTg7DEF
RItx0zfxZWpqw9Hg2hxnrbs0UY2yrn+8jytBOt4yv1gaDon9YljsSwNPog/eBz/i
vz8s1DFGbX3RL6kTaRHbNt+n0QT/j2gDqWRFiQV4L6FjXEbGW3CpYwY+FZVRQvBr
dhUfQGBY01kPSZDMgh5TTyEldLKErcD/bVH2UwHe9xT+Taapdov7sihTrzy7GfWO
EiGBY5rjcJpTuFqYuLEmzv22xHqDRdqgNmVIOLunseXCi5/Vacg=
=xDse
-----END PGP SIGNATURE-----
```

## 0.1.2 - 2020-08-31

- Update README (1ad6ba6)
- Update FastAPI and Starlette tests (5b9706f, 397638e)

Tagger: Brendon Smith <br3ndonland@protonmail.com>

Date: 2020-08-31 11:06:30 -0400

```text
-----BEGIN PGP SIGNATURE-----

iQIzBAABCAAdFiEE8JoyBFTTcRFWvTCPrGY4TPqMabAFAl9NEkIACgkQrGY4TPqM
abDTkQ/8DFWSl70x1QPaofTKHDFpbZhhZS/p4pYXGWtTHDfSEvCheMPjuODsKFV1
AfKuRYWgRwIk0NNQfMdcCFt8V7ch7y9q1euGK+E1gtIzL7MhM5LoJe1ZBDC4p8LV
O6KFwsap6T55TAxGriefOiO5Ij6lH2JGSlwdi0lnlmuy5eBrjinaEMWJHpL35QYu
0wuLzdpfL8lLI3rOWxMMmF8NMX9uKqGIWEqku/2Wf3JFg2dJRTJS72rG55+768fR
nYc7g3Rx+QJHySW5Zpc/kCF7at6FssywfwDfUXIOeCO7jl/YsU6+LaVgPY85bD5g
mJhaimMEyzDRubp/CQSwwgWzJSq7+hiJkfq5zCBRPaGvXBuW6BcHSSbAp88zyvam
L8NgJVhCx/jJLBPTh4BHI7zXj64YfW0H4lTFynw5pkT/tueOAMHM+kXU0QWLLisE
ne8Q1iHqJWBxcr6Zlsj3cZMj2TwMnikl2iRrRamYggrM/8EaiHV3Tj7JIVBHGsX7
pgLYRniXql3NY8R5WmJIf7ZAEN2uR7jbBFpvw3QTY2V03p5rqkBo4w0QyLB7ZELg
SbbMKo8kv5ryBPGS+dKFQFKiVqZza6+0jrcV3kh6IAr5xmv3+UUIxvML16mZddwv
traKUoIG61YQ4fym8C9Te63py/5wfDL+qqjaicw4rutQYtZyLJo=
=oOG3
-----END PGP SIGNATURE-----
```

## 0.1.1 - 2020-08-31

- Correct poetry publish command (681dc09)
- Bump version to 0.1.1 (74900ab)

Tagger: Brendon Smith <br3ndonland@protonmail.com>

Date: 2020-08-31 02:50:01 -0400

```text
-----BEGIN PGP SIGNATURE-----

iQIzBAABCAAdFiEE8JoyBFTTcRFWvTCPrGY4TPqMabAFAl9MneoACgkQrGY4TPqM
abC6bRAA47pAR+2GqeuNBAOrs1R3fYrJ2YnUtJe7Fw5fb8BSHGUZKeJEhs+6Fj0V
EZ/FabG1u9ncWGF4I1jVrd0wWqnCODb+S7rGSP+WAZzfUbWXmrUSacFLxfAhWMAH
vFx+tDrMFCMRW0b55AKPdTeYlQCQcBB+VByfGMXZlFmlIpSs2+C6FM1wn9Pur2m/
+YDEd6+EYBFOBlY9RVv+wEbPUVIp/eI2PjDuuGQr7y4UDxduFEX1SQzlqa0Wa7sk
oG3d5cMzL36twl/RfzKxU9quUQhPyvNauvsYDmAHGPWn1MGtlZCxXqer8d6EtBRo
a+JybetZ08Fq0P18c9Kj/jXCWya/Vx44jS6O0CwQi4WBsUGUcUzHdbcdf3w0zmFh
3vjwR8Yjy/qZ28Xo5r+qCjQ+77rnXzL2+IJgV9NpgYKHvyIzhPmZGgZch3CdQvkN
vT4unJLsWMnSWvthAJhaRNKVsr05NOi/zQJFzcuwUcX9eLxNMV2y904zPBsIYqCH
t1voZ8ducQAt7wgdYhpLqGeNUU0BXu41OqrWRLu2WnPJKj11FiXedYxf0k95N1QE
sNLY9t7hTjXIDP5gYS4IvPn8SeOOoq6EkKioY1Lpumgt/XC05ZJDm4AmvTIbkg6a
k/ttLezWW1GR1aU5TN10HfO6NYKwx3oNMqrTaGuwOY9NvTG2ywE=
=Tn53
-----END PGP SIGNATURE-----
```

## 0.1.0 - 2020-08-31

- Add Dockerfile with Poetry installation and multi-stage builds
  (br3ndonland/inboard#1)
- Add app modules, Gunicorn config, and start scripts
  (br3ndonland/inboard#2)
- Add logging configuration for Gunicorn and Uvicorn
  (br3ndonland/inboard#3)
- Add unit test suite (br3ndonland/inboard#4)
- Add GitHub Actions workflow for Python and Docker builds
  (br3ndonland/inboard#5)

Tagger: Brendon Smith <br3ndonland@protonmail.com>

Date: 2020-08-31 02:14:14 -0400

```text
-----BEGIN PGP SIGNATURE-----

iQIzBAABCAAdFiEE8JoyBFTTcRFWvTCPrGY4TPqMabAFAl9MlYIACgkQrGY4TPqM
abC10g/9FS6A310wXiFjaId6ZV2zJHCVnNWHeDBE3jrdxue46zz7famEHcgjZ3PC
ENzB+xG8vH3/9wqA/RWcfXDdH6+laLbWrACBB54rARCHB5tzDMFYTW+64JOfNgM6
zyuxru47NK6BGFfc01OMy9X6sKu1E6RQrY9GSWvrwwFmsEaIKfVNmWS15s6m751P
uZi5i1c3CyGZqXrcEclLNq0bpBk9wL1bZTp8ZAEpEj/JjzWsP0isGxhVTUOzJtG5
oLXNOuLJtx2XHddeUR2bFj0qgK+Mg2QhZr1d4lVs8Ywve7KVu6Sousv+8Z7IApJx
8jkB5nhooLubotpSRGiIch382UFGtxMORtTkvxGQqgaByxCScpr5+aW0UyS7HhcF
z+/cc3ITrXFQaf2ide0sZhBv/+ntxooy7WwAtl1iOYy6Yxxz7jf3Hj0XyeHUvqVa
jDpw28QDPJJNC//OExBE9TRTipkN3s3IMDQEXxrMyEqhqxdf7O+ICEuWgHzYrcRQ
/XXY5B5VSEU1V3Cq2PTtl0vZt2+USMITqqpOz4z9c5/nPppbZ9KfT7D5ygV5Afli
YJysHc1DHrkOwfGn/LVaKYIeB+KMx8jTq5Rcd+I+myeg+5lbIYPKlrm4tKO833ML
vbGmsUwNvdkFczR9bbtsTKch61SMF0eHRR8tup5ZVgVNvjPd2OY=
=cGPd
-----END PGP SIGNATURE-----
```
