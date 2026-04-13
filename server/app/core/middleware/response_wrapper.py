import json
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

class ResponseWrapperMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        # skip 204 (pas de body) et les non-JSON
        if response.status_code == 204 or response.status_code >= 400:
            return response
        if "application/json" not in response.headers.get("content-type", ""):
            return response

        # Sur un framework "classique" type nestjs le streaming de la réponse est caché en général
        # Ici ce n'est pas le cas, il faut donc parcourir le streaming à la main
        body = b""                          # bytes vide
        async for chunk in response.body_iterator:  # parcourt chaque morceau
            body += chunk                   # assemble
        # maintenant body contient le JSON complet en bytes

        wrapped = {
            "isSuccess": response.status_code < 400,
            "path": request.url.path,
            "data": json.loads(body),
        }

        return Response(
            content=json.dumps(wrapped),
            status_code=response.status_code,
            media_type="application/json",
        )