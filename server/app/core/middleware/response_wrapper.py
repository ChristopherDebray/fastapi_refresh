import json

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response


class ResponseWrapperMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        response = await call_next(request)

        # skip 204 (pas de body) et les non-JSON
        if response.status_code == 204 or response.status_code >= 400:
            return response
        if "application/json" not in response.headers.get("content-type", ""):
            return response

        # Sur un framework "classique" type nestjs le streaming de la réponse est caché en général
        # Ici ce n'est pas le cas, il faut donc parcourir le streaming à la main
        body = b""  # bytes vide
        async for chunk in response.body_iterator:  # type: ignore[attr-defined]  # parcourt chaque morceau
            body += chunk  # assemble
        # maintenant body contient le JSON complet en bytes

        wrapped = {
            "isSuccess": response.status_code < 400,
            "path": request.url.path,
            "data": json.loads(body),
        }

        new_response = Response(
            content=json.dumps(wrapped),
            status_code=response.status_code,
            media_type="application/json",
        )
        # We copy the headers of the initial response to our wrap result
        for key, value in response.headers.items():
            if key.lower() not in ("content-type", "content-length"):
                new_response.headers.append(key, value)
        return new_response
