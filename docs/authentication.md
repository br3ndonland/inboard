# Authentication

## HTTP Basic auth

### Configuration

The [HTTP authentication standard](https://developer.mozilla.org/en-US/docs/Web/HTTP/Authentication) includes HTTP Basic authentication, which, as the name implies, is just a basic method that accepts a username and password. As the [MDN documentation recommends](https://developer.mozilla.org/en-US/docs/Web/HTTP/Authentication#basic_authentication_scheme), HTTP Basic auth should always be used with TLS.

inboard provides utilities for configuring HTTP Basic auth.

For Starlette applications, inboard provides [middleware](https://www.starlette.io/middleware/) for HTTP Basic auth. Starlette middleware are applied to every request.

!!!example "Example of HTTP Basic auth with Starlette middleware"

    ```py
    from inboard import StarletteBasicAuth
    from starlette.applications import Starlette
    from starlette.middleware.authentication import AuthenticationMiddleware

    app = Starlette()
    app.add_middleware(AuthenticationMiddleware, backend=StarletteBasicAuth())
    ```

FastAPI is built on Starlette, so a FastAPI app can be configured with middleware as above, substituting `FastAPI()` for `Starlette()`. inboard also provides a [FastAPI dependency](https://fastapi.tiangolo.com/tutorial/dependencies/), which can be applied to specific API endpoints or [`APIRouter` objects](https://fastapi.tiangolo.com/tutorial/bigger-applications/).

!!!example "Example of HTTP Basic auth with a FastAPI dependency"

    ```py
    from typing import Annotated, Optional

    from fastapi import Depends, FastAPI, status
    from pydantic import BaseModel

    from inboard import fastapi_basic_auth


    class GetHealth(BaseModel):
        application: str
        status: str
        message: Optional[str]


    BasicAuth = Annotated[str, Depends(fastapi_basic_auth)]
    app = FastAPI(title="Example FastAPI app")


    @app.get("/health", status_code=status.HTTP_200_OK)
    async def get_health(auth: BasicAuth) -> GetHealth:
        return GetHealth(application=app.title, status="active")
    ```

### Usage

As described in the [environment variable reference](environment.md) and [contribution guide](contributing.md), when starting the inboard server, the environment variables `BASIC_AUTH_USERNAME` and `BASIC_AUTH_PASSWORD` can be set. The values of these variables can then be passed in with client requests to authenticate.

```sh
# server
docker pull ghcr.io/br3ndonland/inboard
docker run -d -p 80:80 \
  -e "BASIC_AUTH_USERNAME=test_user" \
  -e "BASIC_AUTH_PASSWORD=r4ndom_bUt_memorable" \
  ghcr.io/br3ndonland/inboard

# client: https://httpie.io/
http :80/health -a "test_user":"r4ndom_bUt_memorable"
```

HTTP clients, such as [Hoppscotch](https://hoppscotch.io/) (formerly known as Postwoman), [HTTPie](https://httpie.io/docs#authentication), [Insomnia](https://support.insomnia.rest/article/174-authentication), and [Postman](https://learning.postman.com/docs/sending-requests/authorization/) provide support for HTTP Basic auth.

HTTP Basic auth can also be useful for load balancer health checks in deployed applications. In AWS, [load balancer health checks](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-target-groups.html) don't have HTTP Basic auth capabilities, so it is common to configure authentication bypasses for these checks. However, health checks can also be configured to expect a response of `401` instead of `200` for endpoints requiring authentication. Successful health checks therefore provide two pieces of information: the endpoint is up, and authentication is working. Conversely, if the health check endpoint returns `200`, this is an indication that basic auth is no longer working, and the service will be taken down immediately.

## Further info

For more details on how HTTP Basic auth was implemented, see [br3ndonland/inboard#32](https://github.com/br3ndonland/inboard/pull/32).

For more advanced security, consider [OAuth2](https://oauth.net/2/) with [JSON Web Tokens](https://jwt.io/) (JWT), as described in the [FastAPI docs](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/).
