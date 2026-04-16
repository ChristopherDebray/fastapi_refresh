import json

from jose import JWTError
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import Match

from app.core.security.jwt_service import JwtService

COOKIE_NAME = "access_token"


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        if self._is_public_route(request):
            return await call_next(request)

        token = request.cookies.get(COOKIE_NAME)
        if not token:
            return self._unauthorized(
                request, "You must be logged in to use this route"
            )

        try:
            payload = JwtService.decode_access_token(token)
        except JWTError:
            return self._unauthorized(request, "Invalid or expired token")

        request.state.user = payload
        return await call_next(request)

    def _is_public_route(self, request: Request) -> bool:
        for route in request.app.routes:
            match, _ = route.matches(request.scope)
            if match == Match.FULL:
                return getattr(route, "public", False)
        return False

    def _unauthorized(self, request: Request, detail: str) -> Response:
        return Response(
            content=json.dumps(
                {
                    "isSuccess": False,
                    "path": request.url.path,
                    "error": detail,
                }
            ),
            status_code=401,
            media_type="application/json",
        )
